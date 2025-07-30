from typing import Dict, Any

from mcp import GetPromptResult
from mcp.types import Prompt, PromptArgument, TextContent, PromptMessage

from mysql_mcp_server_pro.prompts.BasePrompt import BasePrompt


class AnalysisMySqlIssues(BasePrompt):
    name = "analyzing-mysql-prompt"
    description = (
        "这是分析mysql相关问题的提示词"
    )

    def get_prompt(self) -> Prompt:
        return Prompt(
            name= self.name,
            description= self.description,
            arguments=[
                PromptArgument(
                    name="desc", description="请输入mysql的问题描述", required=True
                )
            ],
        )

    async def run_prompt(self, arguments: Dict[str, Any]) -> GetPromptResult:

        if "desc" not in arguments:
            raise ValueError("缺少问题描述")

        desc = arguments["desc"]

        prompt = f"你是一个资深的mysql专家，目前有一个问题：{desc},"
        prompt += "请分析原因，并以markdown格式返回结果，要求包含问题分析、解决方案、风险点"

        return GetPromptResult(
            description="mysql prompt",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt),
                )
            ],
        )