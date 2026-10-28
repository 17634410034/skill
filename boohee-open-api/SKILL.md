---
name: boohee-open-api
display_name: 薄荷健康食物数据库
display_name_en: Boohee Food Database
description: 薄荷健康食物数据库能力,可以查询食物与营养成分、通过图片识别食物信息、根据需求生成个性化食谱、记录和查询体重体脂等基础数据。
description_zh: 薄荷健康食物数据库能力,可以查询食物与营养成分、通过图片识别食物信息、根据需求生成个性化食谱、记录和查询体重体脂等基础数据。
description_en: The BooHee Health Food Database has the capability to query food and nutritional information, identify food through images, generate personalized recipes based on needs, and record and query basic data such as weight and body fat.
version: 2.0.0
author: 薄荷健康
---

# 薄荷健康食物数据库

用薄荷健康开放接口（`https://api.boohee.com/open-apis`，官方文档站 `https://ai.boohee.com/docs/`）查食物营养、识别吃了什么、生成食谱、记录体重与饮食。参数、字段、枚举全部来自官方文档原文（`references/` 是逐字快照），不是模型凭记忆写的。

## 介绍

薄荷健康食物数据库能力，可以查询食物与营养成分、通过图片识别食物信息、根据需求生成个性化食谱、记录和查询体重体脂等基础数据。

## 能做什么

1. **查询食物与营养成分**：按名称或商品条码查热量、蛋白质/脂肪/碳水等几十种营养素；拿 GI/GL 升糖指数、红绿灯健康等级、食材构成与可食部；按分类浏览食物，查「一碗米饭」这类日常单位与估重；多样食物一次算出整餐合计营养；按营养素做排行，快速挑高蛋白 / 低脂 / 低嘌呤的选择。
2. **识别你吃了什么**：拍一张饭菜照，识别出食物并给出重量、热量与营养素占比；说一句「早上喝了一杯牛奶、吃了两个鸡蛋」，按早/中/晚餐与加餐拆分并匹配食物库条目。图片识别是异步任务，提交后轮询拿结果。
3. **生成个性化食谱**：输入性别、当前体重、目标热量即可开始；可叠加口味偏好、菜系地区、减重/增肌目标、忌口、慢病与饮食模式（控糖、碳水循环、16:8、高蛋白、素食、地中海、DASH 等）；生成一整周分餐食谱，可对某餐的一道菜「换一换」，替换单菜或整餐；附带食谱概要与饮食模式科普（介绍、禁忌人群、FAQ）。
4. **记录和查询体重、体脂**：写入体重与体脂，删除误记；按日期区间取历史，或取某日前最新一条；直接拿体重 / 体脂曲线数据做趋势展示。
5. **记录和查询饮食**：按餐别批量或单条写入，支持删除与修改（分量、单位、餐别、时间、热量）；查某天全部记录与当日最新；每次写入都返回按餐次分组的当日总热量、蛋白、脂肪、碳水。

## 三步执行流程（每轮按此顺序）

### 第 1 步：确认 API Key

运行 `python3 <技能目录>/scripts/config.py check`，首行给出状态：

- `KEY_OK <配置文件路径>`（退出码 0）→ 凭证就绪，进第 2 步。
- `NO_KEY <配置文件路径>`（没有配置文件时是 `NO_KEY -`，退出码 1）→ **立即停下**：不调用任何业务接口，不用示例数据，也不用模型记忆顶替。按下面四段回复后等用户：

  1. 这次需要薄荷开放平台的 API Key 才能取到真实数据；
  2. 获取地址与步骤：打开 `https://ai.boohee.com/console/` → 登录或注册 → 左侧「API Key 管理」→ 创建 → 复制 `sk-` 开头的完整密钥；
  3. 两种填法：把 key 发给我（我写入文件并脱敏，不在回复里回显），或打开 `config.json` 顶部带 ★ 的 `api_key` 那一行替换占位文字；
  4. 说明填好后回一句即可继续，key 只存在本机（权限 `0600`），配一次长期复用。

除以上两种填法外，不要用任何示例数据、模型常识或第三方食物库数字代替真实查询结果。

### 第 2 步：选接口并请求

