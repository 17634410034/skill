# 接口总览速查

Base URL: `https://api.boohee.com/open-apis`（全部业务接口都需要请求头 `X-Api-Key`）

详细参数/返回字段见同目录章节文件（按「详情」列查对应 `##` 小节）。

## 食物数据 → `02-food-data.md`

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| GET | `/v1/food/search` | 关键词/条码搜索食物，返回基础营养 | `keyword`(1-30字符) 或 `barcode`(13位)；`page`/`per_page`≤50/`sort`=calorie_asc\|calorie_desc/`with_units`(默认加) | 2.1 |
| GET | `/v1/food/detail` | 食物详情（含 GI/GL、几十种营养成分、单位、食材构成） | `code`；`with_ingredients`/`with_units`/`with_materials`（三个默认都开） | 2.2 |
| GET | `/v1/food/categories` | 食物分类列表 | `kind`=group(默认)\|cooking | 2.3 |
| GET | `/v1/food/list` | 指定分类下食物列表 | `id`+`kind`（来自分类接口）；`with_units=true`(默认加) | 2.4 |
| GET | `/v1/food/units` | 食物单位与估重图 | `code` | 2.5 |
| POST | `/v1/food/ingredients` | 按重量/份数批量算合计营养 | `foods[]`：`code`+`weight`(克) 或 `barcode`+`count` | 2.6 |
| GET | `/v1/food/ranks` | 按营养元素排行 | `ingredient`(中文名，如「蛋白质」)；`sort` 0升/1降；`tag` | 2.7 |

## 智能识别 → `03-recognition.md`

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v1/food/image_recognize` | 拍照识食物，返回异步 `task_id` | `image_url` 或 `image_data`(base64)；≤10MB，jpg/jpeg/jpe/png | 3.1 |
| GET | `/v1/food/image_recognize_detail` | 查识别任务结果（状态/食物/营养素/NRV） | `task_id`；`ingredients`（全量编码，默认加）；`with_nrv=true`(默认加) | 3.2 |
| POST | `/v1/food/text_recognize` | 自然语言识别（"早上喝了一杯牛奶"）→ 按餐别返回食物 | `text` | 3.3 |

识别状态码：1 解析中 / 2 已完成 / 3 未识别到食物 / 4 识别失败。
营养素编码子集（3.2 通用）：`gi gl sugar purine fiber_dietary saturated_fat ufa fatty_acid mufa pufa dha n6_fatty_acids n9_fatty_acids n3fa cholesterol vitamin_a/d/e/k thiamine lactoflavin vitamin_b6 vitamin_b12 niacin pantothenic choline biotin vitamin_c natrium kalium calcium phosphor magnesium chlorine iron zinc copper manganese chrome iodine selenium fluorine hg`。

## 智能食谱 → `04-recipe.md`（异步生成，提交后按 user_id + date 取详情）

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v1/recipe/generate` | 生成个性化食谱，返回 `task_id` | `user_id`,`date`,`gender`(1男2女),`latest_weight`,`energy` 必填；可选 `diet_favor`/`diet_area`/`weight_management`/`nutrition_management`/`ban_foods`/`illness`/`diet_mode`/`diet_mode_opt` | 4.1 |
| GET | `/v1/recipe/details` | 按日期取整周食谱（餐别→食物→扩展单位） | `user_id`,`date` | 4.2 |
| GET | `/v1/recipe/replace_foods` | 「换一换」候选菜肴 | `user_id`,`date`,`time_type`,`food_id` | 4.3 |
| POST | `/v1/recipe/replace_food` | 替换单道菜 | `user_id`,`date`,`time_type`,`original_id`,`target_id` | 4.4 |
| POST | `/v1/recipe/replace_meal` | 替换整餐 | `user_id`,`date`,`time_type`,`un_replace_ids` | 4.5 |
| GET | `/v1/recipe/mode_list` | 饮食模式列表 | 无 | 4.6 |
| GET | `/v1/recipe/mode_detail` | 模式详情（介绍/禁忌人群/FAQ/推荐食谱） | `code`,`energy` | 4.7 |
| GET | `/v1/recipe/summary` | 食谱概要 | `user_id`,`date`,`type`=1(概述) | 4.8 |

`diet_mode` 取值：`type2Diabetes crd carbCycling fasting1608 mediumHighProtein fasting vegetarian mediterranean dashDiet`。
`time_type`：1 早餐 / 2 中餐 / 3 晚餐 / 6 早加餐 / 7 午加餐 / 8 晚加餐。

## 体重记录 → `05-weight.md`（路径为 v2）

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v2/weight/record` | 记录体重 | `user_id`,`weight`(kg)；`body_fat`,`record_on` | 5.1 |
| GET | `/v2/weight/records` | 区间体重列表 | `user_id`,`start_date`,`end_date`；`page`,`page_size` | 5.2 |
| GET | `/v2/weight/latest` | 某日期前最新一条 | `user_id`；`record_on` 默认当天 | 5.3 |
| POST | `/v2/weight/delete` | 删除记录 | `user_id`,`id` | 5.4 |
| GET | `/v2/weight/line` | 体重/体脂曲线 | `user_id`；`chart_line_type`=weight\|body_fat,`start_date`,`end_date` | 5.5 |

## 饮食记录 → `06-diet.md`（路径为 v2）

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v2/eating/record` | 批量记录一餐 | `user_id`,`record_on`,`meal_type`,`foods[]`(`food_code`,`amount`,`unit_name`) | 6.1 |
| POST | `/v2/eating/record_single` | 记录单个食物 | `user_id`,`record_on`,`meal_type`,`food_code`,`amount`,`unit_name` | 6.2 |
| POST | `/v2/eating/delete` | 删除饮食记录 | `user_id`,`record_on`,`meal_type`,`food_code` | 6.3 |
| GET | `/v2/eating/records` | 查某天全部记录 | `user_id`,`record_on` | 6.4 |
| POST | `/v2/eating/update` | 改记录（量/餐别/餐时间/热量） | `id` 必填，其余按需 | 6.5 |
| GET | `/v2/eating/latest` | 截止当日最新记录 | `user_id` | 6.6 |

