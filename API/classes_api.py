from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from FastAPI项目.dao_model.classes_dao import get_all_class, get_one_class, add_classes, update_classes, id_in_table, \
    del_classes, class_student, cls_stu_score
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.classes_pdmd import GetClasses, AddClasses, UpdateClasses, ClassesResponse, \
    ClassesStudent, ClassStudentScore


classes_router = APIRouter()


# 查询班级列表，支持筛选班主任、班级状态
@classes_router.get("/classes", response_model=dict,summary="查询班主任所带班级")
def get_classes(db: Session = Depends(get_db), getclass: GetClasses = Depends()):  # 依赖注入
    # 通过get_all_class功能获取到查询结果
    result = get_all_class(db, getclass)
    if result:
        # 让查出来的数据有序，且表头以别名显示
        return {'message': '查询成功',
                'data': [ClassesResponse.model_validate(i).model_dump(by_alias=True) for i in result]}
    raise HTTPException(status_code=404, detail="班级不存在")  # 班级不存在抛出404异常


# 获取单个班级详情
@classes_router.get("/classes/{class_id}", response_model=dict,summary="查询单个班级信息")
def get_class_by_id(db: Session = Depends(get_db), class_id=Path(..., description="班级ID")):
    result = get_one_class(db, class_id)
    if result:
        return {'message': '查询成功', 'data': [ClassesResponse.model_validate(result).model_dump(by_alias=True)]}
    raise HTTPException(status_code=404, detail="班级不存在")


# 新建班级
@classes_router.post("/classes",summary="新建班级")
def post_classes(addclass: AddClasses,db: Session = Depends(get_db)):
    result = add_classes(db, addclass)
    if result:
        return {"message": "添加成功"}
    raise HTTPException(status_code=400, detail="班级已存在")


# 更新班级信息
@classes_router.put("/{class_id}",summary="更新班级信息")
def put_classes(updateclass: UpdateClasses,db: Session = Depends(get_db), class_id: int = Path(..., description='班级id')):
    if not id_in_table(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    update_classes(db, class_id, updateclass)
    return {"message": "修改成功"}


# 逻辑删除班级
@classes_router.delete("/classes/{class_id}",summary="删除班级")
def delete_classes(db: Session = Depends(get_db), class_id: int = Path(..., description='班级id')):
    if not id_in_table(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    del_classes(db, class_id)
    return {"message": "删除成功"}


# 表联动查询
# 查询班级所有学生信息
@classes_router.get("/classes/{class_id}/students", response_model=dict,summary="查询班级所有学生")
def class_get_student(db: Session = Depends(get_db), class_id: int = Path(..., description='班级id')):
    if not id_in_table(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    result = class_student(db, class_id)
    if result:
        return {"message": "查询成功", "data": [ClassesStudent.model_validate(i).model_dump(by_alias=True) for i in result]}
    raise HTTPException(status_code=404, detail="未查询到信息")



# 查询班级所有学生成绩
@classes_router.get("/classes/{class_id}/scores", response_model=dict,summary="查询班级所有学生成绩")
def class_stu_scores(db: Session = Depends(get_db),
                     class_id: int = Path(..., description='班级id'),
                     test_num:int|None = Query(None,alias='考试序次')):
    if not id_in_table(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    result = cls_stu_score(db, class_id,test_num)
    if result:
        return {"message": "查询成功",
                "data": [ClassStudentScore.model_validate(i).model_dump(by_alias=True) for i in result]}
    raise HTTPException(status_code=404, detail="未查询到信息")



