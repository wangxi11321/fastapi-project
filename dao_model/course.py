from sqlalchemy.orm import Session
from FastAPI项目.table_model.dim_course import DimCourse
from FastAPI项目.pydantic_model.course import CourseCreate
from datetime import date
from sqlalchemy import func

PERMANENT_END_DATE = date(9999, 12, 31)



#  新增课程
def create_course(db: Session
                , data: CourseCreate): # 根据请求体限制传入的数据
    # 创建一个数据库对象，把前端传过来的Pydantic数据 → 变成字典字典 **表示拆成 key=value 的形式，传给数据库模型
    course = DimCourse(**data.model_dump())
    db.add(course)  # 把这条数据 加入到数据库会话
    db.commit() # 新增之后要提交
    db.refresh(course) # 刷新数据 放入表中后会生成一个主键ID
    return course # 把插入后的完整数据返回给前端

# 批量新增课程
def batch_create_course(db: Session, courses_data: list):

    courses = [DimCourse(**data.model_dump()) for data in courses_data]
    db.add_all(courses)
    db.commit()
    for course in courses:
        db.refresh(course)
    return courses

# 查询单个课程
def get_course_by_course_id(db: Session, course_id: int):
    # select * from dim_course where course_id = ? and deleted_flag = 0;
    return db.query(DimCourse).filter(
        # select * from dim_course where course_id = ? and deleted_flag = 0;
        DimCourse.course_id == course_id, # 要查询的课程ID和表里的ID进行匹配
        DimCourse.deleted_flag == 0 # 只查未删除的
    ).first()

# 批量查询-查询列表
def get_course_list(db: Session
                    , skip=0 # 页码偏移量 跳过多少
                    , limit=10 # 每页条数
                    , name=None): # 课程名称模糊搜索匹配 默认是None
    # select * from dim_course where deleted_flag = 0;
    query = db.query(DimCourse).filter(DimCourse.deleted_flag == 0) # 只查未删除的
    if name:
        query = query.filter(DimCourse.course_name.like(f"%{name}%")) # SQL中的like模糊匹配
    # 如果不传name进行模糊匹配 直接返回第一次查到的数据
    # 如果传了name进行模糊匹配 返回匹配到的所有数据(模糊匹配不到就会返回空)
    return query.offset(skip).limit(limit).all() # 返回匹配到的所有数据

# 更新课程信息
def update_course(db: Session
                  , course_id: int
                  , data: dict):
    # 先验证课程是否存在
    course = get_course_by_course_id(db, course_id)
    if not course:
        return None # 没找到要更新的课程 返回None
    # 只更新非None的字段
    for k, v in data.items():
        setattr(course, k, v)
    # 自动更新插入时间
    course.insert_date = date.today()
    db.commit() # 更新之后要提交
    return True


# 软删除 只对删除表示进行修改 不删除数据
def delete_course(db: Session
                , course_id: int):
    # 先验证课程是否存在
    course = get_course_by_course_id(db, course_id)
    if not course:
        return None
    course.deleted_flag = 1 # 删除标识改为1
    course.end_time = date.today() # 失效时间改为今天
    db.commit() # 更新之后要提交
    return True

# 恢复误删的课程（撤回）
def restore_course(db: Session
                   , course_id: int):

    course = db.query(DimCourse).filter(
        DimCourse.course_id == course_id,
        DimCourse.deleted_flag == 1
    ).first()
    if not course:
        return None
    course.deleted_flag = 0
    course.end_time = PERMANENT_END_DATE
    db.commit()
    return True

# 查询已删除的课程列表
def get_deleted_course_list(db: Session, skip=0, limit=10):

    return db.query(DimCourse).filter(
        DimCourse.deleted_flag == 1
    ).offset(skip).limit(limit).all()

# 统计有效课程数量
def count_course(db: Session):
    # select count(1) from dim_course where deleted_flag = 0;
    return db.query(DimCourse).filter(DimCourse.deleted_flag == 0).count()

# 统计已删除课程数量
def count_deleted_course(db: Session):
    return db.query(DimCourse).filter(DimCourse.deleted_flag == 1).count()

# 统计每门课有多少学生学习
def count_students_by_course(db: Session):
    """统计每门课有多少学生学习"""
    # 导入分数表
    from FastAPI项目.table_model.score_info import ScoreInfo
    # SQL语句如下
    # select course_id, course_name, count(distinct stu_id) as student_count
    # from dim_course
    # left join score_info on score_info.exam_course_id = dim_course.course_id
    # where dim_course.deleted_flag = 0
    # and score_info.delete_flag = 0
    # group by course_id, course_name;
    results = db.query(
        DimCourse.course_id,
        DimCourse.course_name,
        func.count(func.distinct(ScoreInfo.stu_id)).label('student_count') # 别名
    ).join(
        # 关联分数表 通过考试课程ID关联课程表的课程ID
        ScoreInfo, ScoreInfo.exam_course_id == DimCourse.course_id
    ).filter(
        # 只查询删除标识为0的数据
        DimCourse.deleted_flag == 0,
        ScoreInfo.delete_flag == 0
    ).group_by(
        # 课程ID和课程名称分组
        DimCourse.course_id,
        DimCourse.course_name
    ).all()

    return [
        {
            "course_id": r.course_id,
            "course_name": r.course_name,
            "student_count": r.student_count
        }
        for r in results
    ]



