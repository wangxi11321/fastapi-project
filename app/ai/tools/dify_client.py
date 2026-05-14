import requests
import re
from app.core.config import settings
from typing import Dict, Any, Optional

class DifyClient:
    def __init__(self):
        self.api_key = settings.DIFY_API_KEY
        self.base_url = settings.DIFY_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.use_mock = not self.api_key or self.api_key == "your-dify-api-key"
    
    def _mock_judge_customer(self, customer_info: str) -> Dict[str, Any]:
        match_criteria = []
        missing_criteria = []
        
        education_patterns = ["本科", "硕士", "学士", "研究生"]
        budget_pattern = r"(\d+(?:\.\d+)?)\s*万"
        english_patterns = ["雅思", "托福", "六级", "GRE", "GMAT"]
        country_patterns = ["美国", "英国", "加拿大", "澳大利亚", "新西兰"]
        
        has_education = any(pattern in customer_info for pattern in education_patterns)
        has_budget = False
        budget_match = re.search(budget_pattern, customer_info)
        if budget_match:
            budget = float(budget_match.group(1))
            has_budget = budget >= 30
        has_english = any(pattern in customer_info for pattern in english_patterns)
        has_country = any(pattern in customer_info for pattern in country_patterns)
        
        if has_education:
            match_criteria.append("学历达标")
        else:
            missing_criteria.append("学历")
        
        if has_budget:
            match_criteria.append("预算达标")
        else:
            missing_criteria.append("预算(≥30万)")
        
        if has_english:
            match_criteria.append("英语水平达标")
        else:
            missing_criteria.append("英语水平")
        
        if has_country:
            match_criteria.append("目标国家达标")
        else:
            missing_criteria.append("目标国家")
        
        is_target = len(missing_criteria) == 0
        
        reason = f"客户信息分析：匹配{len(match_criteria)}/4项标准"
        if is_target:
            reason += "，符合目标客户画像"
        else:
            reason += f"，缺失：{', '.join(missing_criteria)}"
        
        return {
            "success": True,
            "is_target": is_target,
            "reason": reason,
            "match_criteria": match_criteria,
            "missing_criteria": missing_criteria,
            "analysis_method": "Mock Rule Engine"
        }
    
    def chat_completion(self, message: str, user_id: str = "default_user", app_id: Optional[str] = None) -> Dict[str, Any]:
        if self.use_mock:
            return {
                "success": True,
                "answer": "Mock response"
            }
        
        url = f"{self.base_url}/chat-messages"
        
        data = {
            "inputs": {},
            "query": message,
            "response_mode": "blocking",
            "user": user_id
        }
        
        if app_id:
            data["app_id"] = app_id
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "message": "调用 Dify API 失败"
            }
    
    def judge_customer(self, customer_info: str, user_id: str = "default_user") -> Dict[str, Any]:
        if self.use_mock:
            return self._mock_judge_customer(customer_info)
        
        prompt = f"""
你是一个留学机构的客户研判专家。请分析以下客户信息，判断是否为目标客户：

客户信息：
{customer_info}

研判标准：
1. 学历达标：本科/硕士/学士/研究生
2. 预算达标：≥30万人民币
3. 英语水平：雅思6.5/托福90/六级/GRE/GMAT
4. 目标国家：美国/英国/加拿大/澳大利亚/新西兰

请输出JSON格式的研判结果：
{{
    "is_target": true/false,
    "reason": "研判理由",
    "match_criteria": ["匹配的标准1", "匹配的标准2"],
    "missing_criteria": ["缺失的标准1"]
}}
"""
        
        result = self.chat_completion(prompt, user_id)
        
        if result.get("success"):
            try:
                import json
                return json.loads(result.get("answer", "{}"))
            except:
                return {
                    "success": True,
                    "is_target": False,
                    "reason": result.get("answer", "无法解析结果"),
                    "match_criteria": [],
                    "missing_criteria": [],
                    "analysis_method": "Dify AI"
                }
        return result

dify_client = DifyClient()
