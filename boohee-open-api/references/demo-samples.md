# 官方文档返回示例（离线速查）

本篇的 JSON **全部是从 `references/01~06` 官网正文里逐字摘录的「返回示例」**，不是实时接口返回，也不是模型生成的数据。它解决一个具体问题：用户还没有 API Key、或当前环境访问不到 `api.boohee.com` 时，助手依然能告诉用户「这个接口真实会返回什么结构、字段叫什么、营养按什么口径给」，而不是空手让用户去注册。

## 使用规则（硬约束，不可省略）

1. **引用本篇任何数据给用户时，回复第一行必须声明**：「以下为薄荷官方接口文档的示例返回，非实时查询结果」。不做推断、不伪装成实时数据。
2. 示例里的 `code` / `food_code`（如 `10001`）是文档演示数据，**不可**直接拿去调写入类接口（`/v2/eating/record`、`/v2/weight/record` 等）；要写入必须先有真实查询结果。
3. 本篇**不是字段定义来源**。参数表、枚举、必填约束一律回 `references/01~06` 原文，需要生成代码时同样以那几篇为准。
4. 用户配好凭证后，一律以实时接口返回为准，本篇只用于对照与演示；两者不一致时按`07-integration-ops.md` 第 8 节走文档漂移核对，不要自行判断谁对谁错。
5. 未收录的接口：1.2 换取 AccessToken（属凭证链路，无演示价值）、3.4 图片识别流式输出（官方示例为大量重复 SSE 帧，每帧结构与 3.2 识别详情一致，看 3.2 即可）。

## 目录

| 能力 | 接口 | 小节 | 来源文件 |
|---|---|---|---|
| 食物搜索 | `GET /v1/food/search` | 2.1 | `references/02-food-data.md` |
| 食物详情 | `GET /v1/food/detail` | 2.2 | `references/02-food-data.md` |
| 食物分类 | `GET /v1/food/categories` | 2.3 | `references/02-food-data.md` |
| 分类食物列表 | `GET /v1/food/list` | 2.4 | `references/02-food-data.md` |
| 食物单位 | `GET /v1/food/units` | 2.5 | `references/02-food-data.md` |
| 批量获取营养信息 | `POST /v1/food/ingredients` | 2.6 | `references/02-food-data.md` |
| 食物排行榜 | `GET /v1/food/ranks` | 2.7 | `references/02-food-data.md` |
| 食物图片识别 | `POST /v1/food/image_recognize` | 3.1 | `references/03-recognition.md` |
| 获取食物识别详情 | `GET /v1/food/image_recognize_detail` | 3.2 | `references/03-recognition.md` |
| 自然语言识别 | `POST /v1/food/text_recognize` | 3.3 | `references/03-recognition.md` |
| 创建智能食谱 | `POST /v1/recipe/generate` | 4.1 | `references/04-recipe.md` |
| 获取智能食谱详情 | `GET /v1/recipe/details` | 4.2 | `references/04-recipe.md` |
| 获取换一换菜肴列表 | `GET /v1/recipe/replace_foods` | 4.3 | `references/04-recipe.md` |
| 替换餐别单个食物 | `POST /v1/recipe/replace_food` | 4.4 | `references/04-recipe.md` |
| 替换整餐食物 | `POST /v1/recipe/replace_meal` | 4.5 | `references/04-recipe.md` |
| 食谱模式列表 | `GET /v1/recipe/mode_list` | 4.6 | `references/04-recipe.md` |
| 食谱模式详情 | `GET /v1/recipe/mode_detail` | 4.7 | `references/04-recipe.md` |
| 食谱概要 | `GET /v1/recipe/summary` | 4.8 | `references/04-recipe.md` |
| 记录体重 | `POST /v2/weight/record` | 5.1 | `references/05-weight.md` |
| 获取体重列表 | `GET /v2/weight/records` | 5.2 | `references/05-weight.md` |
| 获取最新体重记录 | `GET /v2/weight/latest` | 5.3 | `references/05-weight.md` |
| 删除体重记录 | `POST /v2/weight/delete` | 5.4 | `references/05-weight.md` |
| 查询体重曲线 | `GET /v2/weight/line` | 5.5 | `references/05-weight.md` |
| 批量记录饮食 | `POST /v2/eating/record` | 6.1 | `references/06-diet.md` |
| 记录单个食物 | `POST /v2/eating/record_single` | 6.2 | `references/06-diet.md` |
| 删除饮食记录 | `POST /v2/eating/delete` | 6.3 | `references/06-diet.md` |
| 查询饮食记录 | `GET /v2/eating/records` | 6.4 | `references/06-diet.md` |
| 修改饮食记录 | `POST /v2/eating/update` | 6.5 | `references/06-diet.md` |
| 获取当日最新饮食记录 | `GET /v2/eating/latest` | 6.6 | `references/06-diet.md` |


