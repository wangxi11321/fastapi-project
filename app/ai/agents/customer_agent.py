import json
import os
from typing import Dict, Any, Optional
from app.ai.tools.customer_judge import CustomerJudgeTool
from app.core.logger import logger

class CustomerAgent:
    def __init__(self):
        self.judge_tool = CustomerJudgeTool()
        self.prompt_path = os.path.join(os.path.dirname(__file__), "../prompts/customer_judge.txt")

    def load_prompt(self) -> str:
        if os.path.exists(self.prompt_path):
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return self._get_default_prompt()

    def _get_default_prompt(self) -> str:
        return """
你是一个专业的留学咨询客户分析师。请根据以下客户信息，分析该客户是否符合我们的目标客户画像。

目标客户标准：
1. 学历要求：本科、硕士、学士、研究生
2. 预算要求：30万人民币以上
3. 英语水平：雅思6.5、托福90、六级、GRE、GMAT
4. 目标国家：美国、英国、加拿大、澳大利亚、新西兰

请按照以下格式输出分析结果：
{
  "is_target": true/false,
  "reasons": ["原因1", "原因2", "..."],
  "tags": ["标签1", "标签2", "..."],
  "extracted_info": {
    "name": "姓名",
    "phone": "手机号",
    "email": "邮箱",
    "education": "学历",
    "budget": 预算金额,
    "country": "目标国家",
    "english_level": "英语水平"
  }
}

客户信息：
{customer_info}
        """.strip()

    def analyze_customer(self, customer_info: str) -> Dict[str, Any]:
        logger.info("CustomerAgent analyzing customer info")
        
        result = self.judge_tool.judge_customer(customer_info)
        
        logger.info(f"Customer judgment result: is_target={result['is_target']}")
        return result

    def extract_info(self, text: str) -> Dict[str, Any]:
        return self.judge_tool.extract_info(text)