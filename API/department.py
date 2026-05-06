from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentPageResponse, DepartmentBatchCreate
from FastAPI项目.dao_model import department
import re  # 字符串规则匹配工具

department_router = APIRouter(prefix="/api/department")

# 创建部门
@department_router.post("/departments"
                        , response_model=DepartmentResponse # 单个数据返回的响应体
                        , summary="创建部门")
def create_department(data: DepartmentCreate
                      , db: Session = Depends(get_db)):
    # 验证部门ID是否为数字
    if not isinstance(data.department_id, (int, float)):
        raise HTTPException(status_code=400, detail="部门ID必须为数字")
    # 验证部门ID是否为非负
    # if data.department_id < 0:
    #     raise HTTPException(status_code=400, detail="部门ID不能为负数")
    # 验证部门ID是否为正整数
    if not float(data.department_id).is_integer() or data.department_id <= 0:
        raise HTTPException(status_code=400, detail="部门ID必须为正整数")
    # 验证部门ID是否已存在
    if department.get_department_by_department_id(db, data.department_id):
        raise HTTPException(status_code=400, detail="部门ID已存在")
    # 验证部门名称不能为空
    if not data.department_name or not data.department_name.strip():
        raise HTTPException(status_code=400, detail="部门名称不能为空")
    # 验证部门名称不能包含特殊字符
    if re.search(r'[<>\'\"\\/]', data.department_name):
        raise HTTPException(status_code=400, detail="部门名称不能包含特殊字符")
    return department.create_department(db, data)

# 批量创建部门
@department_router.post("/departments/batch"
                        , response_model=List[DepartmentResponse]
                        , summary="批量创建部门")
def batch_create_department(data: DepartmentBatchCreate
                      , db: Session = Depends(get_db)):
    # 验证列表不能为空
    if not data.departments or len(data.departments) == 0:
        raise HTTPException(status_code=400, detail="部门列表不能为空")
    # 验证每个部门的数据
    for item in data.departments:
        # 验证部门ID是否为数字
        if not isinstance(item.department_id, (int, float)):
            raise HTTPException(status_code=400, detail=f"部门ID {item.department_id} 必须为数字")
        # 验证部门ID是否为正整数
        if not float(item.department_id).is_integer() or item.department_id <= 0:
            raise HTTPException(status_code=400, detail=f"部门ID {item.department_id} 必须为正整数")
        # 验证部门ID是否已存在
        if department.get_department_by_department_id(db, item.department_id):
            raise HTTPException(status_code=400, detail=f"部门ID {item.department_id} 已存在")
        # 验证部门名称不能为空
        if not item.department_name or not item.department_name.strip():
            raise HTTPException(status_code=400, detail=f"部门名称不能为空")
        # 验证部门名称不能包含特殊字符
        if re.search(r'[<>\'\"\\/]', item.department_name):
            raise HTTPException(status_code=400, detail=f"部门名称不能包含特殊字符")
    # 批量创建
    return department.batch_create_department(db, data.departments)

# 通过指定部门id查询单个
@department_router.get("/department/{department_id}"
                        , response_model=DepartmentResponse # 单个数据返回的响应体
                        , summary="查询单个部门")
def get_department(department_id: int
                   , db: Session = Depends(get_db)):
    # 验证部门ID是否为数字
    if not isinstance(department_id, (int, float)):
        raise HTTPException(status_code=400, detail="部门ID必须为数字")
    # 验证部门ID是否为非负
    # if department_id < 0:
    #     raise HTTPException(status_code=400, detail="部门ID不能为负数")
    # 验证部门ID是否为正整数
    if not float(department_id).is_integer() or department_id <= 0:
        raise HTTPException(status_code=400, detail="部门ID必须为正整数")
    # 验证部门ID是否存在
    result = department.get_department_by_department_id(db, department_id)
    # 找不到要查询的部门 返回404-部门不存在
    if not result:
        raise HTTPException(status_code=404, detail="部门不存在")
    return result

# 分页查询部门列表
@department_router.get("/departments"
                        , response_model=DepartmentPageResponse
                        , summary="分页查询部门")
