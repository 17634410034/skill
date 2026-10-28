# 运行时操作细则

SKILL.md 承担「三步执行流程 + 能力路由」。本篇是第 2 步（选接口并请求）的执行层细则：本地配置、请求头、发起请求、异步轮询、响应与错误码、已知坑、文档自愈。**要真正发起调用前先读这里。**

> 下文 `<技能目录>` 一律指 SKILL.md 所在目录的**绝对路径**。技能目录不是当前工作目录，照抄相对路径会 `No such file or directory`。

## 目录

1. 本地配置 `config.json` 细则
2. API Key 与请求头
3. 发起请求
4. 异步任务轮询
5. 响应与错误码
6. 关键约束与坑
7. 凭证与个人数据安全
8. 文档漂移自检与自愈
9. 渐进式查阅顺序

---

## 1. 本地配置 `config.json` 细则

`config.json` 存放**用户自己的** API Key 与身体/个人信息，只留在本机、不随技能包分发，权限 `0600`。它让助手不必每轮都追着用户要 key 和 `user_id`。

落点：默认在技能目录；技能目录不可写（只读安装、容器只读挂载）时自动改用 `~/.boohee-open-api/config.json`。旧位置的 `config.json` 仍会被读取，下次写入时迁移到当前可写位置。**实际路径以 `check` / `show` / `init` 打印的为准**，不要自己拼。

**API Key 放在最显眼的位置**：`init` 生成的文件顶部就是第 1 步，`api_key` 独占一块、上面是「第 1 步（必填）」的 ★ 标题。占位文案（或任何含中文的值）会被脚本识别为「还没填」，`check` / `show` / `get api_key` / `call` 都会明确提示，不会拿它去发请求。第 2 块是可选的 `profile`。

### 读写规则（硬规则）

1. 取数或写数据前，**先跑凭证门禁**：
   ```bash
   python3 <技能目录>/scripts/config.py check
   ```
   首行 `KEY_OK`（退出码 0）表示可用；`NO_KEY`（退出码 1）时**停下向用户索取 API Key**，不发请求、不用示例数据顶替。凭证就绪后再看其余字段：
   ```bash
   python3 <技能目录>/scripts/config.py show
   ```
   文件不存在时先 `python3 <技能目录>/scripts/config.py init` 生成模板，再引导用户填或请用户直接给值。
   只有所需字段为空时才向用户索取；拿到后按下面 `set` 写回，不要只记在对话里。
2. 一律通过 `<技能目录>/scripts/config.py` 读写配置，**不要手写 JSON**（脚本校验字段名、保持 0600、原子写）。
3. 环境变量 `BOOHEE_API_KEY` 优先于文件；用户当场提供的值优先于任何存量，并且**必须回写进 `config.json`**（除非用户说"别存"）。
4. 所有请求走 `python3 <技能目录>/scripts/config.py call <METHOD> <PATH> [--json '...']`：它自动带上 `X-Api-Key`，POST 时自动把非空 `profile` 字段合并进 body（用户显式传的同名字段覆盖 profile，`--no-merge-profile` 关闭合并）。
5. 展示配置永远用 `show`（密钥自动脱敏）；`get --secret` 取到的原值只能用于发起请求，**禁止**出现在回复、日志、代码或提交里。

### 命令

```bash
python3 <技能目录>/scripts/config.py init                        # 生成 config.json（模板见 config.example.json）
python3 <技能目录>/scripts/config.py check                       # 凭证门禁：KEY_OK / NO_KEY（退出码 0/1）
python3 <技能目录>/scripts/config.py show                        # 查看当前配置，密钥脱敏
python3 <技能目录>/scripts/config.py set api_key 'sk-xxx'         # 存 API Key
python3 <技能目录>/scripts/config.py set profile.user_id 'U1001'  # 存业务 user_id
python3 <技能目录>/scripts/config.py set profile.gender 1         # 1男 2女
python3 <技能目录>/scripts/config.py set profile.latest_weight 68.5   # 同时写 /v2/weight/record（--no-sync 只存本地）
python3 <技能目录>/scripts/config.py set profile.diet_mode '["vegetarian","dashDiet"]'
python3 <技能目录>/scripts/config.py unset api_key               # 清空
python3 <技能目录>/scripts/config.py call GET '/v1/food/search?keyword=牛奶'   # 路径里的中文会自动转义
```

