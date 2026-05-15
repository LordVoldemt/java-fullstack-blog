from pathlib import Path
import html
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "public" / "assets" / "presentations"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTICLES = [
    {
        "md": DOCS / "microservices" / "redis" / "redis-overview.md",
        "slug": "redis-overview",
        "title": "Redis 入门",
        "summary": "缓存、分布式锁、排行榜与高频坑位，一次看清 Redis 在工程里的角色。",
        "route": "../../presentations/redis-overview-ppt",
    },
    {
        "md": DOCS / "microservices" / "spring-cloud-alibaba" / "spring-cloud-alibaba-overview.md",
        "slug": "spring-cloud-alibaba-overview",
        "title": "Spring Cloud Alibaba 入门",
        "summary": "Nacos、Feign、Gateway、Sentinel、Seata 的协作地图与最小调用链。",
        "route": "../../presentations/spring-cloud-alibaba-overview-ppt",
    },
    {
        "md": DOCS / "ai" / "llm-basics" / "llm-basics-overview.md",
        "slug": "llm-basics-overview",
        "title": "大模型基础入门",
        "summary": "Prompt、Embedding、RAG、工具调用与 MCP 的关系，一次串成完整地图。",
        "route": "../../presentations/llm-basics-overview-ppt",
    },
    {
        "md": DOCS / "ai" / "ai-app-dev" / "ai-app-dev-overview.md",
        "slug": "ai-app-dev-overview",
        "title": "AI 应用开发入门",
        "summary": "从模型接入到 RAG、工具调用与可观测性，面向 Java 开发者的落地路径。",
        "route": "../../presentations/ai-app-dev-overview-ppt",
    },
    {
        "md": DOCS / "project" / "java-projects" / "java-projects-overview.md",
        "slug": "java-projects-overview",
        "title": "Java 项目实战入门",
        "summary": "从功能开发到系统交付，梳理项目经验到底该怎么积累和表达。",
        "route": "../../presentations/java-projects-overview-ppt",
    },
    {
        "md": DOCS / "project" / "ai-projects" / "ai-projects-overview.md",
        "slug": "ai-projects-overview",
        "title": "AI 项目实战入门",
        "summary": "从模型 Demo 到可交付系统，聚焦知识、工具、成本和治理的全链路。",
        "route": "../../presentations/ai-projects-overview-ppt",
    },
    {
        "md": DOCS / "project" / "blog-build" / "blog-build-overview.md",
        "slug": "blog-build-overview",
        "title": "博客搭建与部署入门",
        "summary": "把技术博客当作长期知识系统来建设，兼顾结构、流程和发布体验。",
        "route": "../../presentations/blog-build-overview-ppt",
    },
]

SECTION_RE = re.compile(r"^##\s+(.+)$", re.M)

SVG = """<svg viewBox="0 0 24 24" role="img">
      <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8A2.5 2.5 0 0 1 17.5 16H13v2.4l3.1 1.55a1 1 0 0 1-.9 1.8L12 20.15l-3.2 1.6a1 1 0 0 1-.9-1.8L11 18.4V16H6.5A2.5 2.5 0 0 1 4 13.5v-8Zm2.5-.5a.5.5 0 0 0-.5.5v8a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 .5-.5v-8a.5.5 0 0 0-.5-.5h-11Zm2.25 3.25a1 1 0 0 1 1-1h4.5a1 1 0 1 1 0 2h-4.5a1 1 0 0 1-1-1Zm0 3a1 1 0 0 1 1-1h2.5a1 1 0 1 1 0 2h-2.5a1 1 0 0 1-1-1Z" />
    </svg>"""

