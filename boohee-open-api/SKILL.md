---
name: boohee-open-api
display_name: 薄荷健康食物数据库
display_name_en: Boohee Food Database
description: 薄荷健康开放接口助手。两种用法：一是帮你把食物营养、餐食识别、智能食谱、体重与饮食记录接进自己的应用——按官方文档原文生成可运行的 Go/Python/Java/Node.js 调用代码、RSA 签名链路、异步任务轮询与 Webhook 回调实现，无需先拿到 key；二是配好 API Key 后直接用自然语言查食物营养、拍照识别、生成食谱、记录体重饮食，数据来自官方实时接口。内置 29 段官方文档返回示例供离线对照，另附文档漂移自检与自愈流程。
description_zh: 薄荷健康开放接口助手：按官方文档生成接入代码、讲清签名与 Webhook，或配好 API Key 后直接查营养、识别餐食、配食谱、记体重饮食。含官方示例离线对照与文档自愈。
description_en: Boohee Health Open API assistant. Generate runnable Go/Python/Java/Node.js integration code from the official docs (auth signing, async tasks, webhooks) without a key, or connect an API Key to query food nutrition, recognize meals, build recipes and log weight/diet in real time. Ships 29 official response samples for offline reference, plus doc-drift self-healing.
version: 1.1.0
author: 薄荷健康
---

# 薄荷健康食物数据库

把薄荷健康开放接口（`https://api.boohee.com/open-apis`，官方文档站 `https://ai.boohee.com/docs/`）的能力接进你的应用或日常对话。本技能的所有参数、字段、枚举、示例都来自官方文档原文（`references/` 内为逐字快照），不是模型凭记忆编的。

**两类用法，没有 API Key 也能立刻产出结果：**

| 你的情况 | 本技能给你什么 |
|---|---|
| 我是开发者，正在接入 | 按官方文档生成可运行代码、签名链路、异步轮询、Webhook 验签实现、接口选型与字段说明。**不需要 key** |
| 我想直接问数据 | 配一次 API Key 后，用自然语言查营养、拍照识别、生成食谱、记录体重饮食，返回官方实时数据 |
| 我还没 key 但想先看效果 | 用 `references/demo-samples.md` 里 29 段**官方文档返回示例**演示真实结构与字段口径，会明确标注是示例、非实时数据 |

## 关于命令里的 `<技能目录>`

本技能所有命令都写成 `python3 <技能目录>/scripts/config.py ...`。**`<技能目录>` 必须替换成本 SKILL.md 所在目录的绝对路径**（安装后形如 `~/.workbuddy/skills/boohee-open-api`）。技能目录不是你的工作目录，直接照抄相对路径会报 `No such file or directory`。不确定就先定位：

```bash
ls ~/.workbuddy/skills/boohee-open-api     # 或 find ~ -name SKILL.md -path "*boohee-open-api*"
```

## 能做什么

### 1. 查询食物与营养成分

- 按名称或商品条码查热量、蛋白质/脂肪/碳水等几十种营养素
- 拿到 GI/GL 升糖指数、红绿灯健康等级、食材构成与可食部
- 按分类浏览食物，查「一碗米饭」这类日常单位与估重
- 多样食物一次算出整餐合计营养
- 按营养素做排行，快速挑高蛋白 / 低脂 / 低嘌呤的选择

### 2. 识别你吃了什么

- 拍一张饭菜照，识别出食物并给出重量、热量与营养素占比
- 说一句「早上喝了一杯牛奶、吃了两个鸡蛋」，按早/中/晚餐与加餐拆分并匹配食物库条目
- 支持异步查询与流式边识别边出结果，适合做「拍照记录饮食」

### 3. 生成个性化食谱

- 输入性别、当前体重、目标热量即可开始
- 可叠加口味偏好、菜系地区、减重/增肌目标、忌口、慢病与饮食模式（控糖、碳水循环、16:8、高蛋白、素食、地中海、DASH 等）
- 生成一整周分餐食谱，可对某餐的一道菜「换一换」，替换单菜或整餐
- 附带食谱概要与饮食模式科普（介绍、禁忌人群、FAQ）

### 4. 记录和查询体重、体脂

- 写入体重与体脂，删除误记
- 按日期区间取历史，或取某日前最新一条
- 直接拿体重 / 体脂曲线数据做趋势展示

### 5. 记录和查询饮食

- 按餐别批量或单条写入，支持删除与修改（分量、单位、餐别、时间、热量）
- 查某天全部记录与当日最新
- 每次写入都返回按餐次分组的当日总热量、蛋白、脂肪、碳水

