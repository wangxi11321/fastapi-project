from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from FastAPI项目.pydantic_model.score_pdmd import ScoreInfoCreate, ScoreInfoUpdate, ScoreInfoOut, ScoreInfoRead
from FastAPI项目.dao_model.score_crud import create_score_info, read_all_score, read_score_by_stuid, update_score_by_test_num, \
    delete_score_by_test_num, read_score_by_conditions
from FastAPI项目.db_model.database import get_db


score_router = APIRouter()


# 添加学生成绩信息
@score_router.post("/", response_model=ScoreInfoOut
                            , response_model_exclude_unset=True
                            , summary="添加学生成绩信息")
def add_score(score_info: ScoreInfoCreate, db: Session = Depends(get_db)):
    result = create_score_info(db, score_info)
    if result:
        return {"message": "添加成功", "data": result}
    raise HTTPException(status_code=409, detail="添加失败，该学生成绩信息已存在")


# 查找所有学生成绩信息
@score_router.get("/get_all", response_model=ScoreInfoOut
                    , response_model_exclude_unset=True
                    , summary="查找所有学生成绩信息")
def search_all(db: Session = Depends(get_db)):
    result = read_all_score(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="对不起，目前数据未录入")


# 查找指定学生ID的成绩信息
@score_router.get("/{stu_id}"
                    , response_model=ScoreInfoOut
                    , response_model_exclude_unset=True
                    , summary="查找指定学生ID的成绩信息")
def search_by_stuid(stu_id: int = Path(gt=0), db: Session = Depends(get_db)):
    result = read_score_by_stuid(db, stu_id)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到该学生的成绩")


# 更新/修改指定学生的某次成绩
@score_router.put("/update"
                , response_model=ScoreInfoOut
                , response_model_exclude_unset=True
                , summary="更新/修改指定学生的某次成绩")
def change_score(stu_id: int,
                 test_num: int,
                 exam_course_id: int,
                 score_info: ScoreInfoUpdate,
                 db: Session = Depends(get_db)):
    result = update_score_by_test_num(db, stu_id, test_num, exam_course_id, score_info)
    if result:
        return {"message": "修改成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到该学生该门课程的该次成绩")


# 删除指定学生的某次成绩信息
@score_router.delete("/delete"
                    , response_model=ScoreInfoOut
                    , response_model_exclude_unset=True
                    , summary="删除指定学生的某次成绩信息")
def delete_score(stu_id: int,
                 test_num: int,
                 exam_course_id: int,
                 db: Session = Depends(get_db)):
    result = delete_score_by_test_num(db, stu_id, test_num, exam_course_id)
    if result:
        return {"message": "删除成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到该学生该门课程的该次成绩")


# 按多条件查询学生成绩
@score_router.post("/get_by_conditions"
                    , response_model=ScoreInfoOut
                    , response_model_exclude_unset=True
                    , summary="按多条件查询学生成绩")
def get_score_by_conditions(score_read: ScoreInfoRead, db: Session = Depends(get_db)):
    result = read_score_by_conditions(db, score_read)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到该查询条件的成绩，请检查输入条件而保证条件正确")

