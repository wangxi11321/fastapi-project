from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from FastAPI项目.dao_model.classes_dao import get_all_class, get_one_class, add_classes, update_classes, id_in_table, \
    del_classes, class_student, cls_stu_score
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.classes_pdmd import GetClasses, AddClasses, UpdateClasses, ClassesResponse, \
    ClassesStudent, ClassStudentScore
from FastAPI项目.common.schemas import success_response, fail_response


classes_router = APIRouter()


@classes_router.get("/classes", summary="查询班级列表")
def get_classes(db: Session = Depends(get_db), getclass: GetClasses = Depends(), 
                include_students: bool = Query(False, description="是否包含学生列表"),
                include_scores: bool = Query(False, description="是否包含成绩")):
    result = get_all_class(db, getclass)
    if result:
        data = [ClassesResponse.model_validate(i).model_dump(by_alias=True) for i in result]
        return success_response(data=data)
    return fail_response(msg="班级不存在")


@classes_router.get("/classes/{class_id}", summary="查询单个班级详情")
def get_class_by_id(db: Session = Depends(get_db), class_id: int = Path(..., description="班级ID"),
                    include_students: bool = Query(False, description="是否包含学生"),
                    include_scores: bool = Query(False, description="是否包含成绩")):
    result = get_one_class(db, class_id)
    if not result:
        return fail_response(msg="班级不存在")
    
    response_data = ClassesResponse.model_validate(result).model_dump(by_alias=True)
    
    if include_students:
        students = class_student(db, class_id)
        response_data["students"] = [ClassesStudent.model_validate(i).model_dump(by_alias=True) for i in students]
    
    if include_scores:
        scores = cls_stu_score(db, class_id, None)
        response_data["scores"] = [ClassStudentScore.model_validate(i).model_dump(by_alias=True) for i in scores]
    
    return success_response(data=response_data)


@classes_router.post("/classes", summary="新建班级")
def post_classes(addclass: AddClasses, db: Session = Depends(get_db)):
    result = add_classes(db, addclass)
    if result:
        return success_response(msg="添加成功")
    return fail_response(msg="班级已存在")


@classes_router.put("/classes/{class_id}", summary="更新班级信息")
def put_classes(updateclass: UpdateClasses, db: Session = Depends(get_db), class_id: int = Path(..., description='班级id')):
    if not id_in_table(db, class_id):
        return fail_response(msg="班级不存在")
    update_classes(db, class_id, updateclass)
    return success_response(msg="修改成功")


@classes_router.delete("/classes/{class_id}", summary="删除班级")
def delete_classes(db: Session = Depends(get_db), class_id: int = Path(..., description='班级id')):
    if not id_in_table(db, class_id):
        return fail_response(msg="班级不存在")
    del_classes(db, class_id)
    return success_response(msg="删除成功")