### 6. 帮你把接口接进自己的代码

- 按官方文档生成 Go / Python / Java / Node.js 调用代码与 curl 示例
- RSA 签名算法逐步实现、`access_token` 换取与续期
- 异步任务「提交 → 轮询 → 取详情」与 Webhook 验签（HMAC-SHA256、challenge 验证、1 秒内返回 200）
- 接口选型、字段口径、枚举取值、错误码排错

## 配好 API Key（只用一次，之后不必再管）

**第 1 步：拿 key。** 浏览器打开控制台 `https://ai.boohee.com/console/` → 登录开放平台账号（没有就在控制台注册）→ 左侧「API Key 管理」→ 创建 API Key → 复制以 `sk-` 开头的完整密钥。

**第 2 步：填进去。** 两种任选：

- 打开技能目录下的 `config.json`，最顶上带 ★ 的「第 1 步（必填）」区块里就有 `api_key` 那一行，把占位文字替换成你的密钥，其他区块先都不用动。
- 直接在对话里说「记住我的 key 是 sk-xxx」，助手会写进配置并做脱敏，不会在回复里回显完整值。

还没有 `config.json` 这个文件时，先让助手初始化：`python3 <技能目录>/scripts/config.py init`。

**第 3 步：直接提需求。** 「查一下牛奶按 250ml 算的营养」「拍这张饭菜照，看看我吃了什么」「帮我排这周三餐，我要控糖」「记录我今天早餐吃了全麦面包两片」。

之后身体数据也不用你操心：说一声「我体重 62kg」「我是女生」「我不吃香菜」「我的 user_id 是 U1001」，助手会自动记进同一个文件的 `profile` 区块，后续调用直接复用，不再反复问你。

> `config.json` 只留在你本机（权限 `0600`，不会随技能包上传、不会进版本库）。随时可以说「别存我的数据」让助手清掉。

## 必须遵守的规则

1. **命令一律用绝对路径**：`<技能目录>` 替换成本文件所在目录的绝对路径，不要照抄相对路径。
2. **先查本地配置，再问用户**：调接口前先 `python3 <技能目录>/scripts/config.py show`，已有可用 key 就直接用；文件不存在时先 `init`。`api_key` 还是占位文案或含中文时等同没填，不要拿它发请求。
3. **数据来源分三级，交付时必须说清是哪一级**：
   - **实时接口返回**（已配置凭证）— 最优，可直接用于写入类接口。
   - **官方文档示例返回**（`references/demo-samples.md`）— 无凭证、或环境访问不到接口时使用。**回复第一行必须声明**「以下为薄荷官方接口文档的示例返回，非实时查询结果」，且其中的 `food_code` 不可用于写入。
   - **模型记忆里的通用营养数据** — **严禁**用于交付。用户只要一个大致参考值时，也必须显式说明这是模型常识、不来自薄荷食物库，且不得编造看起来合法的 `code`。
4. **禁止凭记忆编造参数**：所有参数、字段、枚举一律查 `references/`；未文档化的字段/接口先向用户确认。
5. **接口返回与文档对不上时，先怀疑文档过期**：按操作细则第 8 节核对官网原文，不要断言接口坏了，更不要改文档去迎合实现。
6. **凭证与个人数据**：不回显完整值、不写进代码、不进提交、不上传；RSA 私钥只记文件路径，不记内容。

## 需要细节时看这里

| 我要…… | 打开 |
|---|---|
| 找该调哪个接口（方法/路径/关键入参） | [references/00-endpoints.md](./references/00-endpoints.md) |
| 没有 key，想先看接口真实返回长什么样 | [references/demo-samples.md](./references/demo-samples.md)（29 段官方示例，按目录只读需要的小节） |
| 食物营养、识别、食谱、体重、饮食的字段与示例 | `references/02~06-*.md`（按需只读对应章节） |
| 认证签名、`config.json` 字段、异步与 Webhook、排错表、已知坑、文档自愈流程 | [references/07-integration-ops.md](./references/07-integration-ops.md) |
| 官网当前原文、更新本地快照 | `python3 <技能目录>/scripts/fetch_docs.py`（用法见操作细则第 8 节） |

**要真正发起调用或写接入代码前，先读 [references/07-integration-ops.md](./references/07-integration-ops.md)**：本地配置读写规则、Bearer Token 签名链路、异步任务与 Webhook 实现要求、错误码排错、关键约束与坑都在那篇里。