---

## 二、食物数据

### 2.1 食物搜索

接口：`GET /v1/food/search`
来源：`references/02-food-data.md` 2.1（文档编号 `dc8b7beb`，更新时间 2026-09-08 15:09:06）

```json
{
  "code": 0,
  "message": "成功", //字符串类型
  "now": 1722851989, //数字类型
  "data": {
    "page": 1,     // 当前页码
    "per_page": 20, // 每页条数
    "has_more": false,  // 是否还有下一页
    "foods": [
      {
        "code": "10001",
        "name": "苹果（中等大小）",
        "calories": 52,  // 热量（kcal/100g）
        "protein": 0.2, // 蛋白质（g/100g）
        "fat": 0.2,     // 脂肪（g/100g）
        "carbohydrate": 13.5, // 碳水化合物（g/100g）
        "health_light": 1, // 食物红绿灯（0：无，1：绿灯，2：黄灯，3：红灯）
        "is_liquid": false, // 是否液体食物
        "image_url": "https://xxx.boohee.com/food/10001.jpg", // 食物图片地址
        "units": [
          {
            "unit_id": 14,
            "unit_name": "个(中)",
            "weight": "210.0",
            "eat_weight": "159.6"
          },
          // 更多单位
        ]
      },
      // 更多食物...
    ]
  }
}
```

### 2.2 食物详情

