from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.section_intent_customers import IntentCustomerCreate
from app.crud.intent_customers import create_intent_customer
from datetime import datetime, date
from typing import Dict, Any

router = APIRouter()

@router.post("/create_customer")
def create_customer(
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """从 Dify 接收客户信息并新增到 dify 数据库的 customer_info 表"""

    required_fields = [
        'customer_id', 'name', 'gender', 'age', 'province', 'city',
        'phone_number', 'channel_type', 'channel_name', 'education_level',
        'education_status', 'school_name', 'major', 'target_country',
        'target_project_type', 'target_major', 'target_degree',
        'follow_status', 'assigned_consultant', 'follow_notes'
    ]

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise HTTPException(status_code=400, detail=f"缺少必填字段: {', '.join(missing_fields)}")

    try:
        graduate_time_str = data.get('graduate_time', '2024-01-01')
        graduate_time = date.fromisoformat(graduate_time_str)
    except:
        graduate_time = date.today()

    try:
        last_follow_time_str = data.get('last_follow_time', datetime.now().isoformat())
        last_follow_time = datetime.fromisoformat(last_follow_time_str.replace(' ', 'T'))
    except:
        last_follow_time = datetime.now()

    customer_create = IntentCustomerCreate(
        customer_id=data['customer_id'],
        name=data['name'],
        gender=data['gender'],
        age=int(data['age']),
        province=data['province'],
        city=data['city'],
        phone_number=data['phone_number'],
        channel_type=data['channel_type'],
        channel_name=data['channel_name'],
        source_URL=data.get('source_URL'),
        education_level=data['education_level'],
        education_status=data['education_status'],
        school_name=data['school_name'],
        major=data['major'],
        graduate_time=graduate_time,
        english_score=data.get('english_score'),
        german_level=data.get('german_level'),
        education_verified=data.get('education_verified'),
        target_country=data['target_country'],
        target_project_type=data['target_project_type'],
        target_major=data['target_major'],
        target_degree=data['target_degree'],
        study_purpose=data.get('study_purpose'),
        family_income_level=data.get('family_income_level'),
        budget_range=data.get('budget_range'),
        loan_acceptance=data.get('loan_acceptance'),
        payment_ability_level=data.get('payment_ability_level'),
        accept_overseas_study=data.get('accept_overseas_study'),
        accept_closed_training=data.get('accept_closed_training'),
        accept_enterprise_training=data.get('accept_enterprise_training'),
        learning_ability_score=data.get('learning_ability_score'),
        education_upgrade_intention=data.get('education_upgrade_intention'),
        career_upgrade_intention=data.get('career_upgrade_intention'),
        employment_demand=data.get('employment_demand'),
        immigration_intention=data.get('immigration_intention'),
        overseas_development=data.get('overseas_development'),
        high_salary_expectation=data.get('high_salary_expectation'),
        stable_job_expectation=data.get('stable_job_expectation'),
        passport_available=data.get('passport_available'),
        exit_restriction_risk=data.get('exit_restriction_risk'),
        credit_risk=data.get('credit_risk'),
        visa_refusal_history=data.get('visa_refusal_history'),
        high_risk_flag=data.get('high_risk_flag'),
        consult_phase=data.get('consult_phase'),
        follow_status=data['follow_status'],
        assigned_consultant=data['assigned_consultant'],
        last_follow_time=last_follow_time,
        follow_notes=data['follow_notes']
    )

    db_customer = create_intent_customer(db=db, customer=customer_create)

    return {
        "success": True,
        "customer_id": db_customer.id,
        "name": db_customer.name,
        "message": "客户信息已成功保存"
    }