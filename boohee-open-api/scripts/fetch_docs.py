#!/usr/bin/env python3
"""薄荷科学.AI 开放平台文档同步器：检测 references/ 是否落后于官网，并按需更新。

公开接口，无需登录。默认只做检查、不写文件。

  python3 fetch_docs.py                  # 检查漂移（退出码 0=一致 2=有变动 1=出错）
  python3 fetch_docs.py --apply          # 把变动写入 references/
  python3 fetch_docs.py --doc <code|id>  # 打印某篇文档的官网当前原文
  python3 fetch_docs.py --json           # 机器可读的差异报告
  python3 fetch_docs.py <手册code>       # 换一本手册（默认 boohee.ai）
"""
import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.boohee.com/open-interface/v1/panel/docs-index?code={}"
UA = "boohee-skill-docs-sync"

# 章序号 -> 稳定文件名，与 references/ 现有文件保持一致
CHAPTER_NAMES = {
    "一": "01-general",
    "二": "02-food-data",
    "三": "03-recognition",
    "四": "04-recipe",
    "五": "05-weight",
    "六": "06-diet",
}

# 我们自己写出的分篇标记，用于把本地文件反解成逐篇文档
MARKER = re.compile(
    r"^## (?P<title>.+)\n\n> 文档编号: `(?P<code>[^`]+)` · 更新时间: (?P<updated>.+)\n\n",
    re.M,
)
TAIL_SEP = re.compile(r"\s*\n-{3,}\s*$")


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.URLError as exc:
        sys.exit(f"ERROR 拉取失败: {exc.reason}（检查网络是否可达 api.boohee.com）")
    if payload.get("code") != 0:
        sys.exit(f"ERROR 接口异常: code={payload.get('code')} message={payload.get('message')}")
    return payload["data"]["data"]


def flatten(trees):
    """手册目录树 -> 按章分组的逐篇文档。"""
    chapters = []
    for cat in trees[0].get("sub_categories") or []:
        key = cat["name"].split("、")[0]
        fname = CHAPTER_NAMES.get(key)
        docs = {}
        for doc in sorted(cat.get("documents") or [], key=lambda d: d["position"]):
            docs[doc["code"]] = {
                "title": doc["title"],
                "updated_at": doc["updated_at"],
                "content": doc.get("content") or "",
            }
        chapters.append({"name": cat["name"], "file": fname, "docs": docs})
    return chapters


def load_local(ref_dir):
    """把 references/*.md 反解成 code -> 文档，用于与官网比对。"""
    local = {}
    if not os.path.isdir(ref_dir):
        return local
    for fn in sorted(os.listdir(ref_dir)):
        if not fn.endswith(".md") or fn.startswith("00-") or fn.endswith(".new.md"):
            continue
        text = open(os.path.join(ref_dir, fn), encoding="utf-8").read()
        hits = list(MARKER.finditer(text))
        for i, m in enumerate(hits):
            end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
            body = TAIL_SEP.sub("", text[m.end():end].rstrip())
            local[m["code"]] = {
                "title": m["title"],
                "updated_at": m["updated"].strip(),
                "content": body,
                "file": fn,
            }
    return local


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def compare(live_chapters, local):
    added, changed, renamed, missing = [], [], [], []
    seen = set()
    for ch in live_chapters:
        if ch["file"] is None:
            for code, d in ch["docs"].items():
                added.append({"code": code, "title": d["title"], "reason": "新章节未纳入", "file": None})
                seen.add(code)
            continue
        for code, d in ch["docs"].items():
            seen.add(code)
            loc = local.get(code)
            entry = {"code": code, "title": d["title"], "file": ch["file"],
                     "updated_at": d["updated_at"]}
            if loc is None:
                added.append(entry)
            elif sha(loc["content"]) != sha(d["content"].rstrip()):
                entry["local_updated_at"] = loc["updated_at"]
                entry["delta"] = len(d["content"]) - len(loc["content"])
                changed.append(entry)
            elif loc["updated_at"] != d["updated_at"]:
                entry["local_updated_at"] = loc["updated_at"]
                renamed.append(entry)
    for code, loc in local.items():
        if code not in seen:
            missing.append({"code": code, "title": loc["title"], "file": loc["file"]})
    return {"added": added, "changed": changed, "touched": renamed, "removed": missing}


