from datetime import date
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict


T = TypeVar("T")

# 定义创建成绩信息的模型
class ScoreInfoCreate(BaseModel):
    class_id: int = Field(..., description="班级id")
    test_num: int = Field(..., description="考试序次")
    stu_id: int = Field(..., description="学生id")
    exam_course_id: int = Field(..., description="课程id")
    exam_date: date = Field(..., description="考试日期")
    score: float = Field(default=0.00, ge=0, le=100, description="成绩 0.00~100.00")
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 定义查找成绩信息的模型
class ScoreInfoRead(BaseModel):
    class_id: Optional[int] = None
    test_num: Optional[int] = None
    stu_id: Optional[int] = None
    exam_course_id: Optional[int] = None
    exam_date: Optional[date] = None
    score: Optional[float] = None
    score_min: Optional[float] = None
    score_max: Optional[float] = None
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 定义修改成绩信息的模型
class ScoreInfoUpdate(BaseModel):
    class_id: Optional[int] = None
    test_num: Optional[int] = None
    stu_id: Optional[int] = None
    exam_course_id: Optional[int] = None
    exam_date: Optional[date] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)



# 定义单条成绩信息的响应体模型
class ScoreInfoData(BaseModel):
    id: int
    class_id: int
    test_num: int
    stu_id: int
    exam_course_id: int
    exam_date: date
    score: float
    delete_flag: int
    creation_date: date
    insert_date: date
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 统一响应格式
class ScoreInfoOut(BaseModel, Generic[T]):
    message: str
    data: T
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 这是用于统计接口的模型
# 每次考试成绩都在80分以上的模型
class HighScoreData(BaseModel):
    stu_id: int
    stu_name: str
    score: float
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


# 至少两次考试不及格的模型
class LowScoreData(BaseModel):
    stu_name: str
    class_id: int
    score: float
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


class AvgScoreData(BaseModel):
    class_id: int
    test_num: int
    avg_score: float
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)


class StatisticsOut(BaseModel, Generic[T]):
    message: str
    data: T
    # 支持直接从数据库模型的对象列表转为pydantic模型
    model_config = ConfigDict(from_attributes=True)