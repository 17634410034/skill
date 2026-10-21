# 接入操作细则（从 SKILL.md 迁出）

SKILL.md 只留「能做什么 + 怎么开始」。本篇是执行层细则：本地配置字段、认证与签名、请求发起方式、异步与 Webhook、排错、已知坑、文档自愈流程。**要真正发起调用或写代码前先读这里。**

## 目录

1. 本地配置 `config.json` 细则
2. 认证与签名
3. 发起请求
4. 异步任务与 Webhook
5. 排错表
6. 关键约束与坑
7. 凭证与个人数据安全
8. 文档漂移自检与自愈
9. 渐进式查阅顺序

---

## 1. 本地配置 `config.json` 细则

技能目录下 `config.json` 存放**用户自己的** API 凭证与身体/个人信息，`.gitignore` 已排除该文件，权限 `0600`。它让助手不必每轮都追着用户要 key 和 `user_id`。

**API Key 放在最显眼的位置**：`init` 生成的文件顶部就是第 1 步，`api_key` 独占一块、上面是「第 1 步（必填）」的 ★ 标题，与其他待填项分开；占位文案（或任何含中文的值）会被脚本识别为「还没填」，`show`/`get api_key`/`call` 都会明确提示，不会拿它去发请求。第 2 块是可选的 `profile`，进阶凭证（`app_id`/`app_secret`/RSA 私钥/Webhook）排在最后，用户不用 API Key 可以整块忽略。

### 读写规则（硬规则）

1. 要调接口前，**先读 `config.json`，再问用户**：
   ```bash
   python3 scripts/config.py show
   ```
   只有文件不存在、或所需字段为空时才向用户索取；拿到后按下面 `set` 写回，不要只记在对话里。
   `api_key` 若仍是占位文案或含中文，等同没填 —— 脚本已拦住，不要绕过它手工拼 curl 去发请求。
2. 一律通过 `scripts/config.py` 读写配置，**不要手写 JSON**（脚本校验字段名、保持 0600、原子写）。
3. 环境变量 `BOOHEE_API_KEY` / `BOOHEE_APP_ID` / `BOOHEE_APP_SECRET` 优先于文件；用户当场提供的值优先于任何存量，并且**必须回写进 `config.json`**（除非用户说"别存"）。
4. 所有请求走 `python3 scripts/config.py call <METHOD> <PATH> [--json '...']`：它自动挑 `api_key` 或 `access_token`，POST 时自动把非空 `profile` 字段合并进 body（用户显式传的同名字段覆盖 profile，`--no-merge-profile` 关闭合并）。
5. 展示配置永远用 `show`（密钥自动脱敏）；`get --secret` 取到的原值只能用于发起请求，**禁止**出现在回复、日志、代码或提交里。

### 命令

```bash
python3 scripts/config.py init                        # 生成 config.json（模板见 config.example.json）
python3 scripts/config.py show                        # 查看当前配置，密钥脱敏
python3 scripts/config.py set api_key 'sk-xxx'         # 存 API Key
python3 scripts/config.py set profile.user_id 'U1001'  # 存业务 user_id
python3 scripts/config.py set profile.gender 1         # 1男 2女
python3 scripts/config.py set profile.latest_weight 68.5   # 同时写 /v2/weight/record（--no-sync 只存本地）
python3 scripts/config.py set profile.diet_mode '["vegetarian","dashDiet"]'
python3 scripts/config.py unset api_key               # 清空
python3 scripts/config.py call GET '/v1/food/search?keyword=牛奶'   # 路径里的中文会自动转义
```

引导用户手动填写时，直接说位置：**打开 `config.json`，最上面 ★ 标题下的 `api_key` 那一行**，把占位文字换成 `sk-` 开头的完整密钥；其余区块不用动。

### 字段

| 路径 | 用途 |
|---|---|
| `api_key` | X-Api-Key 认证，控制台「API Key 管理」创建 |
| `app_id` / `app_secret` / `rsa_private_key_path` / `token.*` | Bearer Token 链路；`rsa_private_key_path` **只填私钥文件绝对路径**，私钥内容绝不入库、不进配置 |
| `base_url` | 默认生产域名，联调可改 |
| `webhook.app_key` / `webhook.url` | 回调验签与订阅登记 |
| `profile.user_id` | 写入类接口的业务用户 id，必填 |
| `profile.gender` / `latest_weight` / `energy` / `height` / `age` | 食谱生成必填项与记录类接口默认值 |
| `profile.diet_favor` / `diet_area` / `diet_mode` / `weight_management` / `nutrition_management` / `ban_foods` / `illness` | 食谱生成偏好；枚举照 `04-recipe.md` |
| `notes` | 自由备注（过敏、器械、目标等） |

