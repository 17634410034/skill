# 五、体重记录


---

## 5.1 记录体重

> 文档编号: `dc1e43e2` · 更新时间: 2026-09-08 15:08:31

#### 接口说明
记录用户体重数据。

#### 请求地址
```
POST /v2/weight/record
```

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| user_id | 是 | string | 用户唯一标识 |
| weight | 是 | double | 体重(kg) |
| body_fat | 否 | double | 体脂率(%) |
| record_on | 否 | string | 记录日期，格式 yyyy-MM-dd，不传默认今天 |

#### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v1/weight/record' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test_user","weight":65.5,"body_fat":20.1,"record_on":"2024-01-01"}'
```

#### 返回示例
```json
{}
```



---

## 5.2 获取体重列表

> 文档编号: `dc3f0752` · 更新时间: 2026-09-08 15:08:30

#### 接口说明
查询用户体重记录列表。

#### 请求地址
```
GET /v2/weight/records
```

#### 请求头
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| user_id | 是 | string | 用户唯一标识 |
| start_date | 是 | string | 开始日期，格式 yyyy-MM-dd |
| end_date | 是 | string | 结束日期，格式 yyyy-MM-dd |
| page | 否 | int64 | 页码，从1开始，默认 1 |
| page_size | 否 | int64 | 每页条数，默认 20 |

#### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v2/weight/records?user_id=test_user&start_date=2024-01-01&end_date=2024-01-31' \
  -H 'X-Api-Key: {api_key}'
```

#### 返回示例
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "record_on": "2024-01-01",
      "weight": 65.5,
      "body_fat": 20.1,
      "measure_time": "2024-01-01 08:00:00"
    }
  ]
}
```


---

## 5.3 获取最新体重记录

> 文档编号: `dc93c323` · 更新时间: 2026-09-08 15:08:29

#### 接口说明
 获取用户指定日期之前（包含指定日期）的最新一条体重记录。`record_on` 参数不传时默认取当天。

#### 请求地址
`GET /v2/weight/latest`

#### 请求头
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识 |
| `record_on` | string | 否 | 指定日期，格式 `yyyy-MM-dd`，不传默认当天 |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `item` | object | 体重记录，若无记录则为 null |

`item` 结构：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `record_on` | string | 日期，格式 `yyyy-MM-dd` |
| `weight` | double | 体重（kg） |
| `body_fat` | double | 体脂率（%） |
| `measure_time` | string | 测量时间 |

#### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v2/weight/latest?user_id=user_123&record_on=2026-05-12' \
  -H 'X-Api-Key: your_api_key'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "item": {
      "id": 1,
      "record_on": "2026-05-11",
      "weight": 70.5,
      "body_fat": 22.5,
      "measure_time": "2026-05-11 08:00:00"
    }
  }
}
```


---

## 5.4 删除体重记录

> 文档编号: `dc0f01d7` · 更新时间: 2026-09-08 15:08:29

### 接口说明
删除体重记录

### 请求地址
```
POST /v2/weight/delete
```

### 请求头

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| X-Api-Key | 是 | string | API密钥 |

### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| user_id | 是 | string | 用户标识 |
| id | 是 | int64 | 体重记录 ID |

### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v2/weight/delete' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test_user","id":1}'
```

### 返回示例
```json
{}
```


---

## 5.5 查询体重曲线

> 文档编号: `dc986757` · 更新时间: 2026-09-08 15:08:28

### 接口说明
查询体重曲线接口

### 请求地址
```
GET /v2/weight/line
```

### 请求头

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| X-Api-Key | 是 | string | API密钥 |

### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| user_id | 是 | string | 用户标识 |
| page | 否 | int64 | 页码, 从1开始, 默认 1 |
| page_size | 否 | int64 | 每页条数, 默认 20 |
| chart_line_type | 否 | string | 曲线类型 weight、body_fat |
| start_date | 否 | string | 开始日期 yyyy-MM-dd |
| end_date | 否 | string | 结束日期 yyyy-MM-dd |

### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v2/weight/line?user_id=test_user&chart_line_type=weight' \
  -H 'X-Api-Key: {api_key}'
```

### 返回示例
```json
{
  "line_data": [{"record_on": "2026-01-01", "value": 65.5}],
  "has_more": false
}
```