STYLE = """
:root {
  --bg: #04110d;
  --panel: rgba(8, 25, 20, 0.84);
  --panel-strong: rgba(10, 32, 25, 0.94);
  --card: rgba(13, 38, 30, 0.94);
  --line: rgba(55, 180, 146, 0.28);
  --mint: #36f0c0;
  --cyan: #49c6ff;
  --text: #ecfff9;
  --muted: #99cfc1;
  --shadow: 0 24px 80px rgba(0, 0, 0, 0.38);
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  min-height: 100%;
  background:
    radial-gradient(circle at top right, rgba(73, 198, 255, 0.14), transparent 28%),
    radial-gradient(circle at bottom left, rgba(54, 240, 192, 0.12), transparent 30%),
    linear-gradient(135deg, #03100c 0%, #071713 52%, #03100d 100%);
  color: var(--text);
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", Arial, sans-serif;
}
body { overflow: hidden; }
button, a { font: inherit; }
.deck {
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
}
.slide {
  display: none;
  position: relative;
  width: min(100vw, 177.78vh);
  height: min(56.25vw, 100vh);
  padding: 5.2% 5.8%;
  overflow: hidden;
  background:
    radial-gradient(circle at 84% 16%, rgba(73, 198, 255, 0.14), transparent 28%),
    radial-gradient(circle at 8% 88%, rgba(54, 240, 192, 0.12), transparent 24%),
    linear-gradient(135deg, rgba(4, 17, 13, 0.96) 0%, rgba(7, 22, 17, 0.98) 55%, rgba(4, 15, 12, 0.96) 100%);
}
.slide.active { display: block; }
.top-line {
  position: absolute;
  inset: 0 0 auto 0;
  height: 8px;
  background: linear-gradient(90deg, var(--mint), var(--cyan));
}
.page-no {
  position: absolute;
  right: 5.8%;
  bottom: 4.8%;
  color: var(--muted);
  font-size: clamp(11px, 1vw, 15px);
  letter-spacing: 0.04em;
}
.kicker {
  margin: 0 0 0.7rem;
  color: var(--mint);
  font-size: clamp(13px, 1.2vw, 18px);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
h1, h2, h3, p { margin: 0; }
h1, h2 {
  line-height: 1.08;
  letter-spacing: 0;
}
h1 { font-size: clamp(40px, 5.6vw, 78px); max-width: 70%; }
h2 { font-size: clamp(26px, 3.2vw, 46px); max-width: 88%; }
.subtitle {
  margin-top: 0.85rem;
  max-width: 78%;
  color: var(--muted);
  font-size: clamp(15px, 1.4vw, 21px);
  line-height: 1.55;
}
.cover-grid {
  display: grid;
  grid-template-columns: 1.25fr 0.95fr;
  align-items: center;
  gap: 5%;
  height: 100%;
}
.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.72rem;
  margin-top: 2rem;
}
.tag-row span, .step b {
  display: inline-grid;
  place-items: center;
  min-width: 5.6rem;
  min-height: 2.1rem;
  padding: 0.3rem 0.88rem;
  border-radius: 999px;
  border: 1px solid rgba(73, 198, 255, 0.38);
  background: rgba(12, 36, 29, 0.76);
  color: var(--cyan);
  font-weight: 800;
}
.orbit {
  position: relative;
  min-height: min(44vw, 420px);
  border-radius: 24px;
  border: 1px solid rgba(73, 198, 255, 0.2);
  background: rgba(9, 29, 23, 0.7);
  box-shadow: var(--shadow);
}
.core {
  position: absolute;
  inset: 38% 30%;
  display: grid;
  place-items: center;
  border-radius: 18px;
  border: 1px solid rgba(54, 240, 192, 0.28);
  background: rgba(13, 37, 30, 0.95);
  color: var(--mint);
  font-size: clamp(28px, 4vw, 54px);
  font-weight: 900;
}
.orbit span {
  position: absolute;
  padding: 0.5rem 0.82rem;
  border-radius: 999px;
  border: 1px solid rgba(73, 198, 255, 0.35);
  background: rgba(11, 31, 25, 0.92);
  font-weight: 800;
}
.orbit span:nth-child(2) { left: 8%; top: 12%; }
.orbit span:nth-child(3) { right: 8%; top: 15%; }
.orbit span:nth-child(4) { left: 10%; bottom: 14%; }
.orbit span:nth-child(5) { right: 10%; bottom: 13%; }
.timeline {
  margin-top: 7%;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  position: relative;
}
.timeline::before {
  content: "";
  position: absolute;
  left: 5%;
  right: 5%;
  top: 2.05rem;
  border-top: 2px solid rgba(55, 180, 146, 0.24);
}
.step {
  position: relative;
  text-align: center;
}
.step b {
  width: 3.85rem;
  height: 3.85rem;
  min-width: 0;
  min-height: 0;
  padding: 0;
  margin: 0 auto;
  color: var(--mint);
}
.step strong {
  display: block;
  margin-top: 0.95rem;
  font-size: clamp(14px, 1.35vw, 19px);
}
.step p,
.compare p,
.matrix p,
.matrix small,
.card p,
.summary-list span,
.flow div,
.tool-row p {
  color: var(--muted);
  line-height: 1.46;
  font-size: clamp(12px, 1.08vw, 16px);
}
.compare {
  margin-top: 4.8%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5%;
}
.card,
.compare > div,
.matrix > div,
.flow > div,
.summary-list > div,
.tool-row {
  border-radius: 8px;
  border: 1px solid var(--line);
  background: var(--panel);
  box-shadow: var(--shadow);
}
.compare > div { padding: 1.5rem; min-height: 15.4rem; }
.compare h3 { color: var(--mint); margin-bottom: 0.95rem; font-size: clamp(20px, 2vw, 29px); }
.takeaway, .note, .closing {
  margin: 1.8rem auto 0;
  max-width: 86%;
  color: var(--cyan);
  text-align: center;
  font-weight: 800;
  font-size: clamp(17px, 1.55vw, 24px);
}
.matrix {
  margin-top: 4.3%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.matrix > div,
.summary-list > div { padding: 1.2rem; min-height: 8rem; }
.matrix strong,
.summary-list strong,
.tool-row strong { color: var(--mint); font-size: clamp(18px, 1.65vw, 25px); }
.three {
  margin-top: 5.6%;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.15rem;
}
.three .card {
  padding: 1.45rem;
  min-height: 12.2rem;
  text-align: center;
}
.three span {
  color: var(--cyan);
  font-weight: 900;
  font-size: clamp(13px, 1.15vw, 17px);
}
.three strong {
  display: block;
  margin: 0.8rem 0 1rem;
  color: var(--mint);
  font-size: clamp(26px, 2.65vw, 40px);
}
.flow {
  margin-top: 4.7%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.95rem;
}
.flow > div {
  min-height: 4.1rem;
  padding: 0.95rem 1rem;
  color: var(--text);
  font-weight: 800;
}
.flow span {
  color: var(--mint);
  margin-right: 0.5rem;
}
.formula {
  display: block;
  margin: 1.55rem auto 0;
  max-width: 88%;
  padding: 0.9rem;
  border-radius: 8px;
  border: 1px solid var(--line);
  background: rgba(10, 32, 25, 0.88);
  color: var(--cyan);
  text-align: center;
  font-size: clamp(12px, 1.18vw, 18px);
  white-space: normal;
}
.tool-list {
  margin-top: 4.35%;
  display: grid;
  gap: 1rem;
}
.tool-row {
  padding: 1rem 1.25rem;
  display: grid;
  grid-template-columns: 2.2fr 5fr;
  gap: 1rem;
  align-items: center;
}
.summary-list {
  margin-top: 5%;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.85rem;
}
.controls {
  position: fixed;
  left: 50%;
  bottom: 1.1rem;
  transform: translateX(-50%);
  display: flex;
  gap: 0.55rem;
  z-index: 10;
}
button {
  width: 2.5rem;
  height: 2.5rem;
  border: 1px solid rgba(73, 198, 255, 0.36);
  border-radius: 999px;
  background: rgba(4, 17, 13, 0.78);
  color: var(--text);
  font-weight: 900;
  cursor: pointer;
}
button:hover { background: rgba(11, 31, 25, 0.94); }
.an, .anim-item {
  opacity: 0;
  transform: translateY(16px);
  animation: fadeUp 0.56s ease forwards;
}
.active .an:nth-of-type(2),
.active .anim-item:nth-of-type(2) { animation-delay: 0.08s; }
.active .an:nth-of-type(3),
.active .anim-item:nth-of-type(3) { animation-delay: 0.16s; }
@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.static-export .an,
.static-export .anim-item {
  opacity: 1 !important;
  transform: none !important;
  animation: none !important;
}
@media (max-width: 820px) {
  body { overflow: auto; }
  .deck { min-height: 100vh; height: auto; }
  .slide {
    width: 100vw;
    height: auto;
    min-height: 100vh;
    padding: 4.1rem 1.25rem 5rem;
  }
  h1, h2, .subtitle { max-width: 100%; }
  .cover-grid,
  .timeline,
  .compare,
  .matrix,
  .three,
  .flow,
  .summary-list,
  .tool-row { grid-template-columns: 1fr; }
  .timeline::before { display: none; }
  .orbit { min-height: 300px; }
}
"""


