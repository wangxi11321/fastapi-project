from datetime import date

from sqlalchemy import and_, func, desc
from sqlalchemy.orm import Session

from FastAPI项目.table_model.score_info import ScoreInfo
from FastAPI项目.table_model.dim_stu import Student
from FastAPI项目.pydantic_model.score_pdmd import ScoreInfoCreate, ScoreInfoRead, ScoreInfoUpdate, ScoreInfoData, HighScoreData, \
    LowScoreData, AvgScoreData


# 定义添加成绩信息的功能，先判断是否已存在，不存在则添加，若存在返回空值用于接口抛出异常
def create_score_info(db: Session, score_info: ScoreInfoCreate):
    exist_data = db.query(ScoreInfo).filter(ScoreInfo.test_num == score_info.test_num,
                                            ScoreInfo.stu_id == score_info.stu_id,
                                            ScoreInfo.exam_course_id == score_info.exam_course_id,
                                            ScoreInfo.delete_flag == 0
                                            ).first()
    if not exist_data:
        db_score = ScoreInfo(
            class_id=score_info.class_id,
            test_num=score_info.test_num,
            stu_id=score_info.stu_id,
            exam_course_id=score_info.exam_course_id,
            exam_date=score_info.exam_date,
            score=score_info.score,
            delete_flag=0,
            creation_date=date.today(),
            insert_date=date.today()
        )
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
        # 将数据库对象转换为Pydantic模型返回
        return ScoreInfoData.model_validate(db_score)
    else:
        return None


# 所有查询条件都要注意删除标识为0的条件
# 定义查询所有人成绩信息的功能
def read_all_score(db: Session):
    # 查询数据库返回all_score是包含ScoreInfo模型对象的列表
    db_score = db.query(ScoreInfo).filter(ScoreInfo.delete_flag == 0).all()
    # 将数据库对象转换为Pydantic模型返回
    return [ScoreInfoData.model_validate(score) for score in db_score]



# 定义按stu_id查询成绩的功能
def read_score_by_stuid(db: Session, stu_id: int):
    # 每个学生有不止一次成绩，所以最后用all
    db_score = db.query(ScoreInfo).filter(ScoreInfo.stu_id == stu_id, ScoreInfo.delete_flag == 0).all()
    if db_score:
        # 将数据库对象转换为Pydantic模型返回
        return [ScoreInfoData.model_validate(score) for score in db_score]
    else:
        return None


# 定义修改指定学生某次成绩的功能
def update_score_by_test_num(db: Session, stu_id: int, test_num: int, exam_course_id: int, score_info: ScoreInfoUpdate):
    # 先查一遍，确保能查到再更新并返回结果，查不到返回None，然后由接口抛出异常
    db_score = db.query(ScoreInfo).filter(ScoreInfo.stu_id == stu_id,
                                          ScoreInfo.test_num == test_num,
                                          ScoreInfo.exam_course_id == exam_course_id,
                                          ScoreInfo.delete_flag == 0
                                         ).first()
    if db_score:
        db_score.insert_date = date.today()
        # 生成更新数据
        update_data = score_info.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(db_score, k, v)
        db.commit()
        db.refresh(db_score)
        # 将数据库对象转换为Pydantic模型返回
        return ScoreInfoData.model_validate(db_score)
    return None


# 定义删除指定学生成绩的功能
def delete_score_by_test_num(db: Session, stu_id: int, test_num: int, exam_course_id: int):
    db_score = db.query(ScoreInfo).filter(ScoreInfo.stu_id == stu_id,
                                          ScoreInfo.test_num == test_num,
                                          ScoreInfo.exam_course_id == exam_course_id,
                                          ScoreInfo.delete_flag == 0
                                          ).first()
    if db_score:
        db_score.delete_flag = 1
        db.commit()
        db.refresh(db_score)
        # 将数据库对象转换为Pydantic模型返回
        return ScoreInfoData.model_validate(db_score)
    return None