接口：`GET /v1/food/detail`
来源：`references/02-food-data.md` 2.2（文档编号 `dc043193`，更新时间 2026-09-21 16:15:27）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "code": "10001",
    "name": "苹果（中等大小）",
    "health_light": 1, // 食物红绿灯（0：无，1：绿灯，2：黄灯，3：红灯）
    "image_url": "https://xxx.boohee.com/food/10001.jpg",
    "food_weight_url": "https://xxx.boohee.com/food_weight/10001.jpg", // 食物重量图片
    "is_liquid": false, // 是否液体食物
    "food_type": "食材", // 食物类型（食材、菜肴、包装食品）
    "calories": {
      "name": "热量",
      "value": 52,
      "unit": "kcal",
      "unit_name": "千卡",
      "nrv": 0.15 // 即 15%
    },
    "protein": {
      "name": "蛋白质",
      "value": 0.2,
      "unit": "g",
      "unit_name": "克",
      "nrv": 0.03 // 即 3%
    },
    "fat": {
      "name": "脂肪",
      "value": 0.2,
      "unit": "g",
      "unit_name": "克",
      "nrv": 0.03 // 即 3%
    },
    "carbohydrate": {
      "name": "碳水化合物",
      "value": 13.5,
      "unit": "g",
      "unit_name": "克",
      "nrv": 0.27 // 即 27%
    },
    "gi": {
      "name": "血糖指数",
      "value": 50,
      "level": 1, // GI值等级（0：低，1：中，2：高，-1：无数据）
    },
    "gl": {
      "name": "血糖负荷",
      "value": 50,
      "level": 1, // GL值等级（0：低，1：中，2：高，-1：无数据）
    },
    // 更多营养成分数据
    "ingredients": [
      {
        "key": "sugar",
        "type": "carbohydrate",
        "name": "糖",
        "value": 10.5,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.21 // 即 21%
      },
      {
        "key": "fiber",
        "type": "carbohydrate",
        "name": "膳食纤维",
        "value": 2.5,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.1 // 即 10%
      },
      {
        "key": "good_protein",
        "type": "protein",
        "name": "优质蛋白质",
        "value": 0.4,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.06 // 即 6%
      },
      {
        "key": "saturated_fat",
        "type": "fat",
        "name": "饱和脂肪",
        "value": 0.1,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.02 // 即 2%
      },
      {
        "key":" fatty_acid",
        "type": "fat",
        "name": "反式脂肪",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "fa_mufa",
        "type": "fat",
        "name": "单不饱和脂肪酸",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "pufa",
        "type": "fat",
        "name": "多不饱和脂肪酸",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "cholesterol",
        "type": "fat",
        "name": "胆固醇",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "vitamin_a",
        "type": "vitamins",
        "name": "维生素A",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "thiamine",
        "type": "vitamins",
        "name": "维生素B1",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "lactose",
        "type": "vitamins",
        "name": "维生素B2",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_b6",
        "type": "vitamins",
        "name": "维生素B6",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_b12",
        "type": "vitamins",
        "name": "维生素B12",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_c",
        "type": "vitamins",
        "name": "维生素C",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "carotene",
        "type": "vitamins",
        "name": "胡萝卜素",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_d",
        "type": "vitamins",
        "name": "维生素D",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_e",
        "type": "vitamins",
        "name": "维生素E",
        "value": 0.05,
        "unit": "g",
        "unit_name": "克",
        "nrv": 0.01
      },
      {
        "key": "vitamin_k",
        "type": "vitamins",
        "name": "维生素K",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "niacin",
        "type": "vitamins",
        "name": "烟酸",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "pantothenic",
        "type": "vitamins",
        "name": "泛酸",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "biotin",
        "type": "vitamins",
        "name": "生物素",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "natrium",
        "type": "minerals",
        "name": "钠",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "kalium",
        "type": "minerals",
        "name": "钾",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "calcium",
        "type": "minerals",
        "name": "钙",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "phosphor",
        "type": "minerals",
        "name": "磷",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "magnesium",
        "type": "minerals",
        "name": "镁",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "chlorine",
        "type": "minerals",
        "name": "氯",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "iron",
        "type": "minerals",
        "name": "铁",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "zinc",
        "type": "minerals",
        "name": "锌",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "copper",
        "type": "minerals",
        "name": "铜",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "manganese",
        "type": "minerals",
        "name": "锰",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01
      },
      {
        "key": "iodine",
        "type": "minerals",
        "name": "碘",
        "value": 0.05,
        "unit": "μg",
        "unit_name": "微克",
        "nrv": 0.01
      },
      {
        "key": "selenium",
        "type": "minerals",
        "name": "硒",
        "value": 0.05,
        "unit": "μg",
        "unit_name": "微克",
        "nrv": 0.01
      },
      {
        "key": "isoleucine",
        "type": "amino_acid",
        "name": "异亮氨酸",
        "value": 211.6,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "leucine",
        "type": "amino_acid",
        "name": "亮氨酸",
        "value": 342.68,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "lysine",
        "type": "amino_acid",
        "name": "赖氨酸",
        "value": 281.39,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "methionine",
        "type": "amino_acid",
        "name": "蛋氨酸",
        "value": 106.61,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "cystine",
        "type": "amino_acid",
        "name": "胱氨酸",
        "value": 163.32,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "phenylalanine",
        "type": "amino_acid",
        "name": "苯丙氨酸",
        "value": 217.88,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "tyrosine",
        "type": "amino_acid",
        "name": "酪氨酸",
        "value": 164.87,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "threonine",
        "type": "amino_acid",
        "name": "苏氨酸",
        "value": 198.1,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "tryptophan",
        "type": "amino_acid",
        "name": "色氨酸",
        "value": 595.06,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "valine",
        "type": "amino_acid",
        "name": "缬氨酸",
        "value": 210.24,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "arginine",
        "type": "amino_acid",
        "name": "精氨酸",
        "value": 245.78,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "histidine",
        "type": "amino_acid",
        "name": "组氨酸",
        "value": 91.52,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "alanine",
        "type": "amino_acid",
        "name": "丙氨酸",
        "value": 218.62,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "aspartic_acid",
        "type": "amino_acid",
        "name": "天冬氨酸",
        "value": 435.5,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "glutamate",
        "type": "amino_acid",
        "name": "谷氨酸",
        "value": 698.78,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "glycine",
        "type": "amino_acid",
        "name": "甘氨酸",
        "value": 133.68,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "proline",
        "type": "amino_acid",
        "name": "脯氨酸",
        "value": 119.14,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "serine",
        "type": "amino_acid",
        "name": "丝氨酸",
        "value": 299.36,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "sulfur_amino_acid",
        "type": "amino_acid",
        "name": "含硫氨基酸",
        "value": 269.94,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "aromatic_amino_acids",
        "type": "amino_acid",
        "name": "芳香族氨基酸",
        "value": 382.45,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": null
      },
      {
        "key": "purine",
        "type": "other",
        "name": "嘌呤",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "alcohol",
        "type": "other",
        "name": "酒精",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "lutein_zeaxanthin",
        "type": "other",
        "name": "叶黄素+玉米黄素",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01 // 即 1%
      },
      {
        "key": "betaine",
        "type": "other",
        "name": "甜菜碱",
        "value": 0.05,
        "unit": "mg",
        "unit_name": "毫克",
        "nrv": 0.01 // 即 1%
      }
    ],
    "units": [
      {
        "unit_id": 14,
        "unit_name": "个(中)",
        "weight": "210.0",
        "eat_weight": "159.6"
      },
      // 更多单位
    ],
    "materials": { // 菜肴食物才有该字段
      "foods": [
        {
          "name": "鸡蛋",
          "type": "major", // 主要食材
          "weight": 100,
          "desc": ""
        },
        {
          "name": "番茄",
          "type": "major",
          "weight": 200,
          "desc": ""
        },
        {
          "name": "花生油",
          "type": "minor", // 次要食材
          "weight": 10,
          "desc": ""
        },
        {
          "name": "小葱",
          "type": "minor",
          "weight": 5,
          "desc": ""
        },
        {
          "name": "白砂糖",
          "type": "seasoning", // 调味料
          "weight": 2,
          "desc": ""
        },
        {
          "name": "食盐",
          "type": "seasoning",
          "weight": 2,
          "desc": ""
        }
      ],
      "description": "菜肴做法" 
    }
  }
}
```

### 2.3 食物分类

接口：`GET /v1/food/categories`
来源：`references/02-food-data.md` 2.3（文档编号 `dc6baf19`，更新时间 2026-09-08 15:08:59）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "kind": "group",
    "categories": [
      {
        "id": 1,
        "name": "主食类",
      },
      {
        "id": 2,
        "name": "蔬菜类",
      }
      // 更多分类...
    ]
  }
}
```

