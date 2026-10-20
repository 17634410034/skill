# 三、智能识别


---

## 3.1 食物图片识别

> 文档编号: `dc21070c` · 更新时间: 2026-09-17 13:36:09

#### 接口说明
上传食物图片，识别图片中的食物，返回食物名称、热量等相关信息。流式输出接口。

#### 请求地址
**POST `/v1/food/image_recognize`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Body JSON）
|参数名|类型|必填|说明|
|---|---|---|---|
|image_url|String|否|能公网访问的图片URL地址。限制：图片大小不超过10MB；图片为正方形，效果更佳；图片支持格式：.jpe、.jpeg、.jpg、.png。image_url 或 image_data 二选之一|
|image_data|String|否|图片的 base64 数据。image_url 或 image_data 二选之一|


#### 返回示例
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


---

## 3.2 获取食物识别详情

> 文档编号: `dc8e6244` · 更新时间: 2026-09-08 15:08:55

#### 接口说明
根据食物图片识别结果，返回饮食建议。流式输出接口。

#### 请求地址
**GET `/v1/food/image_recognize_detail`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Query）
|参数名|类型|必填|说明|
|---|---|---|---|
| task_id | String | 是 | 识别任务ID |
|ingredients| 否| string|需要返回的营养素数据的营养素编码，半角豆号分隔。具体见支持的营养素列表
|with_nrv| 否| bool | 是否返回nrv数据，如果该参数为true，则返回热量、蛋白质、脂肪、碳水化合物以及ingredients参数指定的营养素的nrv数据

`ingredients `支持的营养素列表
| key | name |
  |-----|------|
| gi| 血糖生成指数|
|gl|升糖负荷|
  | sugar | 糖 |
  | purine | 嘌呤 |
  | fiber_dietary | 膳食纤维 |
  | saturated_fat | 饱和脂肪(酸) |
  | ufa | 不饱和脂肪酸 |
  | fatty_acid | 反式脂肪(酸) |
  | mufa | 单不饱和脂肪酸 |
  | pufa | 多不饱和脂肪酸 |
  | dha | DHA |
  | n6_fatty_acids | n6脂肪酸 |
  | n9_fatty_acids | n9脂肪酸 |
  | n3fa | n-3脂肪酸 |
  | cholesterol | 胆固醇 |
  | vitamin_a | 维生素A |
  | vitamin_d | 维生素D |
  | vitamin_e | 维生素E |
  | vitamin_k | 维生素K |
  | thiamine | 维生素B1(硫胺素) |
  | lactoflavin | 维生素B2(核黄素) |
  | vitamin_b6 | 维生素B6(吡哆醇) |
  | vitamin_b12 | 维生素B12(钴胺素) |
  | niacin | 烟酸(烟酰胺/尼克酸) |
  | pantothenic | 泛酸 |
  | choline | 胆碱 |
  | biotin | 生物素 |
  | vitamin_c | 维生素C(抗坏血酸) |
  | natrium | 钠 |
  | kalium | 钾 |
  | calcium | 钙 |
  | phosphor | 磷 |
  | magnesium | 镁 |
  | chlorine | 氯 |
  | iron | 铁 |
  | zinc | 锌 |
  | copper | 铜 |
  | manganese | 锰 |
  | chrome | 铬 |
  | iodine | 碘 |
  | selenium | 硒 |
  | fluorine | 氟 |
  | hg | 汞 |

### 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `status` | int64 | 识别状态：1-解析中，2-已完成，3-未识别到食物，4-识别失败 |
| `err_message` | string | 失败原因说明（当 status 不为 2 时） |
| `content` | string | 识别过程中的文本 |
| `eating_items` | array | 识别出的食物列表 |

