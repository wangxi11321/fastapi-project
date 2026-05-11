import re
from typing import Dict, Any, Optional
from app.schemas.intent_customers import IntentCustomerCreate

class CustomerJudgeTool:
    TARGET_CRITERIA = {
        "education": ["本科", "硕士", "学士", "研究生"],
        "budget": 30.0,
        "english_level": ["雅思6.5", "托福90", "六级", "GRE", "GMAT"],
        "countries": ["美国", "英国", "加拿大", "澳大利亚", "新西兰"]
    }

    @staticmethod
    def extract_info(text: str) -> Dict[str, Any]:
        info = {
            "name": None,
            "phone": None,
            "email": None,
            "education": None,
            "major": None,
            "budget": None,
            "country": None,
            "english_level": None,
            "target_school": None,
            "target_major": None
        }
        
        phone_pattern = r'1[3-9]\d{9}'
        email_pattern = r'[\w.-]+@[\w.-]+\.\w+'
        budget_pattern = r'(\d+(?:\.\d+)?)\s*(万|万元|美元|usd|USD)'
        
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            info["phone"] = phone_match.group()
        
        email_match = re.search(email_pattern, text, re.IGNORECASE)
        if email_match:
            info["email"] = email_match.group()
        
        budget_match = re.search(budget_pattern, text)
        if budget_match:
            info["budget"] = float(budget_match.group(1))
        
        for edu in CustomerJudgeTool.TARGET_CRITERIA["education"]:
            if edu in text:
                info["education"] = edu
                break
        
        for country in CustomerJudgeTool.TARGET_CRITERIA["countries"]:
            if country in text:
                info["country"] = country
                break
        
        for level in CustomerJudgeTool.TARGET_CRITERIA["english_level"]:
            if level in text:
                info["english_level"] = level
                break
        
        name_pattern = r'(姓名|名字|我叫|我是)\s*([\u4e00-\u9fa5]{2,4})'
        name_match = re.search(name_pattern, text)
        if name_match:
            info["name"] = name_match.group(2)
        
        return info

    @staticmethod
    def judge_customer(customer_info: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        extracted = CustomerJudgeTool.extract_info(customer_info)
        
        reasons = []
        tags = []
        is_target = True
        
        if extracted["education"]:
            reasons.append(f"学历符合要求: {extracted['education']}")
            tags.append("学历达标")
        else:
            reasons.append("学历信息未明确")
            is_target = False
        
        if extracted["budget"] and extracted["budget"] >= CustomerJudgeTool.TARGET_CRITERIA["budget"]:
            reasons.append(f"预算充足: {extracted['budget']}万")
            tags.append("预算达标")
        elif extracted["budget"]:
            reasons.append(f"预算不足: {extracted['budget']}万，建议预算30万以上")
            is_target = False
        else:
            reasons.append("预算信息未明确")
            is_target = False
        
        if extracted["country"]:
            reasons.append(f"目标国家: {extracted['country']}")
            tags.append(f"意向国家:{extracted['country']}")
        else:
            reasons.append("目标国家未明确")
        
        if extracted["english_level"]:
            reasons.append(f"英语水平: {extracted['english_level']}")
            tags.append("英语达标")
        else:
            reasons.append("英语水平未明确")
        
        return {
            "is_target": is_target,
            "reason": "; ".join(reasons),
            "tags": ",".join(tags),
            "extracted_info": extracted
        }

    @staticmethod
    def judge_and_create(customer_info: str) -> IntentCustomerCreate:
        result = CustomerJudgeTool.judge_customer(customer_info)
        extracted = result["extracted_info"]
        
        return IntentCustomerCreate(
            name=extracted["name"] or "未知",
            phone=extracted["phone"] or "未知",
            email=extracted["email"],
            education=extracted["education"],
            major=extracted["major"],
            budget=extracted["budget"],
            country=extracted["country"],
            english_level=extracted["english_level"],
            target_school=extracted["target_school"],
            target_major=extracted["target_major"],
            tags=result["tags"],
            is_target=result["is_target"]
        )