### 2.4 分类食物列表

接口：`GET /v1/food/list`
来源：`references/02-food-data.md` 2.4（文档编号 `dcb6ee92`，更新时间 2026-09-08 15:08:58）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "page": 1,     // 当前页码
    "per_page": 20, // 每页条数
    "has_more": false,
    "foods": [
      {
        "code": "10001",
        "name": "苹果（中等大小）",
        "calories": 52,  // 热量（kcal/100g）
        "protein": 0.2, // 蛋白质（g/100g）
        "fat": 0.2,     // 脂肪（g/100g）
        "carbohydrate": 13.5, // 碳水化合物（g/100g）
        "health_light": 1, // 食物红绿灯（0：无，1：绿色，2：黄色，3：红色）
        "is_liquid": false, // 是否液体食物
        "image_url": "https://xxx.boohee.com/food/10001.jpg", // 食物图片地址
        "units": [
          {
            "unit_id": 14,
            "unit_name": "个(中)",
            "weight": "210.0",
            "eat_weight": "159.6"
          },
          // 更多单位
        ],
      },
      // 更多食物...
    ]
  }
}
```

### 2.5 食物单位

接口：`GET /v1/food/units`
来源：`references/02-food-data.md` 2.5（文档编号 `dc00259c`，更新时间 2026-09-08 15:08:58）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "code": "10001",
    "name": "苹果（中等大小）",
    "calories": 52,  // 热量（kcal/100g）
    "image_url": "https://xxx.boohee.com/food/10001.jpg", // 食物图片地址
    "units": [
      {
        "unit_id": 14,
        "unit_name": "个(中)",
        "weight": "210.0",
        "eat_weight": "159.6",
        "calories": "86.2" // 单位重量热量
      }
    ] 
  }
}
```

### 2.6 批量获取营养信息

