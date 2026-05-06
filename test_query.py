import sqlite3

db_path = "d:/王玺善汇总/技能提升/沃林/FastAPI项目/fastapi.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("数据库中学生表的所有数据：")
print("=" * 60)

cursor.execute("SELECT id, stu_id, stu_name, class_id, gender, age FROM dim_stu ORDER BY id")
rows = cursor.fetchall()

print(f"{'id':<4} {'stu_id':<8} {'stu_name':<15} {'class_id':<10} {'gender':<6} {'age':<4}")
print("-" * 60)
for row in rows:
    print(f"{row[0]:<4} {row[1]:<8} {row[2]:<15} {row[3]:<10} {row[4]:<6} {row[5]:<4}")

print(f"\n总记录数: {len(rows)}")
conn.close()
