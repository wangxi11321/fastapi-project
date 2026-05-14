# Dify 客户研判接口配置指南

## 接口信息

**接口地址**: `POST http://your-server/api/tools/create_customer_from_dify`

**Content-Type**: `application/json`

## 请求参数

### 请求体 JSON 结构

```json
{
    "name": "客户姓名",
    "phone": "联系电话",
    "education": "学历",
    "budget": 30.0,
    "english_level": "英语水平",
    "target_country": "目标国家",
    "customer_info": "完整客户信息文本",
    "is_target": true,
    "judge_reason": "研判理由"
}
```

### 字段说明

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| `name` | string | ✅ 是 | 客户姓名 | "张三" |
| `phone` | string | ✅ 是 | 联系电话 | "13800138001" |
| `education` | string | 否 | 学历 | "本科" |
| `budget` | float | 否 | 预算（万） | 30.0 |
| `english_level` | string | 否 | 英语水平 | "雅思7分" |
| `target_country` | string | 否 | 目标国家 | "英国" |
| `customer_info` | string | 否 | 完整客户信息 | "客户张三，本科毕业..." |
| `is_target` | boolean | 否 | 是否目标客户 | true |
| `judge_reason` | string | 否 | 研判理由 | "符合目标客户画像" |

## Dify 配置步骤

### 1. 在 Dify 中创建自定义工具

1. 进入 Dify 控制台
2. 选择你的应用
3. 进入 "工具" -> "添加工具"
4. 选择 "自定义 API 工具"

### 2. 配置工具信息

```yaml
工具名称: create_customer_from_dify
工具描述: 将客户信息保存到数据库
请求方式: POST
请求URL: http://your-server/api/tools/create_customer_from_dify
```

### 3. 配置请求头

```
Content-Type: application/json
```

### 4. 配置请求体（JSON）

在 Dify 的参数配置中添加以下字段：

```json
{
  "name": "{{name}}",
  "phone": "{{phone}}",
  "education": "{{education}}",
  "budget": {{budget}},
  "english_level": "{{english_level}}",
  "target_country": "{{target_country}}",
  "customer_info": "{{customer_info}}",
  "is_target": {{is_target}},
  "judge_reason": "{{judge_reason}}"
}
```

### 5. 在 Agent 中使用

在 Dify 的 Agent 对话流中：

1. 添加 "LLM" 节点，提取客户信息
2. 配置输出变量：
   - `name`: 客户姓名
   - `phone`: 联系电话
   - `education`: 学历
   - `budget`: 预算
   - `english_level`: 英语水平
   - `target_country`: 目标国家
   - `is_target`: 是否目标客户
   - `judge_reason`: 研判理由

3. 添加 "工具" 节点，调用 `create_customer_from_dify`
4. 将 LLM 的输出变量映射到工具参数

## 完整 Dify Workflow 示例

```
用户: "我想去英国留学，本科毕业，预算40万，雅思7分"

    ↓

LLM 节点（提取信息）:
  name: "用户"（或从对话中获取）
  phone: "13800138001"（或询问用户）
  education: "本科"
  budget: 40.0
  english_level: "雅思7分"
  target_country: "英国"
  customer_info: "用户想去英国留学，本科毕业，预算40万，雅思7分"
  is_target: true
  judge_reason: "学历、预算、英语、目标国家都符合"

    ↓

工具节点（保存到数据库）:
  调用 create_customer_from_dify
  参数: {name, phone, education, budget, ...}

    ↓

返回: {"success": true, "customer_id": 1, "message": "客户信息已成功保存"}
```

## 测试接口

### 使用 cURL 测试

```bash
curl -X POST http://127.0.0.1:8000/api/tools/create_customer_from_dify \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "phone": "13800138001",
    "education": "本科",
    "budget": 40.0,
    "english_level": "雅思7分",
    "target_country": "英国",
    "customer_info": "客户张三，本科毕业，预算40万，雅思7分，想去英国留学",
    "is_target": true,
    "judge_reason": "完全符合目标客户画像"
  }'
```

### 使用 Python 测试

```python
import requests

response = requests.post(
    'http://127.0.0.1:8000/api/tools/create_customer_from_dify',
    json={
        "name": "张三",
        "phone": "13800138001",
        "education": "本科",
        "budget": 40.0,
        "english_level": "雅思7分",
        "target_country": "英国",
        "customer_info": "客户张三，本科毕业，预算40万，雅思7分，想去英国留学",
        "is_target": True,
        "judge_reason": "完全符合目标客户画像"
    }
)

print(response.json())
```

## 响应示例

### 成功响应 (200)

```json
{
    "success": true,
    "customer_id": 1,
    "name": "张三",
    "phone": "13800138001",
    "is_target": true,
    "message": "客户信息已成功保存"
}
```

### 错误响应 (400)

```json
{
    "detail": "姓名和电话不能为空"
}
```

## 注意事项

1. **必填字段**: `name` 和 `phone` 是必填的
2. **数据类型**: `budget` 必须是数字类型（如 40.0），不能是字符串
3. **布尔值**: `is_target` 必须是 true/false，不能是字符串
4. **URL 配置**: 确保 Dify 能访问到你的服务器地址
