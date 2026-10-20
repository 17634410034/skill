# 六、饮食记录


---

## 6.1 批量记录饮食

> 文档编号: `dcfb94a0` · 更新时间: 2026-09-08 15:08:26

#### 接口说明
批量记录用户饮食数据。

#### 请求地址
```
POST /v2/eating/record
```

#### 请求头
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户唯一标识 |
| `record_on` | string | 是 | 记录日期，格式 `yyyy-MM-dd` |
| `meal_type` | int64 | 是 | 餐别，见下方餐别说明 |
| `foods` | array | 是 | 食物列表（仅支持食物库食物） |

餐别类型 `meal_type` 枚举值：

| 值 | 说明 |
|----|------|
| 1 | 早餐 |
| 2 | 中餐 |
| 3 | 晚餐 |
| 4 | 加餐 |
| 6 | 上午加餐 |
| 7 | 下午加餐 |
| 8 | 晚上加餐 |

`foods` 数组元素：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `food_code` | string | 是 | 食物编码（仅支持食物库食物） |
| `amount` | double | 是 | 数量 |
| `unit_name` | string | 是 | 单位名称（如：克、个、碗） |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `count` | int64 | 记录的食物条数 |
| `daily` | object | 当天饮食数据 |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
|`id`| int64 | 饮食记录id|


#### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v2/eating/record' \
  -H 'X-Api-Key: your_api_key' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user_123",
    "record_on": "2026-05-12",
    "meal_type": 1,
    "foods": [
      { "food_code": "food_001", "amount": 2, "unit_name": "个" },
      { "food_code": "food_002", "amount": 250, "unit_name": "毫升" }
    ]
  }'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "count": 2,
    "daily": {
      "meals": [
        {
          "meal_type": 1,
          "items": [
            {
              "food_name": "牛奶",
              "food_code": "food_milk",
              "amount": 250,
              "unit_name": "毫升",
              "calories": 135,
              "protein": 7.5,
              "fat": 8,
              "carbohydrate": 8.5,
              "id": 1
            }
          ],
          "total_calories": 135,
          "total_protein": 7.5,
          "total_fat": 8,
          "total_carbohydrate": 8.5
        }
      ],
      "total_calories": 135,
      "total_protein": 7.5,
      "total_fat": 8,
      "total_carbohydrate": 8.5
    }
  }
}
```


---

## 6.2 记录单个食物

> 文档编号: `dc5454c5` · 更新时间: 2026-09-08 15:08:25

#### 接口说明
记录单个食物到饮食中。

#### 请求地址
```
POST /v2/eating/record_single
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
| record_on | 是 | string | 记录日期，格式 yyyy-MM-dd |
| meal_type | 是 | int | 餐别：1=早餐，2=午餐，3=晚餐，4=加餐，6=早加餐，7=午加餐，8=晚加餐 |
| food_code | 是 | string | 食物编码 |
| amount | 是 | double | 数量 |
| unit_name | 是 | string | 单位名称（如：克，个，碗） |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id` | int64 | 饮食记录 ID |
| `food_name` | string | 食物名称 |
| `calories` | double | 摄入热量（kcal） |
| `daily` | object | 当天饮食数据 |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
|`id`| int64 | 饮食记录id|

#### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v2/eating/record_single' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test_user","record_on":"2024-01-01","meal_type":1,"food_code":"00000001","amount":100,"unit_name":"克"}'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "id": 12345,
    "food_name": "米饭",
    "calories": 232,
    "daily": {
      "meals": [
        {
          "meal_type": 2,
          "items": [
            {
              "food_name": "米饭",
              "food_code": "food_rice",
              "amount": 200,
              "unit_name": "克",
              "calories": 232,
              "protein": 5.2,
              "fat": 0.6,
              "carbohydrate": 51.4,
               "id": 1 
            }
          ],
          "total_calories": 232,
          "total_protein": 5.2,
          "total_fat": 0.6,
          "total_carbohydrate": 51.4
        }
      ],
      "total_calories": 232,
      "total_protein": 5.2,
      "total_fat": 0.6,
      "total_carbohydrate": 51.4
    }
  }
}
```