def html_escape(text: str) -> str:
    return html.escape(text, quote=True)


def take_paragraphs(text: str, max_count: int = 6):
    paragraphs = []
    for block in text.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("<a class=\"presentation-link\""):
            continue
        if stripped.startswith("如果你想先看一版可视化讲解"):
            continue
        paragraphs.append(stripped)
        if len(paragraphs) >= max_count:
            break
    return paragraphs


def bullets_from_paragraph(paragraph: str, max_items: int = 4):
    items = []
    for line in paragraph.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
    return items[:max_items]


def extract_sections(text: str):
    matches = list(SECTION_RE.finditer(text))
    sections = []
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append((title, body))
    return sections


def build_deck(article):
    text = article["md"].read_text(encoding="utf-8")
    sections = extract_sections(text)
    intro_paragraphs = take_paragraphs(text, 5)
    overview_points = bullets_from_paragraph(text, 4)
    if not overview_points:
        overview_points = [title for title, _ in sections[:4]]

    learning_points = []
    for _, body in sections:
        items = bullets_from_paragraph(body, 5)
        if items:
            learning_points = items
            break
    if not learning_points:
        learning_points = [title for title, _ in sections[:5]]

    tags = []
    for title, _ in sections[:5]:
        tag = title.replace("：", " ").replace("，", " ").replace("、", " ")
        tag = tag[:18].strip()
        if tag:
            tags.append(tag)

    slides = [
        {
            "type": "cover",
            "kicker": article["title"],
            "title": article["title"],
            "subtitle": article["summary"],
            "tags": tags[:5] or ["Overview", "Map", "Practice"],
        }
    ]

    if intro_paragraphs:
        slides.append(
            {
                "type": "compare",
                "kicker": "Overview",
                "title": "先把这篇文章的主线看清",
                "subtitle": "用一页把主题、问题背景和阅读目标压缩出来。",
                "leftTitle": "文章要解决什么",
                "rightTitle": "你会得到什么",
                "left": intro_paragraphs[:3],
                "right": overview_points[:4],
                "takeaway": "先看整体地图，再往具体场景和代码细节深入，阅读成本会低很多。",
            }
        )

    if learning_points:
        items = []
        for idx, point in enumerate(learning_points[:5], start=1):
            items.append((f"{idx:02d}", point[:26], "从这一步建立直觉，再把细节逐层展开。"))
        while len(items) < 5:
            fallback = sections[len(items)][0][:26] if len(sections) > len(items) else "补充理解"
            items.append((f"{len(items) + 1:02d}", fallback, "围绕实际项目语境继续推进。"))
        slides.append(
            {
                "type": "timeline",
                "kicker": "Reading Path",
                "title": "一条适合初学者的阅读顺序",
                "subtitle": "把最容易卡住的概念先串起来，再往后看细节。",
                "items": items[:5],
            }
        )

    matrix_items = []
    for title, body in sections[:6]:
        summary = body.split("\n\n")[0].replace("\n", " ").strip()
        summary = re.sub(r"\s+", " ", summary)
        if len(summary) > 36:
            summary = summary[:36] + "..."
        matrix_items.append((title[:18], summary or "围绕这个主题展开工程解释。", "文章中的一个关键节点"))
    if matrix_items:
        slides.append(
            {
                "type": "matrix",
                "kicker": "Concept Map",
                "title": "文章核心板块一页总览",
                "subtitle": "把目录里最重要的主题放到同一张地图上。",
                "items": matrix_items[:6],
            }
        )

    detail_sections = sections[1:4] if len(sections) > 3 else sections[:3]
    if detail_sections:
        cards = []
        for idx, (title, body) in enumerate(detail_sections[:3], start=1):
            snippet = body.split("\n\n")[0].replace("\n", " ").strip()
            snippet = re.sub(r"\s+", " ", snippet)
            if len(snippet) > 64:
                snippet = snippet[:64] + "..."
            cards.append((f"0{idx}", title[:18], snippet or "围绕这个主题展开讲解。"))
        slides.append(
            {
                "type": "three",
                "kicker": "Key Blocks",
                "title": "最值得优先吃透的三个模块",
                "subtitle": "先掌握关键块，剩下的内容会顺很多。",
                "items": cards,
                "note": "读完这三块以后，再回头补上下游细节，通常最省力。",
            }
        )

    flow_steps = [title[:20] for title, _ in sections[:7]]
    if flow_steps:
        slides.append(
            {
                "type": "flow",
                "kicker": "Study Flow",
                "title": "把整篇文章当成一条推进链来看",
                "subtitle": "从概念理解走到工程落地，尽量保持路径连续。",
                "steps": flow_steps[:7],
                "formula": " -> ".join(flow_steps[:7]),
            }
        )

    closeout_titles = []
    for title, _ in sections:
        if any(key in title for key in ("误区", "常见问题", "面试常问", "下一步", "总结")):
            closeout_titles.append(title)
    tool_items = []
    if closeout_titles:
        for title in closeout_titles[:3]:
            tool_items.append((title[:22], "这部分适合在读完主体后回看，用来校正理解和补齐边界。"))
    else:
        for title, _ in sections[-3:]:
            tool_items.append((title[:22], "作为收口章节，帮助你把前面的内容重新组织一遍。"))
    slides.append(
        {
            "type": "tools",
            "kicker": "Closeout",
            "title": "读到最后，要把哪些信息带走",
            "subtitle": "别只记术语，重点是形成可复用的判断。",
            "items": tool_items,
            "note": "如果后续要展开成系列文章，最适合从这些总结节点继续往下拆。",
        }
    )

    summary_items = [(title[:14], "建立直觉") for title, _ in sections[:5]]
    slides.append(
        {
            "type": "summary",
            "kicker": "Summary",
            "title": "一页回看整篇文章的主脉络",
            "subtitle": "你现在应该已经能把主题、场景、关键模块和落地方向串起来。",
            "items": summary_items[:5],
            "closing": "把这张演示页当成速记版地图，回到原文时会更容易抓住重点。",
        }
    )

    return slides, text