### 自动记录（用户把信息告诉助手时）

用户口头给出凭证或个人信息时，主动落盘，不要等用户去编辑文件：

| 用户说了什么 | 写哪里 |
|---|---|
| 「key 是 sk-xxx」「用这个 app_id」 | `set api_key …` / `set app_id …` |
| 「我的 user_id / 薄荷 id 是 U1001」 | `set profile.user_id U1001` |
| 「我是女生 / 男生」 | `set profile.gender 2` / `1` |
| 「我体重 68.5kg」 | `set profile.latest_weight 68.5`（同步写体重记录接口；用户只让参考、不想留档时加 `--no-sync`） |
| 「我要减脂 / 控糖」 | `set profile.goal …`，并按 `04-recipe.md` 映射到 `weight_management` / `diet_mode` |
| 「我不吃香菜和虾」「我有糖尿病」 | `set profile.ban_foods '[…]'` / `set profile.illness '[…]'`（先查枚举编号，别猜） |
| 「每天目标热量 1500」「身高 165」 | `set profile.energy 1500` / `set profile.height 165` |

纪律：

- **写前先 `show`**：已有值与用户新口径冲突（旧体重、换了的 key）时，向用户确认再覆盖，不要静默改写。
- **只记用户明确提供的信息**，不要从识别结果或食谱内容反推身体状况写进 profile；推断值（如从照片推算体重）只能出现在回复里。
- **删除即清场**：用户说"别存我的数据"时，逐项 `unset` 或直接删除 `config.json`，并说明该文件只在本机。
- `config.json` 内容不进代码、不进提交、不在回复里完整回显；每次改配置告知用户改了哪个字段，写入类接口调用结果按接口返回原样说明。

---

## 2. 认证与签名

优先级：环境变量 > `config.json` > 向用户索取。**索取之前先执行 `python3 scripts/config.py show`**，配置里已有可用凭证就直接用；确认缺失才问，拿到后按第 1 节 `set` 回写。

`https://api.boohee.com/open-apis` 下除 `/v1/access_token` 外的**所有接口都必须带凭证**，否则返回 HTTP 200 但 `{"code":1049,"message":"缺少认证凭证，请提供 AccessToken 或 X-Api-Key"}`。凭证有两种，任选其一放到请求头：

### 方式一：X-Api-Key（默认推荐，一步到位）

1. 浏览器打开控制台 `https://ai.boohee.com/console/`，用开放平台账号登录（没有账号可在控制台注册；需要开通应用时联系平台对接方）。
2. 进入「API Key 管理」，创建一个 API Key，值形如 `sk-` + 十六进制串。
3. 每次请求带一个头即可：

```bash
python3 scripts/config.py call GET '/v1/food/search?keyword=牛奶'
# 等价于：
curl 'https://api.boohee.com/open-apis/v1/food/search?keyword=%E7%89%9B%E5%A5%B6' \
  -H 'X-Api-Key: sk-你的key' -H 'Accept: */*'
```

### 方式二：Bearer Token（需要 RSA 私钥，仅长期服务端调用才值得）

前置：平台分配给你的 `app_id`、`app_secret`，以及**由平台方提供的 RSA 私钥**（签名要用它，需要从控制台下载）。

1. 组装 `{app_id, timestamp}`，`timestamp` 为秒级时间戳，与服务器时差 **不超过 60 秒**。
2. 按 `01-general.md` 1.3 生成 `sign`：参数按 key 正序 → 拼成 `app_idbooheetimestamp1470042310` → 首尾各拼一次 `app_secret`（无分隔符）→ 用 RSA 私钥做 RSA-SHA256 → base64 结果即 `sign`。
3. `POST /v1/access_token`，Body JSON 传 `app_id` / `timestamp` / `sign`，拿回 `data.access_token` 与 `expires_in`（默认 86400 秒）。
4. 后续请求带 `-H 'Authorization: Bearer {access_token}'`；过期后重新走 1-3。

### 没有凭证时怎么办（硬规则）

- **先查本地配置**：`python3 scripts/config.py show`；已有 `api_key` 或未过期 `token.access_token` 就直接用。
- 配置里确实没有时**停下来向用户要**：说明缺 `X-Api-Key`（或 `app_id` + `app_secret` + RSA 私钥），并给出上面的获取路径；拿到后 `set` 进 `config.json`，别只留在对话里。
- **严禁**拿模型记忆里的通用成分表、其他食物库数据顶替开放平台接口返回值交付给用户。
- 用户明确表示拿不到凭证、仍要求给参考值时，必须在结果开头标注「以下为通用营养参考值，非薄荷食物库返回，`food_code` 不存在、不可用于写入类接口」，且不得编造看起来合法的 `food_code`。