`meal_type`：1 早餐 / 2 中餐 / 3 晚餐 / 4 加餐 / 6 上午加餐 / 7 下午加餐 / 8 晚上加餐。
写入类接口（6.1–6.5）返回的 `daily` 结构一致：按 `meals[]` 分组 + 每餐与全日 `total_calories/total_protein/total_fat/total_carbohydrate`。

## 完整取数参数（默认加满）

官网把补充字段做成默认关闭的开关，不传就静默省略。本技能默认全部打开，除非用户明确只要摘要：

| 接口 | 追加参数 | 带回内容 |
|---|---|---|
| GET `/v1/food/detail` | `with_ingredients=true&with_units=true&with_materials=true` | `ingredients` 完整营养项、`units` 所有扩展单位（如 1 碗多少克）、`materials` 菜肴全部食材与做法 |
| GET `/v1/food/search` | `with_units=true` | 每个食物的扩展单位与估重，最热门单位排第一 |
| GET `/v1/food/list` | `with_units=true` | 同上 |
| GET `/v1/food/image_recognize_detail` | `with_nrv=true&ingredients=<全量编码>` | 指定营养素 + 热量/蛋白/脂肪/碳水及这些营养素的 NRV |

现成命令：

```bash
python3 <技能目录>/scripts/config.py call GET '/v1/food/detail?code=10001&with_ingredients=true&with_units=true&with_materials=true'
python3 <技能目录>/scripts/config.py call GET '/v1/food/search?keyword=牛奶&with_units=true'
python3 <技能目录>/scripts/config.py call GET '/v1/food/list?id=1&kind=group&with_units=true'
python3 <技能目录>/scripts/config.py call GET '/v1/food/image_recognize_detail?task_id=<task_id>&with_nrv=true&ingredients=gi,gl,sugar,purine,fiber_dietary,saturated_fat,ufa,fatty_acid,mufa,pufa,dha,n6_fatty_acids,n9_fatty_acids,n3fa,cholesterol,vitamin_a,vitamin_d,vitamin_e,vitamin_k,thiamine,lactoflavin,vitamin_b6,vitamin_b12,niacin,pantothenic,choline,biotin,vitamin_c,natrium,kalium,calcium,phosphor,magnesium,chlorine,iron,zinc,copper,manganese,chrome,iodine,selenium,fluorine,hg'
```

识别详情全量营养素编码（43 个，复制即用）：
`gi gl sugar purine fiber_dietary saturated_fat ufa fatty_acid mufa pufa dha n6_fatty_acids n9_fatty_acids n3fa cholesterol vitamin_a vitamin_d vitamin_e vitamin_k thiamine lactoflavin vitamin_b6 vitamin_b12 niacin pantothenic choline biotin vitamin_c natrium kalium calcium phosphor magnesium chlorine iron zinc copper manganese chrome iodine selenium fluorine hg`

## 公共约定

- **凭证**：全部业务接口必须带 `X-Api-Key`（控制台 `https://ai.boohee.com/console/` →「API Key 管理」创建）。缺失时 HTTP 仍是 200，body 为 `{"code":1049,"message":"缺少认证凭证..."}`。
- 统一响应外层：`{code, message, now, data}`，`code=0` 成功，非 0 失败。
- 食物字段通用含义：`calories`(kcal/100g)、`protein`/`fat`/`carbohydrate`(g/100g)、`health_light`(0无/1绿/2黄/3红)、`is_liquid`、`image_url`。
- 食物详情额外字段：`food_type`（食材/菜肴/包装食品）、`food_weight_url`（估重图）、`gi`/`gl`（含 `level`：0低/1中/2高/-1无数据）、`materials`（仅菜肴返回；`foods[]` 每项含 `type`=major 主要/minor 次要/seasoning 调味料、`weight`、`desc`；顶层 `description` 为做法）。
- `units` 元素：`unit_id`/`unit_name`/`weight`(该单位总重 g)/`eat_weight`(可食部 g)。
- `ingredients` 元素：`key`/`type`（carbohydrate、protein、fat、vitamins、minerals、amino_acid、other）/`name`/`value`/`unit`/`unit_name`/`nrv`。
- 营养素对象：`{name, value, unit, unit_name, nrv}`，`nrv` 为小数（0.15 = 15%）；氨基酸的 `nrv` 通常为 `null`。

## 官网文档自身的不一致（实测时以真实返回为准）

1. 域名混用：正文写 `https://api.boohee.com/open-apis`，但部分接口示例里出现 `https://api.iboohee.com/open-apis`。
2. 5.1 请求地址标 `POST /v2/weight/record`，示例却是 `/v1/weight/record`。
3. 4.3 地址 `/v1/recipe/replace_foods`，示例是 `/replace-foods`；4.6 地址 `/v1/recipe/mode_list`，示例是 `/mode-list`。