引导用户手动填写时，直接说位置：**打开 `show` 第一行给出的那个 `config.json`，最上面 ★ 标题下的 `api_key` 那一行**，把占位文字换成 `sk-` 开头的完整密钥；其余区块不用动。

### 字段

| 路径 | 用途 |
|---|---|
| `api_key` | 唯一凭证，请求头 `X-Api-Key`；控制台「API Key 管理」创建 |
| `profile.user_id` | 写入类接口的业务用户 id，必填 |
| `profile.gender` / `latest_weight` / `energy` / `height` / `age` | 食谱生成必填项与记录类接口默认值 |
| `profile.diet_favor` / `diet_area` / `diet_mode` / `weight_management` / `nutrition_management` / `ban_foods` / `illness` | 食谱生成偏好；枚举照 `04-recipe.md` |
| `profile.goal` | 用户的减脂/增肌等目标描述，用于映射 `weight_management` / `diet_mode` |

旧版本配置里的进阶凭证字段会在读取时自动丢弃，不需要手工清理。

### 自动记录（用户把信息告诉助手时）

用户口头给出凭证或个人信息时，主动落盘，不要等用户去编辑文件：

| 用户说了什么 | 写哪里 |
|---|---|
| 「key 是 sk-xxx」 | `set api_key …` |
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

## 2. API Key 与请求头

- 获取：控制台 `https://ai.boohee.com/console/` → 登录或注册 → 左侧「API Key 管理」→ 创建 → 复制 `sk-` 开头的完整密钥。
- 请求头：`X-Api-Key: <key>`。**所有业务接口只认这一种凭证**；`config.py call` 会自动带上，不要手工拼请求。
- 缺失或无效时 HTTP 仍是 200，body 为 `{"code":1049,"message":"缺少认证凭证..."}`。看到 1049 就是没带 key 或 key 不可用，不是接口故障。
- 环境变量 `BOOHEE_API_KEY` 优先于 `config.json`，适合 CI 或临时试用。

## 3. 发起请求

1. **确认凭证已就绪**：先 `python3 <技能目录>/scripts/config.py check`，`KEY_OK` 才继续；再用 `show` 查看 `user_id` 等字段。
2. **定位接口**：用 `00-endpoints.md` 的速查表匹配能力，不要自造路径。版本前缀：食物 / 识别 / 食谱是 `v1`，体重 / 饮食记录是 `v2`。
3. **带业务身份**：食谱、体重、饮食接口必须传 `user_id`，默认取 `profile.user_id`；为空时先问用户。
4. **两段式查询**：`/v1/food/search` 拿 `food_code` 后再查 `/v1/food/detail`；分类先 `/v1/food/categories` 拿 `id` 和 `kind`，再查 `/v1/food/list`。
5. **图片输入**：`image_url` 或 `image_data`（base64），≤10MB，jpg/jpeg/jpe/png。
6. **分页**：`search` 的 `per_page` 最大 50，返回带 `has_more`；体重与曲线接口用 `page` / `page_size`，返回带 `total` / `has_more`。用户要全量时按需翻页，并在回答里说明范围。

## 4. 异步任务轮询

1. **图片识别**：`POST /v1/food/image_recognize` 只返回 `task_id`；随后轮询 `GET /v1/food/image_recognize_detail?task_id=…`。
   - `status=1` 解析中 → 继续轮询；`status=2` 已完成；`status=3` 未识别到食物；`status=4` 识别失败。
   - 拿到结果后，营养值是**每 100g**，要按识别出的 `amount` 折算成实际摄入。