接口：`POST /v1/food/ingredients`
来源：`references/02-food-data.md` 2.6（文档编号 `dc199d79`，更新时间 2026-09-08 15:08:57）

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "foods": [
      { "name": "鸡蛋", "code": "food_001","barcode":"", weight: 100, count: 0},
      { "name": "牛奶", "code": "food_002","barcode":"96123456", weight: 0, count: 1 }
    ],
    "calories": { "name": "热量", "value": 280, "unit": "kcal", "unit_name": "千卡" },
    "protein": { "name": "蛋白质", "value": 20.5, "unit": "g", "unit_name": "克" },
    "fat": { "name": "脂肪", "value": 12.3, "unit": "g", "unit_name": "克" },
    "carbohydrate": { "name": "碳水化合物", "value": 15.6, "unit": "g", "unit_name": "克" },
    "ingredients": [
      { "key": "calcium", "type": "mineral", "name": "钙", "value": 150, "unit": "mg", "unit_name": "毫克" }
    ]
  }
}
```

### 2.7 食物排行榜

接口：`GET /v1/food/ranks`
来源：`references/02-food-data.md` 2.7（文档编号 `dc188fd3`，更新时间 2026-09-08 15:08:56）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "title": "高硒-调味品类", // 食物排行标题
    "category": "按类别+营养素", //类别
    "ingredient_name": "硒", // 营养元素
    "description": "好吃，热量低", // 食物排行描述
    "foods": [
      {
        "code": "pingguo_junzhi",
        "name": "苹果",
        "image_url": "http://s.boohee.cn/house/food_mid/mid_photo_2015126214658469.jpg",
        "is_liquid": false,
        "health_light": 1,
        "calories": "54", // 每 100 克热量值，单位：千卡
        "ingredient_weight": 4.1, // 每 100 克营养素值
        "ingredient_unit": "克", // 营养素单位
      }
    ]
  }
}
```


---

## 三、智能识别

### 3.1 食物图片识别

接口：`POST /v1/food/image_recognize`
来源：`references/03-recognition.md` 3.1（文档编号 `dc21070c`，更新时间 2026-09-17 13:36:09）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "task_id": "xxxxxxx"
  }
}
```

### 3.2 获取食物识别详情

接口：`GET /v1/food/image_recognize_detail`
来源：`references/03-recognition.md` 3.2（文档编号 `dc8e6244`，更新时间 2026-09-08 15:08:55）

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "status": 2,
    "err_message": "",
    "content": "识别中...",
    "eating_items": [
      {
        "code": "food_001",
        "name": "番茄炒蛋",
        "calories": 85,
        "protein": 4.5,
        "fat": 6.2,
        "carbohydrate": 3.8,
        "health_light": 1,
        "is_liquid": false,
        "image_url": "https://cdn.boohee.com/foods/tomato_egg.jpg",
        "amount": 200,
        "ingredients": [
          {
            "key": "n3fa",
            "name": "n-3脂肪酸",
            "value": 0.03,
            "unit": "g",
            "unit_name": "克"
          },
          {
            "key": "vitamin_c",
            "name": "维生素C(抗坏血酸)",
            "value": 1.24,
            "unit": "mg",
            "unit_name": "毫克"
          },
          {
            "key": "n6_fatty_acids",
            "name": "n6脂肪酸",
            "value": 0,
            "unit": "g",
            "unit_name": "克"
          }
        ],
        "nrv": [
          {
            "key": "n3fa",
            "name": "n-3脂肪酸",
            "value": 0
          },
          {
            "key": "vitamin_c",
            "name": "维生素C(抗坏血酸)",
            "value": 0.01
          },
          {
            "key": "n6_fatty_acids",
            "name": "n6脂肪酸",
            "value": 0
          },
          {
            "key": "protein",
            "name": "蛋白质",
            "value": 0.07
          },
          {
            "key": "fat",
            "name": "脂肪",
            "value": 0.06
          },
          {
            "key": "carbohydrate",
            "name": "碳水化合物",
            "value": 0.12
          },
          {
            "key": "calories",
            "name": "热量",
            "value": 0.1
          }
        ]
      }
    ]
  }
}
```

### 3.3 自然语言识别

接口：`POST /v1/food/text_recognize`
来源：`references/03-recognition.md` 3.3（文档编号 `dc88e1fe`，更新时间 2026-09-08 15:08:54）

```json
{
  "code": 0,
  "message": "success",
  "now": 1722851989,
  "data": {
    "result": [
      {
        "time_type": 1, //1: 早餐，2: 中餐，3: 晚餐，6：早加餐，7：午加餐，8：晚加餐
        "foods": [
          {
            "code": "10001",
            "name": "苹果（中等大小）",
            "calorie": 52,  // 热量（kcal/100g）
            "protein": 0.2, // 蛋白质（g/100g）
            "fat": 0.2,     // 脂肪（g/100g）
            "carbohydrate": 13.5, // 碳水化合物（g/100g）
            "health_light": 1, // 食物红绿灯（0：无，1：绿色，2：黄色，3：红色）
            "is_liquid": false, // 是否液体食物
            "image_url": "https://xxx.boohee.com/food/10001.jpg", // 食物图片地址
            "amount": 150, // 估重（克）
          }
        ]
      }
    ]
    
  }
}
```


---

## 四、智能食谱

### 4.1 创建智能食谱