1. 用 `references/00-endpoints.md` 的速查表把需求映射到接口，不要自造路径。版本前缀：食物 / 识别 / 食谱是 `v1`，体重 / 饮食记录是 `v2`。
2. 所有请求走 `python3 <技能目录>/scripts/config.py call <METHOD> <PATH> [--json '...']`，不要手拼请求直接发。
3. 食谱、体重、饮食接口必须带业务 `user_id`：先读 `profile.user_id`，没有就问用户，不要编造。
4. 两段式查询：`/v1/food/search` 拿 `food_code` 后再查 `/v1/food/detail`；分类先 `/v1/food/categories` 拿 `id` 和 `kind`，再查 `/v1/food/list`。
5. 异步任务：图片识别 `POST /v1/food/image_recognize` 拿 `task_id` → 轮询 `GET /v1/food/image_recognize_detail`，`status=1` 继续、`2` 完成、`3` 未识别、`4` 失败。食谱 `generate` 只回 `task_id` 且没有轮询接口，稍后用 `user_id` + `date` 查 `/v1/recipe/details`。
6. 参数、必填项、枚举只查 `references/`，不凭记忆补。

### 第 3 步：合并与总结

1. 多个接口的结果按用户的问题合并，不要把每段 JSON 依次贴出来。
2. 统一口径再比较：营养值多为每 100g，按实际重量或份数折算；热量统一 kcal、重量统一 g；枚举翻译成中文。
3. 回答里给关键数值和判断，标注「数据来自实时接口」，需要时附接口来源。
4. 分页或异步未完成时说明覆盖范围（如「前 20 条」「识别仍在处理中」），不要让用户误以为拿到了全量。

## 命令与路径约定

本技能所有命令都写成 `python3 <技能目录>/scripts/config.py ...`。**`<技能目录>` 就是你读到本 SKILL.md 时它所在的目录**，用它的绝对路径。各平台安装位置不同（`~/.qoder/skills/<name>`、`~/.gemini/skills/<name>`、`~/.workbuddy/skills/<name>__skillhub`、项目内的 `.qoder/skills/<name>` 都可能），不要照抄相对路径，否则会报 `No such file or directory`。不确定就按 frontmatter 的 `name` 定位：

```bash
find ~ -name SKILL.md -exec grep -l '^name: boohee-open-api' {} + 2>/dev/null
```

## API Key：获取与配置

1. **获取**：打开 `https://ai.boohee.com/console/` → 登录或注册 → 左侧「API Key 管理」→ 创建 → 复制 `sk-` 开头的完整密钥。
2. **写入**，三选一：
   - 对话里直接给：助手写进配置并脱敏；用户没给之前不要猜、不要用别的值顶替。
   - 手动填：打开 `config.json`，最上面带 ★ 的「第 1 步（必填）」区块里把 `api_key` 的占位文字替换成密钥。
   - 命令行：`python3 <技能目录>/scripts/config.py set api_key 'sk-xxx'`；还没有配置文件时先 `init`。
3. **位置**：默认在技能目录；技能目录不可写时自动改用 `~/.boohee-open-api/config.json`。以脚本打印的路径为准。
4. `config.json` 只留在本机，权限 `0600`，不随技能包上传、不进版本库。随时说「别存我的数据」即可清除。
5. 环境变量 `BOOHEE_API_KEY` 优先于文件，适合 CI 或临时试用。

## 硬性规则

1. **命令一律用绝对路径**：`<技能目录>` 替换成本文件所在目录的绝对路径。
2. **只用本技能的查询能力**：不提供接入代码、签名算法、Webhook 实现或 SDK 说明；用户问到这些时说明本技能不覆盖。
3. **无凭证不代答**：`NO_KEY` 时不得调用业务接口，不得用示例数据或模型常识冒充查询结果，也不得编造看起来合法的 `food_code`。
4. **参数只查 `references/`**：未文档化的字段或接口先向用户确认，不凭记忆补。
5. **写操作必须有真实 `user_id` 和真实 `food_code`**。
6. **异步必须等到终态**再总结；任务还在处理中时如实说明。
7. **接口返回与文档对不上时，先怀疑文档过期**：按 `07-integration-ops.md`「文档漂移自检与自愈」核对官网原文，不要断言接口坏了，也不要改文档去迎合实现。
8. **凭证与个人数据**：不回显完整值、不写进代码、不进提交、不上传。

## 需要细节时看这里

| 我要…… | 打开 |
|---|---|
| 找该调哪个接口（方法/路径/关键入参） | [references/00-endpoints.md](./references/00-endpoints.md) |
| 本地配置、请求头、异步轮询、排错表、已知坑、文档自愈流程 | [references/07-integration-ops.md](./references/07-integration-ops.md) |
| 食物营养、识别、食谱、体重、饮食的字段与枚举 | `references/02`~`06` 各篇（内部参数依据，按需只读对应章节） |
| 官网当前原文、更新本地快照 | `python3 <技能目录>/scripts/fetch_docs.py`（用法见操作细则「文档漂移自检与自愈」） |

**发起调用前先读 [references/07-integration-ops.md](./references/07-integration-ops.md)**：本地配置读写规则、`X-Api-Key` 请求头、异步轮询、错误码排错、关键约束与坑都在那篇里。
