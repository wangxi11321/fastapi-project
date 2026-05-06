#额外新增联表查询功能
from sqlalchemy import func
from sqlalchemy.orm import Session
from FastAPI项目.table_model.dim_stu import Student
from FastAPI项目.table_model.score_info import ScoreInfo

# ===================== 1. 计算总分 =====================
# 计算单个学生所有科目总分（学生表 + 成绩表 JOIN）
def calc_total_score(db: Session, stu_id: int):
    try:
        # ===================== 手写 JOIN 联表查询 =====================
        result = (
            db.query(
                Student.stu_id,
                Student.stu_name,
                func.sum(ScoreInfo.score).label("total_score")
            )
            .join(ScoreInfo, Student.stu_id == ScoreInfo.stu_id)
            .filter(Student.stu_id == stu_id)
            .filter(ScoreInfo.delete_flag == 0)
            .group_by(Student.stu_id, Student.stu_name)
            .first()
        )

        if not result:
            return {
                "status": "success",
                "stu_id": stu_id,
                "stu_name": None,
                "total_score": 0,
                "msg": "该学生暂无成绩"
            }

        return {
            "status": "success",
            "stu_id": result.stu_id,
            "stu_name": result.stu_name,
            "total_score": float(result.total_score)
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"计算总分失败：{str(e)}"
        }

# ===================== 2. 总分排名 =====================
def get_total_rank(db: Session, stu_name: str):
    try:
        # 1. 先查询【所有学生】的总分（降序）
        data = db.query(
            Student.stu_name,
            func.sum(ScoreInfo.score).label("total_score")
        ).join(
            ScoreInfo, Student.stu_id == ScoreInfo.stu_id
        ).filter(
            Student.deleted_flag == 0,
            ScoreInfo.delete_flag == 0
        ).group_by(
            Student.stu_id,
            Student.stu_name
        ).order_by(
            func.sum(ScoreInfo.score).desc()
        ).all()

        # 2. 遍历找排名
        rank = 0
        total_score = 0
        found = False

        for index, item in enumerate(data):
            if item.stu_name == stu_name:
                rank = index + 1
                total_score = float(item.total_score)
                found = True
                break

        if not found:
            return {
                "status": "success",
                "stu_name": stu_name,
                "rank": 0,
                "total_score": 0,
                "msg": "该学生暂无成绩"
            }

        return {
            "status": "success",
            "stu_name": stu_name,
            "rank": rank,
            "total_score": total_score
        }

    except Exception as e:
        # 打印真实错误！！！
        print("错误详情：", str(e))
        return {
            "status": "fail",
            "msg": f"排名查询失败：{str(e)}"
        }
# ===================== 3. 单科排名（语文/数学/英语） =====================
def get_subject_rank(db: Session, stu_name: str):
    try:
        # 1. 先查出这个学生的所有科目成绩
        student = db.query(Student).filter(
            Student.stu_name == stu_name,
            Student.deleted_flag == 0
        ).first()

        if not student:
            return {"status": "fail", "msg": "学生不存在"}

        # 2. 子查询：每一门科目，所有人的排名
        from sqlalchemy import func
        rank_subquery = db.query(
            ScoreInfo.exam_course_id,
            ScoreInfo.stu_id,
            ScoreInfo.score,
            func.rank()
            .over(
                partition_by=ScoreInfo.exam_course_id,
                order_by=ScoreInfo.score.desc()
            ).label("rank")
        ).filter(
            ScoreInfo.delete_flag == 0
        ).subquery()

        # 3. 关联查询：该学生每科的成绩 + 排名
        result = db.query(
            ScoreInfo.exam_course_id,
            ScoreInfo.score,
            rank_subquery.c.rank
        ).join(
            rank_subquery,
            (ScoreInfo.stu_id == rank_subquery.c.stu_id) &
            (ScoreInfo.exam_course_id == rank_subquery.c.exam_course_id)
        ).filter(
            ScoreInfo.stu_id == student.stu_id,
            ScoreInfo.delete_flag == 0
        ).all()

        # 4. 格式化返回
        subjects = []
        for exam_course_id, score, rank in result:
            subjects.append({
                "course_id": exam_course_id,
                "score": float(score) if score else 0,
                "rank": rank
            })

        return {
            "status": "success",
            "stu_name": stu_name,
            "stu_id": student.stu_id,
            "subjects": subjects
        }

    except Exception as e:
        return {
            "status": "fail",
            "msg": f"单科排名查询失败：{str(e)}"
        }
# ===================== 4. 近5次成绩趋势 =====================
def get_score_trend(db: Session, stu_name: str):
    try:
        # 1. 先根据姓名找到学生
        student = db.query(Student).filter(
            Student.stu_name == stu_name,
            Student.deleted_flag == 0
        ).first()

        if not student:
            return {"status": "fail", "msg": "学生不存在"}

        # 2. 查询该学生所有成绩（按考试次数排序）
        scores = db.query(
            ScoreInfo.exam_course_id,
            ScoreInfo.test_num,
            ScoreInfo.score
        ).filter(
            ScoreInfo.stu_id == student.stu_id,
            ScoreInfo.delete_flag == 0
        ).order_by(
            ScoreInfo.exam_course_id,
            ScoreInfo.test_num
        ).all()

        # 3. 按科目分组
        from collections import defaultdict
        subject_map = defaultdict(list)
        for cid, test_num, score in scores:
            subject_map[cid].append(score)

        # 4. 计算每科趋势
        result = []
        for cid, score_list in subject_map.items():
            # 只取最近5次
            recent = score_list[-5:]
            trend = "平稳"

            if len(recent) >= 2:
                first = recent[0]
                last = recent[-1]
                diff = last - first

                if diff > 5:
                    trend = "上升"
                elif diff < -5:
                    trend = "下降"
                else:
                    trend = "平稳"

            result.append({
                "course_id": cid,
                "recent_scores": [float(s) for s in recent],
                "trend": trend
            })

        return {
            "status": "success",
            "stu_name": stu_name,
            "stu_id": student.stu_id,
            "subjects": result
        }

    except Exception as e:
        print("趋势错误：", str(e))
        return {
            "status": "fail",
            "msg": f"成绩趋势查询失败：{str(e)}"
        }