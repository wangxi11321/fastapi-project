from sqlalchemy.orm import Session
from FastAPI项目.table_model.dim_department import DimDepartment
from FastAPI项目.pydantic_model.department import DepartmentCreate
from datetime import date
from sqlalchemy import func


#  新增部门
def create_department(db: Session
                      , data: DepartmentCreate): # 根据请求体限制传入的数据
    # 创建一个数据库对象，把前端传过来的Pydantic数据 → 变成字典字典 **表示拆成
    # key=value 的形式，传给数据库模型
    department = DimDepartment(**data.model_dump())
    db.add(department) # 把这条数据 加入到数据库会话
    db.commit() # 新增之后要提交
    db.refresh(department) # 刷新数据 放入表中后会生成一个主键ID
    return department  # 把插入后的完整数据返回给前端

# 批量新增部门
def batch_create_department(db: Session, departments_data: list):
    """批量新增部门"""
    departments = [DimDepartment(**data.model_dump()) for data in departments_data]
    db.add_all(departments)
    db.commit()
    for department in departments:
        db.refresh(department)
    return departments

# 批量查询-查询列表
def get_department_by_department_id(db: Session
                                    , department_id: int):
    # select * from dim_department where department_id = ? and deleted_flag = 0;
    return db.query(DimDepartment).filter(
        DimDepartment.department_id == department_id, # 要查询的部门ID和表里的部门ID进行匹配
        DimDepartment.deleted_flag == 0 # 只查未删除的
    ).first()

# 分页查询部门列表
def get_department_list(db: Session
                        , skip=0
                        , limit=5
                        , name=None):
    # select * from dim_department where deleted_flag = 0;
    query = db.query(DimDepartment).filter(DimDepartment.deleted_flag == 0) # 只查未删除的
    if name:
        # 如果不传name进行模糊匹配 直接返回第一次查到的数据
        # 如果传了name进行模糊匹配 返回匹配到的所有数据(模糊匹配不到就会返回空)
        query = query.filter(DimDepartment.department_name.like(f"%{name}%")) # SQL中的like模糊匹配
    return query.offset(skip).limit(limit).all()

# 更新部门信息
def update_department(db: Session
                , department_id: int
                , data: dict):
    # 先验证课程是否存在department_id
    department = get_department_by_department_id(db, department_id)
    if not department:
        return None # 没找到要更新的课程 返回None
    for k, v in data.items():
        setattr(department, k, v)
    # 自动更新插入时间
    department.insert_date = date.today()
    db.commit() # 更新之后要提交
    return True

# 删除部门信息 软删除
def delete_department(db: Session
                , department_id: int):
    department = get_department_by_department_id(db, department_id)
    if not department:
        return None # 没找到要删除的课程 返回None
    department.deleted_flag = 1 # 删除标识改为1
    department.end_time = date.today() # 失效时间改为今天
    db.commit() # 更新之后要提交
    return True

# 恢复误删的部门（撤回）
def restore_department(db: Session
                       , department_id: int):

    department = db.query(DimDepartment).filter(
        DimDepartment.department_id == department_id,
        DimDepartment.deleted_flag == 1
    ).first()
    if not department:
        return None
    department.deleted_flag = 0
    department.end_time = date(9999, 12, 31)
    db.commit()
    return True

# 查询已删除的部门列表
def get_deleted_department_list(db: Session, skip=0, limit=10):

    return db.query(DimDepartment).filter(
        DimDepartment.deleted_flag == 1
    ).offset(skip).limit(limit).all()


# 统计有效部门数量
def count_department(db: Session):
    # select count(1) from dim_course where deleted_flag = 0;
    return db.query(DimDepartment).filter(DimDepartment.deleted_flag == 0).count()

def count_employees_by_department(db: Session):

    # 导入员工表
    from FastAPI项目.table_model.dim_employees import DimEmployees
    # SQL语句如下
    # select department_id, department_name, count(distinct employee_id) as employees_count
    # from dim_department
    # left join dim_employees on dim_employees.department_id = dim_department.department_id
    # where dim_department.deleted_flag = 0
    # and dim_employees.delete_flag = 0
    # group by department_id, department_name;
    results = db.query(
        DimDepartment.department_id,
        DimDepartment.department_name,
        func.count(func.distinct(DimEmployees.employee_id)).label('employees_count') # 别名
    ).join(
        # 关联员工表 通过部门ID关联员工表的部门ID
        DimEmployees, DimEmployees.department_id == DimDepartment.department_id
    ).filter(
        # 只查询删除标识为0的数据
        DimDepartment.deleted_flag == 0,
        DimEmployees.deleted_flag == 0
    ).group_by(
        # 部门ID和部门名称分组
        DimDepartment.department_id,
        DimDepartment.department_name
    ).all()

    return [
        {
            "department_id": r.department_id,
            "department_name": r.department_name,
            "employees_count": r.employees_count
        }
        for r in results
    ]