def render(rep):
    lines = []
    for kind, label in (("changed", "内容已变动"), ("added", "本地缺失"),
                        ("touched", "仅时间戳变动"), ("removed", "官网已删除")):
        items = rep[kind]
        if not items:
            continue
        lines.append(f"[{kind}] {label} {len(items)} 篇：")
        for it in items[:40]:
            extra = ""
            if kind == "changed":
                extra = f"（{it.get('local_updated_at')} → {it['updated_at']}，正文 {it['delta']:+d} 字符）"
            elif kind == "touched":
                extra = f"（{it.get('local_updated_at')} → {it['updated_at']}）"
            lines.append(f"  - {it['title']}  code={it['code']}  {it.get('file') or '-'} {extra}")
        if len(items) > 40:
            lines.append(f"  ... 另有 {len(items) - 40} 篇")
    return "\n".join(lines) if lines else "一致：本地 references/ 与官网当前版本逐篇比对无差异。"


def apply_writes(live_chapters, ref_dir):
    written = []
    for ch in live_chapters:
        fname = ch["file"] or f"{ch['name']}.new"
        parts = [f"# {ch['name']}\n"]
        for code, d in ch["docs"].items():
            parts.append(
                f"\n---\n\n## {d['title']}\n\n"
                f"> 文档编号: `{code}` · 更新时间: {d['updated_at']}\n\n{d['content']}\n"
            )
        path = os.path.join(ref_dir, f"{fname}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(parts))
        written.append((os.path.basename(path), len(ch["docs"])))
    return written


def show_doc(token, live_chapters, limit):
    for ch in live_chapters:
        for code, d in ch["docs"].items():
            if token != code:
                continue
            body = d["content"]
            print(f"# {d['title']}  (code={code} · 更新时间 {d['updated_at']} · {len(body)} 字符)")
            print(f"# 所属章节: {ch['name']} -> references/{ch['file'] or '未纳入'}.md")
            print()
            if len(body) > limit:
                print(body[:limit])
                print(f"\n... [已截断 {len(body) - limit} 字符；去掉 --truncate 或调大 --truncate 取全文]")
            else:
                print(body)
            return True
    print(f"未找到 code/序号为 {token} 的文档。用 --check 看当前收录了哪些。")
    return False


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="同步薄荷开放平台文档到 references/", add_help=True)
    ap.add_argument("code", nargs="?", default="boohee.ai", help="手册 code，默认 boohee.ai")
    ap.add_argument("--apply", action="store_true", help="把变动写入 references/")
    ap.add_argument("--doc", metavar="CODE", help="打印指定文档的官网当前原文")
    ap.add_argument("--json", action="store_true", help="输出机器可读差异报告")
    ap.add_argument("--truncate", type=int, default=6000, help="--doc 的截断长度，默认 6000")
    ap.add_argument("-o", "--out", default=os.path.join(here, "..", "references"), help="references 目录")
    args = ap.parse_args()

    ref_dir = os.path.abspath(args.out)
    trees = http_json(API.format(args.code))
    if not trees:
        sys.exit(f"ERROR 手册 {args.code} 无内容")
    chapters = flatten(trees)

    if args.doc:
        sys.exit(0 if show_doc(args.doc, chapters, args.truncate) else 1)

    rep = compare(chapters, load_local(ref_dir))
    drift = any(rep[k] for k in rep)

    if args.json:
        print(json.dumps({"manual": trees[0]["name"], "drift": drift, **rep}, ensure_ascii=False, indent=2))
    else:
        print(f"手册: {trees[0]['name']} (code={args.code}) · 官网 {sum(len(c['docs']) for c in chapters)} 篇")
        print(render(rep))

    if args.apply:
        os.makedirs(ref_dir, exist_ok=True)
        for name, n in apply_writes(chapters, ref_dir):
            print(f"  写入 {name}（{n} 篇）")
        print("已更新 references/。注意：SKILL.md 与 references/00-endpoints.md 是人工整理的索引，"
              "需按上面的变动同步复核，然后 git diff 交人工确认后再提交。")
    elif drift:
        print("\n本地落后于官网。执行 `python3 scripts/fetch_docs.py --apply` 更新 references/。")

    sys.exit(2 if drift else 0)


if __name__ == "__main__":
    main()
