# 薄荷科学.AI 开放平台 API Skill

把薄荷科学.AI 健康 AI 基础能力平台 [ai.boohee.com/docs](https://ai.boohee.com/docs/) 的开放接口文档，整理成一份可被 AI 编程助手（Qoder CLI / Desktop）自动加载使用的 **Skill**。

装上之后，你直接用自然语言提需求，助手就会按官方文档的口径去调接口，而不是凭记忆编造字段和营养数据。

```
你：查一下牛奶的营养，按 250ml 算
助手：（读 skill → 拿 X-Api-Key → GET /v1/food/search + /v1/food/detail → 按 250g 折算）
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

凭证只放环境变量或当场提供，不要写进代码、不要提交进仓库。

## 目录结构

```
.
├── SKILL.md              # 助手读的主文档：凭证获取、接入流程、排错、约束与坑
├── references/
│   ├── 00-endpoints.md   # 31 个接口速查表（方法/路径/作用/关键入参 → 章节定位）
│   ├── 01-general.md     # 一、通用规范（官网原文逐字导出）
│   ├── 02-food-data.md   # 二、食物数据
│   ├── 03-recognition.md # 三、智能识别
│   ├── 04-recipe.md      # 四、智能食谱
│   ├── 05-weight.md      # 五、体重记录
│   └── 06-diet.md        # 六、饮食记录
└── scripts/
    └── fetch_docs.py     # 文档漂移自检 + 自愈：比对官网、拉单篇原文、按需更新 references/
```

`references/01~06` 是官网正文的**逐字导出**（保留文档编号与更新时间），不是二手总结；`00-endpoints.md` 和 `SKILL.md` 是在其之上整理的索引与决策指引。

## 文档会过期，所以自带自愈能力

`references/` 是某一时刻的官网快照，官方随时会改接口。这个 skill 把「发现对不上 → 核对官网 → 更新自己」做成了固定流程：助手遇到 404、字段消失、枚举被拒时，先怀疑文档过期，而不是断言接口坏了或编造参数。

```bash
python3 scripts/fetch_docs.py --doc dc199d79   # 看某篇文档的官网当前原文（只读）
python3 scripts/fetch_docs.py                  # 全量比对，逐篇列出变动（只读，退出码 0=一致 2=有漂移）
python3 scripts/fetch_docs.py --apply          # 变动写回 references/（幂等，不产生虚假 diff）
```

数据源是文档站的公开接口，无需登录。`--apply` 只重写 `references/01~06`；`SKILL.md` 与 `00-endpoints.md` 属于人工整理的索引，要按变动复核后再 `git diff` 提交。

默认只同步「薄荷科学.AI」这一本手册，也就是本 skill 覆盖的能力范围。

## 已知文档问题

官网文档自身存在若干不一致（示例域名混用 `api.iboohee.com`、5.1 的 v1/v2 路径、4.3/4.6 下划线与连字符、流式接口路径官方错拼 `image_recongize_stream`），已在 `references/00-endpoints.md` 末尾逐条列出，联调时以真实返回为准。发现新的坑欢迎提 issue 或 PR。
