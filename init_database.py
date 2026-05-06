import pymysql
from db_model.config import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME

create_tables_sql = """
CREATE TABLE IF NOT EXISTS `dim_employees` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id', 
   `employee_id` int DEFAULT NULL COMMENT '雇员编号', 
   `employee_name` varchar(100) DEFAULT NULL COMMENT '雇员名称', 
   `position_name` varchar(100) DEFAULT NULL COMMENT '职位名称（教师/助教/顾问）', 
   `create_time` date DEFAULT NULL COMMENT '创建时间（生效时间）', 
   `department_id` VARCHAR(50) DEFAULT NULL COMMENT '所属部门（如教学部、就业部）', 
   `hire_time` DATE DEFAULT NULL COMMENT '入职时间', 
   `end_time` date DEFAULT NULL COMMENT '失效时间', 
   `deleted_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='雇员维表';
 
CREATE TABLE IF NOT EXISTS `dim_course` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id', 
   `course_id` int DEFAULT NULL COMMENT '课程编号', 
   `course_name` varchar(255) DEFAULT NULL COMMENT '课程名称', 
   `create_time` date DEFAULT NULL COMMENT '创建时间（生效时间）', 
   `end_time` date DEFAULT NULL COMMENT '失效时间', 
   `deleted_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='课程维表';
 
CREATE TABLE IF NOT EXISTS `dim_department` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id', 
   `department_id` int DEFAULT NULL COMMENT '雇员编号', 
   `department_name` varchar(100) DEFAULT NULL COMMENT '雇员名称', 
   `create_time` date DEFAULT NULL COMMENT '创建时间（生效时间）', 
   `end_time` date DEFAULT NULL COMMENT '失效时间', 
   `deleted_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='部门维表';
 
CREATE TABLE IF NOT EXISTS `dim_class` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id', 
   `class_id` int DEFAULT NULL COMMENT '班级编号', 
   `class_name` varchar(255) DEFAULT NULL COMMENT '班级名称', 
   `class_star_date` date DEFAULT NULL COMMENT '开班时间', 
   `class_end_date` date DEFAULT NULL COMMENT '结课时间', 
   `course_id` int DEFAULT NULL COMMENT '课程编号', 
   `teacher_id` int DEFAULT NULL COMMENT '授课教师编号', 
   `head_teacher_id` int DEFAULT NULL COMMENT '班主任编号', 
   `tutor_id` int DEFAULT NULL COMMENT '助教编号', 
   `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间', 
   `deleted_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班级维表';
 
CREATE TABLE IF NOT EXISTS `dim_stu` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键id', 
   `stu_id` int DEFAULT NULL COMMENT '学生编号', 
   `stu_name` varchar(100) DEFAULT NULL COMMENT '姓名', 
   `class_id` int DEFAULT NULL COMMENT '班级编号', 
   `gender` varchar(10) DEFAULT NULL COMMENT '性别', 
   `age` int DEFAULT NULL COMMENT '年龄', 
   `hometown` varchar(255) DEFAULT NULL COMMENT '籍贯', 
   `graduate_school` varchar(100) DEFAULT NULL COMMENT '毕业院校', 
   `major` varchar(50) DEFAULT NULL COMMENT '专业', 
   `education` varchar(50) DEFAULT NULL COMMENT '学历', 
   `advisor_id` int DEFAULT NULL COMMENT '顾问编号', 
   `enroll_time` date DEFAULT NULL COMMENT '入学时间', 
   `graduate_time` date DEFAULT NULL COMMENT '毕业时间', 
   `course_id` int DEFAULT NULL COMMENT '所学课程编码', 
   `stu_flag` varchar(255) DEFAULT NULL COMMENT '学生标签', 
   `deleted_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `create_time` date DEFAULT NULL COMMENT '创建时间（生效时间）', 
   `end_time` date DEFAULT NULL COMMENT '失效时间', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生维表';
 
CREATE TABLE IF NOT EXISTS `dwd_score_info_detail` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键', 
   `class_id` int DEFAULT NULL COMMENT '班级编号', 
   `test_num` int DEFAULT NULL COMMENT '考核次序', 
   `stu_id` int DEFAULT NULL COMMENT '学生编号', 
   `exam_course_id` int DEFAULT NULL COMMENT '考核课程编号', 
   `exam_date` date DEFAULT NULL COMMENT '考核时间', 
   `score` float DEFAULT NULL COMMENT '成绩', 
   `delete_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `creation_date` date DEFAULT NULL COMMENT '创建时间', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='考试成绩明细表';
 
CREATE TABLE IF NOT EXISTS `dwd_employment_info_detail` ( 
   `id` int NOT NULL AUTO_INCREMENT COMMENT '主键', 
   `class_id` int DEFAULT NULL COMMENT '班级编号', 
   `stu_id` int DEFAULT NULL COMMENT '学生编号', 
   `employment_open_date` date DEFAULT NULL COMMENT '就业开放时间', 
   `first_offer_date` date DEFAULT NULL COMMENT '第一次拿offer的时间', 
   `get_offer_num` int DEFAULT NULL COMMENT '获得offer数量', 
   `employment_date` date DEFAULT NULL COMMENT '就业时间', 
   `mployment_status` varchar(20) DEFAULT NULL COMMENT '就业状态', 
   `employment_company_name` varchar(255) DEFAULT NULL COMMENT '就业公司名称', 
   `company_city` varchar(255) DEFAULT NULL COMMENT '公司所在城市', 
   `company_type` varchar(255) DEFAULT NULL COMMENT '企业所处行业', 
   `job_position` varchar(255) DEFAULT NULL COMMENT '就职岗位', 
   `salary` float DEFAULT NULL COMMENT '就业薪资', 
   `delete_flag` int DEFAULT '0' COMMENT '是否删除 0否1是', 
   `creation_date` date DEFAULT NULL COMMENT '创建时间', 
   `insert_date` date DEFAULT NULL COMMENT '数据插入时间', 
   PRIMARY KEY (`id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='就业信息明细表';
"""

