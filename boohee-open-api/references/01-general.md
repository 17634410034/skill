# 一、通用规范


---

## 1.1 请求方式

> 文档编号: `dcbf0f02` · 更新时间: 2026-07-09 18:03:58

#### 接口域名

- `https://api.boohee.com/open-apis`

#### 请求规范

- 认证方式
  - 1：Bearer Token (JWT) （使用 app_id 和 app_secret ，通过 accessToken 接口获取 accessToken 进行认证）
  - 2：X-Api-Key（直接在接口请求头中添加 X-Api-Key 字段，值为后台创建的 API Key）
- 响应数据格式: JSON

#### 请求示例
```bash
// 示例1：使用 Bearer Token 认证
curl 'https://api.boohee.com/open-apis/v1/food/search?keyword=abc' \
  --header 'Accept: */*' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.......' \

// 示例2：使用 X-Api-Key 认证
curl 'https://api.boohee.com/open-apis/v1/food/search?keyword=abc' \
  --header 'Accept: */*' \
  --header 'X-Api-Key: sk-1234567890abcdef1234567890abcdef123'
```

#### 返回规范

所有接口返回数据格式均为 JSON。
```json
{
  "code": 0, //数字类型,
  "message": "string", //字符串类型"
  "now": 1722851989, //数字类型
  "data": //任意类型（无数据时为null/空对象/空数组）
}
``` 

|字段|类型|说明|
|---|---|---|
|code|Integer|返回 0 表示成功，非 0 表示失败|
|message|String|处理信息|
|data|任意类型（无数据时为null/空对象/空数组）|


---

## 1.2 获取访问令牌

> 文档编号: `dc4ee88e` · 更新时间: 2026-06-15 10:15:30

#### 接口说明
申请访问薄荷开放平台的凭证（AccessToken），所有其他接口均需携带有效 AccessToken 调用。

#### 请求地址
**POST `/v1/access_token`**