2. **智能食谱**：`POST /v1/recipe/generate` 只返回 `task_id`，没有轮询接口；生成需要时间，稍后用 `GET /v1/recipe/details?user_id=&date=` 取结果。长时间为空就告诉用户稍后再查，不要反复空转。
3. **自然语言识别**：`POST /v1/food/text_recognize` 同步返回，不需要轮询。
4. 任务未到终态时**不要**把中间状态当成最终结果交付；回答里说明「仍在处理中」。

## 5. 响应与错误码

统一响应外层：`{"code": 0, "message": "...", "now": 时间戳, "data": {...}}`。`code=0` 成功，非 0 失败；失败时以 `message` 为准向用户说明，不猜。

| 现象 | 原因与处理 |
|---|---|
| `code:1049` 缺少认证凭证 | 请求头没带 `X-Api-Key`，或 key 是占位/含中文。先跑 `check` |
| `code:0` 但 `data` 为空 | 多为 `keyword` 超 30 字符、`food_code` 不存在、`barcode` 非 13 位；按速查表核对入参 |
| 识别/食谱任务一直没结果 | 异步接口只返回 `task_id`，必须轮询详情或稍后重查；不是接口坏了 |
| HTTP 5xx | 平台侧问题，重试；不要改路径去"绕" |
| 参数/字段/枚举与 `references/` 快照对不上 | 先怀疑文档过期，走「文档漂移自检与自愈」，不要直接断言接口故障 |

## 6. 关键约束与坑

- 枚举值必须查原文：`meal_type`/`time_type`（1早餐 2中餐 3晚餐 4加餐 6/7/8 加餐）、`health_light`（0无 1绿 2黄 3红）、`gender`、`ban_foods` 1-14、`illness` 1-6、`diet_mode` 字符串集合等，都在各章表格里，别猜。
- 营养数据口径是「每 100g」，实际摄入要按 `amount`/`weight` 折算；`nrv` 是小数（0.15 = 15%）。
- 搜索用 `keyword` 或 `barcode`；写饮食记录只接受食物库的 `food_code`（`foods` 备注「仅支持食物库食物」）。
- 食谱详情的 `food_id` 官方标注「不再返回，请使用 `food_code`」，一律用 `food_code`。
- 官网文档存在自相矛盾处（示例域名 `api.iboohee.com`、5.1 的 v1/v2、4.3/4.6 的下划线与连字符），已在 `00-endpoints.md` 末尾列出；以真实返回为准，不要据此推断接口不存在。
- 未文档化的字段/接口一律先向用户确认，不要虚构。

## 7. 凭证与个人数据安全

`X-Api-Key` 只从环境变量、`config.json` 或用户当场提供处取，不写入代码、不提交仓库、不在日志/回复中回显完整值。

`config.json` 是本机私有文件（0600，不随技能包分发）：只放用户自己的 key 与档案；不要把别人的 key 写进示例、不要把 `config.json` 打包上传技能；演示命令里的 key 一律用占位值。

## 8. 文档漂移自检与自愈

官方文档随时会改，`references/` 是某一时刻的快照。**当你按文档调用接口却对不上时，第一反应应是怀疑文档过期，而不是断言接口坏了或擅自编造参数。**

### 触发信号（出现任一即启动下面的流程）

- 路径 404 / 方法不允许，而文档写的是别的方法或版本
- 返回了文档里没有的字段，或文档声明存在的字段不再返回
- 必填参数被拒、枚举值报非法（如 `meal_type`、`diet_mode`、`ban_foods` 取值与文档不符）
- `code` 非 0 且 `message` 与排错表的成因都对不上
- 官网「已知文档问题」清单里某条已经不复现

### 三步流程

**第 1 步：实时核对单篇（不写文件，先确认事实）**