`eating_items` 数组元素：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `code` | string | 食物编码 |
| `name` | string | 食物名称 |
| `calories` | int64 | 热量（kcal/100g） |
| `protein` | double | 蛋白质（g/100g） |
| `fat` | double | 脂肪（g/100g） |
| `carbohydrate` | double | 碳水化合物（g/100g） |
| `health_light` | int64 | 食物红绿灯 |
| `is_liquid` | bool | 是否液体食物 |
| `image_url` | string | 食物图片地址 |
| `amount` | double | 估重（克） |
|`ingredients`| array |营养素数据，需要请求参数中ingredients字段传值|
|`nrv`|array|nrv数据，需要请求参数中with_nrv=true|

`ingredients` 数组元素:

| 字段名 | 类型 | 说明 |
|--------|------|------|
|key|string|营养素编码|
|name|string|营养素名称|
|value|double|数值，每100g食物中的含量|
|unit|string|单位，比如：mg等|
|unit_name|string|单位中文名，比如：毫克|

`nrv` 数组元素：
| 字段名 | 类型 | 说明 |
|--------|------|------|
|key|string|营养素编码|
|name|string|营养素名称|
|value|double|数值|


### 请求示例
```bash
curl -X GET 'https://api.boohee.com/open-apis/v1/food/image_recognize_detail?task_id=task_xxxxx&with_nrv=true&ingredients=vitamin_c, n3fa, n6_fatty_acids' \
  -H 'X-Api-Key: {api_key}'
```

#### 返回示例
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


---

## 3.3 自然语言识别

> 文档编号: `dc88e1fe` · 更新时间: 2026-09-08 15:08:54

#### 接口说明
根据自然语言描述，返回食物名称、热量等相关信息。

#### 请求地址
**POST `/v1/food/text_recognize`**

#### 请求头（Header）
| 参数名 | 类型 | 必填 | 描述 |
|-------|------|------|------|
| Authorization | String | 否 | Bearer {accessToken} ，Authorization 和 X-Api-Key 二选一 |
| X-Api-Key | String | 否 | API Key ，Authorization 和 X-Api-Key 二选一 |

#### 请求参数（Body JSON）
|参数名|类型|必填|说明|
|---|---|---|---|
| text | String | 是 | 自然语言描述，如：早上喝了一杯牛奶 |

#### 返回示例
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

## 3.4 食物图片识别(流式输出)

> 文档编号: `dce4f10a` · 更新时间: 2026-09-08 15:08:53

### 接口说明
食物图片识别，流式输出

### 请求地址
```
POST /v1/food/image_recongize_stream
```

### 请求头

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| X-Api-Key | 是 | string | API密钥 |
| Content-Type | 是 | string | application/json |

### 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|---|---|---|---|
| image_url | 否 | string | 能公网访问的图片URL地址，image_url 或 image_data 二选一 |
| image_data | 否 | string | 图片的 base64 数据，image_url 或 image_data 二选一 |
|ingredients| 否| string|需要返回的营养素数据的营养素编码，半角豆号分隔。编码见下方支持的营养素列表
|with_nrv| 否| bool | 是否返回nrv数据，如果该参数为true，则返回热量、蛋白质、脂肪、碳水化合物以及ingredients参数指定的营养素的nrv数据

`ingredients `支持的营养素列表
| key | name |
  |-----|------|
