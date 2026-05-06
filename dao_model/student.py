# 数据访问层 DAO
# 作用：直接操作数据库，封装所有 SQLAlchemy 逻辑
# 只做数据库操作，不包含业务逻辑，提供给 API 调用
# 包含：增、删、改、查、统计
from sqlalchemy import func, TextClause
from FastAPI项目.table_model.dim_stu import Student
from FastAPI项目.pydantic_model.student import StudentCreate
from datetime import date
from sqlalchemy.orm import Session
# 【增】新增学生（对应 dim_stu 表）
# 功能：手动生成 stu_id，插入一条新学生记录
def add_student_dao(db: Session, stu: StudentCreate):
    try:  # 异常捕获，失败时回滚
        # 查询当前最大的stu_id，手动生成新id
        max_stu_id = db.query(func.max(Student.stu_id)).scalar() or 0
        # 新ID = 最大ID + 1
        new_stu_id = max_stu_id + 1
        # 构建 ORM 学生对象，对应数据库字段
        new_student = Student(
            # ========== 前端传的字段 ==========
            stu_name=stu.stu_name,#学⽣姓名
            gender=stu.gender,#性别
            age=stu.age,#年龄
            class_id=stu.class_id,#学⽣班级
            hometown=stu.hometown,#籍贯
            graduate_school=stu.graduate_school,#毕业院校
            major=stu.major,#专业
            education=stu.education,#学历
            advisor_id=stu.advisor_id,#顾问编号
            course_id=stu.course_id,
            stu_flag=stu.stu_flag,
            stu_id=new_stu_id,#学⽣编号
            enroll_time=stu.enroll_time ,#毕业时间
            graduate_time=stu.graduate_time,  #毕业时间
            # ========== 默认固定值 ==========
            deleted_flag=0,   # 逻辑删除标记：0=未删除
            create_time=date.today(),# 创建时间：当前日期
            end_time=None, # 结束时间：默认为空
            insert_date=date.today()# 插入日期：当前日期
        )
        # 将对象加入数据库会话
        db.add(new_student)
        # 提交事务，真正写入数据库
        db.commit()
        # 刷新对象，获取数据库生成的最新字段
        db.refresh(new_student)
        # 新增：返回统一格式的结果
        return {
            "status": "success",
            "msg": "新增学生成功",
            "data": {
                "stu_id": new_student.stu_id,
                "stu_name": new_student.stu_name
            }
        }
    # 异常捕获：数据库操作失败
    except Exception as e:
        # 新增：失败时回滚事务，避免脏数据
        db.rollback()
        return {
            "status": "fail",
            "msg": f"新增学生失败：{str(e)}",
            "data": None
        }
# 【查】简单学生列表（无条件、固定字段）
# 功能：返回精简字段 + 分页，用于首页列表
def Read_simple_student_dao(db: Session, page=1, size=10):
    try:
        # # 基础查询：只查未被逻辑删除的学生
        query = db.query(Student).filter(Student.deleted_flag == 0)
        # 统计总条数
        total = query.count()
        page = page if page else 1
        size = size if size else 10
        # 拼接分页：偏移量 + 限制条数
        query = query.offset((page - 1) * size).limit(size)
        # 执行查询，获取列表
        data_list = query.all()
        # 格式化：只返回需要的精简字段
        result = []
        for s in data_list:
            result.append({
                "stu_id": s.stu_id,          # 学生编号
                "class_id": s.class_id,      # 班级编号
                "stu_name": s.stu_name,      # 姓名
                "gender": s.gender,          # 性别
                "age": s.age,                # 年龄
                "hometown": s.hometown,      # 籍贯
                "education": s.education     # 学历
            })
        # 返回统一格式
        return {
            "status": "success",
            "total": total,
            "page": page,
            "size": size,
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"查询学生列表失败：{str(e)}",
            "data": [],
            "total": 0
        }
# 【查】多条件查询（支持：姓名模糊、学号精确、班级）
# 用于：单个学生查询、高级搜索
def Read_student_dao(db: Session, stu_name: str = None, stu_id: int = None,class_id: int = None,):
    try:
        # 基础查询：只查未删除的数
        query = db.query(Student).filter(Student.deleted_flag == 0)
        # 名字模糊查询
        if stu_name is not None and stu_name.strip() != "":
            query = query.filter(Student.stu_name.like(f"%{stu_name.strip()}%"))
        # 学号精确查询（有值才查，不传就不查）
        if stu_id is not None:
            query = query.filter(Student.stu_id == stu_id)
        # 班级精确查询（有值才查，不传就不查）
        if class_id is not None:
            query = query.filter(Student.class_id == class_id)

        data_list = query.all()
        # 格式化结果：把ORM对象转字典（前端能识别）
        result = []
        for s in data_list:
            result.append({
                "stu_id": s.stu_id,
                "stu_name": s.stu_name,
                "gender": s.gender,
                "age": s.age,
                "class_id": s.class_id,
                "major": s.major,
                "advisor_id": s.advisor_id,
                "course_id": s.course_id,
                "hometown": s.hometown,
                "graduate_school": s.graduate_school,
                "education": s.education,
                "stu_flag": s.stu_flag,
                "enroll_time": s.enroll_time.strftime("%Y-%m-%d") if s.enroll_time else None,
                "graduate_time": s.graduate_time.strftime("%Y-%m-%d") if s.graduate_time else None
            })
        # 5. 返回统一格式的结果
        return {
            "status": "success",
            "total": len(data_list),  # 用列表长度即可
            "data": result
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"查询学生失败：{str(e)}",
            "data": [],
            "total": 0
        }