def render_slide(data, index, total):
    parts = [
        f'<section class="slide slide-{data["type"]}" data-index="{index}">',
        '<div class="top-line"></div>',
        f'<div class="page-no">{index:02d} / {total:02d}</div>',
    ]
    if data["type"] == "cover":
        parts.extend(
            [
                '<div class="cover-grid anim-item">',
                '<div class="cover-copy">',
                f'<p class="kicker an">{html_escape(data["kicker"])}</p>',
                f'<h1 class="an">{html_escape(data["title"])}</h1>',
                f'<p class="subtitle an">{html_escape(data["subtitle"])}</p>',
                '<div class="tag-row an">',
                "".join(f"<span>{html_escape(tag)}</span>" for tag in data["tags"]),
                "</div></div>",
                '<div class="orbit an"><div class="core">PPT</div><span>Overview</span><span>Practice</span><span>Map</span><span>Notes</span></div>',
                "</div>",
            ]
        )
    else:
        parts.extend(
            [
                f'<p class="kicker an">{html_escape(data["kicker"])}</p>',
                f'<h2 class="an">{html_escape(data["title"])}</h2>',
                f'<p class="subtitle an">{html_escape(data["subtitle"])}</p>',
            ]
        )
        slide_type = data["type"]
        if slide_type == "timeline":
            parts.append('<div class="timeline anim-item">')
            for num, title, desc in data["items"]:
                parts.append(
                    f'<div class="step"><b>{html_escape(num)}</b><strong>{html_escape(title)}</strong><p>{html_escape(desc)}</p></div>'
                )
            parts.append("</div>")
        elif slide_type == "compare":
            parts.append('<div class="compare anim-item">')
            parts.append(f'<div><h3>{html_escape(data["leftTitle"])}</h3>')
            parts.extend(f"<p>{html_escape(item)}</p>" for item in data["left"])
            parts.append("</div>")
            parts.append(f'<div><h3>{html_escape(data["rightTitle"])}</h3>')
            parts.extend(f"<p>{html_escape(item)}</p>" for item in data["right"])
            parts.append("</div></div>")
            parts.append(f'<div class="takeaway anim-item">{html_escape(data["takeaway"])}</div>')
        elif slide_type == "matrix":
            parts.append('<div class="matrix anim-item">')
            for name, solve, metaphor in data["items"]:
                parts.append(
                    f'<div><strong>{html_escape(name)}</strong><p>{html_escape(solve)}</p><small>{html_escape(metaphor)}</small></div>'
                )
            parts.append("</div>")
        elif slide_type == "three":
            parts.append('<div class="three anim-item">')
            for num, title, desc in data["items"]:
                parts.append(
                    f'<div class="card"><span>{html_escape(num)}</span><strong>{html_escape(title)}</strong><p>{html_escape(desc)}</p></div>'
                )
            parts.append("</div>")
            parts.append(f'<div class="note anim-item">{html_escape(data["note"])}</div>')
        elif slide_type == "flow":
            parts.append('<div class="flow anim-item">')
            for idx, step in enumerate(data["steps"], start=1):
                parts.append(f'<div><span>{idx}</span>{html_escape(step)}</div>')
            parts.append("</div>")
            parts.append(f'<code class="formula anim-item">{html_escape(data["formula"])}</code>')
        elif slide_type == "tools":
            parts.append('<div class="tool-list anim-item">')
            for title, desc in data["items"]:
                parts.append(
                    f'<div class="tool-row"><strong>{html_escape(title)}</strong><p>{html_escape(desc)}</p></div>'
                )
            parts.append("</div>")
            parts.append(f'<div class="note anim-item">{html_escape(data["note"])}</div>')
        elif slide_type == "summary":
            parts.append('<div class="summary-list anim-item">')
            for title, desc in data["items"]:
                parts.append(f'<div><strong>{html_escape(title)}</strong><span>{html_escape(desc)}</span></div>')
            parts.append("</div>")
            parts.append(f'<div class="closing anim-item">{html_escape(data["closing"])}</div>')
    parts.append("</section>")
    return "\n".join(parts)


