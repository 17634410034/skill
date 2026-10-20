# 四、智能食谱


---

## 4.1 创建智能食谱

> 文档编号: `dc23870d` · 更新时间: 2026-09-08 15:08:37

### 接口说明
根据用户信息和偏好生成智能食谱，返回异步任务ID。

### 请求路径
`POST /v1/recipe/generate`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识 |
| date | string | 是 | 日期，格式 yyyy-MM-dd，不传则以当前日期推导。生成指定日期所在自然周当周食谱 |
| gender | int64 | 是 | 用户性别（1：男，2：女） |
| latest_weight| double| 是| 最新体重|
| energy | int64 | 是 | 用户能量需求（kcal/天） |
| diet_favor | int64 | 否 | 饮食偏好（1：正常，2：素食，3：蛋奶素食） |
| diet_area | array | 否 | 饮食区域（1：东北，2：西北，3：华北，4：华东，5：华中，6：西南，7：华南） |
| weight_management | int64 | 否 | 体重管理目标（1：增肌，2：减重，3：塑形） |
| nutrition_management | array | 否 | 营养管理目标（1：减脂，2：增肌，3：塑形，4：营养均衡，5：控糖，6：控压） |
| ban_foods | array | 否 | 禁忌食物列表，1：猪肉、2：内脏、3：香菜、4：葱、5：蒜、6：辣椒、7：含有麸质的谷物及其制品、8：甲壳纲类动物及其制品、9：鱼类及其制品、10：蛋类及其制品、11：花生及其制品、12：大豆及其制品、13：乳及乳制品、14：坚果果仁类制品 |
| illness | array | 否 | 疾病（1：糖尿病，2：痛风，3：甲亢，4：甲减，5：高血压，6：高血脂） |
| diet_mode | string | 否 | 饮食模式（type2Diabetes、crd、carbCycling、fasting1608、mediumHighProtein、fasting、vegetarian、mediterranean、dashDiet） |
| diet_mode_opt | object | 否 | 饮食模式选项 |
| diet_mode_opt.fasting_days | array | 否 | 轻断日（1-7，选2天） |
| diet_mode_opt.vegetarian_days | array | 否 | 弹性素食日 |
| diet_mode_opt.low_carbon_days | array | 否 | 碳循环日-低碳 |
| diet_mode_opt.medium_carbon_days | array | 否 | 碳循环日-中碳 |
| diet_mode_opt.high_carbon_days | array | 否 | 碳循环日-高碳 |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| task_id | string | 任务ID |

### 请求示例

```json
{
  "user_id": "user_001",
  "date": "2024-01-15",
  "gender": 2,
  "latest_weight": 75,
  "energy": 1500,
  "diet_favor": 1,
  "weight_management": 2,
  "nutrition_management": [1],
  "illness": []
}
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "task_id": "recipe_task_abc123"
  }
}
```


---

## 4.2 获取智能食谱详情

> 文档编号: `dcfd0e49` · 更新时间: 2026-09-08 15:08:36

### 接口说明
根据日期获取用户的完整食谱。

