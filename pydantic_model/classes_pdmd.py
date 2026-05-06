from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# 创建开关枚举类
class DeletedFlag(int, Enum):
    flag1 = 0
    flag2 = 1


# 班级信息查询请求体
class GetClasses(BaseModel):
    head_teacher_id: int | None = Field(default=None, alias="班主任id")  # 取别名,班主任id可为空
    deleted_flag: DeletedFlag = Field(default=DeletedFlag.flag1, alias="删除状态")


# 添加数据请求体
class AddClasses(BaseModel):
    class_id: int = Field(..., le=999999999, alias='班级id')  # 班级id，非空
    class_name: str = Field(...,max_length=15, alias='班级名称(必填)')  # 班级名称
    class_star_date: date = Field(...,alias='开班时间(必填)')  # 开班时间
    class_end_date: date = Field(default='9999-12-31', alias='结课时间(必填)')  # 结课时间
    course_id: Optional[int] = Field(None, alias='课程编号(选填)')  # 课程编号
    teacher_id: Optional[int] = Field(None, alias='授课老师编号(选填)')  # 授课老师编号
    head_teacher_id: int = Field(..., alias='班主任编号(必填)')  # 班主任编号
    tutor_id: Optional[int] = Field(None, alias='助教编号(选填)')  # 助教编号
    insert_date: date = Field(default=date.today(), alias='数据插入时间(必填)')  # 数据插入时间


# 修改班级数据请求体
class UpdateClasses(BaseModel):
    class_name: Optional[str] = Field(None, max_length=15, alias='班级名称')  # 班级名称,可选
    class_star_date: Optional[date] = Field(None, alias='开班时间')  # 开班时间
    class_end_date: Optional[date] = Field(None, alias='结课时间')  # 结课时间
    course_id: Optional[int] = Field(None, alias='课程编号')  # 课程编号
    teacher_id: Optional[int] = Field(None, alias='授课老师编号')  # 授课老师编号
    head_teacher_id: Optional[int] = Field(None, alias='班主任编号')  # 班主任编号
    tutor_id: Optional[int] = Field(None, alias='助教编号')  # 助教编号
    insert_date: Optional[date] = Field(None, alias='数据插入时间')  # 数据插入时间


# 班级信息响应体
class ClassesResponse(BaseModel):
    class_id: int = Field(alias='班级id')  # 班级id，非空
    class_name: str = Field(alias='班级名称')  # 班级名称
    class_star_date: date | None = Field(alias='开班时间')  # 开班时间
    class_end_date: date | None = Field(alias='结课时间')  # 结课时间
    course_id: int | None = Field(alias='课程编号')  # 课程编号
    teacher_id: int | None = Field(alias='授课老师编号')  # 授课老师编号
    head_teacher_id: int | None = Field(alias='班主任编号')  # 班主任编号
    tutor_id: int | None = Field(alias='助教编号')  # 助教编号
    insert_date: date | None = Field(alias='数据插入时间')  # 数据插入时间

    model_config = {
        "from_attributes": True,  # 让pydantic模型能接收数据库查出来的对象
        "populate_by_name": True,  # 支持别名
        "ordered": True  # 字段有序
    }


# 班级学生信息响应体
class ClassesStudent(BaseModel):
    class_id: int = Field(alias='班级id')
    class_name: str = Field(alias='班级名称')
    stu_id: int = Field(alias='学生id')
    stu_name: str = Field(alias='学生名称')
    gender: str | None = Field(alias='性别')
    age: int | None = Field(alias='年龄')
    hometown: str | None = Field(alias='籍贯')
    graduate_school: str | None = Field(alias='毕业院校')
    major: str | None = Field(alias='专业')
    education: str | None = Field(alias='学历')
    enroll_time: date | None = Field(alias='入学时间')
    graduate_time: date | None = Field(alias='毕业时间')

    model_config = {
        "from_attributes": True,  # 让pydantic模型能接收数据库查出来的对象
        "populate_by_name": True,  # 支持别名
        "ordered": True  # 字段有序
    }



# 班级学生成绩响应
class ClassStudentScore(BaseModel):
    class_id: int = Field(alias='班级id')
    class_name: str = Field(alias='班级名称')
    stu_id: int = Field(alias='学生id')
    stu_name: str = Field(alias='学生名称')
    test_num: int = Field(alias='考试序次')  # 考试序次
    exam_course_id: int = Field(alias='课程id')  # 课程id
    exam_date: date = Field(alias='考试日期')  # 考试日期
    score: float = Field(alias='考试日期')  # 考试分数

    model_config = {
        "from_attributes": True,  # 让pydantic模型能接收数据库查出来的对象
        "populate_by_name": True,  # 支持别名
        "ordered": True  # 字段有序
    }