def render_html(title, slides):
    slides_html = "\n".join(render_slide(slide, idx, len(slides)) for idx, slide in enumerate(slides, start=1))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_escape(title)} PPT</title>
<style>
{STYLE}
</style>
</head>
<body>
<main class="deck">
{slides_html}
</main>
<nav class="controls" aria-label="幻灯片控制">
  <button type="button" id="prev" title="上一页">&#8592;</button>
  <button type="button" id="next" title="下一页">&#8594;</button>
</nav>
<script>
const slides = Array.from(document.querySelectorAll('.slide'));
let current = 0;
function resetAnimations(slide) {{
  slide.querySelectorAll('.an, .anim-item, [style*="animation"]').forEach((item) => {{
    const clone = item.cloneNode(true);
    item.parentNode.replaceChild(clone, item);
  }});
}}
function showSlide(index) {{
  current = (index + slides.length) % slides.length;
  slides.forEach((slide, idx) => slide.classList.toggle('active', idx === current));
  resetAnimations(slides[current]);
  history.replaceState(null, '', '#' + (current + 1));
}}
document.getElementById('prev').addEventListener('click', () => showSlide(current - 1));
document.getElementById('next').addEventListener('click', () => showSlide(current + 1));
document.addEventListener('keydown', (event) => {{
  if (event.key === 'ArrowRight' || event.key === ' ') {{
    event.preventDefault();
    showSlide(current + 1);
  }}
  if (event.key === 'ArrowLeft') {{
    event.preventDefault();
    showSlide(current - 1);
  }}
}});
if (new URLSearchParams(location.search).has('static')) {{
  document.documentElement.classList.add('static-export');
}}
const hashIndex = Number.parseInt(location.hash.replace('#', ''), 10);
showSlide(Number.isFinite(hashIndex) ? hashIndex - 1 : 0);
</script>
</body>
</html>
"""


def build_link(route: str, title: str) -> str:
    return f"""<a class="presentation-link" href="{route}" target="_blank" rel="noopener">
  <span class="presentation-link__icon" aria-hidden="true">
    {SVG}
  </span>
  <span>
    <strong>打开 {title} PPT 演示版</strong>
    <small>浏览器幻灯片版速览，支持方向键和空格切换</small>
  </span>