---

## 6.3 删除饮食记录

> 文档编号: `dc5dc9b3` · 更新时间: 2026-09-08 15:08:03

#### 接口说明
删除用户的饮食记录。

#### 请求地址
```
POST /v2/eating/delete
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
| record_on | 是 | string | 记录日期，格式 yyyy-MM-dd |
| meal_type | 是 | int | 餐别：1=早餐，2=午餐，3=晚餐，4=加餐，6=早加餐，7=午加餐，8=晚加餐 |
| food_code | 是 | string | 食物编码 |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `daily` | object | 当天饮食数据 |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
|`id`| int64 | 饮食记录id|


#### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v2/eating/delete' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test_user","record_on":"2024-01-01","meal_type":1,"food_code":"00000001"}'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "id": 12345,
    "food_name": "米饭",
    "calories": 232,
    "daily": {
      "meals": [
        {
          "meal_type": 2,
          "items": [
            {
              "food_name": "米饭",
              "food_code": "food_rice",
              "amount": 200,
              "unit_name": "克",
              "calories": 232,
              "protein": 5.2,
              "fat": 0.6,
              "carbohydrate": 51.4,
              "id": 1
            }
          ],
          "total_calories": 232,
          "total_protein": 5.2,
          "total_fat": 0.6,
          "total_carbohydrate": 51.4
        }
      ],
      "total_calories": 232,
      "total_protein": 5.2,
      "total_fat": 0.6,
      "total_carbohydrate": 51.4
    }
  }
}
```


---

## 6.4 查询饮食记录

> 文档编号: `dc208f2e` · 更新时间: 2026-09-08 15:08:02

#### 接口说明
查询用户某一天的饮食记录。

#### 请求地址
```
GET /v2/eating/records
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
| record_on | 是 | string | 记录日期，格式 yyyy-MM-dd |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `daily` | object | 当天饮食数据 |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
|`id`| int64 | 饮食记录id|


#### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v2/eating/records?user_id=test_user&record_on=2024-01-01' \
  -H 'X-Api-Key: {api_key}'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "daily": {
      "meals": [
        {
          "meal_type": 1,
          "items": [
            { "meal_type": 1, "food_name": "鸡蛋", "food_code": "food_001", "amount": 2, "unit_name": "个", "calories": 120, "protein": 8.8, "fat": 5.2, "carbohydrate": 1.6, "id": 1 }
          ],
          "total_calories": 120,
          "total_protein": 8.8,
          "total_fat": 5.2,
          "total_carbohydrate": 1.6
        },
        {
          "meal_type": 2,
          "items": [
            { "meal_type": 2, "food_name": "米饭", "food_code": "food_100", "amount": 200, "unit_name": "克", "calories": 232, "protein": 4.6, "fat": 0.8, "carbohydrate": 50.2, "id": 2 }
          ],
          "total_calories": 232,
          "total_protein": 4.6,
          "total_fat": 0.8,
          "total_carbohydrate": 50.2
        }
      ],
      "total_calories": 352,
      "total_protein": 13.4,
      "total_fat": 6.0,
      "total_carbohydrate": 51.8
    }
  }
}
```


---

## 6.5 修改饮食记录

> 文档编号: `dc5ef8ff` · 更新时间: 2026-09-08 15:08:00

#### 接口说明
修改饮食记录。

