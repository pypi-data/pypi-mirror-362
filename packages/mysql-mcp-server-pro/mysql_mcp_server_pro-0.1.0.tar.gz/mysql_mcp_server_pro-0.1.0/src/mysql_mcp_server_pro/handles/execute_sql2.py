from typing import Dict, Any, Sequence, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import logging
import time
from contextlib import contextmanager
from functools import wraps

from mysql.connector import Error as MySQLError, pooling
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mcp import Tool
from mcp.types import TextContent

from .base import BaseHandler
from ..config import get_db_config, get_role_permissions
from ..handles.exceptions import SQLPermissionError, SQLExecutionError

logger = logging.getLogger(__name__)

# 配置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def retry_on_error(max_retries=3, delay=1):
    """重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (MySQLError, SQLExecutionError) as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        logger.warning(f"第 {attempt + 1} 次尝试失败: {e}, {delay} 秒后重试")
                        time.sleep(delay)
                    continue
            raise last_error
        return wrapper
    return decorator

class SQLOperation(str, Enum):
    """SQL 操作类型枚举"""
    SELECT = 'SELECT'
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CREATE = 'CREATE'
    ALTER = 'ALTER'
    DROP = 'DROP'
    TRUNCATE = 'TRUNCATE'
    SHOW = 'SHOW'
    DESCRIBE = 'DESCRIBE'
    EXPLAIN = 'EXPLAIN'

    @classmethod
    def from_str(cls, value: str) -> 'SQLOperation':
        """从字符串创建 SQLOperation 枚举值"""
        try:
            return cls(value.upper())
        except ValueError:
            raise ValueError(f"不支持的SQL操作类型: {value}")

@dataclass
class SQLResult:
    """SQL 执行结果"""
    success: bool
    message: str
    columns: Optional[List[str]] = None
    rows: Optional[List[Tuple]] = None
    affected_rows: int = 0

class ExecuteSQL(BaseHandler):
    """SQL 执行处理器"""
    
    name = "execute_sql"
    description = "在MySQL数据库上执行SQL (支持多条SQL语句，以分号分隔)"

    # SQL操作正则模式
    SQL_COMMENT_PATTERN = re.compile(r'--.*$|/\*.*?\*/', re.MULTILINE|re.DOTALL)
    
    # 数据库连接池
    _pool: Optional[MySQLConnectionPool] = None
    
    def __init__(self):
        """初始化处理器"""
        super().__init__()
    
    @classmethod
    @retry_on_error(max_retries=3, delay=2)
    def _get_pool(cls) -> MySQLConnectionPool:
        """获取或创建数据库连接池（懒加载）
        
        Returns:
            MySQLConnectionPool: 数据库连接池实例
            
        Raises:
            SQLExecutionError: 连接池初始化失败时抛出
        """
        if cls._pool is None:
            try:
                config = get_db_config()
                pool_config = {
                    'host': config.get('host'),
                    'port': config.get('port', 3306),
                    'user': config.get('user'),
                    'password': config.get('password'),
                    'database': config.get('database'),
                    'pool_name': 'mcp_mysql_pool',
                    'pool_size': 5,
                    'pool_reset_session': True,
                    'connect_timeout': 30,  # 增加连接超时时间
                    'connection_timeout': 30,  # 连接获取超时
                    'use_pure': True,
                    'get_warnings': True,
                    'raise_on_warnings': True,
                    'autocommit': True,  # 自动提交
                    'time_zone': '+8:00',  # 设置时区
                    'charset': 'utf8mb4',  # 设置字符集
                    'collation': 'utf8mb4_unicode_ci'
                }
                
                # 验证必要的配置
                required_fields = ['host', 'user', 'password', 'database']
                missing_fields = [field for field in required_fields if not pool_config.get(field)]
                if missing_fields:
                    raise ValueError(f"缺少必要的数据库配置: {', '.join(missing_fields)}")
                
                logger.info(f"正在初始化数据库连接池，目标数据库: {pool_config['host']}:{pool_config['port']}")
                cls._pool = pooling.MySQLConnectionPool(**pool_config)
                logger.info("数据库连接池初始化成功")
            except MySQLError as e:
                logger.error(f"数据库连接池初始化失败: {e}")
                raise SQLExecutionError(f"数据库连接池初始化失败: {e}")
            except ValueError as e:
                logger.error(f"数据库配置错误: {e}")
                raise SQLExecutionError(f"数据库配置错误: {e}")
        return cls._pool

    def _get_allowed_operations(self) -> Set[SQLOperation]:
        """获取当前角色允许的操作列表"""
        config = get_db_config()
        role = config.get("role", "readonly")
        return {SQLOperation.from_str(op) for op in get_role_permissions(role)}

    def get_tool_description(self) -> Tool:
        """获取工具描述"""
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要执行的SQL语句"
                    }
                },
                "required": ["query"]
            }
        )

    @staticmethod
    def clean_sql(sql: str) -> str:
        """清理SQL语句，移除注释和多余空白
        
        Args:
            sql: 原始SQL语句
            
        Returns:
            清理后的SQL语句
        """
        # 移除注释
        sql = ExecuteSQL.SQL_COMMENT_PATTERN.sub('', sql)
        # 规范化空白字符
        return ' '.join(sql.split())

    def extract_operations(self, sql: str) -> Set[SQLOperation]:
        """提取SQL语句中的所有操作类型
        
        Args:
            sql: SQL语句
            
        Returns:
            操作类型集合
        """
        sql = self.clean_sql(sql.upper())
        return {
            op for op in SQLOperation 
            if re.search(rf'\b{op.value}\b', sql)
        }

    def check_permissions(self, operations: Set[SQLOperation]) -> bool:
        """检查操作权限
        
        Args:
            operations: 操作类型集合
            
        Returns:
            是否有权限执行所有操作
            
        Raises:
            SQLPermissionError: 当权限不足时
        """
        allowed = self._get_allowed_operations()
        unauthorized = operations - allowed
        
        if unauthorized:
            raise SQLPermissionError(
                f"权限不足: 当前角色无权执行以下操作: {', '.join(op.value for op in unauthorized)}"
            )
        return True

    @contextmanager
    @retry_on_error(max_retries=3, delay=1)
    def get_db_connection(self) -> PooledMySQLConnection:
        """从连接池获取数据库连接"""
        start_time = time.time()
        connection = None
        try:
            # 获取或创建连接池
            pool = self._get_pool()
            connection = pool.get_connection()
            
            # 验证连接是否有效
            if not connection.is_connected():
                connection.reconnect()
                
            logger.debug(f"获取数据库连接成功，耗时: {time.time() - start_time:.2f}秒")
            yield connection
            
        except MySQLError as e:
            logger.error(f"数据库连接获取失败: {e}")
            raise SQLExecutionError(f"数据库连接获取失败: {e}")
        finally:
            if connection:
                try:
                    if connection.is_connected():
                        connection.close()
                    logger.debug("数据库连接已归还到连接池")
                except Exception as e:
                    logger.error(f"关闭数据库连接失败: {e}")

    def execute_single_statement(
        self, 
        cursor: MySQLCursor, 
        statement: str,
        conn: MySQLConnection
    ) -> SQLResult:
        """执行单条SQL语句"""
        start_time = time.time()
        try:
            # 检查权限
            operations = self.extract_operations(statement)
            self.check_permissions(operations)

            cursor.execute(statement)
            execution_time = time.time() - start_time
            logger.debug(f"SQL执行耗时: {execution_time:.2f}秒")
            
            if cursor.description:  # SELECT 类查询
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                logger.info(f"查询成功，返回 {len(rows)} 条记录")
                return SQLResult(
                    success=True,
                    message=f"查询执行成功 (耗时: {execution_time:.2f}秒)",
                    columns=columns,
                    rows=rows
                )
            else:  # 非查询语句
                conn.commit()
                affected = cursor.rowcount
                logger.info(f"执行成功，影响 {affected} 行")
                return SQLResult(
                    success=True,
                    message=f"执行成功 (耗时: {execution_time:.2f}秒)",
                    affected_rows=affected
                )
                
        except MySQLError as e:
            logger.error(f"SQL执行错误: {e}, SQL: {statement}")
            raise SQLExecutionError(f"执行失败: {e}")
        except Exception as e:
            logger.error(f"未预期的错误: {e}, SQL: {statement}")
            raise SQLExecutionError(f"执行出现未预期的错误: {e}")

    def format_result(self, result: SQLResult) -> str:
        """格式化SQL执行结果
        
        Args:
            result: SQL执行结果
            
        Returns:
            格式化后的结果字符串
        """
        if not result.success:
            return result.message
            
        if result.columns and result.rows:  # SELECT 类查询结果
            # 将所有值转换为字符串，None转换为"NULL"
            formatted_rows = [
                ",".join("NULL" if v is None else str(v) for v in row)
                for row in result.rows
            ]
            return "\n".join([",".join(result.columns)] + formatted_rows)
        else:  # 非查询语句结果
            return f"{result.message}。影响行数: {result.affected_rows}"

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """执行SQL工具"""
        if "query" not in arguments:
            return [TextContent(type="text", text="错误: 缺少查询语句")]

        query = arguments["query"]
        statements = [stmt.strip() for stmt in query.split(';') if stmt.strip()]
        results = []
        
        if not statements:
            return [TextContent(type="text", text="错误: SQL语句为空")]

        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    for statement in statements:
                        try:
                            result = self.execute_single_statement(cursor, statement, conn)
                            results.append(self.format_result(result))
                        except (SQLPermissionError, SQLExecutionError) as e:
                            error_msg = str(e)
                            results.append(error_msg)
                            logger.warning(f"SQL执行警告: {error_msg}, SQL: {statement}")
                            # 对于权限错误，继续执行下一条语句
                            # 对于执行错误，根据实际情况决定是否继续
                            if isinstance(e, SQLExecutionError):
                                break

            return [TextContent(type="text", text="\n---\n".join(results))]
            
        except Exception as e:
            error_msg = f"执行过程中出现错误: {str(e)}"
            logger.error(error_msg)
            return [TextContent(type="text", text=error_msg)]