---

## 3. 发起请求

1. **确认凭证已就绪**（见第 1、2 节）：`python3 scripts/config.py show` 取本地配置，选一种认证方式，全程统一；请求统一用 `config.py call` 发起。
2. **定位接口**：用 `00-endpoints.md` 的速查表匹配能力，不要自造路径。注意版本前缀：食物/识别/食谱是 `v1`，体重/饮食记录是 `v2`。

## 4. 异步任务与 Webhook

1. **异步能力走「提交 → 回调/轮询 → 取详情」**：
   - 图片识别：`POST /v1/food/image_recognize` 拿 `task_id` → 轮询 `GET /v1/food/image_recognize_detail`，或订阅 `food_recognize` Webhook。
   - 智能食谱：`POST /v1/recipe/generate` 拿 `task_id` → 订阅 `smart_recipe` Webhook → 用 `user_id` + 请求时传的 `date` 调 `GET /v1/recipe/details`。
   - 需要边生成边展示时改用流式接口 `POST /v1/food/image_recongize_stream`（SSE，`end=true` 的那帧才带完整 `food_info`）。
2. **实现 Webhook 时严格照 `01-general.md` 1.4**：1 秒内返回 200；用 `app_key` 对 `{timestamp}.{event}.{raw_body}` 做 HMAC-SHA256 验签（raw body 不可反序列化后重新序列化）；地址验证需返回 `HMAC-SHA256(app_key, challenge)` 的 hex；回调只给状态，数据仍要回查详情接口；IP 不固定，禁止用 IP 白名单。

## 5. 排错表

| 现象 | 原因与处理 |
|---|---|
| `code:1049` 缺少认证凭证 | 请求头没带 `X-Api-Key` 也没带 `Authorization`；补凭证。别当成接口故障 |
| `code:0` 但 `data` 为空 | 多为 `keyword` 超 30 字符、`food_code` 不存在、`barcode` 非 13 位；先按速查表核对入参 |
| `access_token` 换取失败 | `timestamp` 与服务器差超 60 秒，或 `sign` 拼接顺序/RSA 私钥/appSecret 用错（对照 1.3 逐步验证） |
| 识别/食谱任务一直不出结果 | 这两个是异步接口，只返回 `task_id`；必须轮询详情接口或接好 Webhook |
| HTTP 5xx | 平台侧问题，重试；不要改路径去"绕" |
| 参数/字段/枚举与 `references/` 快照对不上 | 先怀疑文档过期，走第 8 节，不要直接断言接口故障 |

## 6. 关键约束与坑

- 枚举值必须查原文：`meal_type`/`time_type`（1早餐 2中餐 3晚餐 4加餐 6/7/8 加餐）、`health_light`（0无 1绿 2黄 3红）、`gender`、`ban_foods` 1-14、`illness` 1-6、`diet_mode` 字符串集合等，都在各章表格里，别猜。
- 营养数据口径是「每 100g」，实际摄入要按 `amount`/`weight` 折算；`nrv` 是小数（0.15 = 15%）。
- 搜索用 `keyword` 或 `barcode`；写饮食记录只接受食物库的 `food_code`（`foods` 备注「仅支持食物库食物」）。
- 食谱详情的 `food_id` 官方标注「不再返回，请使用 `food_code`」，新代码一律用 `food_code`。
- 流式识别路径官方拼写就是 `image_recongize_stream`（拼错），照抄，不要"修正"成 recognize。
- 官网文档存在自相矛盾处（示例域名 `api.iboohee.com`、5.1 的 v1/v2、4.3/4.6 的下划线与连字符），已在 `00-endpoints.md` 末尾列出；联调时以真实返回为准，不要据此推断接口不存在。
- 未文档化的字段/接口一律先向用户确认，不要虚构。

## 7. 凭证与个人数据安全

`app_secret`、`app_key`、`X-Api-Key`、`access_token` 只从环境变量、`config.json` 或用户当场提供处取，不写入代码、不提交仓库、不在日志/回复中回显完整值。

`config.json` 是本机私有文件（0600、已 gitignore）：只放用户自己的凭证与档案，RSA 私钥只存路径不存内容；不要把别人的凭证写进示例、不要把 `config.json` 打包上传技能；演示命令里的 key 一律用占位值。

## 8. 文档漂移自检与自愈