# 【删】删除学生
def del_student_dao(db: Session, stu_id: int):
    try:
        # 1. 根据学号查学生
        stu_obj = db.query(Student).filter(
            Student.stu_id == stu_id,
            Student.deleted_flag == 0
        ).first()

        if not stu_obj:
            return {
                "status": "fail",
                "msg": "该学生不存在或已删除",
                "data": None
            }

        # 2. 逻辑删除
        stu_obj.deleted_flag = 1
        db.commit()

        return {
            "status": "success",
            "msg": "学生删除成功",
            "data": {
                "stu_id": stu_obj.stu_id,
                "stu_name": stu_obj.stu_name
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "fail",
            "msg": f"删除失败：{str(e)}",
            "data": None
        }
# 【改】修改学生信息
# 根据 stu_id 更新所有字段
def update_student_dao(db: Session, stu_id: int, stu: StudentCreate):
    try:
        # 1. 查要修改的学生
        stu_obj = db.query(Student).filter(
            Student.stu_id == stu_id,
            Student.deleted_flag == 0
        ).first()

        if not stu_obj:
            return {
                "status": "fail",
                "msg": "学生不存在或已删除",
                "data": None
            }

        # 2. 更新字段（全部覆盖）
        stu_obj.stu_name = stu.stu_name
        stu_obj.gender = stu.gender
        stu_obj.age = stu.age
        stu_obj.class_id = stu.class_id
        stu_obj.hometown = stu.hometown
        stu_obj.graduate_school = stu.graduate_school
        stu_obj.major = stu.major
        stu_obj.education = stu.education
        stu_obj.advisor_id = stu.advisor_id
        stu_obj.course_id = stu.course_id
        stu_obj.stu_flag = stu.stu_flag

        # 如果需要更新时间
        if stu.enroll_time:
            stu_obj.enroll_time = stu.enroll_time
        if stu.graduate_time:
            stu_obj.graduate_time = stu.graduate_time

        # 3. 提交
        db.commit()
        db.refresh(stu_obj)

        return {
            "status": "success",
            "msg": "修改成功",
            "data": {
                "stu_id": stu_obj.stu_id,
                "stu_name": stu_obj.stu_name
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "fail",
            "msg": f"修改失败：{str(e)}",
            "data": None
        }
# 2.6统计分析
# 查询所有超过30岁的学员的信息
def Read_student_over_30_dao(db: Session):
    try:
        # 未删除 + 年龄>30
        query = db.query(Student).filter(
            Student.deleted_flag == 0,
            Student.age > 30
        )
        data_list = query.all()
        # 格式化结果：把ORM对象转字典（前端能识别）
        result = []
        for s in data_list:
            result.append({
                "stu_id": s.stu_id,
                "stu_name": s.stu_name,
                "gender": s.gender,
                "age": s.age,
                "class_id": s.class_id,
                "major": s.major,
                "advisor_id": s.advisor_id,
                "course_id": s.course_id,
                "hometown": s.hometown,
                "graduate_school": s.graduate_school,
                "education": s.education,
                "stu_flag": s.stu_flag,
                "enroll_time": s.enroll_time.strftime("%Y-%m-%d") if s.enroll_time else None,
                "graduate_time": s.graduate_time.strftime("%Y-%m-%d") if s.graduate_time else None
            })
        # 5. 返回统一格式的结果
        return {
            "status": "success",
            "msg": f"查询到 {len(result)} 条数据",
            "data": result,
            "total": len(result)
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"查询学生失败：{str(e)}",
            "data": [],
            "total": 0
        }

# 【统计】按班级统计：总人数、男生、女生人数
# 使用原生 SQL 统计
def stat_class_gender_dao(db: Session):
    try:
        from sqlalchemy import text
        # 原生SQL：分组统计班级人数与性别
        sql:TextClause = text("""
            SELECT 
                class_id,
                COUNT(*) AS total,
                SUM(CASE WHEN gender = '男' THEN 1 ELSE 0 END) AS male,
                SUM(CASE WHEN gender = '女' THEN 1 ELSE 0 END) AS female
            FROM dim_stu
            GROUP BY class_id
        """)
        result = db.execute(sql).fetchall()

        data = []
        for row in result:
            data.append({
                "class_id": row[0],
                "total": row[1],
                "男": row[2],
                "女": row[3]
            })

        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        return {
            "status": "fail",
            "msg": str(e)
        }