#### 请求参数（Body JSON）
|参数名|类型|必填|说明|
|---|---|---|---|
|app_id|String|是|开发者平台分配的app_id|
|timestamp|Long|是|当前时间戳（秒级），与服务器时间差不超过 60 秒钟|
|sign|String|是|签名，生成规则见[签名生成规则](#签名生成规则)|


#### 请求示例
```bash
curl --request POST 'https://api.iboohee.com/open-apis/v1/access_token' \
  --header 'Content-Type: application/json' \
  --header 'Accept: */*' \
  --data-raw '{
    "app_id": "boohee",
    "timestamp": 1470042310,
    "sign": "27f61732856d133758e7f8927a3abed1"
  }'
```

#### 返回示例
```json
{
  "code": 0,  // 返回0表示成功，非0表示失败
  "message": "成功", //字符串类型
  "now": 1722851989, //数字类型
  "data": {
    "access_token": "abcdef1234567890abcdef1234567890",
    "expires_in": 86400,  // 过期时间（秒），默认 1 天
  }
}
```
#### 补充说明
token 过期后，需重新调用获取新的 token。


---

## 1.3 签名生成规则

> 文档编号: `dce33fcf` · 更新时间: 2026-07-14 15:30:23

举例：假设请求参数键值对如下

```yml
app_id: boohee
timestamp: 1470042310
```

#### 第一步

对数所有请求参数按照键名进行正序排序，排序结果如下，注意要保持键值对的对应关系且 appKey 不参与运算。

```yml
app_id: boohee
timestamp: 1470042310
```

#### 第二步

循环对每个键值进行拼接处理，拼接成如下的字符串：`app_idbooheetimestamp1470042310`

#### 第三步

计算sign
1.获取 appSecret， 假如当前实例中的 appSecret  为 12345

2.将 appSecret 拼接在第二步的结果的前后， 注意没有任何拼接符，结果如下：`12345app_idbooheetimestamp147004231012345`

3.将上述字符串进行 RSA-sha256（私钥由薄荷提供） 加密后即可得到 sign，加密结果如下：

```yml
s7pIZLzMs4HveepEj7Z3hB2ULKQyAjm/qAaR8OZlzfQKjDIReQR16yLnEyRQhT2pM4V0H7imX8LilL7PcsmybCADnsdLh18cN59XZSUFAC8lVwrCtxJVyq92tLjEcZx1I0ztg+JlWj0ArCg/NggiH5tBmgS1E++s3Qa8reCctoUGpgghm6GdPlcQw29nryUw4UgjMBVCE9heAyIpCJZ8j8YqvuFof2NpvzMxesnKVTvLyW55lA/q0AemhEibm8XCRxDGBSHaQSVWbMZBWk/CwzETTD6bS8VkMxZBshmqJS6T3qWew0dpE4DYLOiXKypMa+foJbTUMdsbSPFuG8LtQSwKNM47BIOJvIpXquJPoVgT4Pe24jH6jmWTQWAHFQa95SI15BbN/jnloY2KNWc5C8DJ4xqpl5Jx4WYKQ0ze5aNsESMTb58/ETL9Qxr7tQXomqr4QruaM+DajKmG0pm7DQHS37ENfx2gbEsvG3onJhWxURwaFJfmc0PabHnZjCpT530yZAFjeC4ydUWOfHXMiqzQQcC4anwkzEP/2mc5a3blyQ1yDR24NlHLrPTKHsTQ+w/wdF89ejyATl1ga/363qKWXxiff4azq3epXNwElCmEWihmEhWcb5R+FGL9vnLyXfGFvoWd247S4R/WNWNcZnAyWN2Vkpb+L+3G6A6+bws=
```


4.将计算的 sign 作为一个请求参数放到参数列表中

```yml
app_id: boohee
timestamp: 1470042310000
sign: 2s7pIZLzMs4HveepEj7Z3hB2ULKQyAjm/qAaR8OZlzfQKjDIReQR16yLnEyRQhT2pM4V0H7imX8LilL7PcsmybCADnsdLh18cN59XZSUFAC8lVwrCtxJVyq92tLjEcZx1I0ztg+JlWj0ArCg/NggiH5tBmgS1E++s3Qa8reCctoUGpgghm6GdPlcQw29nryUw4UgjMBVCE9heAyIpCJZ8j8YqvuFof2NpvzMxesnKVTvLyW55lA/q0AemhEibm8XCRxDGBSHaQSVWbMZBWk/CwzETTD6bS8VkMxZBshmqJS6T3qWew0dpE4DYLOiXKypMa+foJbTUMdsbSPFuG8LtQSwKNM47BIOJvIpXquJPoVgT4Pe24jH6jmWTQWAHFQa95SI15BbN/jnloY2KNWc5C8DJ4xqpl5Jx4WYKQ0ze5aNsESMTb58/ETL9Qxr7tQXomqr4QruaM+DajKmG0pm7DQHS37ENfx2gbEsvG3onJhWxURwaFJfmc0PabHnZjCpT530yZAFjeC4ydUWOfHXMiqzQQcC4anwkzEP/2mc5a3blyQ1yDR24NlHLrPTKHsTQ+w/wdF89ejyATl1ga/363qKWXxiff4azq3epXNwElCmEWihmEhWcb5R+FGL9vnLyXfGFvoWd247S4R/WNWNcZnAyWN2Vkpb+L+3G6A6+bws=ed1
```


---

## 1.4 事件回调

> 文档编号: `dc1e26bf` · 更新时间: 2026-09-15 13:47:06

# 事件回调通知（Webhook）接入指南

## 概述

开放平台支持通过回调通知（Webhook）的方式，在特定业务事件完成时主动向您配置的服务器地址推送结果。相比于轮询方式，回调通知具有实时性强、资源消耗低的优点。

本文档面向开发者，帮助您：

- 了解当前支持的业务事件类型
- 实现符合规范的回调接收服务
- 正确校验回调请求签名
- 排查回调接收中的常见问题

> 💡 回调地址的配置和订阅管理请在开发者后台「事件回调」完成，本文档不涉及后台操作。

## 支持的业务事件

当前开放平台支持订阅以下业务事件：

| 事件类型 `event` | 名称 | 说明 |
| --- | --- | --- |
| `smart_recipe` | 智能食谱 | AI 生成个性化食谱方案完成后推送 |
| `food_recognize` | 食物识别 | 图片识别食物并计算热量完成后推送 |

> 💡 后续平台新增的业务事件类型会同步在本节更新，可订阅列表以控制台展示为准。

## 回调接收服务要求

您需要在自己的服务器上实现一个 HTTPS 接口，用于接收来自开放平台的 POST 请求。该接口必须满足以下要求：

- 支持 `POST` 方法，`Content-Type: application/json`
- 在 **1 秒内**返回 HTTP `200` 状态码
- 能正确处理地址验证（challenge-response）和业务事件两种请求
- 基于请求签名做来源校验，拒绝非法请求

## 地址验证（Challenge-Response）

当您在控制台提交或修改回调地址时，系统会立即向该地址发起一次验证请求，用于确认：

1. 您的服务器能够正常接收来自开放平台的请求
2. 您持有该应用的 `app_key`，能够正确构造签名

### 验证请求

**请求方式**：`POST`

**请求头**：

与业务事件回调相同，包含 `X-Boohee-App-Id`、`X-Boohee-Event`（值为 `callback_url_validation`）、`X-Boohee-Timestamp`、`X-Boohee-Signature`。

**请求体**（JSON）：

```json
{
  "event_id": "...",
  "event": "callback_url_validation",
  "timestamp": 1725436800,
  "data": {
    "challenge": "a1b2c3d4e5f6789012345678901234ab"
  }
}
```

其中 `challenge` 为服务端随机生成的 32 位十六进制字符串。

### 期望的响应

您的服务器必须：

1. 从请求体中读取 `challenge` 值
2. 使用 `app_key` 作为密钥，对 `challenge` 计算 HMAC-SHA256 签名
3. **响应体直接返回该签名的 hex 编码字符串**（不需要 JSON 包装）
4. 返回 HTTP `200` 状态码

示例响应：

```
HTTP/1.1 200 OK
Content-Type: text/plain

a3c2e1d4f5b6...（HMAC-SHA256 hex 字符串）
```

### 地址验证示例代码

**Python（Flask）**：

```python
import hashlib
import hmac
from flask import Flask, request

app = Flask(__name__)
APP_KEY = "your_app_key"  # 从开放平台控制台获取

def hmac_sha256(key: str, data: str) -> str:
    return hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json()

    #地址验证：返回 challenge 的 HMAC-SHA256 签名
    if payload.get("event") == "callback_url_validation":
        challenge = payload["data"]["challenge"]
        return hmac_sha256(APP_KEY, challenge), 200

    #...业务事件处理见下文
```

**Go（Gin）**：

```go
import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "github.com/gin-gonic/gin"
)

const appKey = "your_app_key" // 从开放平台控制台获取

func hmacSHA256(key, data string) string {
    mac := hmac.New(sha256.New, []byte(key))
    mac.Write([]byte(data))
    return hex.EncodeToString(mac.Sum(nil))
}

func Webhook(c *gin.Context) {
    var payload map[string]any
    c.ShouldBindJSON(&payload)

    // 地址验证
    if payload["event"] == "callback_url_validation" {
        data := payload["data"].(map[string]any)
        challenge := data["challenge"].(string)
        c.String(200, hmacSHA256(appKey, challenge))
        return
    }

    // ...业务事件处理见下文
}
```

## 接收业务事件回调

当订阅的业务事件完成时，系统会向您配置的回调地址发起 POST 请求。

### 请求格式

**请求方式**：`POST`

**请求头**：

| Header | 类型 | 说明 |
| --- | --- | --- |
| `Content-Type` | string | 固定 `application/json` |
| `X-Boohee-App-Id` | string | 您的应用 ID |
| `X-Boohee-Event` | string | 事件类型，与 body 中的 `event` 字段一致 |
| `X-Boohee-Timestamp` | string | Unix 时间戳（秒），用于签名校验和防重放 |
| `X-Boohee-Signature` | string | 请求签名，HMAC-SHA256 的 hex 编码字符串 |

**请求体**（JSON）：

```json
{
  "event_id": "a1b2c3d4e5f6789012345678901234ab",
  "event": "food_recognize",
  "timestamp": 1725436800,
  "data": {
    "task_id": "task_abc123",
    // 其他业务数据，结构随 event 不同而变化
  }
}
```

字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `event_id` | string | 事件唯一 ID，用于幂等去重和日志关联 |
| `event` | string | 事件类型，如 `smart_recipe`、`food_recognize` |
| `timestamp` | int64 | 事件实际发生时间（Unix 时间戳，秒），即业务任务完成的时间 |
| `data` | object | 业务数据，包含 `task_id` 及其他字段，具体结构参见「业务事件数据」章节 |

> 💡 **`data.task_id` 的来源**：
>
> `task_id` 是您在发起异步任务时由接口返回的标识，用于将回调与原始请求关联起来。它位于 `data` 字段内，与其他业务数据一起下发。
>
> - `food_recognize`：调用 `POST /open-apis/v1/food/image_recognize` 发起识别任务时，接口响应中返回。
> - `smart_recipe`：调用 `POST /open-apis/v1/recipe/generate` 发起食谱生成任务时，接口响应中返回。

> ⏰ **`timestamp`（body）与 Header 中 `X-Boohee-Timestamp` 的区别**：
>
> - **`timestamp`**（body）：事件实际发生时间，即业务任务完成的时间，代表"事情什么时候发生"。
> - **`X-Boohee-Timestamp`**（Header）：HTTP 回调请求的发送时间，即系统向您服务器发起 POST 请求时的当前时间，用于签名校验和防重放。
> - 两者存在细微差异（毫秒到秒级），来源于系统处理与投递延迟。验签和新鲜度校验应使用 Header 中的 `X-Boohee-Timestamp`，业务时间记录使用 body 中的 `timestamp`。

### 签名校验（必须）

为保障请求安全，您**必须**在服务端校验签名。校验流程：

**第一步**：从请求头获取 `X-Boohee-Signature`、`X-Boohee-Timestamp`、`X-Boohee-Event` 三个值。

**第二步**：读取**原始请求体** `raw_body`（不要做 JSON 反序列化后再序列化，必须保持原始字符串）。

**第三步**：按以下算法计算期望签名：

``` python
sign_data = "{timestamp}.{event}.{raw_body}"
expected_sign = HMAC-SHA256("{app_key}", sign_data)
```

> ⚠️ 使用 `app_key` 作为 HMAC 密钥，对 `timestamp`、`event`、`raw_body` 以 `.` 分隔拼接后的字符串计算 HMAC-SHA256，结果为 hex 编码字符串。

**第四步**：比对 `X-Boohee-Signature` 与 `expected_sign`，不一致则拒绝请求（返回 403）。

### 完整接收示例

**Python（Flask）**：

```python
import hashlib
import hmac
import time
from flask import Flask, request, abort

app = Flask(__name__)
APP_KEY = "your_app_key"
APP_ID = "your_app_id"

def verify_signature(timestamp: str, event: str, signature: str, raw_body: bytes) -> bool:
    """校验请求签名（HMAC-SHA256）"""
    sign_data = f"{timestamp}.{event}.{raw_body.decode()}"
    expected = hmac.new(APP_KEY.encode(), sign_data.encode(), hashlib.sha256).hexdigest()
    return signature == expected

@app.route("/webhook", methods=["POST"])
def webhook():
    app_id = request.headers.get("X-Boohee-App-Id")
    event = request.headers.get("X-Boohee-Event")
    timestamp = request.headers.get("X-Boohee-Timestamp")
    signature = request.headers.get("X-Boohee-Signature")

    #1. 校验签名
    if not verify_signature(timestamp, event, signature, request.data):
        abort(403)

    #2. （推荐）校验 timestamp，防止重放攻击
    if abs(int(timestamp) - time.time()) > 300:  # 超过 5 分钟拒绝
        abort(403)

    payload = request.get_json()

    #3. 处理地址验证
    if event == "callback_url_validation":
        challenge = payload["data"]["challenge"]
        return hmac.new(APP_KEY.encode(), challenge.encode(), hashlib.sha256).hexdigest(), 200

    #4. 处理业务事件（建议异步处理，快速返回 200）
    handle_business_event(payload)
    return "ok", 200

def handle_business_event(payload: dict):
    """异步处理业务事件，避免阻塞响应"""
    #TODO: 将事件放入队列或异步任务
    pass
```

**Go（Gin）**：

```go
package main

import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "io"
    "math"
    "net/http"
    "strconv"
    "time"

    "github.com/gin-gonic/gin"
)

const (
    appKey = "your_app_key"
    appID  = "your_app_id"
)

func verifyHMACSignature(timestamp, event, signature string, rawBody []byte) bool {
    signData := fmt.Sprintf("%s.%s.%s", timestamp, event, string(rawBody))
    mac := hmac.New(sha256.New, []byte(appKey))
    mac.Write([]byte(signData))
    expected := hex.EncodeToString(mac.Sum(nil))
    return hmac.Equal([]byte(signature), []byte(expected))
}

func Webhook(c *gin.Context) {
    hAppID := c.GetHeader("X-Boohee-App-Id")
    event := c.GetHeader("X-Boohee-Event")
    timestamp := c.GetHeader("X-Boohee-Timestamp")
    signature := c.GetHeader("X-Boohee-Signature")

    // 读取原始请求体
    rawBody, _ := io.ReadAll(c.Request.Body)

    // 1. 校验签名（HMAC-SHA256）
    if !verifyHMACSignature(timestamp, event, signature, rawBody) {
        c.Status(http.StatusForbidden)
        return
    }

    // 2. （推荐）校验 timestamp，防止重放攻击
    ts, _ := strconv.ParseInt(timestamp, 10, 64)
    if math.Abs(float64(time.Now().Unix()-ts)) > 300 {
        c.Status(http.StatusForbidden)
        return
    }

    // 3. 解析 JSON
    var payload map[string]any
    json.Unmarshal(rawBody, &payload)

    // 4. 地址验证（返回 challenge 的 HMAC-SHA256 签名）
    if event == "callback_url_validation" {
        data := payload["data"].(map[string]any)
        challenge := data["challenge"].(string)
        challengeMac := hmac.New(sha256.New, []byte(appKey))
        challengeMac.Write([]byte(challenge))
        c.String(200, hex.EncodeToString(challengeMac.Sum(nil)))
        return
    }

    _ = hAppID // 可用于日志记录

    // 5. 异步处理业务事件
    go handleBusinessEvent(payload)
    c.String(200, "ok")
}

func handleBusinessEvent(payload map[string]any) {
    // TODO: 实际业务处理逻辑
}
```

## 响应要求

- 收到回调后必须在 **1 秒内**返回 HTTP `200` 状态码
- 响应体内容无强制要求，建议返回 `ok` 等简短内容
- 返回非 200 状态码或超时会视为推送失败

> 💡 建议将实际业务处理逻辑放到异步任务中执行，接口只负责接收并快速响应。

## 业务事件数据

回调本质上是「任务完成通知」，`data` 字段仅包含任务状态，不包含完整的业务结果。收到回调后，请根据 `event` 调用对应的详情接口获取完整数据。

### `food_recognize` - 食物识别

当食物图片识别任务完成（成功、未识别到食物、失败任一终态）时推送。**状态为「解析中」时不会推送**。

**回调 `data` 字段：**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | string | 任务 ID，来源见上文说明 |
| `status` | int | 任务状态：`2` = 识别成功，`3` = 未识别到食物，`4` = 识别失败 |

回调示例：

```json
{
  "event_id": "a1b2c3d4e5f6789012345678901234ab",
  "event": "food_recognize",
  "timestamp": 1725436800,
  "data": {
    "task_id": "a1b2c3d4e5f6",
    "status": 2
  }
}
```

**获取识别结果：**

```
GET /open-apis/v1/food/image_recognize_detail?task_id={task_id}
```

### `smart_recipe` - 智能食谱

当 AI 个性化食谱方案生成完成（成功或失败）时推送。

**回调 `data` 字段：**

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | string | 任务 ID，来源见上文说明 |
| `user_id` | string | 生成该食谱的用户标识 |
| `status` | int | 任务状态：`2` = 生成失败，`3` = 生成成功 |

回调示例：

```json
{
  "event_id": "f67890123456789012345678901234ab",
  "event": "smart_recipe",
  "timestamp": 1725436800,
  "data": {
    "task_id": "task_abc123",
    "user_id": "user_xyz",
    "status": 3
  }
}
```

**获取食谱详情：**

```
GET /open-apis/v1/recipe/details?user_id={user_id}&date={date}
```

> 💡 `date` 为您在调用 `/open-apis/v1/recipe/generate` 时传入的「食谱归属日期」。

### 状态值速查表

| 业务类型 | `status` | 含义 | 是否推送 |
| --- | --- | --- | --- |
| `food_recognize` | 1 | 解析中 | ❌ 不推送 |
| `food_recognize` | 2 | 识别成功 | ✅ 推送 |
| `food_recognize` | 3 | 未识别到食物 | ✅ 推送 |
| `food_recognize` | 4 | 识别失败 | ✅ 推送 |
| `smart_recipe` | 2 | 生成失败 | ✅ 推送 |
| `smart_recipe` | 3 | 生成成功 | ✅ 推送 |

## 推荐处理流程

1. 收到回调 → 校验签名（HMAC-SHA256）→ 校验 timestamp → 立即返回 `200`
2. 基于 `event_id` 做幂等判断，已处理过则忽略
3. 根据 `event` 调用对应的详情接口获取完整数据：
   - `food_recognize`：使用 `data.task_id` 查询
   - `smart_recipe`：使用 `data.user_id` + 您发起请求时指定的 `date` 查询
4. 异步写入业务系统


## 常见问题

### Q：地址验证失败，回调地址无法保存？

常见原因：

- 服务端未在 1 秒内返回响应
- 响应体不是 challenge 的 HMAC-SHA256 签名（应返回 HMAC-SHA256(appKey, challenge) 的 hex 编码）
- 签名算法不正确
- 网络不通（服务器 IP 被防火墙拦截、DNS 解析失败等）

建议先用 `curl` 本地模拟验证逻辑，确认签名正确后再排查网络问题。

### Q：如何测试回调接收？

1. 使用 [ngrok](https://ngrok.com/) 等内网穿透工具暴露本地服务
2. 在控制台配置公网地址，会自动触发地址验证
3. 通过业务接口触发异步任务
4. 查看控制台「回调日志」确认推送结果

### Q：`app_key` 在哪里获取？

登录开放平台控制台，在「API Key 管理」中查看。

### Q：回调请求来源 IP 是否固定？

系统通过内网服务集群发起回调，**IP 不固定**。请勿通过 IP 白名单限制回调请求，应通过签名验证来确保请求来源的合法性。

### Q：收到回调后业务处理失败怎么办？

建议的处理方式：

1. 接口先返回 200，避免被判定为推送失败
2. 将事件放入消息队列或任务队列
3. 业务处理失败时通过自己的重试机制兜底
4. 通过控制台「回调日志」查看推送记录

## 安全建议

1. **必须校验签名**：不要仅依赖 IP 或请求来源判断请求合法性
2. **校验 timestamp**：建议拒绝 timestamp 与当前时间相差超过 5 分钟的请求，防止重放攻击
3. **使用 HTTPS**：避免回调数据在传输过程中被窃取
4. **保护 `app_key`**：不要将 `app_key` 硬编码到前端代码或公开仓库
5. **幂等处理**：基于 `event_id` 做幂等，避免重复处理造成业务异常
6. **不要同步处理耗时业务**：避免接口超时导致推送失败



---

## 1.5 SDK下载

> 文档编号: `dcc091bc` · 更新时间: 2026-09-15 13:39:09

## 1.4 SDK 下载

薄荷科学.ai 提供多语言 SDK，封装了请求签名、Token 管理、流式接口等通用逻辑，帮助开发者快速接入。

**GitHub 仓库**：https://github.com/BOOHEEAI/sdk

### 支持语言

| 语言 | 目录 | 最低版本 |
|------|------|----------|
| Go | [go/](https://github.com/BOOHEEAI/sdk/tree/main/go) | Go 1.18+ |
| Python | [python/](https://github.com/BOOHEEAI/sdk/tree/main/python) | Python 3.7+ |
| Java | [java/](https://github.com/BOOHEEAI/sdk/tree/main/java) | Java 8+ |
| Node.js | [nodejs/](https://github.com/BOOHEEAI/sdk/tree/main/nodejs) | Node 18+ |

### 安装

各语言均从源码引用，安装方式请参阅对应目录下的 README：

- [Go SDK](https://github.com/BOOHEEAI/sdk/blob/main/go/README.md)
- [Python SDK](https://github.com/BOOHEEAI/sdk/blob/main/python/README.md)
- [Java SDK](https://github.com/BOOHEEAI/sdk/blob/main/java/README.md)
- [Node.js SDK](https://github.com/BOOHEEAI/sdk/blob/main/nodejs/README.md)

### 快速开始

以 Python 为例：

```python
from boohee_sdk import BooheeClient, AuthMode, BaseReq, HttpMethod

class FoodSearchReq(BaseReq):
    def __init__(self, keyword: str):
        self.keyword = keyword

    def get_method(self) -> HttpMethod:
        return HttpMethod.GET

    def get_url(self) -> str:
        return '/open-apis/v1/food/search'

    def get_query_params(self):
        return {'keyword': self.keyword}

client = BooheeClient(
    api_key='your_api_key',
    auth_mode=AuthMode.API_KEY
)

resp = client.execute(FoodSearchReq('苹果'))
resp.raise_for_error()
print(resp.data)
```

### 认证模式

SDK 支持两种认证模式，与 API 文档中的认证方式一致：

- **API Key 模式**：适用于服务端调用，使用 API Key 进行认证
- **Access Token 模式**：适用于需要用户授权的场景，使用 RSA 签名获取 Access Token

### 流式接口

所有 SDK 均支持 SSE 流式接口（如食物图片识别）：

```python
for chunk in client.execute_stream(req):
    print(chunk, end='', flush=True)
```

### 问题反馈

如有问题或建议，请在 GitHub 仓库提交 [Issue](https://github.com/BOOHEEAI/sdk/issues)。