### 请求路径
`GET /v1/recipe/details`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户标识 |
| date | string | 是 | 食谱归属日期，格式 yyyy-MM-dd |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
|task_id| string|任务id，生成食谱的task_id|
| recipe_list | array | 食谱列表 |
| recipe_list[].date | string | 日期 |
| recipe_list[].daily_type | int64 | 标记特殊日期（1：轻断日，2：素食日，3：低碳日，4：中碳日，5：高碳日） |
| recipe_list[].calories | int64 | 热量 |
| recipe_list[].fat | double | 当日总脂肪 |
| recipe_list[].protein | double | 当日总蛋白质 |
| recipe_list[].carbohydrate | double | 当日总碳水化合物 |
| recipe_list[].meals | array | 餐别列表 |
| recipe_list[].meals[].meal_type | string | 餐别code |
| recipe_list[].meals[].meal_name | string | 餐别中文 |
| recipe_list[].meals[].calories | double | 当餐热量 |
| recipe_list[].meals[].fat | double | 当餐脂肪 |
| recipe_list[].meals[].protein | double | 当餐蛋白质 |
| recipe_list[].meals[].carbohydrate | double | 当餐碳水 |
| recipe_list[].meals[].time_type | int64 | 餐别类型 |
| recipe_list[].meals[].food_list | array | 食物列表 |
| recipe_list[].meals[].food_list[].food_id | string | 食物id，不再返回，请使用food_code 字段 |
| recipe_list[].meals[].food_list[].food_code | string | 食物 code |
| recipe_list[].meals[].food_list[].food_name | string | 食物名称 |
| recipe_list[].meals[].food_list[].image_url | string | 食物图片 |
| recipe_list[].meals[].food_list[].calories | int64 | 热量 |
| recipe_list[].meals[].food_list[].protein | int64 | 蛋白质 |
| recipe_list[].meals[].food_list[].fat | int64 | 脂肪 |
| recipe_list[].meals[].food_list[].carbohydrate | int64 | 碳水 |
| recipe_list[].meals[].food_list[].health_light | int64 | 食物红绿灯 |
| recipe_list[].meals[].food_list[].is_liquid | bool | 是否液体 |
| recipe_list[].meals[].food_list[].count | int64 | 数量（g） |
| recipe_list[].meals[].food_list[].unit_count | int64 | 显示数量值 |
| recipe_list[].meals[].food_list[].unit_name | string | 显示数量单位 |
| recipe_list[].meals[].food_list[].extension_units | array | 扩展单位列表 |
| recipe_list[].meals[].food_list[].extension_units[].unit_id | int64 | 单位ID |
| recipe_list[].meals[].food_list[].extension_units[].unit | string | 单位名称 |
| recipe_list[].meals[].food_list[].extension_units[].unit_value | double | 单位重量（g） |
| recipe_list[].meals[].food_list[].extension_units[].eat_value | double | 可食部重量（g） |

### 请求示例

```
GET https://api.iboohee.com/open-apis/v1/recipe/details?user_id=user_001&date=2024-01-15
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "task_id":"9f50127c-fae4-44ac-866b-e2239e7541ed",
    "recipe_list": [
      {
        "date": "2024-01-15",
        "daily_type": 0,
        "calories": 1500,
        "fat": 50.0,
        "protein": 90.0,
        "carbohydrate": 180.0,
        "meals": [
          {
            "meal_type": "breakfast",
            "meal_name": "早餐",
            "calories": 400,
            "fat": 15.0,
            "protein": 20.0,
            "carbohydrate": 50.0,
            "time_type": 1,
            "food_list": [
              {
                 "food_id": "", // 此字段不再返回具体内容，请改用food_code字段
                "food_code": "food_milk",
                "food_name": "牛奶",
                "image_url": "https://example.com/milk.jpg",
                "calories": 54,
                "protein": 3,
                "fat": 3,
                "carbohydrate": 5,
                "health_light": 1,
                "is_liquid": true,
                "count": 250,
                "unit_count": 1,
                "unit_name": "杯",
                "extension_units": [
                  { "unit_id": 1, "unit": "杯", "unit_value": 250, "eat_value": 250 }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```


---

## 4.3 获取换一换菜肴列表

> 文档编号: `dcbb1867` · 更新时间: 2026-09-08 15:08:35

### 接口说明

获取可替换的菜肴选项列表。

### 请求路径
`GET /v1/recipe/replace_foods`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识 |
| date | string | 是 | 日期，格式 yyyy-MM-dd |
| time_type | int64 | 是 | 餐别类型（1：早餐，2：午餐，3：晚餐，6：上午加餐，7：下午加餐，8：晚上加餐） |
| food_id | string | 是 | 被替换菜肴code |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| food_list | array | 可替换菜肴列表（结构同食谱详情中的食物条目） |
| food_list[].food_code | string | 食物 code |
| food_list[].food_name | string | 食物名称 |
| food_list[].image_url | string | 食物图片 |
| food_list[].calories | int64 | 热量 |
| food_list[].protein | int64 | 蛋白质 |
| food_list[].fat | int64 | 脂肪 |
| food_list[].carbohydrate | int64 | 碳水 |
| food_list[].health_light | int64 | 食物红绿灯 |
| food_list[].is_liquid | bool | 是否液体 |
| food_list[].count | int64 | 数量（g） |
| food_list[].unit_count | int64 | 显示数量值 |
| food_list[].unit_name | string | 显示数量单位 |
| food_list[].extension_units | array | 扩展单位列表 |