# 定义按自定义组合条件(and条件)查询学生信息的功能
def read_score_by_conditions(db: Session, read_conditions: ScoreInfoRead):
    # 基础查询条件:删除标识为0
    and_conditions = [ScoreInfo.delete_flag == 0]
    # 自定义条件的存在判断与拼接
    if read_conditions.class_id is not None:
        and_conditions.append(ScoreInfo.class_id == read_conditions.class_id)
    if read_conditions.test_num is not None:
        and_conditions.append(ScoreInfo.test_num == read_conditions.test_num)
    if read_conditions.stu_id is not None:
        and_conditions.append(ScoreInfo.stu_id == read_conditions.stu_id)
    if read_conditions.exam_course_id is not None:
        and_conditions.append(ScoreInfo.exam_course_id == read_conditions.exam_course_id)
    if read_conditions.exam_date is not None:
        and_conditions.append(ScoreInfo.exam_date == read_conditions.exam_date)
    if read_conditions.score is not None:
        and_conditions.append(ScoreInfo.score == read_conditions.score)
    if read_conditions.score_min is not None:
        and_conditions.append(ScoreInfo.score >= read_conditions.score_min)
    if read_conditions.score_max is not None:
        and_conditions.append(ScoreInfo.score <= read_conditions.score_max)
    db_data = db.query(ScoreInfo).filter(and_(*and_conditions)).all()
    if db_data:
        # 将数据库对象转换为Pydantic模型返回
        return [ScoreInfoData.model_validate(data) for data in db_data]
    return None


# 查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩
def read_high_score_info(db: Session):
    # 子查询找到最低分>=80分的学生
    sub_query = (db.query(ScoreInfo.stu_id,Student.stu_name)
               .join(Student, ScoreInfo.stu_id ==Student.stu_id)
               .filter(ScoreInfo.delete_flag == 0)
               .group_by(ScoreInfo.stu_id,Student.stu_name)
               .having(func.min(ScoreInfo.score)>=80)
               .subquery())
    # 主查询再把最低分>=80分的学生的成绩也查到
    # subquery()得到的是子查询对象，要取到子查询的字段需要子查询.c.字段，.c表示子查询的列（column）
    db_data = (db.query(sub_query.c.stu_id, sub_query.c.stu_name, ScoreInfo.score)
               .join(ScoreInfo,sub_query.c.stu_id == ScoreInfo.stu_id)
               .filter(ScoreInfo.delete_flag == 0)
               .all())
    if db_data:
        # 将数据库对象转换为Pydantic模型返回
        return [HighScoreData.model_validate(data) for data in db_data]
    return None


# 查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
def read_low_score_info(db: Session):
    # 子查询，查出删除标识为0且两次以上不及格的学生id和班级id
    sub_query = (db.query(ScoreInfo.stu_id, ScoreInfo.class_id)
               .filter(ScoreInfo.score<60, ScoreInfo.delete_flag == 0)
               .group_by(ScoreInfo.stu_id, ScoreInfo.class_id)
               .having(func.count() >= 2).subquery())
    # 主查询，查出两次以上不及格的学生姓名，班级id和不及格成绩
    db_data = (db.query(Student.stu_name, ScoreInfo.class_id, ScoreInfo.score)
               .join(Student, Student.stu_id == ScoreInfo.stu_id)
               .join(sub_query, (sub_query.c.stu_id == ScoreInfo.stu_id)
                     &(sub_query.c.class_id == ScoreInfo.class_id))
               .all())
    if db_data:
        # 将数据库对象转换为Pydantic模型返回
        return [LowScoreData.model_validate(data) for data in db_data]
    return None


# 统计每次考试每个班级的平均分，按照从⾼到低排序
def read_avg_score_info(db:Session):
    db_data = (db.query(ScoreInfo.class_id, ScoreInfo.test_num, func.avg(ScoreInfo.score).label("avg_score"))
               .filter(ScoreInfo.delete_flag == 0)
               .group_by(ScoreInfo.class_id, ScoreInfo.test_num)
               .order_by(desc("avg_score"))
               .all())
    if db_data:
        # 将数据库对象转换为Pydantic模型返回
        return [AvgScoreData.model_validate(data) for data in db_data]
    return None