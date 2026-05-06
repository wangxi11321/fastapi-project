import sqlite3
import sys

db_path = "d:/王玺善汇总/技能提升/沃林/FastAPI项目/fastapi.db"

def connect_db():
    return sqlite3.connect(db_path)

def show_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    return [t[0] for t in tables]

def show_table_structure(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    conn.close()
    return columns

def query_table(table_name, limit=10):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def execute_sql(sql):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if sql.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = f"执行成功，影响了 {cursor.rowcount} 行"
        conn.close()
        return result
    except Exception as e:
        conn.close()
        return f"执行失败: {e}"

def main():
    print("=" * 60)
    print("数据库管理工具")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 查看所有表")
        print("2. 查看表结构")
        print("3. 查询表数据")
        print("4. 执行SQL语句")
        print("5. 退出")
        
        choice = input("\n输入选项编号: ")
        
        if choice == '1':
            tables = show_tables()
            print("\n数据库中的表:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
        
        elif choice == '2':
            tables = show_tables()
            print("\n选择要查看结构的表:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
            idx = int(input("输入表编号: ")) - 1
            if 0 <= idx < len(tables):
                columns = show_table_structure(tables[idx])
                print(f"\n表 {tables[idx]} 的结构:")
                print(f"{'序号':<4} {'字段名':<20} {'类型':<20} {'是否主键':<10}")
                print("-" * 60)
                for col in columns:
                    pk = "是" if col[5] else "否"
                    print(f"{col[0]:<4} {col[1]:<20} {col[2]:<20} {pk:<10}")
        
        elif choice == '3':
            tables = show_tables()
            print("\n选择要查询的表:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
            idx = int(input("输入表编号: ")) - 1
            if 0 <= idx < len(tables):
                limit = int(input("输入查询条数(默认10): ") or "10")
                rows = query_table(tables[idx], limit)
                print(f"\n表 {tables[idx]} 的数据:")
                columns = show_table_structure(tables[idx])
                header = " | ".join([col[1] for col in columns])
                print(header)
                print("-" * len(header))
                for row in rows:
                    print(" | ".join([str(cell) for cell in row]))
        
        elif choice == '4':
            print("\n输入SQL语句 (输入 'quit' 返回主菜单):")
            print("提示: 可以执行 SELECT、INSERT、UPDATE、DELETE 等语句")
            print("示例: INSERT INTO dim_stu (stu_id, stu_name, class_id) VALUES (5001, '新学生', 3001)")
            print("示例: UPDATE dim_stu SET stu_name='修改后的名字' WHERE stu_id=4001")
            
            while True:
                sql = input("\nSQL> ").strip()
                if sql.lower() == 'quit':
                    break
                if not sql:
                    continue
                
                result = execute_sql(sql)
                print("\n执行结果:")
                if isinstance(result, list):
                    for row in result:
                        print(row)
                else:
                    print(result)
        
        elif choice == '5':
            print("退出数据库管理工具")
            break
        
        else:
            print("无效选项，请重新输入")

if __name__ == '__main__':
    main()
