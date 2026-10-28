#!/usr/bin/env python3
"""技能本地配置：存放 API 凭证与个人资料，供调用接口时自动读取。

config.json 只留在本机、不随技能包分发，权限 0600。API Key 就放在文件最上方
api_key 那一行（模板里用 ★ 标注）。环境变量 BOOHEE_API_KEY 优先于文件内容。

config.json 默认放在技能目录；技能目录不可写（只读安装、容器只读挂载）时自动改用
~/.boohee-open-api/config.json。旧位置的 config.json 仍会被读取，下次写入时迁移到
当前可写位置。实际路径以 init/show 的输出为准。

下文 `<技能目录>` 一律指 SKILL.md 所在目录（即本脚本所在目录的上一级）的绝对路径，
不要依赖当前工作目录。

  python3 <技能目录>/scripts/config.py init                    # 从 config.example.json 生成 config.json
  python3 <技能目录>/scripts/config.py check                   # 凭证门禁：KEY_OK / NO_KEY（退出码 0/1）
  python3 <技能目录>/scripts/config.py show                    # 查看当前配置（密钥脱敏）
  python3 <技能目录>/scripts/config.py get profile.user_id     # 取值
  python3 <技能目录>/scripts/config.py set api_key 'sk-xxx'     # 写凭证
  python3 <技能目录>/scripts/config.py set profile.gender 1    # 写资料（1男 2女）
  python3 <技能目录>/scripts/config.py set profile.latest_weight 68.5  # 同步写体重记录接口
  python3 <技能目录>/scripts/config.py unset api_key           # 清空某个值
  python3 <技能目录>/scripts/config.py call GET /v2/weight/latest       # 带凭证调接口，自动合并 profile
  python3 <技能目录>/scripts/config.py call POST /v2/weight/record --json '{"weight":68.5}'
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import quote, urlsplit, urlunsplit

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SELF = os.path.abspath(__file__)
LOCAL_CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
USER_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".boohee-open-api")
USER_CONFIG_PATH = os.path.join(USER_CONFIG_DIR, "config.json")
# 技能目录可写就存技能目录，否则退到用户目录，避免只读安装下整条配置链路失效
CONFIG_PATH = LOCAL_CONFIG_PATH if os.access(SKILL_DIR, os.W_OK) else USER_CONFIG_PATH
EXAMPLE_PATH = os.path.join(SKILL_DIR, "config.example.json")
DEFAULT_BASE_URL = "https://api.boohee.com/open-apis"
SECRET_KEYS = ("api_key",)
ENV_OVERRIDES = {"api_key": "BOOHEE_API_KEY"}
# 旧版本遗留的开发者字段：读取时丢弃，避免 show 明文带出 app_secret / access_token
LEGACY_KEYS = {"_advanced_title", "app_id", "app_secret", "rsa_private_key_path",
               "token", "webhook", "base_url", "notes"}
# 模板里的占位文案（改这里即可，运行时判定不依赖它完全一致）
API_KEY_PLACEHOLDER = ">>>>在这里填写你的key<<<<<"

STAR_NOTICE = f"★★★★★ API Key 填在 {CONFIG_PATH} 最上面的 api_key 那一行（控制台 https://ai.boohee.com/console/ →「API Key 管理」创建）★★★★★"

# 与 config.example.json 保持一致（该文件缺失时的兜底模板）
TEMPLATE = {
    "_step1_title": "★★★★★★★★★★★★★ 第 1 步（必填 · 只需要这一个就能跑起来）★★★★★★★★★★★★★",
    "_step1_hint": "key 在控制台 https://ai.boohee.com/console/ →「API Key 管理」创建，sk- 开头，整串填进下面 api_key 那一行。",
    "api_key": API_KEY_PLACEHOLDER,
    "_step2_title": "第 2 步（可选 · 不填也能查食物，填了才能记录与生成食谱）",
    "profile": {
        "user_id": "",
        "gender": None,
        "latest_weight": None,
        "energy": None,
        "height": None,
        "age": None,
        "goal": "",
        "diet_favor": "",
        "diet_area": "",
        "diet_mode": [],
        "weight_management": None,
        "nutrition_management": None,
        "ban_foods": [],
        "illness": [],
        "updated_at": None,
    },
}


def config_source():
    """读哪个文件：优先当前写入位置，其次另一处（兼容换过位置的旧配置）。"""
    other = USER_CONFIG_PATH if CONFIG_PATH == LOCAL_CONFIG_PATH else LOCAL_CONFIG_PATH
    for path in (CONFIG_PATH, other):
        if os.path.exists(path):
            return path
    return None


def normalize(cfg):
    """丢弃旧版本的开发者字段，保证展示与回写都不再带 app_secret / access_token。"""
    for key in LEGACY_KEYS:
        cfg.pop(key, None)
    cfg.setdefault("profile", {})
    return cfg


def load_config():
    path = config_source()
    if not path:
        sys.exit(
            f"ERROR 还没有配置文件（已查找 {LOCAL_CONFIG_PATH} 与 {USER_CONFIG_PATH}）\n"
            f"先执行 python3 {SELF} init"
        )
    with open(path, encoding="utf-8") as fp:
        cfg = json.load(fp)
    for key, env in ENV_OVERRIDES.items():
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return normalize(cfg)


def save_config(cfg):
    cfg = normalize(cfg)
    cfg["profile"]["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    tmp = CONFIG_PATH + ".tmp"
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), mode=0o700, exist_ok=True)
        with open(tmp, "w", encoding="utf-8") as fp:
            json.dump(cfg, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
        os.replace(tmp, CONFIG_PATH)
        os.chmod(CONFIG_PATH, 0o600)
    except OSError as exc:
        sys.exit(f"ERROR 无法写入 {CONFIG_PATH}：{exc}")
    print(f"已写入 {CONFIG_PATH}")


def dig(obj, path):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(path)
        cur = cur[part]
    return cur


def punch(obj, path, value):
    parts = path.split(".")
    cur = obj
    for part in parts[:-1]:
        if part not in cur or not isinstance(cur[part], dict):
            raise KeyError(f"未知配置项：{path}")
        cur = cur[part]
    if parts[-1] not in cur:
        raise KeyError(f"未知配置项：{path}")
    cur[parts[-1]] = value
    return obj


def parse_scalar(raw):
    if raw in ("", "null"):
        return None if raw == "null" else ""
    if raw == "true":
        return True
    if raw == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    if raw.startswith("[") or raw.startswith("{"):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            sys.exit(f"ERROR 值不是合法 JSON：{exc}")
    return raw


def mask(value):
    if not isinstance(value, str) or not value:
        return value
    if len(value) <= 8:
        return "****"
    return f"{value[:5]}…{value[-2:]}（{len(value)} 位，已脱敏）"


def mask_tree(node, prefix=""):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            path = f"{prefix}{k}"
            out[k] = mask(v) if is_secret(path) and isinstance(v, str) and v else mask_tree(v, path + ".")
        return out
    if isinstance(node, list):
        return [mask_tree(i, prefix) for i in node]
    return node


def usable_api_key(value):
    """占位文案或含中文的值不算已填：HTTP 请求头只能是 ASCII，放行会直接崩在发送环节。"""
    if not value or value == API_KEY_PLACEHOLDER:
        return False
    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def has_api_key(cfg):
    return usable_api_key(cfg.get("api_key") or "")


def credential_headers(cfg):
    if not has_api_key(cfg):
        sys.exit(
            "ERROR 没有可用凭证。\n"
            f"  {STAR_NOTICE}\n"
            f"  命令写入：python3 {SELF} set api_key 'sk-xxx'\n"
            "  或手动编辑：上面路径的 config.json 顶部 api_key 那一行的占位文字替换成真实密钥"
        )
    api_key = cfg["api_key"]
    if not api_key.startswith("sk-"):
        print(f"提示：api_key 不是 sk- 开头，请确认已从控制台完整复制：{mask(api_key)}")
    return {"X-Api-Key": api_key}


def http_call(method, path, body, headers):
    url = path if path.startswith("http") else DEFAULT_BASE_URL + path
    # 允许直接写中文参数（?keyword=牛奶），这里统一转成 percent-encoded ASCII
    parts = urlsplit(url)
    url = urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/%"),
                      quote(parts.query, safe="=&%"), parts.fragment))
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        sys.exit(f"ERROR HTTP {exc.code}: {exc.read().decode(errors='replace')[:400]}")
    except urllib.error.URLError as exc:
        sys.exit(f"ERROR 请求失败: {exc.reason}")


def sync_weight(cfg, weight, record_on):
    if not weight:
        return
    user_id = cfg["profile"].get("user_id")
    if not user_id:
        print("提示：profile.user_id 为空，体重只记在本地配置，未写入接口。")
        return
    body = {"user_id": user_id, "weight": weight}
    if record_on:
        body["record_on"] = record_on
    resp = http_call("POST", "/v2/weight/record", body, {**credential_headers(cfg), "Content-Type": "application/json"})
    if resp.get("code") == 0:
        print("体重已写入 /v2/weight/record。")
    else:
        print(f"警告：本地已更新，但体重接口未成功：code={resp.get('code')} message={resp.get('message')}")


def cmd_init(_args):
    existing = config_source()
    if existing:
        sys.exit(f"{existing} 已存在，未覆盖。要重置请先手动删除。")
    template = TEMPLATE
    if os.path.exists(EXAMPLE_PATH):
        try:
            with open(EXAMPLE_PATH, encoding="utf-8") as fp:
                template = json.load(fp)
        except json.JSONDecodeError as exc:
            print(f"警告：config.example.json 解析失败（{exc}），改用脚本内置模板。")
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), mode=0o700, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as fp:
            json.dump(template, fp, ensure_ascii=False, indent=2)
            fp.write("\n")
        os.chmod(CONFIG_PATH, 0o600)
    except OSError as exc:
        sys.exit(f"ERROR 无法写入 {CONFIG_PATH}：{exc}")
    print(f"已创建 {CONFIG_PATH}（0600，只留在本机，不随技能包分发）")
    print(STAR_NOTICE)
    print(f"手动填写：打开文件，把 api_key 那一行的「{API_KEY_PLACEHOLDER}」换成真实密钥。")
    print(f"或交给助手：python3 {SELF} set api_key 'sk-xxx'")


def cmd_check(_args):
    """凭证门禁：首行给 Agent 可机械判断的状态，退出码 0=有凭证，1=没有。"""
    path = config_source()
    cfg = {}
    if path:
        try:
            with open(path, encoding="utf-8") as fp:
                cfg = json.load(fp)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"NO_KEY {path}")
            print(f"  配置文件读不出来：{exc}")
            print(f"  修复：删除后重新 python3 {SELF} init")
            sys.exit(1)
    for key, env in ENV_OVERRIDES.items():
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    normalize(cfg)
    if has_api_key(cfg):
        print(f"KEY_OK {path or '-'}")
        return
    print(f"NO_KEY {path or '-'}")
    print("  获取：https://ai.boohee.com/console/ → 登录/注册 →「API Key 管理」→ 创建 → 复制 sk- 开头的完整密钥")
    print(f"  写入：python3 {SELF} set api_key 'sk-xxx'（还没有配置文件时先 python3 {SELF} init）")
    print("  填好后重新运行 check")
    sys.exit(1)


def cmd_show(_args):
    cfg = load_config()
    print(STAR_NOTICE)
    api_key = cfg.get("api_key") or ""
    if not usable_api_key(api_key):
        reason = "还是占位值/空" if api_key in ("", API_KEY_PLACEHOLDER) else "含中文等非法字符，不会被当作密钥发出"
        print(f"当前 api_key 不可用（{reason}），填写位置见上面提示\n")
    print(json.dumps(mask_tree(cfg), ensure_ascii=False, indent=2))


def cmd_get(args):
    cfg = load_config()
    try:
        value = dig(cfg, args.path)
    except KeyError:
        sys.exit(f"ERROR 未知配置项：{args.path}")
    if args.path == "api_key" and not usable_api_key(value if isinstance(value, str) else ""):
        sys.exit(f"ERROR api_key 还没填成可用密钥（占位或含中文）。\n  {STAR_NOTICE}")
    if args.secret:
        print(value)
        return
    print(json.dumps(mask(value) if is_secret(args.path) else value, ensure_ascii=False))


def cmd_set(args):
    cfg = load_config()
    value = parse_scalar(args.value)
    try:
        punch(cfg, args.path, value)
    except KeyError as exc:
        sys.exit(f"ERROR {exc}")
    save_config(cfg)
    print(f"{args.path} = {mask(value) if is_secret(args.path) else json.dumps(value, ensure_ascii=False)}")
    if args.path in ("profile.latest_weight", "profile.weight"):
        if args.no_sync:
            print("已跳过体重记录接口同步（--no-sync）。")
        else:
            sync_weight(cfg, value, args.record_on)


def is_secret(path):
    return path.split(".")[-1] in SECRET_KEYS


def empty_like(value, path=""):
    if is_secret(path):
        return ""
    if isinstance(value, (list, dict)):
        return type(value)()
    if isinstance(value, (int, float, bool)) or value is None:
        return None
    return ""


def cmd_unset(args):
    cfg = load_config()
    try:
        punch(cfg, args.path, empty_like(dig(cfg, args.path), args.path))
    except KeyError as exc:
        sys.exit(f"ERROR {exc}")
    save_config(cfg)
    print(f"{args.path} 已清空")


def cmd_call(args):
    cfg = load_config()
    path = args.path if args.path.startswith("/") else "/" + args.path
    headers = {**credential_headers(cfg), "Accept": "application/json"}
    body = None
    if args.method.upper() == "POST":
        body = json.loads(args.json) if args.json else {}
        if not args.no_merge_profile:
            profile = {k: v for k, v in cfg["profile"].items() if k not in ("updated_at", "goal") and v not in (None, "", [])}
            body = {**profile, **body}
        headers["Content-Type"] = "application/json"
    print(json.dumps(http_call(args.method.upper(), path, body, headers), ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="薄荷开放平台技能本地配置")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="生成 config.json").set_defaults(func=cmd_init)
    sub.add_parser("check", help="检查是否已有可用 API Key（KEY_OK / NO_KEY）").set_defaults(func=cmd_check)
    sub.add_parser("show", help="查看配置（脱敏）").set_defaults(func=cmd_show)

    p_get = sub.add_parser("get", help="读取一个配置项")
    p_get.add_argument("path")
    p_get.add_argument("--secret", action="store_true", help="输出原值（供脚本取用，禁止回显给用户或写日志）")
    p_get.set_defaults(func=cmd_get)

    p_set = sub.add_parser("set", help="写入一个配置项")
    p_set.add_argument("path")
    p_set.add_argument("value")
    p_set.add_argument("--no-sync", action="store_true", help="写 profile.latest_weight 时不调体重记录接口")
    p_set.add_argument("--record-on", help="体重记录日期 YYYY-MM-DD，默认当天")
    p_set.set_defaults(func=cmd_set)

    p_unset = sub.add_parser("unset", help="清空一个配置项")
    p_unset.add_argument("path")
    p_unset.set_defaults(func=cmd_unset)

    p_call = sub.add_parser("call", help="带配置里的凭证调用接口")
    p_call.add_argument("method", choices=["GET", "POST", "get", "post"])
    p_call.add_argument("path")
    p_call.add_argument("--json", help="POST 的 body JSON")
    p_call.add_argument("--no-merge-profile", action="store_true", help="不自动把 profile 合并进 body")
    p_call.set_defaults(func=cmd_call)

    ns = parser.parse_args()
    ns.func(ns)


if __name__ == "__main__":
    main()