### 请求示例

```
GET https://api.iboohee.com/open-apis/v1/recipe/replace-foods?user_id=user_001&date=2024-01-15&time_type=2&food_id=food_rice
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "food_list": [
      {
        "food_code": "food_noodle",
        "food_name": "面条",
        "image_url": "https://example.com/noodle.jpg",
        "calories": 110,
        "protein": 4,
        "fat": 1,
        "carbohydrate": 24,
        "health_light": 1,
        "is_liquid": false,
        "count": 200,
        "unit_count": 1,
        "unit_name": "碗",
        "extension_units": []
      }
    ]
  }
}
```


---

## 4.4 替换餐别单个食物

> 文档编号: `dc3750cd` · 更新时间: 2026-09-08 15:08:35

### 接口说明
将食谱中的单个菜肴替换为另一个。

### 请求路径
`POST /v1/recipe/replace_food`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识 |
| date | string | 是 | 日期，格式 yyyy-MM-dd |
| time_type | int64 | 是 | 餐别类型 |
| original_id | string | 是 | 被替换菜肴ID |
| target_id | string | 是 | 替换到的菜肴ID |

### 返回参数

无（空对象）

### 请求示例

```json
{
  "user_id": "user_001",
  "date": "2024-01-15",
  "time_type": 2,
  "original_id": "food_rice",
  "target_id": "food_noodle"
}
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {}
}
```


---

## 4.5 替换整餐食物

> 文档编号: `dc4a4a1b` · 更新时间: 2026-09-08 15:08:34

### 接口说明
替换食谱中的某一餐别的所有食物

### 请求路径
`POST /v1/recipe/replace_meal`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识 |
| date | string | 是 | 日期，格式 yyyy-MM-dd |
| time_type | int64 | 是 | 餐别类型 |
| un_replace_ids | array | 否 | 不需要替换的食物ID列表 |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| meal_type | string | 餐别code |
| meal_name | string | 餐别中文 |
| calories | double | 当餐热量 |
| fat | double | 当餐脂肪 |
| protein | double | 当餐蛋白质 |
| carbohydrate | double | 当餐碳水 |
| food_list | array | 食物列表（结构同食谱详情中的食物条目） |

### 请求示例

```json
{
  "user_id": "user_001",
  "date": "2024-01-15",
  "time_type": 2,
  "un_replace_ids": ["food_egg"]
}
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "meal_type": "lunch",
    "meal_name": "午餐",
    "calories": 500,
    "fat": 18.0,
    "protein": 25.0,
    "carbohydrate": 60.0,
    "food_list": [
      {
        "food_code: "food_egg",
        "food_name": "鸡蛋",
        "image_url": "https://example.com/egg.jpg",
        "calories": 144,
        "protein": 13,
        "fat": 9,
        "carbohydrate": 3,
        "health_light": 2,
        "is_liquid": false,
        "count": 50,
        "unit_count": 1,
        "unit_name": "个",
        "extension_units": []
      }
    ]
  }
}
```


---

## 4.6 食谱模式列表

> 文档编号: `dc1b777a` · 更新时间: 2026-09-08 15:08:33

### 接口说明
获取饮食谱模式列表内容

### 请求路径
`GET /v1/recipe/mode_list`

### 请求参数

无

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| mode_list | array | 饮食模式列表 |
| mode_list[].code | string | 饮食模式 code |
| mode_list[].name | string | 饮食模式名称 |
| mode_list[].icon_url | string | 饮食模式图标 |
| mode_list[].description | string | 子标题 |
| mode_list[].tags | array | 标签列表 |

### 请求示例

```
GET https://api.iboohee.com/open-apis/v1/recipe/mode-list
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "mode_list": [
      {
        "code": "mediterranean",
        "name": "地中海饮食",
        "icon_url": "https://example.com/mediterranean.svg",
        "description": "以植物性食物为主的健康饮食模式",
        "tags": ["健康", "心血管"]
      },
      {
        "code": "fasting1608",
        "name": "16:8 轻断食",
        "icon_url": "https://example.com/fasting.svg",
        "description": "每天16小时禁食，8小时进食",
        "tags": ["减脂", "断食"]
      }
    ]
  }
}
```