</a>"""


def replace_intro_link(text: str, route: str, title: str) -> str:
    new_block = build_link(route, title)
    card_pattern = re.compile(r'<a class="presentation-link"[\s\S]*?</a>\s*', re.M)
    if card_pattern.search(text):
        return card_pattern.sub(new_block + "\n\n", text, count=1)

    inline_pattern = re.compile(
        r"^如果你想先看一版可视化讲解，可以打开：\[[^\]]+\]\([^)]+\)。\s*$",
        re.M,
    )
    if inline_pattern.search(text):
        return inline_pattern.sub(new_block, text, count=1)

    heading_match = re.search(r"^# .+$", text, re.M)
    if not heading_match:
        return new_block + "\n\n" + text
    insert_at = heading_match.end()
    return text[:insert_at] + "\n\n" + new_block + "\n" + text[insert_at:]


def main():
    for article in ARTICLES:
        slides, source_text = build_deck(article)
        html_path = OUT_DIR / f'{article["slug"]}-ppt.html'
        html_path.write_text(render_html(article["title"], slides), encoding="utf-8")
        updated = replace_intro_link(source_text, article["route"], article["title"])
        article["md"].write_text(updated, encoding="utf-8")
        print(f'UPDATED::{article["md"].relative_to(ROOT)}::{html_path.relative_to(ROOT)}')


if __name__ == "__main__":
    main()