| gi| 血糖生成指数|
|gl|升糖负荷|
  | sugar | 糖 |
  | purine | 嘌呤 |
  | fiber_dietary | 膳食纤维 |
  | saturated_fat | 饱和脂肪(酸) |
  | ufa | 不饱和脂肪酸 |
  | fatty_acid | 反式脂肪(酸) |
  | mufa | 单不饱和脂肪酸 |
  | pufa | 多不饱和脂肪酸 |
  | dha | DHA |
  | n6_fatty_acids | n6脂肪酸 |
  | n9_fatty_acids | n9脂肪酸 |
  | n3fa | n-3脂肪酸 |
  | cholesterol | 胆固醇 |
  | vitamin_a | 维生素A |
  | vitamin_d | 维生素D |
  | vitamin_e | 维生素E |
  | vitamin_k | 维生素K |
  | thiamine | 维生素B1(硫胺素) |
  | lactoflavin | 维生素B2(核黄素) |
  | vitamin_b6 | 维生素B6(吡哆醇) |
  | vitamin_b12 | 维生素B12(钴胺素) |
  | niacin | 烟酸(烟酰胺/尼克酸) |
  | pantothenic | 泛酸 |
  | choline | 胆碱 |
  | biotin | 生物素 |
  | vitamin_c | 维生素C(抗坏血酸) |
  | natrium | 钠 |
  | kalium | 钾 |
  | calcium | 钙 |
  | phosphor | 磷 |
  | magnesium | 镁 |
  | chlorine | 氯 |
  | iron | 铁 |
  | zinc | 锌 |
  | copper | 铜 |
  | manganese | 锰 |
  | chrome | 铬 |
  | iodine | 碘 |
  | selenium | 硒 |
  | fluorine | 氟 |
  | hg | 汞 |


### 返回字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `result_code` | int | 结果编码，非0表示错误 |
|`message`| string|code=0时候该字段是success，code非0时候表示的是具体的错误信息|
|`server_time`| int64|服务器时间|
|`trace_id`| string|请求唯一标识，系统内部产生。如果反馈及 debug 请提供 traceId|
|`data`|object|识别结果数据,具体字段见下方识别结果对象说明|

识别结果:
| 字段名 | 类型 | 说明 |
|--------|------|------|
|`task_id"`|string|识别任务id|
|`end`|bool|是否结束|
|`content`|string|识别中，流式输出内容|
|`food_info`|食物信息数组|食物信息|

食物信息：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `code` | string | 食物编码 |
| `name` | string | 食物名称 |
| `calories` | int64 | 热量（kcal/100g） |
| `protein` | double | 蛋白质（g/100g） |
| `fat` | double | 脂肪（g/100g） |
| `carbohydrate` | double | 碳水化合物（g/100g） |
| `health_light` | int64 | 食物红绿灯 |
| `is_liquid` | bool | 是否液体食物 |
| `image_url` | string | 食物图片地址 |
| `amount` | double | 估重（克） |
|`ingredients`| array |营养素数据，需要请求参数中ingredients字段传值|
|`nrv`|array|nrv数据，需要请求参数中with_nrv=true|

`ingredients` 数组元素:

| 字段名 | 类型 | 说明 |
|--------|------|------|
|key|string|营养素编码|
|name|string|营养素名称|
|value|double|数值，每100g食物中的含量|
|unit|string|单位，比如：mg等|
|unit_name|string|单位中文名，比如：毫克|

`nrv` 数组元素：
| 字段名 | 类型 | 说明 |
|--------|------|------|
|key|string|营养素编码|
|name|string|营养素名称|
|value|double|数值|


### 请求示例
```bash
curl -X POST 'https://api.iboohee.com/open-apis/v1/food/image_recongize_stream' \
  -H 'X-Api-Key: {api_key}' \
  -H 'Content-Type: application/json' \
  -d '{"image_url":"https://img.boohee.cn/ghp/foods/000/000/001/140_1.jpg","with_nrv": true, "ingredients":"sugar,purine,fatty_acid,vitamin_a"}'
```