---

## 4.7 食谱模式详情

> 文档编号: `dcf977b1` · 更新时间: 2026-10-16 14:37:03

### 接口说明
获取食谱模式介绍内容

### 请求路径
`GET /v1/recipe/mode_detail`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | string | 是 | 饮食模式 code |
| energy | int64 | 是 | 用户能量需求（kcal/天） |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | string | 饮食模式 code |
| name | string | 名称 |
| description | string | 描述 |
| bg_url | string | 背景图片 |
| reference | array | 参考文献列表 |
| taboo_crowd | array | 禁忌人群列表 |
| faq | array | Q&A 列表 |
| faq[].question | string | 问题 |
| faq[].answer | string | 答案 |
| recommend_recipe | object | 食谱推荐 |
| recommend_recipe.calories | int64 | 热量 |
| recommend_recipe.fat | object | 脂肪（MacroNutrient） |
| recommend_recipe.protein | object | 蛋白质（MacroNutrient） |
| recommend_recipe.carbohydrate | object | 碳水化合物（MacroNutrient） |
| recommend_recipe.meals | array | 餐别列表 |

**MacroNutrient 结构**：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| name | string | 名称 |
| value | uint32 | 值（g） |
| percent | uint32 | 供能比（%） |
| tips | string | 提示 |

### 请求示例

```
GET https://api.iboohee.com/open-apis/v1/recipe/mode_detail?code=mediterranean&energy=1500
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "code": "mediterranean",
    "name": "地中海饮食",
    "description": "地中海饮食是一种以植物性食物为主的健康饮食模式...",
    "bg_url": "https://example.com/bg_mediterranean.jpg",
    "reference": ["参考文献1", "参考文献2"],
    "taboo_crowd": ["孕妇", "儿童"],
    "faq": [
      {
        "question": "地中海饮食适合减脂吗？",
        "answer": "地中海饮食强调健康的脂肪摄入..."
      }
    ],
    "recommend_recipe": {
      "calories": 1500,
      "fat": { "name": "脂肪", "value": 50, "percent": 30, "tips": "以橄榄油为主" },
      "protein": { "name": "蛋白质", "value": 90, "percent": 24, "tips": "鱼虾为主" },
      "carbohydrate": { "name": "碳水化合物", "value": 180, "percent": 46, "tips": "全谷物" },
      "meals": []
    }
  }
}
```


---

## 4.8 食谱概要

> 文档编号: `dcdc5c64` · 更新时间: 2026-09-08 15:08:32

### 接口说明
获取食谱概要

### 请求路径
`GET /v1/recipe/summary`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| user_id | string | 是 | 用户唯一标识 |
| date | string | 是 | 日期，格式 yyyy-MM-dd，不传则以当前日期推导 |
| time_type | int64 | 否 | 餐别类型 |
| type | int64 | 是 | 分析类型（1：概述） |

### 返回参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| recipe_info | object | 食谱信息 |
| recipe_info.name | string | 名称 |
| recipe_info.code | string | code |
| recipe_info.calories | int64 | 热量 |
| recipe_info.fat | object | 脂肪（MacroNutrient） |
| recipe_info.protein | object | 蛋白质（MacroNutrient） |
| recipe_info.carbohydrate | object | 碳水化合物（MacroNutrient） |
| recipe_info.description | string | 食谱描述 |

### 请求示例

```
GET https://api.boohee.com/open-apis/v1/recipe/summary?user_id=user_001&date=2024-01-15&type=1
```

### 返回结果示例

```json
{
  "code": 0,
  "message": "",
  "data": {
    "recipe_info": {
      "name": "地中海饮食",
      "code": "mediterranean",
      "calories": 1500,
      "fat": { "name": "脂肪", "value": 50, "percent": 30, "tips": "以橄榄油为主" },
      "protein": { "name": "蛋白质", "value": 90, "percent": 24, "tips": "鱼虾为主" },
      "carbohydrate": { "name": "碳水化合物", "value": 180, "percent": 46, "tips": "全谷物" },
      "description": "今日食谱以地中海饮食模式为基础..."
    }
  }
}
```
