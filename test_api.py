import urllib.request
import urllib.parse
import json

port = 8002
url = f"http://127.0.0.1:{port}/students"
data = {
    "stu_id": 5001,
    "stu_name": "测试学生",
    "class_id": 3001
}

print("测试新增学生API...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, ensure_ascii=False)}")

try:
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print(f"\n状态码: {response.status}")
        print(f"响应: {result}")
except Exception as e:
    print(f"请求失败: {e}")

print("\n" + "="*50)
print("测试获取学生列表API...")
list_url = f"http://127.0.0.1:{port}/students?page=1&size=10"
try:
    req = urllib.request.Request(list_url)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"状态码: {response.status}")
        print(f"总记录数: {result.get('total', 0)}")
        print(f"当前页: {result.get('page', 0)}")
        print(f"数据条数: {len(result.get('data', []))}")
        if result.get('data'):
            print("\n第一页学生数据:")
            for s in result['data']:
                print(f"  stu_id: {s.get('stu_id')}, stu_name: {s.get('stu_name')}")
except Exception as e:
    print(f"请求失败: {e}")

print("\n" + "="*50)
print("测试获取最后一页学生列表API...")
list_url = f"http://127.0.0.1:{port}/students?page=4&size=10"
try:
    req = urllib.request.Request(list_url)
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"状态码: {response.status}")
        print(f"总记录数: {result.get('total', 0)}")
        print(f"当前页: {result.get('page', 0)}")
        print(f"数据条数: {len(result.get('data', []))}")
        if result.get('data'):
            print("\n最后一页学生数据:")
            for s in result['data']:
                print(f"  stu_id: {s.get('stu_id')}, stu_name: {s.get('stu_name')}")
except Exception as e:
    print(f"请求失败: {e}")