### 返回示例
```json
id:1
data:{"result_code":0,"message":"success","server_time":1782701027244,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"食物：香芋地瓜丸","food_info":[]}}

id:2
data:{"result_code":0,"message":"success","server_time":1782701027367,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":", 45","food_info":[]}}

id:3
data:{"result_code":0,"message":"success","server_time":1782701027508,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"g","food_info":[]}}

id:4
data:{"result_code":0,"message":"success","server_time":1782701027684,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"\n食物：盐酥杏鲍","food_info":[]}}

id:5
data:{"result_code":0,"message":"success","server_time":1782701027908,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"菇, 90","food_info":[]}}

id:6
data:{"result_code":0,"message":"success","server_time":1782701028085,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"g","food_info":[]}}

id:7
data:{"result_code":0,"message":"success","server_time":1782701028307,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"\n食物：超值四拼炸鸡","food_info":[]}}

id:8
data:{"result_code":0,"message":"success","server_time":1782701028526,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"（含琥珀酱甜辣、西域孜","food_info":[]}}

id:9
data:{"result_code":0,"message":"success","server_time":1782701028679,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"然粉、蜂蜜芥末酱）","food_info":[]}}

id:10
data:{"result_code":0,"message":"success","server_time":1782701028908,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":", 200","food_info":[]}}

id:11
data:{"result_code":0,"message":"success","server_time":1782701029101,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"g","food_info":[]}}

id:12
data:{"result_code":0,"message":"success","server_time":1782701030093,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"\n食物：无骨鸡块（每","food_info":[]}}

id:13
data:{"result_code":0,"message":"success","server_time":1782701030198,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"单限1，放套餐里）","food_info":[]}}

id:14
data:{"result_code":0,"message":"success","server_time":1782701030287,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":", 60","food_info":[]}}

id:15
data:{"result_code":0,"message":"success","server_time":1782701030388,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"g","food_info":[]}}

id:16
data:{"result_code":0,"message":"success","server_time":1782701030492,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"\n食物：随机小吃（现卷手作）","food_info":[]}}

id:17
data:{"result_code":0,"message":"success","server_time":1782701030588,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":", 30","food_info":[]}}

id:18
data:{"result_code":0,"message":"success","server_time":1782701030772,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":false,"content":"g","food_info":[]}}

id:19
data:{"result_code":0,"message":"success","server_time":1782701031273,"trace_id":"231391ae106a41db:231391ae106a41db:0:1","data":{"task_id":"9664b05f721c4b62ac03eb85232ad44c","end":true,"food_info":[{"code":"fd229dfc","name":"香芋地瓜丸","calories":"199","protein":4.08,"fat":3.77,"carbohydrate":37.45,"health_light":"2","is_liquid":false,"image_url":"https://f.boohee.cn/house/upload_food/2022/7/26/mid_photo_url_c02fc97cc0ed9bb6e3c9a31177dee63d.jpg","amount":45,"saturated_fat":0,"fiber":0,"ingredients":[{"key":"sugar","name":"糖","value":1.59,"unit":"g","unit_name":"克"},{"key":"purine","name":"嘌呤","value":8.76,"unit":"mg","unit_name":"毫克"},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0,"unit":"g","unit_name":"克"},{"key":"vitamin_a","name":"维生素A","value":20.32,"unit":"μg","unit_name":"微克"}],"nrv":[{"key":"sugar","name":"糖","value":0},{"key":"purine","name":"嘌呤","value":0},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0},{"key":"vitamin_a","name":"维生素A","value":0.03},{"key":"protein","name":"蛋白质","value":0.07},{"key":"fat","name":"脂肪","value":0.06},{"key":"carbohydrate","name":"碳水化合物","value":0.12},{"key":"calories","name":"热量","value":0.1}]},{"code":"xingbaogu","name":"盐酥杏鲍菇","calories":"35","protein":1.3,"fat":0.1,"carbohydrate":8.3,"health_light":"1","is_liquid":false,"image_url":"https://f.boohee.cn/house/upload_food/2022/1/18/slim_c9177f3d30604e7ea827bb1f8d34ddcb.jpg","amount":90,"saturated_fat":0,"fiber":0,"ingredients":[{"key":"sugar","name":"糖","value":2.86,"unit":"g","unit_name":"克"},{"key":"purine","name":"嘌呤","value":94,"unit":"mg","unit_name":"毫克"},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0,"unit":"g","unit_name":"克"},{"key":"vitamin_a","name":"维生素A","value":0,"unit":"μg","unit_name":"微克"}],"nrv":[{"key":"sugar","name":"糖","value":0},{"key":"purine","name":"嘌呤","value":0},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0},{"key":"vitamin_a","name":"维生素A","value":0},{"key":"protein","name":"蛋白质","value":0.02},{"key":"fat","name":"脂肪","value":0},{"key":"carbohydrate","name":"碳水化合物","value":0.03},{"key":"calories","name":"热量","value":0.02}]},{"code":"fd9d578a","name":"超值四拼炸鸡（含琥珀酱甜辣、西域孜然粉、蜂蜜芥末酱）","calories":"333","protein":0.67,"fat":26.67,"carbohydrate":26.67,"health_light":"3","is_liquid":false,"image_url":"https://f.boohee.cn/house/upload_food/2020/2/19/mid_photo_url_a53ec600178a224f99174a2c13ca753a.jpg","amount":200,"saturated_fat":0,"fiber":0,"ingredients":[{"key":"sugar","name":"糖","value":4,"unit":"g","unit_name":"克"},{"key":"purine","name":"嘌呤","value":0,"unit":"mg","unit_name":"毫克"},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0,"unit":"g","unit_name":"克"},{"key":"vitamin_a","name":"维生素A","value":0,"unit":"μg","unit_name":"微克"}],"nrv":[{"key":"sugar","name":"糖","value":0},{"key":"purine","name":"嘌呤","value":0},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0},{"key":"vitamin_a","name":"维生素A","value":0},{"key":"protein","name":"蛋白质","value":0.01},{"key":"fat","name":"脂肪","value":0.44},{"key":"carbohydrate","name":"碳水化合物","value":0.09},{"key":"calories","name":"热量","value":0.17}]},{"code":"fd96c553","name":"无骨鸡块（每单限1，放套餐里）","calories":"187","protein":17.3,"fat":6.92,"carbohydrate":13.92,"health_light":"2","is_liquid":false,"image_url":"https://f.boohee.cn/house/upload_food/2022/7/26/slim_mid_photo_url_a4fb1a719206560a622ed8fcd69c9dfe.jpg","amount":60,"saturated_fat":0,"fiber":0,"ingredients":[{"key":"sugar","name":"糖","value":0,"unit":"g","unit_name":"克"},{"key":"purine","name":"嘌呤","value":123.22,"unit":"mg","unit_name":"毫克"},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0,"unit":"g","unit_name":"克"},{"key":"vitamin_a","name":"维生素A","value":39.5,"unit":"μg","unit_name":"微克"}],"nrv":[{"key":"sugar","name":"糖","value":0},{"key":"purine","name":"嘌呤","value":0},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0},{"key":"vitamin_a","name":"维生素A","value":0.05},{"key":"protein","name":"蛋白质","value":0.29},{"key":"fat","name":"脂肪","value":0.12},{"key":"carbohydrate","name":"碳水化合物","value":0.05},{"key":"calories","name":"热量","value":0.09}]},{"code":"fdd68cfa","name":"随机小吃（现卷手作）","calories":"447","protein":10.1,"fat":25.02,"carbohydrate":43.91,"health_light":"2","is_liquid":false,"image_url":"https://f.boohee.cn/house/upload_food/2021/7/23/mid_photo_url_09.png","amount":30,"saturated_fat":0,"fiber":0,"ingredients":[{"key":"sugar","name":"糖","value":12.39,"unit":"g","unit_name":"克"},{"key":"purine","name":"嘌呤","value":0.58,"unit":"mg","unit_name":"毫克"},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0,"unit":"g","unit_name":"克"},{"key":"vitamin_a","name":"维生素A","value":31.49,"unit":"μg","unit_name":"微克"}],"nrv":[{"key":"sugar","name":"糖","value":0},{"key":"purine","name":"嘌呤","value":0},{"key":"fatty_acid","name":"反式脂肪(酸)","value":0},{"key":"vitamin_a","name":"维生素A","value":0.04},{"key":"protein","name":"蛋白质","value":0.17},{"key":"fat","name":"脂肪","value":0.42},{"key":"carbohydrate","name":"碳水化合物","value":0.15},{"key":"calories","name":"热量","value":0.22}]}]}}
```

