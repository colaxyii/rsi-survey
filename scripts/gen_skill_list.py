#!/usr/bin/env python3
"""Render the installed-skills inventory as an Obsidian-flavoured markdown note."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "skills.json")
OUT = os.path.join(HERE, "..", "技能清单.md")
SCAN_DATE = "2026-10-13"

CATEGORIES = [
    ("系统内置", [
        "imagegen", "openai-docs", "review-agent", "skill-creator", "skill-installer",
    ]),
    ("插件附带（已启用）", [
        "documents", "pdf", "presentations", "spreadsheets", "excel-live-control",
        "template-creator", "visualize",
    ]),
    ("调研与检索", [
        "agent-reach", "arxiv", "media-crawler", "yichen-web-research", "paper-xray",
    ]),
    ("写作与研究", [
        "research-paper-writing", "writing-plans", "humanizer", "creative-ideation",
    ]),
    ("图像生成", [
        "openai-gpt-image", "black-forest-labs-flux", "bytedance-seedream",
    ]),
    ("视频生成", [
        "google-veo", "kling-video", "minimax-hailuo-video", "seedance-2-0",
    ]),
    ("音视频后期与质检", [
        "editing-montage", "social-short-production", "ffmpeg-media-finishing", "generated-media-qa",
    ]),
    ("音频 / 语音 / 音乐", [
        "elevenlabs-tts", "elevenlabs-sound-effects", "minimax-speech",
        "volcengine-doubao-speech-tts", "suno-music",
    ]),
    ("设计与文档产出", [
        "claude-design", "huashu-design", "sketch", "popular-web-designs",
        "guizang-social-card-skill", "powerpoint",
    ]),
    ("社交平台发布", [
        "auto-redbook-skills", "xiaohongshu-upload", "douyin-upload", "bilibili-upload",
        "kuaishou-upload",
    ]),
    ("开发与运行环境", [
        "jupyter-live-kernel",
    ]),
]

DISABLED = ["plugin-management", "create-pet", "pets", "update-pet"]

FORTUNE = [
    "bazi", "horosa-agent", "lenormand", "mingli-master", "mingyu", "taibu-divination",
    "tarot", "tarot-guide", "tarot-waite", "yijing-suangua",
    "vedic-calculator", "vedic-core", "vedic-prashna", "vedic-reader",
]

# short Chinese/English labels overriding the long frontmatter blurbs
LABELS = {
    "imagegen": "文生图 / 改图（系统内置的图像生成能力）",
    "openai-docs": "OpenAI / Codex 官方文档查询与自述类问题",
    "review-agent": "对指定代码改动做只读、缺陷优先的评审",
    "skill-creator": "创建或更新一个 Codex skill",
    "skill-installer": "从精选列表或 GitHub 仓库安装 skill",
    "documents": "创建 / 编辑 / 批注 .docx 文档，带渲染校验",
    "pdf": "读写、渲染、校验 PDF（含 AcroForm 表单）",
    "presentations": "创建 / 编辑 PPTX 与 Google Slides",
    "spreadsheets": "创建 / 编辑 / 分析 xlsx、csv，公式与图表",
    "excel-live-control": "通过 ChatGPT 插件控制正在打开的 Excel",
    "template-creator": "从参考稿提炼可复用的 artefact 模板 skill",
    "visualize": "在对话里直接生成可视化与可交互小工具",
    "agent-reach": "16 平台互联网调研路由器（小红书/X/Reddit/B站/YouTube 等）",
    "arxiv": "按关键词 / 作者 / 分类检索 arXiv 论文，附 Semantic Scholar",
    "media-crawler": "基于 MediaCrawler 的多平台公开信息采集",
    "yichen-web-research": "跨平台跨阶段的系统深度研究总入口",
    "paper-xray": "讲透单篇论文：还原思路、讲透公式、怀疑式审读",
    "research-paper-writing": "面向 NeurIPS / ICML / ICLR 的论文写作",
    "writing-plans": "动代码前先把多步任务写成计划",
    "humanizer": "改写掉 AI 味，保留原意",
    "creative-ideation": "用命名方法做创意发散",
    "openai-gpt-image": "OpenAI GPT Image 系列生图与改图",
    "black-forest-labs-flux": "FLUX.2 系列生图、编辑、微调与部署",
    "bytedance-seedream": "字节 Seedream 生图与自然语言改图",
    "google-veo": "Google Veo 视频生成（含原生音频）",
    "kling-video": "快手可灵视频生成与运镜控制",
    "minimax-hailuo-video": "MiniMax 海螺视频生成 API",
    "seedance-2-0": "字节 Seedance 2.0 视频生成",
    "editing-montage": "剪辑与蒙太奇设计（节奏、转场、匹配剪辑）",
    "social-short-production": "竖版短视频从策划到成片交付",
    "ffmpeg-media-finishing": "ffmpeg 转码、规格化、字幕、批量导出的收尾流程",
    "generated-media-qa": "AI 生成媒体的质量验收与合规检查",
    "elevenlabs-tts": "ElevenLabs 语音合成与声音克隆",
    "elevenlabs-sound-effects": "ElevenLabs 音效生成",
    "minimax-speech": "MiniMax 语音合成、克隆与音色设计",
    "volcengine-doubao-speech-tts": "火山引擎豆包语音合成",
    "suno-music": "Suno 音乐生成与版权边界判断",
    "claude-design": "一次性 HTML 设计稿（落地页 / 幻灯片 / 原型）",
    "huashu-design": "花叔 Design：HTML 高保真原型、幻灯片、动画",
    "sketch": "一次性 HTML 草稿，出 2-3 个方案对比",
    "popular-web-designs": "54 套真实设计系统（Stripe / Linear / Vercel 等）",
    "guizang-social-card-skill": "归藏风格社媒卡片、实况照片拼图、公众号封面",
    "powerpoint": "python-pptx 读写 .pptx",
    "auto-redbook-skills": "小红书笔记素材创作（标题 + 正文 + 图片卡片）",
    "xiaohongshu-upload": "小红书登录校验与图文 / 视频发布",
    "douyin-upload": "抖音登录校验与图文 / 视频发布",
    "bilibili-upload": "B 站登录校验与视频上传",
    "kuaishou-upload": "快手登录校验与图文 / 视频发布",
    "plugin-management": "发现 / 建议可用插件，检查插件权限与依赖",
    "create-pet": "创建、修复、校验、预览、上传 ChatGPT 动画宠物",
    "pets": "列出 / 选择 / 下载 / 删除 ChatGPT 动画宠物",
    "update-pet": "检查 / 校验 / 修复 / 更新自定义动画宠物",
    "huashu-nuwa": "女娲造人：调研 → 思维框架提炼 → 生成人物视角 Skill",
    "jupyter-live-kernel": "对接本地常驻 Jupyter kernel 做交互式计算",
}


def one_line(desc, limit=150):
    desc = re.sub(r"\s+", " ", desc or "").strip()
    if not desc:
        return ""
    cut = len(desc)
    for mark in ("。", "！", "；", ". ", "．"):
        i = desc.find(mark)
        if 0 < i < limit:
            cut = min(cut, i + len(mark))
    return desc[: min(cut, limit)].strip()


def main():
    skills = json.load(open(SRC))
    by_name = {}
    for s in skills:
        name = s["name"].lower()  # frontmatter varies in case (Presentations vs presentations)
        s = dict(s, name=name)
        if name == "xhs-note-creator":  # nested duplicate of auto-redbook-skills
            continue
        prev = by_name.get(name)
        if prev is None or len(s["dir"]) < len(prev["dir"]):
            by_name[name] = s

    seen = set()
    lines = []
    lines.append("---")
    lines.append('title: "已安装技能清单"')
    lines.append('aliases: ["skill 清单", "技能目录"]')
    lines.append("tags: [skills, tools, index]")
    lines.append(f"added: {SCAN_DATE}")
    lines.append(f"scan_date: {SCAN_DATE}")
    lines.append("---")
    lines.append("")
    lines.append("# 已安装技能清单")
    lines.append("")
    lines.append(
        f"> 扫描时间 **{SCAN_DATE}** ｜ 来源 `~/.codex/skills/` 与 `~/.codex/plugins/cache/`"
    )
    lines.append(">")
    lines.append(
        f"> 共 **{len(by_name) - len([d for d in DISABLED if d in by_name])} 个在用技能**"
        f"，另有 {len(DISABLED)} 个已下载但未启用。"
    )
    lines.append("")
    lines.append("## 一览")
    lines.append("")
    lines.append("| 分类 | 数量 |")
    lines.append("|---|---|")
    for cat, names in CATEGORIES:
        lines.append(f"| {cat} | {len([n for n in names if n in by_name])} |")
    lines.append(
        "| 思维框架与人物视角 | "
        f"{len([n for n in by_name if n.startswith('huashu-nuwa') or n.endswith('-perspective') or n == 'x-mastery-mentor'])} |"
    )
    lines.append(f"| 命理与占卜 | {len([n for n in FORTUNE if n in by_name])} |")
    lines.append("")

    for cat, names in CATEGORIES:
        present = [n for n in names if n in by_name]
        if not present:
            continue
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| 技能 | 说明 | 位置 |")
        lines.append("|---|---|---|")
        for n in present:
            s = by_name[n]
            seen.add(n)
            desc = LABELS.get(n) or one_line(s["description"])
            rel = "~/.codex/skills/" + s["rel"] if s["kind"] == "user" else "plugins/" + s["rel"]
            lines.append(f"| `{n}` | {desc} | `{rel}` |")
        lines.append("")

    # fortune-telling group
    lines.append("## 命理与占卜")
    lines.append("")
    lines.append("| 技能 | 说明 | 位置 |")
    lines.append("|---|---|---|")
    for n in FORTUNE:
        if n not in by_name:
            continue
        s = by_name[n]
        seen.add(n)
        desc = LABELS.get(n) or one_line(s["description"], 110)
        lines.append(f"| `{n}` | {desc} | `~/.codex/skills/{s['rel']}` |")
    lines.append("")

    # perspective group
    persp = sorted(
        n for n in by_name
        if (n.startswith("huashu-nuwa") or n.endswith("-perspective") or n == "x-mastery-mentor")
        and n not in seen
    )
    lines.append("## 思维框架与人物视角")
    lines.append("")
    lines.append("> 由 `huashu-nuwa`（女娲造人）蒸馏生成的人物视角 Skill，调用方式如「用芒格的视角看这个决策」。")
    lines.append("")
    lines.append("| 技能 | 说明 | 位置 |")
    lines.append("|---|---|---|")
    for n in persp:
        s = by_name[n]
        seen.add(n)
        desc = LABELS.get(n) or one_line(s["description"], 110)
        lines.append(f"| `{n}` | {desc} | `~/.codex/skills/{s['rel']}` |")
    lines.append("")

    rest = sorted(set(by_name) - seen - set(DISABLED))
    if rest:
        lines.append("## 其他")
        lines.append("")
        lines.append("| 技能 | 说明 | 位置 |")
        lines.append("|---|---|---|")
        for n in rest:
            s = by_name[n]
            desc = LABELS.get(n) or one_line(s["description"], 110)
            lines.append(f"| `{n}` | {desc} | `~/.codex/skills/{s['rel']}` |")
        lines.append("")

    lines.append("## 已下载但未启用")
    lines.append("")
    lines.append("| 技能 | 说明 | 位置 |")
    lines.append("|---|---|---|")
    for n in DISABLED:
        s = by_name.get(n)
        if not s:
            continue
        lines.append(f"| `{n}` | {one_line(s['description'], 110)} | `plugins/{s['rel']}` |")
    lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append("- 技能目录由 Codex 启动时扫描 `~/.codex/skills/**/SKILL.md` 与已启用插件生成；")
    lines.append("  插件开关在 `~/.codex/config.toml` 的 `[plugins.\"...\"]` 段里。")
    lines.append("- 上表「位置」列为磁盘路径，排查「为什么这个技能没生效」时先看这里。")
    lines.append("- 新增技能后重跑 `scripts/scan_skills.py` + `scripts/gen_skill_list.py` 即可刷新本文件。")

    open(OUT, "w").write("\n".join(lines) + "\n")
    print("written:", OUT)
    print("active skills:", len([n for n in by_name if n not in DISABLED]), "disabled:", len(DISABLED))


if __name__ == "__main__":
    main()