接口：`POST /v1/recipe/generate`
来源：`references/04-recipe.md` 4.1（文档编号 `dc23870d`，更新时间 2026-09-08 15:08:37）

```json
{
  "code": 0,
  "message": "",
  "data": {
    "task_id": "recipe_task_abc123"
  }
}
```

### 4.2 获取智能食谱详情

接口：`GET /v1/recipe/details`
来源：`references/04-recipe.md` 4.2（文档编号 `dcfd0e49`，更新时间 2026-09-08 15:08:36）

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

### 4.3 获取换一换菜肴列表

接口：`GET /v1/recipe/replace_foods`
来源：`references/04-recipe.md` 4.3（文档编号 `dcbb1867`，更新时间 2026-09-08 15:08:35）

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

### 4.4 替换餐别单个食物

接口：`POST /v1/recipe/replace_food`
来源：`references/04-recipe.md` 4.4（文档编号 `dc3750cd`，更新时间 2026-09-08 15:08:35）

```json
{
  "code": 0,
  "message": "",
  "data": {}
}
```

### 4.5 替换整餐食物

接口：`POST /v1/recipe/replace_meal`
来源：`references/04-recipe.md` 4.5（文档编号 `dc4a4a1b`，更新时间 2026-09-08 15:08:34）

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

### 4.6 食谱模式列表

接口：`GET /v1/recipe/mode_list`
来源：`references/04-recipe.md` 4.6（文档编号 `dc1b777a`，更新时间 2026-09-08 15:08:33）

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

### 4.7 食谱模式详情

接口：`GET /v1/recipe/mode_detail`
来源：`references/04-recipe.md` 4.7（文档编号 `dcf977b1`，更新时间 2026-10-16 14:37:03）

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

### 4.8 食谱概要

接口：`GET /v1/recipe/summary`
来源：`references/04-recipe.md` 4.8（文档编号 `dcdc5c64`，更新时间 2026-09-08 15:08:32）

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


---

## 五、体重记录

### 5.1 记录体重

接口：`POST /v2/weight/record`
来源：`references/05-weight.md` 5.1（文档编号 `dc1e43e2`，更新时间 2026-09-08 15:08:31）

```json
{}
```

### 5.2 获取体重列表

接口：`GET /v2/weight/records`
来源：`references/05-weight.md` 5.2（文档编号 `dc3f0752`，更新时间 2026-09-08 15:08:30）

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

### 5.3 获取最新体重记录

接口：`GET /v2/weight/latest`
来源：`references/05-weight.md` 5.3（文档编号 `dc93c323`，更新时间 2026-09-08 15:08:29）

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

### 5.4 删除体重记录

接口：`POST /v2/weight/delete`
来源：`references/05-weight.md` 5.4（文档编号 `dc0f01d7`，更新时间 2026-09-08 15:08:29）

```json
{}
```

### 5.5 查询体重曲线

接口：`GET /v2/weight/line`
来源：`references/05-weight.md` 5.5（文档编号 `dc986757`，更新时间 2026-09-08 15:08:28）

```json
{
  "line_data": [{"record_on": "2026-01-01", "value": 65.5}],
  "has_more": false
}
```


---

## 六、饮食记录

### 6.1 批量记录饮食

接口：`POST /v2/eating/record`
来源：`references/06-diet.md` 6.1（文档编号 `dcfb94a0`，更新时间 2026-09-08 15:08:26）

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

### 6.2 记录单个食物

接口：`POST /v2/eating/record_single`
来源：`references/06-diet.md` 6.2（文档编号 `dc5454c5`，更新时间 2026-09-08 15:08:25）

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

### 6.3 删除饮食记录

接口：`POST /v2/eating/delete`
来源：`references/06-diet.md` 6.3（文档编号 `dc5dc9b3`，更新时间 2026-09-08 15:08:03）

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

### 6.4 查询饮食记录

接口：`GET /v2/eating/records`
来源：`references/06-diet.md` 6.4（文档编号 `dc208f2e`，更新时间 2026-09-08 15:08:02）

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

### 6.5 修改饮食记录

接口：`POST /v2/eating/update`
来源：`references/06-diet.md` 6.5（文档编号 `dc5ef8ff`，更新时间 2026-09-08 15:08:00）

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

### 6.6 获取当日最新饮食记录

接口：`GET /v2/eating/latest`
来源：`references/06-diet.md` 6.6（文档编号 `dc2fe733`，更新时间 2026-09-08 15:07:44）

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