def get_department_list(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 5,
    department_name: Optional[str] = None
):
    # 验证页码是否为数字
    if not isinstance(page, (int, float)):
        raise HTTPException(status_code=400, detail="页码必须为数字")
    # 验证页码是否为正整数
    if not float(page).is_integer() or page <= 0:
        raise HTTPException(status_code=400, detail="页码必须为正整数")
    # 验证条数是否为数字
    if not isinstance(page_size, (int, float)):
        raise HTTPException(status_code=400, detail="每页条数必须为数字")
    # 验证条数是否为正整数
    if not float(page_size).is_integer() or page_size <= 0:
        raise HTTPException(status_code=400, detail="每页条数必须为正整数")
    skip = (page - 1) * page_size
    data = department.get_department_list(db, skip, page_size, department_name)
    total = department.count_department(db)
    return DepartmentPageResponse(total=total, page=page, page_size=page_size, data=data)

# 修改部门信息
@department_router.put("/department/update/{department_id}", summary="修改部门信息")
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    # 验证部门ID是否为数字
    if not isinstance(department_id, (int, float)):
        raise HTTPException(status_code=400, detail="部门ID必须为数字")
    # 验证部门ID是否为非负
    # if department_id < 0:
    #     raise HTTPException(status_code=400, detail="部门ID不能为负数")
    # 验证部门ID是否为正整数
    if not float(department_id).is_integer() or department_id <= 0:
        raise HTTPException(status_code=400, detail="部门ID必须为正整数")
    update_data = data.model_dump(exclude_unset=True) # 只更新传了的字段
    # 验证要修改的部门名称不能为空
    if 'department_name' in update_data:
        if not update_data['department_name'] or not update_data['department_name'].strip():
            raise HTTPException(status_code=400, detail="部门名称不能为空")
        if re.search(r'[<>\'\"\\/]', update_data['department_name']):
            raise HTTPException(status_code=400, detail="部门名称不能包含特殊字符")
    # 找不到要更新的部门 返回404-部门不存在
    if not department.update_department(db, department_id, update_data):
        raise HTTPException(status_code=404, detail="要修改的部门不存在")
    # 返回更新后的完整数据
    updated_data = department.get_department_by_department_id(db, department_id)
    return {"message": "更新成功",  "data": updated_data}

# 根据部门ID删除部门 只对删除标识进行修改 不删除数据
@department_router.delete("/department/delete/{department_id}", summary="删除部门(软删除)")
def delete_department(department_id: int
                  , db: Session = Depends(get_db)):
    # 验证部门ID是否为数字
    if not isinstance(department_id, (int, float)):
        raise HTTPException(status_code=400, detail="部门ID必须为数字")
    # 验证部门ID是否为非负
    # if department_id < 0:
    #     raise HTTPException(status_code=400, detail="部门ID不能为负数")
    # 验证部门ID是否为正整数
    if not float(department_id).is_integer() or department_id <= 0:
        raise HTTPException(status_code=400, detail="部门ID必须为正整数")
    # 找不到要删除的部门 返回404-部门不存在
    if not department.delete_department(db, department_id):
        raise HTTPException(status_code=404, detail="要删除的部门不存在")
    return {"message": "删除成功"}

# 恢复误删的部门（撤回）
@department_router.put("/department/restore/{department_id}", summary="恢复误删部门")
def restore_department(department_id: int, db: Session = Depends(get_db)):

    if not float(department_id).is_integer() or department_id <= 0:
        raise HTTPException(status_code=400, detail="部门ID必须为正整数")
    result = department.restore_department(db, department_id)
    if not result:
        raise HTTPException(status_code=404, detail="要恢复的部门不存在或未被删除")
    restored_department = department.get_department_by_department_id(db, department_id)
    return {"message": "恢复成功", "data": restored_department}

# 查询已删除的部门列表（可恢复列表）
@department_router.get("/departments/deleted", summary="查询已删除部门列表")
def get_deleted_departments(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 10
):

    skip = (page - 1) * page_size
    data = department.get_deleted_department_list(db, skip, page_size)
    total = department.count_deleted_department(db)
    return {"total": total, "page": page, "page_size": page_size, "data": data}

