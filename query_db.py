import sqlite3

db_path = "d:/王玺善汇总/技能提升/沃林/FastAPI项目/fastapi.db"

def show_tables():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    print("=" * 60)
    print("数据库表列表：")
    print("=" * 60)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table[0]}")

    print("\n" + "=" * 60)
    print("各表数据统计：")
    print("=" * 60)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"{table[0]}: {count} 条记录")

    print("\n" + "=" * 60)
    print("各表数据预览：")
    print("=" * 60)

    queries = {
        "dim_department (部门)": "SELECT * FROM dim_department LIMIT 5",
        "dim_employees (员工)": "SELECT * FROM dim_employees LIMIT 5",
        "dim_course (课程)": "SELECT * FROM dim_course LIMIT 5",
        "dim_class (班级)": "SELECT * FROM dim_class LIMIT 5",
        "dim_stu (学生)": "SELECT * FROM dim_stu LIMIT 5",
        "dwd_score_info_detail (成绩)": "SELECT * FROM dwd_score_info_detail LIMIT 5",
        "dwd_employment_info_detail (就业)": "SELECT * FROM dwd_employment_info_detail LIMIT 5"
    }

    for name, query in queries.items():
        print(f"\n【{name}】")
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(f"查询失败: {e}")

    connection.close()

if __name__ == '__main__':
    show_tables()
