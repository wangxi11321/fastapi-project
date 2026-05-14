from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class IntentCustomerBase(BaseModel):
    customer_id: str
    name: str
    gender: str
    age: int
    province: str
    city: str
    phone_number: str
    channel_type: str
    channel_name: str
    source_URL: Optional[str] = None
    education_level: str
    education_status: str
    school_name: str
    major: str
    graduate_time: date
    english_score: Optional[str] = None
    german_level: Optional[str] = None
    education_verified: Optional[bool] = None
    target_country: str
    target_project_type: str
    target_major: str
    target_degree: str
    study_purpose: Optional[str] = None
    family_income_level: Optional[str] = None
    budget_range: Optional[str] = None
    loan_acceptance: Optional[bool] = None
    payment_ability_level: Optional[bool] = None
    accept_overseas_study: Optional[bool] = None
    accept_closed_training: Optional[bool] = None
    accept_enterprise_training: Optional[bool] = None
    learning_ability_score: Optional[int] = None
    education_upgrade_intention: Optional[bool] = None
    career_upgrade_intention: Optional[bool] = None
    employment_demand: Optional[bool] = None
    immigration_intention: Optional[bool] = None
    overseas_development: Optional[bool] = None
    high_salary_expectation: Optional[bool] = None
    stable_job_expectation: Optional[bool] = None
    passport_available: Optional[bool] = None
    exit_restriction_risk: Optional[bool] = None
    credit_risk: Optional[bool] = None
    visa_refusal_history: Optional[bool] = None
    high_risk_flag: Optional[bool] = None
    consult_phase: Optional[str] = None
    follow_status: str
    assigned_consultant: str
    last_follow_time: datetime
    follow_notes: str

class IntentCustomerCreate(IntentCustomerBase):
    pass

class IntentCustomerResponse(IntentCustomerBase):
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True

class CustomerJudgeRequest(BaseModel):
    customer_info: str
    file_path: Optional[str] = None