#### 请求地址
```
POST /v2/eating/update
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
| record_on | 否 | string | 记录日期，格式 yyyy-MM-dd |
| meal_type | 否 | int | 餐别：1=早餐，2=午餐，3=晚餐，4=加餐，6=早加餐，7=午加餐，8=晚加餐 |
| amount | 否 | double | 数量 |
| unit_name | 否 | string | 单位名称（如：克，个，碗） |
| id | 是 | int64 | 饮食记录 ID |
| meal_at| 否 | string | 餐时间，格式 yyyy-MM-dd HH:mm:ss |
| calory| 否 | double | 摄入热量（kcal） |
| unit_id| 否 | int64 | 单位 ID |

#### 返回字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| `id` | int64 | 饮食记录 ID |
| `food_name` | string | 食物名称 |
| `calories` | double | 摄入热量（kcal） |
| `daily` | object | 当天饮食数据 |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
|`id`| int64 | 饮食记录id|

#### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v2/eating/update' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"test_user","record_on":"2024-01-01","meal_type":1,"amount":100,"unit_name":"克","id":1}'
```

#### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "id": 12345,
    "food_name": "米饭",
    "calories": 232,
    "daily": {
      "meals": [
        {
          "meal_type": 2,
          "items": [
            {
              "food_name": "米饭",
              "food_code": "food_rice",
              "amount": 200,
              "unit_name": "克",
              "calories": 232,
              "protein": 5.2,
              "fat": 0.6,
              "carbohydrate": 51.4,
               "id": 1 
            }
          ],
          "total_calories": 232,
          "total_protein": 5.2,
          "total_fat": 0.6,
          "total_carbohydrate": 51.4
        }
      ],
      "total_calories": 232,
      "total_protein": 5.2,
      "total_fat": 0.6,
      "total_carbohydrate": 51.4
    }
  }
}
```


---

## 6.6 获取当日最新饮食记录

> 文档编号: `dc2fe733` · 更新时间: 2026-09-08 15:07:44

### 接口说明
获取截止当日最新的饮食记录

### 请求地址
```
GET /v2/eating/latest
```

### 请求头

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| X-Api-Key | 是 | string | API密钥 |

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `user_id` | string | 是 | 用户标识 |

### 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `record_on` | string | 记录日期，格式 `yyyy-MM-dd` |
| `daily` | object | 当天饮食数据（同记录饮食接口） |

`daily` 对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meals` | array | 按餐别分组的饮食数据 |
| `total_calories` | double | 当日总热量（kcal） |
| `total_protein` | double | 当日总蛋白质（g） |
| `total_fat` | double | 当日总脂肪（g） |
| `total_carbohydrate` | double | 当日总碳水化合物（g） |

`meals` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `items` | array | 食物明细 |
| `total_calories` | double | 该餐总热量（kcal） |
| `total_protein` | double | 该餐总蛋白质（g） |
| `total_fat` | double | 该餐总脂肪（g） |
| `total_carbohydrate` | double | 该餐总碳水化合物（g） |

`items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `meal_type` | int64 | 餐别 |
| `food_name` | string | 食物名称 |
| `food_code` | string | 食物编码 |
| `amount` | double | 数量 |
| `unit_name` | string | 单位名称 |
| `calories` | double | 摄入热量（kcal） |
| `protein` | double | 蛋白质（g） |
| `fat` | double | 脂肪（g） |
| `carbohydrate` | double | 碳水化合物（g） |
| `id` | int64| 饮食记录id|


### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v2/eating/latest?user_id=user_123' \
  -H 'X-Api-Key: your_api_key'
```

### 返回示例
```json
{
  "code": 0,
  "message": "",
  "data": {
    "record_on": "2026-05-12",
    "daily": {
      "meals": [
        {
          "meal_type": 1,
          "items": [
            { "meal_type": 1, "food_name": "鸡蛋", "food_code": "food_001", "amount": 2, "unit_name": "个", "calories": 120, "protein": 8.8, "fat": 5.2, "carbohydrate": 1.6, "id": 1 }
          ],
          "total_calories": 120,
          "total_protein": 8.8,
          "total_fat": 5.2,
          "total_carbohydrate": 1.6
        }
      ],
      "total_calories": 120,
      "total_protein": 8.8,
      "total_fat": 5.2,
      "total_carbohydrate": 1.6
    }
  }
}
```
