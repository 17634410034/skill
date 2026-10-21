# 薄荷科学.AI 开放平台 API Skill

把薄荷科学.AI 健康 AI 基础能力平台 [ai.boohee.com/docs](https://ai.boohee.com/docs/) 的开放接口文档，整理成一份可被 AI 编程助手（Qoder CLI / Desktop）自动加载使用的 **Skill**。

装上之后，你直接用自然语言提需求，助手就会按官方文档的口径去调接口，而不是凭记忆编造字段和营养数据。凭证和身体数据只在第一次配置，之后由 `config.json` 长期留存并被自动读取。

```
你：查一下牛奶的营养，按 250ml 算
助手：（读 skill → 拿 X-Api-Key → GET /v1/food/search + /v1/food/detail → 按 250g 折算）

你：我 62kg、女生，帮我排这周三餐
助手：（读 config.json 里的 profile → 生成食谱 → 顺手把体重写回配置和体重接口）
```

## 内容范围

覆盖默认手册「薄荷科学.AI」全部 35 篇文档：六章、31 个接口 + Webhook 回调协议 + 多语言 SDK。

| 章节 | 能力 |
|---|---|
| 一、通用规范 | 域名与响应规范、`X-Api-Key` / AccessToken 认证、RSA 签名算法、事件回调（Webhook）、SDK |
| 二、食物数据 | 食物搜索、详情（GI/GL + 数十种营养素）、分类、分类列表、单位估重、批量营养计算、营养排行 |
| 三、智能识别 | 食物图片识别（异步 / SSE 流式）、识别详情、自然语言识别 |
| 四、智能食谱 | 生成食谱、食谱详情、换一换、替换单菜/整餐、饮食模式列表与详情、食谱概要 |
| 五、体重记录 | 记录、列表、最新一条、删除、体重/体脂曲线 |
| 六、饮食记录 | 批量/单条写入、删除、修改、按天查询、当日最新 |
| 接入操作细则（`07-integration-ops.md`，非官网导出） | `config.json` 读写、认证签名、异步与 Webhook、排错表、已知坑、文档自愈流程 |

## 安装

前提：仓库已 clone 到本地。

**方式一：软链到用户级 skill 目录（推荐，所有项目可用）**

```bash
ln -s "$(pwd)" ~/.qoder/skills/boohee-open-api
```

**方式二：只在某个项目里用**

```bash
ln -s "$(pwd)" <你的项目路径>/.qoder/skills/boohee-open-api
```

装完重启会话或执行 `/skills reload`，用 `/skills list` 确认能看到 `boohee-open-api`。

## 使用

- 显式调用：`/boohee-open-api`
- 自动触发：提到「薄荷」「开放平台」「食物库接口」「营养 API」，或需要调 `api.boohee.com/open-apis` 时

**调用接口需要凭证**，助手找不到会停下来问你要：

- 简单路径：登录 [控制台](https://ai.boohee.com/console/) → 「API Key 管理」→ 创建 API Key（`sk-` 开头），请求带 `-H 'X-Api-Key: sk-xxx'`。
- 长期服务端调用：`app_id` + `app_secret` + **薄荷提供的 RSA 私钥** → `POST /v1/access_token` 换 Bearer Token。细节见 `references/01-general.md`。

## 把凭证和身体数据交给 `config.json`

装完初始化一次，之后助手自己读、自己写，你不必每轮重复提供：

```bash
python3 scripts/config.py init                              # 生成 config.json（不进 git，权限 0600）
python3 scripts/config.py set api_key 'sk-xxx'               # 或 profile.user_id / profile.gender / profile.latest_weight
python3 scripts/config.py show                              # 随时查看，密钥自动脱敏
python3 scripts/config.py call GET '/v1/food/search?keyword=牛奶'   # 自动带凭证；POST 自动合并 profile
```

**API Key 的位置**：`init` 之后打开 `config.json`，第一屏就是带 ★ 标记的「第 1 步」区块，`api_key` 单独占一行，就在「第 1 步」标题下面那行 —— 把占位文字 `>>>>在这里填写你的key<<<<<` 换成你的真实密钥即可（key 在控制台「API Key 管理」创建，`sk-` 开头）。身体数据、忌口等档案在第 2 块 `profile`（可选），`app_id`/RSA 私钥/Webhook 这些进阶项排在最后，不用 API Key 之外的认证方式时可以整块忽略。没替换占位值时，脚本会直接提示「还没填」，不会拿假 key 去发请求。

两种填法，任选或混用：

- **手动填**：`init` 后编辑 `config.json` 顶部那一行 `api_key`（其余字段含义见文件内注释与 `references/07-integration-ops.md` 第 1 节的字段表）。
- **一句话让助手记下来**：把 key、`user_id`、身高体重、忌口、饮食目标告诉助手，助手按 `references/07-integration-ops.md` 的「自动记录」规则写回配置；报体重时默认同步调用 `/v2/weight/record` 留档，不想留档说一声即可。

优先级：环境变量 `BOOHEE_API_KEY` / `BOOHEE_APP_ID` / `BOOHEE_APP_SECRET` > `config.json` > 现场向你要。取到的 key 一次落盘，后续复用，不再重复询问。

安全边界：`config.json` 只留在本机、已被 `.gitignore` 排除，不会提交也不会随技能包上传；RSA 私钥只填文件路径，不填内容；助手展示配置时脱敏，回复与日志里不会出现完整 key；体重、忌口这类档案只记录你明确说过的内容，不做推断落盘，随时可以说「别存我的数据」清场。

## 目录结构

```
.
├── SKILL.md              # 门面：能做什么、怎么用起来、key 去哪拿、硬规则（细节一律外链到 references/）
├── config.example.json   # 配置模板（复制为 config.json 使用）
├── config.json           # 你本机的凭证与个人档案，不进 git
├── references/
│   ├── 00-endpoints.md   # 31 个接口速查表（方法/路径/作用/关键入参 → 章节定位）
│   ├── 01-general.md     # 一、通用规范（官网原文逐字导出）
│   ├── 02-food-data.md   # 二、食物数据
│   ├── 03-recognition.md # 三、智能识别
│   ├── 04-recipe.md      # 四、智能食谱
│   ├── 05-weight.md      # 五、体重记录
│   ├── 06-diet.md        # 六、饮食记录
│   └── 07-integration-ops.md  # 接入操作细则：配置读写、签名、异步/Webhook、排错、已知坑、文档自愈
└── scripts/
    ├── config.py         # 读写 config.json（凭证/档案）+ 带凭证调接口
    └── fetch_docs.py     # 文档漂移自检 + 自愈：比对官网、拉单篇原文、按需更新 references/
```

`references/01~06` 是官网正文的**逐字导出**（保留文档编号与更新时间），不是二手总结；`00-endpoints.md` 是索引，`SKILL.md` 是门面与决策入口，`07-integration-ops.md` 是从 SKILL.md 迁出的执行细则。

## 文档会过期，所以自带自愈能力

`references/` 是某一时刻的官网快照，官方随时会改接口。这个 skill 把「发现对不上 → 核对官网 → 更新自己」做成了固定流程：助手遇到 404、字段消失、枚举被拒时，先怀疑文档过期，而不是断言接口坏了或编造参数。

```bash
python3 scripts/fetch_docs.py --doc dc199d79   # 看某篇文档的官网当前原文（只读）
python3 scripts/fetch_docs.py                  # 全量比对，逐篇列出变动（只读，退出码 0=一致 2=有漂移）
python3 scripts/fetch_docs.py --apply          # 变动写回 references/（幂等，不产生虚假 diff）
```

数据源是文档站的公开接口，无需登录。`--apply` 只重写 `references/01~06`；`SKILL.md`、`00-endpoints.md` 与 `07-integration-ops.md` 属于人工整理的内容，要按变动复核后再 `git diff` 提交。

默认只同步「薄荷科学.AI」这一本手册，也就是本 skill 覆盖的能力范围。

## 已知文档问题

官网文档自身存在若干不一致（示例域名混用 `api.iboohee.com`、5.1 的 v1/v2 路径、4.3/4.6 下划线与连字符、流式接口路径官方错拼 `image_recongize_stream`），已在 `references/00-endpoints.md` 末尾逐条列出，联调时以真实返回为准。发现新的坑欢迎提 issue 或 PR。