官方文档随时会改，`references/` 是某一时刻的快照。**当你按文档调用接口却对不上时，第一反应应是怀疑文档过期，而不是断言接口坏了或擅自编造参数。**

### 触发信号（出现任一即启动下面的流程）

- 路径 404 / 方法不允许，而文档写的是别的方法或版本
- 返回了文档里没有的字段，或文档声明存在的字段不再返回
- 必填参数被拒、枚举值报非法（如 `meal_type`、`diet_mode`、`ban_foods` 取值与文档不符）
- `code` 非 0 且 `message` 与第 5 节排错表的成因都对不上
- 域名、认证头、Webhook 事件类型与文档描述冲突
- 官网「已知文档问题」清单里某条已经不复现

### 三步流程

**第 1 步：实时核对单篇（不写文件，先确认事实）**

```bash
python3 scripts/fetch_docs.py --doc <文档编号> --truncate 20000
```

文档编号就是各章每篇标题下 `> 文档编号: \`dcbf0f02\`` 那个值。它拉的是官网当前原文，直接和 `references/` 里的旧文本对照，能立刻判断是"你记错了"还是"文档真改了"。

**第 2 步：全量差异检查（只读，不改文件）**

```bash
python3 scripts/fetch_docs.py            # 人读摘要
python3 scripts/fetch_docs.py --json     # 需要程序化处理时
```

退出码：`0` 一致 / `2` 有漂移 / `1` 出错。报告会逐篇列出「内容已变动 / 本地缺失 / 仅时间戳变动 / 官网已删除」，并给出行数增减与新旧更新时间。

**第 3 步：应用更新**

```bash
python3 scripts/fetch_docs.py --apply
```

只重写 `references/01~06`（逐字导出，幂等，不会产生虚假 diff）。新出现的章节会落成 `<章名>.new.md` 并提示人工确认，不会自动接管。

### 更新后必须做的复核（不可省略）

1. `references/00-endpoints.md`、`SKILL.md` 和本篇是**人工整理的索引**，脚本不会改。逐条核对受影响的接口路径、方法、参数、枚举是否还在。
2. 重读「已知文档问题」清单：官方可能已修掉某条，别继续把已修复的当坑告诉用户；也可能新增了矛盾。
3. 用 `git diff` 把变更交给用户过目，**由用户决定是否提交**。不要静默改完就走。
4. 若变动影响的是你正在实现的功能，改完要用真实调用验证一次，而不是只看文档对齐就收工。

### 边界纪律

- 允许自动执行第 1、2 步（只读）。第 3 步写文件前，若你处在只读环境或用户未授权改动仓库，先说明再动手。
- **禁止**为了让接口"看起来能用"而删除文档里的约束、改写枚举、或把 `references/` 改成迎合当前实现的样子。事实以官网为准。
- 拉取失败（无外网、接口下线）时，明确告诉用户"无法核对官网，当前依据是 `references/` 的快照，快照时间见各篇更新时间"，不要假装已验证。
- 核对范围只限本 skill 覆盖的「薄荷科学.AI」手册（`scripts/fetch_docs.py` 默认 `code=boohee.ai`）。文档站还挂了其他项目的手册，其中含客户定制与内部资料，**不要**在 skill、回复或代码里列举它们的名字、code 或目录接口。

## 9. 渐进式查阅顺序

1. **先读 `00-endpoints.md`** — 全部接口的方法、路径、作用、关键入参速查表，用于定位该用哪个接口。
2. **再按需读对应章节原文** — 需要参数表、返回结构、示例时才打开：

| 需求 | 文件 |
|---|---|
| 域名/认证/响应规范、获取 AccessToken、RSA 签名算法、Webhook 回调、SDK | `01-general.md` |
| 食物搜索、详情、分类、分类列表、单位估重、批量营养计算、营养排行 | `02-food-data.md` |
| 图片识别（异步/流式 SSE）、识别详情、自然语言转食物 | `03-recognition.md` |
| 生成智能食谱、食谱详情、换一换、替换单菜/整餐、饮食模式列表与详情、食谱概要 | `04-recipe.md` |
| 体重记录增删查、最新体重、体重/体脂曲线 | `05-weight.md` |
| 饮食记录批量/单条写入、删除、修改、按天查询、当日最新 | `06-diet.md` |
| 本地配置细则、认证签名、异步/Webhook、排错、已知坑、文档自愈 | `07-integration-ops.md`（本篇） |

每章文件是官网文档的逐字导出（含 `> 文档编号 / 更新时间`），可直接引用其中的表格与 curl 示例。

3. **涉及用户本人时读 `config.json`** — 凭证、`user_id`、体重、忌口等存量信息见第 1 节，别反复问用户要。
