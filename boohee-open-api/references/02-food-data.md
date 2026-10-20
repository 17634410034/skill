# 二、食物数据


---

## 2.1 食物搜索

> 文档编号: `dc8b7beb` · 更新时间: 2026-09-08 15:09:06

#### 接口说明
根据关键词搜索食物，获取食物的基础信息。

#### 请求地址
**GET `/v1/food/search`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
|keyword|String|是|搜索关键词（如“苹果”“米饭”），长度1-30字符。keyword 和 barcode 二选一|
|barcode|String|否|食物条码（13位数字），用于查询特定食物。keyword 和 barcode 二选一|
|page|Integer|否|页码，默认1|
|per_page|Integer|否|每页条数，默认20，最大50|
|sort|String|否|排序方式，可选值：calorie_asc（热量升序）、calorie_desc（热量降序），默认无排序|
|with_units | Boolean | 否 | 是否返回 units 字段数据(最热门的排第一)，默认 false|


#### 请求示例
```bash
curl --request GET 'https://api.boohee.com/open-apis/v1/food/search?keyword=%E8%8B%B9%E6%9E%9C' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.......'
```

#### 返回示例
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


---

## 2.2 食物详情

> 文档编号: `dc043193` · 更新时间: 2026-09-21 16:15:27

#### 接口说明
根据食物 code 获取食物详情。

#### 请求地址
**GET `/v1/food/detail`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| code | String | 是 | 食物编码（从食物搜索接口获取）|
| with_ingredients | Boolean | 否 | 是否返回 ingredients 字段数据，默认 false |
| with_units | Boolean | 否 | 是否返回 units 字段数据，默认 false |
| with_materials | Boolean | 否 | 是否返回 materials 字段数据，默认 false |

#### 返回示例
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


---

## 2.3 食物分类

> 文档编号: `dc6baf19` · 更新时间: 2026-09-08 15:08:59

#### 接口说明
根据食物ID列表，批量获取食物的信息。

#### 请求地址
**GET `/v1/food/categories`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| kind | String | 否 | 分类种类，取值为 group（通用分类）  / cooking（烹饪分类），默认 group |


#### 返回示例
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


---

## 2.4 分类食物列表

> 文档编号: `dcb6ee92` · 更新时间: 2026-09-08 15:08:58

#### 接口说明
获取指定分类下的食物列表。

#### 请求地址
**GET `/v1/food/list`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| id | Integer | 是 | 分类ID，从分类接口获取 |
| kind | String | 是 | 分类类型，从分类接口获取 |
| with_units | Boolean | 否 | 是否返回 units 字段数据(最热门的排第一)，默认 false |


#### 返回示例
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


---

## 2.5 食物单位

> 文档编号: `dc00259c` · 更新时间: 2026-09-08 15:08:58

#### 接口说明
获取食物分类的估重图。

#### 请求地址
**GET `/v1/food/units`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| code | String | 是 | 食物编码，从食物列表接口获取 |


#### 返回示例
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


---

## 2.6 批量获取营养信息

> 文档编号: `dc199d79` · 更新时间: 2026-09-08 15:08:57

### 接口说明
获取指定食物的营养元素信息。

### 请求地址
```
POST /v1/food/ingredients
```

### 请求头

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| X-Api-Key | 是 | string | API密钥 |
| Content-Type | 是 | string | application/json |

### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| `foods` | array | 是 | 食物列表 |

`foods` 数组元素：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `code` | string | 是 | 食物编码 ；与 barcode 二选一|
| `weight` | double | 是 | 食物重量。单位为：克；传 code 时，必需传 weight |
| `barcode` | string | 是 | 食物 69 码；与 code 二选一 |
| `count` | int | 是 | 食物份数。传 barcode 时，可传该值，且该值优先级大于 weight；传 code 时，不需要传 count |

### 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `foods` | array | 食物名称列表 |
| `calories` | object | 总热量信息 |
| `protein` | object | 总蛋白质信息 |
| `fat` | object | 总脂肪信息 |
| `carbohydrate` | object | 总碳水化合物信息 |
| `ingredients` | array | 更多营养成分 |

`foods` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `name` | string | 食物名称 |
| `code` | string | 食物编码 |
|`barcode`|string|69码，仅在使用了69码查询的食物信息中返回|
| `weight` | double | 食物重量。单位为：克；传 code 时返回 |
| `count` | int | 食物份数。传 barcode 时返回 |

