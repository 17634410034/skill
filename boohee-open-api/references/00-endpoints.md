# 接口总览速查

Base URL: `https://api.boohee.com/open-apis`（除 `/v1/access_token` 外，全部需要 `Authorization: Bearer {access_token}` 或 `X-Api-Key` 二选一）

详细参数/返回字段见同目录章节文件（按「详情」列查对应 `##` 小节）。

## 一、通用规范 → `01-general.md`

| Method | Path | 作用 | 详情 |
|---|---|---|---|
| POST | `/v1/access_token` | 用 app_id+timestamp+sign 换取 AccessToken（有效期默认 86400s） | 1.2 |
| — | Webhook 回调 | 平台主动 POST 推送 `smart_recipe` / `food_recognize` 事件；含 challenge 地址验证、HMAC-SHA256 验签 | 1.4 |
| — | SDK | Go/Python/Java/Node.js SDK，仓库 https://github.com/BOOHEEAI/sdk | 1.5 |

签名规则（1.3）：参数按 key 正序排序 → 拼成 `k1v1k2v2...` → 首尾各拼一次 appSecret（无分隔符）→ RSA-SHA256（私钥由平台对接方提供）→ 作为 `sign` 参数。

## 二、食物数据 → `02-food-data.md`

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| GET | `/v1/food/search` | 关键词/条码搜索食物，返回基础营养 | `keyword`(1-30字符) 或 `barcode`(13位)；`page`/`per_page`≤50/`sort`=calorie_asc\|calorie_desc/`with_units` | 2.1 |
| GET | `/v1/food/detail` | 食物详情（含 GI/GL、几十种营养成分、单位、食材构成） | `code`；`with_ingredients`/`with_units`/`with_materials` | 2.2 |
| GET | `/v1/food/categories` | 食物分类列表 | `kind`=group(默认)\|cooking | 2.3 |
| GET | `/v1/food/list` | 指定分类下食物列表 | `id`+`kind`（来自分类接口） | 2.4 |
| GET | `/v1/food/units` | 食物单位与估重图 | `code` | 2.5 |
| POST | `/v1/food/ingredients` | 按重量/份数批量算合计营养 | `foods[]`：`code`+`weight`(克) 或 `barcode`+`count` | 2.6 |
| GET | `/v1/food/ranks` | 按营养元素排行 | `ingredient`(中文名，如「蛋白质」)；`sort` 0升/1降；`tag` | 2.7 |

## 三、智能识别 → `03-recognition.md`

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v1/food/image_recognize` | 拍照识食物，返回异步 `task_id` | `image_url` 或 `image_data`(base64)；≤10MB，jpg/jpeg/jpe/png | 3.1 |
| GET | `/v1/food/image_recognize_detail` | 查识别任务结果（状态/食物/营养素/NRV） | `task_id`；`ingredients`(逗号分隔编码)；`with_nrv` | 3.2 |
| POST | `/v1/food/text_recognize` | 自然语言识别（"早上喝了一杯牛奶"）→ 按餐别返回食物 | `text` | 3.3 |
| POST | `/v1/food/image_recongize_stream` | 图片识别 SSE 流式输出（注意路径拼写 `recongize`） | 同 3.1 + `ingredients`/`with_nrv` | 3.4 |

识别状态码：1 解析中 / 2 已完成 / 3 未识别到食物 / 4 识别失败。
营养素编码子集（3.2、3.4 通用）：`gi gl sugar purine fiber_dietary saturated_fat ufa fatty_acid mufa pufa dha n6_fatty_acids n9_fatty_acids n3fa cholesterol vitamin_a/d/e/k thiamine lactoflavin vitamin_b6 vitamin_b12 niacin pantothenic choline biotin vitamin_c natrium kalium calcium phosphor magnesium chlorine iron zinc copper manganese chrome iodine selenium fluorine hg`。

## 四、智能食谱 → `04-recipe.md`（异步生成，配合 `smart_recipe` 回调）

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

## 五、体重记录 → `05-weight.md`（路径为 v2）

| Method | Path | 作用 | 关键入参 | 详情 |
|---|---|---|---|---|
| POST | `/v2/weight/record` | 记录体重 | `user_id`,`weight`(kg)；`body_fat`,`record_on` | 5.1 |
| GET | `/v2/weight/records` | 区间体重列表 | `user_id`,`start_date`,`end_date`；`page`,`page_size` | 5.2 |
| GET | `/v2/weight/latest` | 某日期前最新一条 | `user_id`；`record_on` 默认当天 | 5.3 |
| POST | `/v2/weight/delete` | 删除记录 | `user_id`,`id` | 5.4 |
| GET | `/v2/weight/line` | 体重/体脂曲线 | `user_id`；`chart_line_type`=weight\|body_fat,`start_date`,`end_date` | 5.5 |

## 六、饮食记录 → `06-diet.md`（路径为 v2）

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

## 公共约定

- **凭证**：除 `/v1/access_token` 外全部接口必须带 `X-Api-Key`（控制台 `https://ai.boohee.com/console/` →「API Key 管理」创建）或 `Authorization: Bearer {access_token}`。缺失时 HTTP 仍是 200，body 为 `{"code":1049,"message":"缺少认证凭证，请提供 AccessToken 或 X-Api-Key"}`。
- 统一响应外层：`{code, message, now, data}`，`code=0` 成功，非 0 失败。
- 食物字段通用含义：`calories`(kcal/100g)、`protein`/`fat`/`carbohydrate`(g/100g)、`health_light`(0无/1绿/2黄/3红)、`is_liquid`、`image_url`。
- `units` 元素：`unit_id`/`unit_name`/`weight`(该单位总重 g)/`eat_weight`(可食部 g)。
- 营养素对象：`{name, value, unit, unit_name, nrv}`，`nrv` 为小数（0.15 = 15%）。

## 官网文档自身的不一致（实测时以真实返回为准）

1. 域名混用：正文写 `https://api.boohee.com/open-apis`，但 1.2 / 3.4 / 4.2 / 4.3 / 4.6 的示例里出现 `https://api.iboohee.com/open-apis`。
2. 5.1 请求地址标 `POST /v2/weight/record`，示例 curl 却是 `/v1/weight/record`。
3. 4.3 地址 `/v1/recipe/replace_foods`，示例是 `/replace-foods`；4.6 地址 `/v1/recipe/mode_list`，示例是 `/mode-list`。
4. 3.4 流式接口路径官方就是 `image_recongize_stream`（recognize 拼写错误），照抄不要「修正」。
5. 1.1/1.2 认证描述与签名算法细节：`access_token` 走 RSA 签名，SDK 文档另有 Access Token 模式；X-Api-Key 直接在控制台创建。