```bash
python3 <技能目录>/scripts/fetch_docs.py --doc <文档编号> --truncate 20000
```

文档编号就是各章每篇标题下 `> 文档编号: \`dcbf0f02\`` 那个值。它拉的是官网当前原文，直接和 `references/` 里的旧文本对照，能立刻判断是"你记错了"还是"文档真改了"。

**第 2 步：全量差异检查（只读，不改文件）**

```bash
python3 <技能目录>/scripts/fetch_docs.py            # 人读摘要
python3 <技能目录>/scripts/fetch_docs.py --json     # 需要程序化处理时
```

退出码：`0` 一致 / `2` 有漂移 / `1` 出错。报告会逐篇列出「内容已变动 / 本地缺失 / 仅时间戳变动 / 官网已删除」，并给出行数增减与新旧更新时间。

**第 3 步：应用更新**

```bash
python3 <技能目录>/scripts/fetch_docs.py --apply
```

只重写 `references/02~06` 业务文档（逐字导出，幂等，不会产生虚假 diff）。本技能只同步这五篇业务文档，其他章节不纳入；`00-endpoints.md`、`SKILL.md` 和本篇是人工整理的索引，脚本不会改。

### 更新后必须做的复核（不可省略）

1. `references/00-endpoints.md`、`SKILL.md` 和本篇是**人工整理的索引**，逐条核对受影响的接口路径、方法、参数、枚举是否还在。
2. 重读「已知文档问题」清单：官方可能已修掉某条，别继续把已修复的当坑告诉用户；也可能新增了矛盾。
3. 把变更前后对照列给用户过目，**由用户决定是否保留**。不要静默改完就走。
4. 若变动影响的是你正在实现的功能，改完要用真实调用验证一次，而不是只看文档对齐就收工。

### 边界纪律

- 允许自动执行前两步（只读）。写文件前，若处在只读环境或用户未授权改动技能目录，先说明再动手。
- **禁止**为了让接口"看起来能用"而删除文档里的约束、改写枚举、或把 `references/` 改成迎合当前实现的样子。事实以官网为准。
- 拉取失败（无外网、接口下线）时，明确告诉用户"无法核对官网，当前依据是 `references/` 的快照，快照时间见各篇更新时间"，不要假装已验证。
- 核对范围只限本技能覆盖的「薄荷科学.AI」开放接口手册（`<技能目录>/scripts/fetch_docs.py` 默认 `code=boohee.ai`）。**不要**用其他手册 code 去拉取内容，也不要在技能、回复或代码里列举与本技能无关的手册名或目录接口。

## 9. 渐进式查阅顺序

1. **先读 `00-endpoints.md`** — 全部接口的方法、路径、作用、关键入参速查表，用于定位该用哪个接口。
2. **再按需读对应章节原文** — 需要参数表、返回结构、枚举时才打开：

| 需求 | 文件 |
|---|---|
| 食物搜索、详情、分类、分类列表、单位估重、批量营养计算、营养排行 | `02-food-data.md` |
| 图片识别、识别详情、自然语言转食物 | `03-recognition.md` |
| 生成智能食谱、食谱详情、换一换、替换单菜/整餐、饮食模式列表与详情、食谱概要 | `04-recipe.md` |
| 体重记录增删查、最新体重、体重/体脂曲线 | `05-weight.md` |
| 饮食记录批量/单条写入、删除、修改、按天查询、当日最新 | `06-diet.md` |
| 本地配置细则、请求头、异步轮询、排错、已知坑、文档自愈 | `07-integration-ops.md`（本篇） |

每章文件是官网文档的逐字导出（含 `> 文档编号 / 更新时间`）。其中的 curl 与返回示例仅供核对参数与字段口径，**不向用户展示**。

3. **涉及用户本人时读 `config.json`** — 凭证、`user_id`、体重、忌口等存量信息见「本地配置」，别反复问用户要。