营养信息对象（`calories` / `protein` / `fat` / `carbohydrate`）：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `name` | string | 名称 |
| `value` | double | 数值 |
| `unit` | string | 单位 |
| `unit_name` | string | 单位名称 |

更多营养成分对象：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `key` | string | 键 |
| `type` | string | 类型 |
| `name` | string | 名称 |
| `value` | double | 数值 |
| `unit` | string | 单位 |
| `unit_name` | string | 单位名称 |

### 请求示例
```bash
curl -X POST 'https://api.boohee.com/open-apis/v1/food/ingredients' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"foods":[{"code":"00000001","weight":100},{"barcode":"6920907805161","count":1}]}'
```

### 返回示例
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


---

## 2.7 食物排行榜

> 文档编号: `dc188fd3` · 更新时间: 2026-09-08 15:08:56

#### 接口说明
根据食物营养信息，返回食物排行榜。

#### 请求地址
**GET `/v1/food/ranks`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| ingredient | String | 是 | 要排行的营养元素名称。如：蛋白质 |
| sort | String | 否 | 按照营养价值排序，正序：0（默认）；倒序：1 |
| tag | String | 否 | 食物标签。如：高蛋白 |

支持的营养元素名:
| 元素名 | 元素名 | 元素名 | 元素名 | 元素名 | 元素名 | 元素名 | 元素名 | 元素名 | 元素名 |
| ---- | :------- | :------ | :------ | :------ | :------ | :------- | :------- | :------- | --- |
| 重量 | 可食重量 | 体积 | 水 | 含水量 | 液体 | 热量 | 能量 | 热能 | 卡 |
| GI | gi | GL | gl | 蛋白质 | 蛋白 | 大豆蛋白 | 植物蛋白质 | 植物蛋白 | 动物蛋白质 |
| 动物蛋白 | 脂肪 | 脂 | 脂肪酸 | 饱和脂肪 | 饱和脂肪酸 | 不饱和脂肪 | 不饱和脂肪酸 | 单不饱和脂肪 | 单不饱和脂肪酸 |
| 多不饱和脂肪 | 多不饱和脂肪酸 | n-3脂肪酸 | 欧米伽-3 | Ω-3 | Ω3 | 反式脂肪 | 反式脂肪酸 | 胆固醇 | 碳水化合物 |
| 碳水 | 糖 | 纤维 | 膳食纤维 | 膳食纤维素 | 钠 | 维生素A | 维生素a | 维A | 胡萝卜素 |
| 维生素D | 维生素d | 维D | 维生素E | 维生素e | 维E | 维生素K | 维生素k | 维K | 维生素B1 |
| 维生素b1 | 硫胺素 | 维生素B2 | 维生素b2 | 核黄素 | 维生素B3 | 维生素b3 | 维生素B6 | 维生素b6 | 吡哆醇 |
| 维生素B12 | 维生素b12 | 钴胺素 | 维生素C | 维生素c | 维C | 抗坏血酸 | 烟酸 | 烟酰胺 | 尼克酸 |
| 叶酸 | 胆碱 | 泛酸 | 生物素 | 磷 | 钾 | 钙 | 镁 | 铁 | 铁质 |
| 锌 | 碘 | 硒 | 铜 | 锰 | 氟 | 铬 | 汞 | DHA | dha |
| 原花青素 | 槲皮素 | 花色苷 | 大豆异黄酮 | 叶黄素 | 植物甾醇 | 肉碱 | 酒精度 | 嘌呤 |

---

支持的食物标签：

| 标签名 | 标签名 | 标签名 | 标签名 | 标签名 | 标签名 | 标签名 | 标签名 | 标签名 | 标签名 |
| ---- | :------- | :------ | :------ | :------ | :------ | :------- | :------- | :------- | --- |
| 水果 | 蔬菜 | 蔬菜水果  | 主食 | 鱼 | 薯 | 蔬果  | 蔬菜菌藻 | 乳制品 | 肉蛋 |
| 奶 | 菌藻 | 坚果 | 谷薯 | 谷 | 豆制品 | 豆 | 蛋 | 肉 | 谷薯杂豆 |
| 坚果种子 | 大豆 | 调味品 | 禽畜 | 水产 | 植物 | 海鲜 | 鱼虾海鲜 | 油脂 | Easy食品 |
| 禽 |高嘌呤食物 | 中高嘌呤食物 | 中低嘌呤食物 | 中低嘌呤食物 | 低嘌呤食物 | 其他 | 

GI 营养素目前支持的食物标签：

| 标签名 | 标签名 | 
| ---- | :------- |
| 水果 | 主食 |

#### 返回示例
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
