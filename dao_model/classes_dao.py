from datetime import date

from sqlalchemy import func, case, and_

from FastAPI项目.table_model.dim_class import DimClass
from FastAPI项目.table_model.score_info import ScoreInfo
from FastAPI项目.table_model.dim_stu import Student
from FastAPI项目.table_model.employment_info import EmploymentInfo

#判断班级id是否存在或已删除
def id_in_table(db, class_id):
    result = db.query(DimClass).filter(DimClass.class_id == class_id,DimClass.deleted_flag == 0).first()
    if result:
        return 1
    else:
        return 0

def get_all_class(db, getclass):
    # 通过班主任id以及班级状态查询班级信息
    if getclass.head_teacher_id is None:
        return db.query(DimClass).filter(DimClass.deleted_flag == getclass.deleted_flag.value).all()
    all_class = db.query(DimClass).filter(
        and_(DimClass.head_teacher_id == getclass.head_teacher_id,
             DimClass.deleted_flag == getclass.deleted_flag.value
             )).all()
    return all_class


#通过班级iD获取班级信息
def get_one_class(db, class_id):
    get_one_class = db.query(DimClass).filter(DimClass.class_id == class_id, DimClass.deleted_flag == 0).first()
    print(get_one_class)
    return get_one_class


#添加班级信息
def add_classes(db, addclass):
    if id_in_table(db, addclass.class_id):
        return 0
    aclass = DimClass(**addclass.model_dump())  # 把python模型对象转成普通字典,赋值给对象
    db.add(aclass)  # 添加数据
    db.commit()
    return 1

#更新班级信息
def update_classes(db, class_id, updateclass):
    udclass = updateclass.model_dump()  # 把修改的数据以字典的格式传进来
    db.query(DimClass).filter(DimClass.class_id == class_id).update(
        {i: j for i, j in udclass.items() if j is not None})
    db.commit()

#删除班级信息
def del_classes(db, class_id):
    db.query(DimClass).filter(
        DimClass.class_id == class_id,
        DimClass.deleted_flag == 0
    ).update({'class_end_date': date.today(), 'deleted_flag': 1})
    db.commit()


# 把查询出来的元组内容转成字典合并
def retuen_all_result(result):
    alldata = []
    for i in result:
        thedict = {}
        for j in range(0, len(i)):
            thedict = thedict | i[j].__dict__
        alldata.append(thedict)
    return alldata


# 查询班级学生信息
def class_student(db, class_id):
    result = db.query(DimClass, Student).join(
        Student, DimClass.class_id == Student.class_id
    ).filter(DimClass.class_id == class_id
             , DimClass.deleted_flag == 0).all()
    allstudents = retuen_all_result(result)
    return allstudents

#查询班级所有学生成绩
def cls_stu_score(db, class_id,test_num):
    if test_num is None:
        result = db.query(DimClass, Student, ScoreInfo).join(
            Student, DimClass.class_id == Student.class_id
        ).join(ScoreInfo,
               Student.stu_id == ScoreInfo.stu_id
               ).filter(DimClass.class_id == class_id
                        , DimClass.deleted_flag == 0).all()
        allscore = retuen_all_result(result)
        return allscore

    result = db.query(DimClass, Student, ScoreInfo).join(
        Student, DimClass.class_id == Student.class_id
    ).join(ScoreInfo,
           Student.stu_id == ScoreInfo.stu_id
           ).filter(DimClass.class_id == class_id
                    , DimClass.deleted_flag == 0,
                    ScoreInfo.test_num == test_num).all()
    allscore = retuen_all_result(result)
    return allscore

#统计分析
#统计班级总人数，男女生比例
def cls_stu_count(db):
    man_count = func.count(case((Student.gender == '男', 1), else_=None)).label('man_count')
    woman_count = func.count(case((Student.gender == '女', 1), else_=None)).label('woman_count')

    result = db.query(DimClass.class_id, DimClass.class_name, man_count, woman_count).join(
        Student, DimClass.class_id == Student.class_id
    ).filter(
        and_(DimClass.deleted_flag == 0, Student.deleted_flag == 0)
    ).group_by(DimClass.class_id, DimClass.class_name).all()

    data = []
    for i in result:
        data.append({'班级id': i[0],
                     '班级名称': i[1],
                     '总人数': i.man_count + i.woman_count,
                     '男生占比': round(float(i.man_count / (i.man_count + i.woman_count)), 2),
                     '女生占比': round(float(i.woman_count / (i.woman_count + i.man_count)), 2)})
    return data

#统计班级各个序次的平均分
def class_sc_avg(db,test_num):
    data = []
    if test_num is None:
        result = db.query(DimClass.class_id.label('class_id'),
                          DimClass.class_name.label('class_name'),
                          ScoreInfo.test_num.label('test_num'),
                          func.round(func.avg(ScoreInfo.score), 2).label('score')).join(
            Student,
            DimClass.class_id == Student.class_id
        ).join(ScoreInfo,
               Student.stu_id == ScoreInfo.stu_id
               ).filter(
            and_(DimClass.deleted_flag == 0,
                 Student.deleted_flag == 0,
                 ScoreInfo.delete_flag == 0)
        ).group_by(
            DimClass.class_id, DimClass.class_name, ScoreInfo.test_num).all()
    else:
        result = db.query(DimClass.class_id.label('class_id'),
                          DimClass.class_name.label('class_name'),
                          ScoreInfo.test_num.label('test_num'),
                          func.round(func.avg(ScoreInfo.score), 2).label('score')).join(
            Student,
            DimClass.class_id == Student.class_id
        ).join(ScoreInfo,
               Student.stu_id == ScoreInfo.stu_id
               ).filter(
            and_(DimClass.deleted_flag == 0,
                 Student.deleted_flag == 0,
                 ScoreInfo.delete_flag == 0,
                 ScoreInfo.test_num == test_num)
        ).group_by(
            DimClass.class_id, DimClass.class_name, ScoreInfo.test_num).all()

    for i in result:
        data.append({'班级id': i.class_id,
                     '班级名称': i.class_name,
                     '考试序次': i.test_num,
                     '平均分': i.score})
    data.sort(key=lambda x: x['平均分'], reverse=True)
    return data

#统计班级平均就业天数
def class_em_avg(db):
    result = db.query(DimClass.class_id.label('class_id'),
                      DimClass.class_name.label('class_name'),
                      func.round(func.avg(func.datediff(
                          EmploymentInfo.employment_date,
                          EmploymentInfo.first_offer_date)
                               ),1).label('days')).join(Student,
                                       DimClass.class_id == Student.class_id
                                       ).join(EmploymentInfo,
                                              Student.stu_id == EmploymentInfo.stu_id
                                              ).filter(and_(DimClass.deleted_flag == 0,
                                                            Student.deleted_flag == 0,
                                                            EmploymentInfo.delete_flag == 0,
                                                            EmploymentInfo.employment_status == '已就业')
                                                       ).group_by(DimClass.class_id, DimClass.class_name).all()
    data = []
    for i in result:
        data.append({'班级id': i.class_id,
                     '班级名称': i.class_name,
                     '平均就业天数': i.days})
    return data
