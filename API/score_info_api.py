from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from FastAPI项目.pydantic_model.score_pdmd import ScoreInfoCreate, ScoreInfoUpdate, ScoreInfoOut, ScoreInfoRead
from FastAPI项目.dao_model.score_crud import create_score_info, read_all_score, read_score_by_stuid, update_score_by_test_num, \
    delete_score_by_test_num, read_score_by_conditions
from FastAPI项目.db_model.database import get_db
from FastAPI项目.common.schemas import success_response, fail_response


score_router = APIRouter()


@score_router.get("/scores", summary="查询成绩列表")
def search_scores(db: Session = Depends(get_db), 
                  stu_id: int = Query(None, description="学生ID"),
                  test_num: int = Query(None, description="考试序次"),
                  exam_course_id: int = Query(None, description="课程ID")):
    if stu_id or test_num or exam_course_id:
        score_read = ScoreInfoRead(stu_id=stu_id, test_num=test_num, exam_course_id=exam_course_id)
        result = read_score_by_conditions(db, score_read)
    else:
        result = read_all_score(db)
    
    if result:
        return success_response(data=result)
    return fail_response(msg="未查询到成绩信息")


@score_router.get("/scores/{stu_id}", summary="查询指定学生成绩")
def search_by_stuid(stu_id: int = Path(gt=0, description="学生ID"), db: Session = Depends(get_db)):
    result = read_score_by_stuid(db, stu_id)
    if result:
        return success_response(data=result)
    return fail_response(msg="未找到该学生的成绩")


@score_router.post("/scores", summary="添加学生成绩")
def add_score(score_info: ScoreInfoCreate, db: Session = Depends(get_db)):
    result = create_score_info(db, score_info)
    if result:
        return success_response(msg="添加成功", data=result)
    return fail_response(msg="添加失败，该学生成绩信息已存在")


@score_router.put("/scores/{stu_id}", summary="更新学生成绩")
def change_score(stu_id: int = Path(gt=0, description="学生ID"),
                 test_num: int = Query(..., description="考试序次"),
                 exam_course_id: int = Query(..., description="课程ID"),
                 score_info: ScoreInfoUpdate = Depends(),
                 db: Session = Depends(get_db)):
    result = update_score_by_test_num(db, stu_id, test_num, exam_course_id, score_info)
    if result:
        return success_response(msg="修改成功", data=result)
    return fail_response(msg="未找到该学生该门课程的该次成绩")


@score_router.delete("/scores/{stu_id}", summary="删除学生成绩")
def delete_score(stu_id: int = Path(gt=0, description="学生ID"),
                 test_num: int = Query(..., description="考试序次"),
                 exam_course_id: int = Query(..., description="课程ID"),
                 db: Session = Depends(get_db)):
    result = delete_score_by_test_num(db, stu_id, test_num, exam_course_id)
    if result:
        return success_response(msg="删除成功", data=result)
    return fail_response(msg="未找到该学生该门课程的该次成绩")