insert_data_sql = [
    """INSERT INTO dim_department (department_id, department_name, create_time, end_time, deleted_flag, insert_date)
    VALUES
    (1,'教学部','2025-01-01',NULL,0,'2025-01-01'),
    (2,'就业部','2025-01-01',NULL,0,'2025-01-01'),
    (3,'教研部','2025-01-01',NULL,0,'2025-01-01'),
    (4,'行政部','2025-01-01',NULL,0,'2025-01-01');""",
    
    """INSERT INTO dim_employees (employee_id, employee_name, position_name, create_time, department_id, hire_time, end_time, deleted_flag, insert_date)
    VALUES
    (1001,'张老师','教师','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1002,'李顾问','顾问','2025-01-01',2,'2024-09-01',NULL,0,'2025-01-01'),
    (1003,'王助教','助教','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1004,'赵班主任','班主任','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1005,'刘老师','教师','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1006,'陈顾问','顾问','2025-01-01',2,'2024-09-01',NULL,0,'2025-01-01'),
    (1007,'周助教','助教','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1008,'吴班主任','班主任','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1009,'郑老师','教师','2025-01-01',1,'2024-09-01',NULL,0,'2025-01-01'),
    (1010,'孙顾问','顾问','2025-01-01',2,'2024-09-01',NULL,0,'2025-01-01');""",
    
    """INSERT INTO dim_course (course_id, course_name, create_time, end_time, deleted_flag, insert_date)
    VALUES
    (2001,'Python全栈开发','2025-01-01',NULL,0,'2025-01-01'),
    (2002,'大数据分析','2025-01-01',NULL,0,'2025-01-01'),
    (2003,'人工智能基础','2025-01-01',NULL,0,'2025-01-01'),
    (2004,'前端开发实战','2025-01-01',NULL,0,'2025-01-01');""",
    
    """INSERT INTO dim_class (class_id, class_name, class_star_date, class_end_date, course_id, teacher_id, head_teacher_id, tutor_id, create_time, deleted_flag, insert_date)
    VALUES
    (3001,'Python全栈2501班','2025-01-10','2025-07-10',2001,1001,1004,1003,NOW(),0,'2025-01-10'),
    (3002,'大数据2502班','2025-02-10','2025-08-10',2002,1005,1008,1007,NOW(),0,'2025-02-10'),
    (3003,'人工智能2503班','2025-03-10','2025-09-10',2003,1009,1004,1003,NOW(),0,'2025-03-10'),
    (3004,'前端开发2504班','2025-04-10','2025-10-10',2004,1001,1008,1007,NOW(),0,'2025-04-10');""",
    
    """INSERT INTO dim_stu (stu_id, stu_name, class_id, gender, age, hometown, graduate_school, major, education, advisor_id, enroll_time, graduate_time, course_id, stu_flag, deleted_flag, create_time, end_time, insert_date)
    VALUES
    (4001,'陈明',3001,'男',22,'北京','北京理工大学','计算机','本科',1002,'2025-01-10',NULL,2001,'优秀',0,'2025-01-10',NULL,'2025-01-10'),
    (4002,'刘芳',3001,'女',21,'上海','上海大学','软件工程','本科',1002,'2025-01-10',NULL,2001,'良好',0,'2025-01-10',NULL,'2025-01-10'),
    (4003,'王强',3002,'男',25,'广州','中山大学','数据科学','本科',1006,'2025-02-10',NULL,2002,'一般',0,'2025-02-10',NULL,'2025-02-10'),
    (4004,'张伟',3002,'男',32,'深圳','深圳大学','计算机','专科',1006,'2025-02-10',NULL,2002,'待提高',0,'2025-02-10',NULL,'2025-02-10'),
    (4005,'李娜',3001,'女',23,'杭州','浙江大学','人工智能','硕士',1002,'2025-01-10',NULL,2001,'优秀',0,'2025-01-10',NULL,'2025-01-10'),
    (4006,'刘洋',3003,'男',28,'成都','电子科技大学','计算机','本科',1010,'2025-03-10',NULL,2003,'良好',0,'2025-03-10',NULL,'2025-03-10'),
    (4007,'陈丽',3003,'女',24,'重庆','重庆大学','软件','本科',1010,'2025-03-10',NULL,2003,'优秀',0,'2025-03-10',NULL,'2025-03-10'),
    (4008,'周明',3004,'男',33,'武汉','武汉大学','计算机','专科',1002,'2025-04-10',NULL,2004,'待提高',0,'2025-04-10',NULL,'2025-04-10'),
    (4009,'吴静',3004,'女',22,'长沙','湖南大学','软件','本科',1002,'2025-04-10',NULL,2004,'良好',0,'2025-04-10',NULL,'2025-04-10'),
    (4010,'郑浩',3001,'男',26,'南京','东南大学','计算机','本科',1002,'2025-01-10',NULL,2001,'一般',0,'2025-01-10',NULL,'2025-01-10'),
    (4011,'孙悦',3002,'女',29,'西安','西安电子科大','软件','本科',1006,'2025-02-10',NULL,2002,'良好',0,'2025-02-10',NULL,'2025-02-10'),
    (4012,'马超',3003,'男',35,'济南','山东大学','计算机','专科',1010,'2025-03-10',NULL,2003,'待提高',0,'2025-03-10',NULL,'2025-03-10'),
    (4013,'胡琳',3004,'女',25,'郑州','郑州大学','数据科学','本科',1002,'2025-04-10',NULL,2004,'良好',0,'2025-04-10',NULL,'2025-04-10'),
    (4014,'林宇',3001,'男',27,'合肥','中科大','人工智能','硕士',1002,'2025-01-10',NULL,2001,'优秀',0,'2025-01-10',NULL,'2025-01-10'),
    (4015,'谢婷',3002,'女',23,'福州','福州大学','软件','本科',1006,'2025-02-10',NULL,2002,'良好',0,'2025-02-10',NULL,'2025-02-10'),
    (4016,'罗勇',3003,'男',31,'南昌','南昌大学','计算机','专科',1010,'2025-03-10',NULL,2003,'待提高',0,'2025-03-10',NULL,'2025-03-10'),
    (4017,'宋佳',3004,'女',24,'贵阳','贵州大学','软件','本科',1002,'2025-04-10',NULL,2004,'良好',0,'2025-04-10',NULL,'2025-04-10'),
    (4018,'韩超',3001,'男',30,'兰州','兰州大学','计算机','本科',1002,'2025-01-10',NULL,2001,'一般',0,'2025-01-10',NULL,'2025-01-10'),
    (4019,'冯雨',3002,'女',26,'西宁','青海大学','数据科学','本科',1006,'2025-02-10',NULL,2002,'良好',0,'2025-02-10',NULL,'2025-02-10'),
    (4020,'曹磊',3003,'男',28,'银川','宁夏大学','软件','本科',1010,'2025-03-10',NULL,2003,'良好',0,'2025-03-10',NULL,'2025-03-10'),
    (4021,'彭欣',3004,'女',22,'哈尔滨','哈工大','计算机','本科',1002,'2025-04-10',NULL,2004,'优秀',0,'2025-04-10',NULL,'2025-04-10'),
    (4022,'袁刚',3001,'男',34,'长春','吉林大学','计算机','专科',1002,'2025-01-10',NULL,2001,'待提高',0,'2025-01-10',NULL,'2025-01-10'),
    (4023,'于雪',3002,'女',25,'沈阳','东北大学','软件','本科',1006,'2025-02-10',NULL,2002,'良好',0,'2025-02-10',NULL,'2025-02-10'),
    (4024,'董斌',3003,'男',29,'呼和浩特','内蒙古大学','数据科学','本科',1010,'2025-03-10',NULL,2003,'一般',0,'2025-03-10',NULL,'2025-03-10'),
    (4025,'程月',3004,'女',27,'乌鲁木齐','新疆大学','计算机','本科',1002,'2025-04-10',NULL,2004,'良好',0,'2025-04-10',NULL,'2025-04-10'),
    (4026,'吕文',3001,'男',23,'苏州','苏州大学','软件','本科',1002,'2025-01-10',NULL,2001,'良好',0,'2025-01-10',NULL,'2025-01-10'),
    (4027,'姚丽',3002,'女',31,'无锡','江南大学','计算机','专科',1006,'2025-02-10',NULL,2002,'待提高',0,'2025-02-10',NULL,'2025-02-10'),
    (4028,'方超',3003,'男',26,'常州','常州大学','数据科学','本科',1010,'2025-03-10',NULL,2003,'良好',0,'2025-03-10',NULL,'2025-03-10'),
    (4029,'金娜',3004,'女',24,'南通','南通大学','软件','本科',1002,'2025-04-10',NULL,2004,'良好',0,'2025-04-10',NULL,'2025-04-10'),
    (4030,'魏明',3001,'男',29,'扬州','扬州大学','计算机','本科',1002,'2025-01-10',NULL,2001,'一般',0,'2025-01-10',NULL,'2025-01-10');""",
    
    """INSERT INTO dwd_score_info_detail (class_id, test_num, stu_id, exam_course_id, exam_date, score, delete_flag, creation_date, insert_date)
    VALUES
    (3001,1,4001,2001,'2025-03-01',92.5,0,'2025-03-01','2025-03-01'),
    (3001,1,4002,2001,'2025-03-01',85.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4005,2001,'2025-03-01',88.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4010,2001,'2025-03-01',72.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4014,2001,'2025-03-01',95.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4018,2001,'2025-03-01',55.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4022,2001,'2025-03-01',48.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4026,2001,'2025-03-01',78.0,0,'2025-03-01','2025-03-01'),
    (3001,1,4030,2001,'2025-03-01',62.0,0,'2025-03-01','2025-03-01'),
    (3002,1,4003,2002,'2025-04-01',59.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4004,2002,'2025-04-01',55.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4011,2002,'2025-04-01',75.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4015,2002,'2025-04-01',82.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4019,2002,'2025-04-01',68.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4023,2002,'2025-04-01',76.0,0,'2025-04-01','2025-04-01'),
    (3002,1,4027,2002,'2025-04-01',45.0,0,'2025-04-01','2025-04-01'),
    (3001,2,4001,2001,'2025-04-15',95.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4002,2001,'2025-04-15',78.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4005,2001,'2025-04-15',90.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4010,2001,'2025-04-15',68.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4014,2001,'2025-04-15',92.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4018,2001,'2025-04-15',52.0,0,'2025-04-15','2025-04-15'),
    (3001,2,4022,2001,'2025-04-15',42.0,0,'2025-04-15','2025-04-15'),
    (3002,2,4003,2002,'2025-05-15',65.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4004,2002,'2025-05-15',48.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4011,2002,'2025-05-15',80.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4015,2002,'2025-05-15',85.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4019,2002,'2025-05-15',72.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4023,2002,'2025-05-15',78.0,0,'2025-05-15','2025-05-15'),
    (3002,2,4027,2002,'2025-05-15',40.0,0,'2025-05-15','2025-05-15');""",
    
    """INSERT INTO dwd_employment_info_detail
    (class_id, stu_id, employment_open_date, first_offer_date, get_offer_num, employment_date, mployment_status,
    employment_company_name, company_city, company_type, job_position, salary, delete_flag, creation_date, insert_date)
    VALUES
    (3001,4001,'2025-05-01','2025-05-10',3,'2025-05-20','已就业','字节跳动','北京','互联网','后端开发',15000,0,'2025-05-20','2025-05-20'),
    (3001,4002,'2025-05-01','2025-05-15',2,'2025-05-25','已就业','腾讯','深圳','互联网','测试开发',13000,0,'2025-05-25','2025-05-25'),
    (3001,4005,'2025-05-01','2025-05-08',4,'2025-05-18','已就业','阿里','杭州','互联网','算法工程师',18000,0,'2025-05-18','2025-05-18'),
    (3001,4014,'2025-05-01','2025-05-12',5,'2025-05-22','已就业','百度','北京','互联网','AI工程师',20000,0,'2025-05-22','2025-05-22'),
    (3001,4018,'2025-05-01',NULL,0,NULL,'未就业',NULL,NULL,NULL,NULL,0,0,'2025-06-01','2025-06-01'),
    (3001,4022,'2025-05-01',NULL,0,NULL,'未就业',NULL,NULL,NULL,NULL,0,0,'2025-06-01','2025-06-01'),
    (3002,4003,'2025-06-01','2025-06-12',1,'2025-06-20','已就业','京东','上海','电商','数据分析师',11000,0,'2025-06-20','2025-06-20'),
    (3002,4004,'2025-06-01',NULL,0,NULL,'未就业',NULL,NULL,NULL,NULL,0,0,'2025-06-20','2025-06-20'),
    (3002,4011,'2025-06-01','2025-06-10',2,'2025-06-18','已就业','拼多多','上海','电商','数据开发',12500,0,'2025-06-18','2025-06-18'),
    (3002,4015,'2025-06-01','2025-06-08',3,'2025-06-15','已就业','网易','杭州','互联网','大数据开发',14000,0,'2025-06-15','2025-06-15'),
    (3003,4006,'2025-07-01','2025-07-10',2,'2025-07-20','已就业','美团','北京','互联网','算法工程师',16000,0,'2025-07-20','2025-07-20'),
    (3003,4007,'2025-07-01','2025-07-05',3,'2025-07-15','已就业','滴滴','北京','互联网','AI产品',13500,0,'2025-07-15','2025-07-15'),
    (3004,4008,'2025-08-01',NULL,0,NULL,'未就业',NULL,NULL,NULL,NULL,0,0,'2025-08-10','2025-08-10'),
    (3004,4009,'2025-08-01','2025-08-12',2,'2025-08-22','已就业','小米','北京','互联网','前端开发',12000,0,'2025-08-22','2025-08-22');"""
]

def init_database():
    try:
        print(f"连接数据库: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("创建表结构...")
        for sql in create_tables_sql.split(';'):
            sql = sql.strip()
            if sql:
                cursor.execute(sql)
        
        print("插入数据...")
        for sql in insert_data_sql:
            cursor.execute(sql)
        
        connection.commit()
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        if 'connection' in locals():
            connection.rollback()
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == '__main__':
    init_database()
