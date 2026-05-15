from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path
from typing import Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
ASSET_DIR = DOCS_DIR / "public" / "assets" / "presentations"
ROUTE_DIR = DOCS_DIR / "presentations"
CONFIG_PATH = ROOT / "scripts" / "presentation_targets.json"

EXCLUDED_PARTS = {".vitepress", "public", "presentations"}

def iter_markdown_files() -> Iterable[Path]:
    for path in DOCS_DIR.rglob("*.md"):
        rel = path.relative_to(DOCS_DIR)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        yield path


def strip_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    raw_frontmatter = parts[0][4:]
    try:
        data = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError:
        data = {}
    return data, parts[1]


def make_slug(path: Path) -> str:
    rel = path.relative_to(DOCS_DIR)
    stem = path.stem
    if stem != "index":
        return stem
    if len(rel.parts) == 1:
        return "home-index"
    return "-".join(rel.parts[:-1]) + "-index"


def clean_line(line: str) -> str:
    line = re.sub(r"`([^`]+)`", r"\1", line)
    line = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", line)
    line = re.sub(r"<[^>]+>", "", line)
    return re.sub(r"\s+", " ", line).strip()


def truncate(text: str, limit: int = 74) -> str:
    text = clean_line(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "..."


def parse_markdown(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    frontmatter, body = strip_frontmatter(raw)
    lines = body.splitlines()
    title = ""
    intro: list[str] = []
    sections: list[dict] = []
    current: dict | None = None
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        if line.startswith("# "):
            title = clean_line(line[2:])
            continue
        if line.startswith("## "):
            current = {"title": clean_line(line[3:]), "items": []}
            sections.append(current)
            continue
        if line.startswith("### "):
            if current is not None:
                current["items"].append(clean_line(line[4:]))
            continue

        stripped = clean_line(line)
        if not stripped:
            continue

        if stripped.startswith("|") or set(stripped) <= {"|", "-", " "}:
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            text = clean_line(stripped[2:])
        elif re.match(r"^\d+\.\s+", stripped):
            text = clean_line(re.sub(r"^\d+\.\s+", "", stripped))
        else:
            text = stripped

        if not text:
            continue

        if current is None:
            intro.append(text)
        else:
            current["items"].append(text)

    if not title:
        title = str(frontmatter.get("title") or frontmatter.get("hero", {}).get("text") or path.stem)

    if not intro and frontmatter.get("hero", {}).get("tagline"):
        intro.append(str(frontmatter["hero"]["tagline"]))

    return {
        "frontmatter": frontmatter,
        "title": title,
        "intro": intro[:6],
        "sections": [
            {
                "title": section["title"],
                "items": [item for item in section["items"] if item][:8],
            }
            for section in sections
            if section["title"]
        ],
    }


def build_slides(meta: dict) -> list[dict]:
    title = meta["title"]
    intro = meta["intro"][:4]
    sections = meta["sections"]

    slides = [
        {
            "kind": "cover",
            "title": title,
            "subtitle": truncate(intro[0], 96) if intro else "从文章主线到关键知识点的可视化速览。",
            "chips": [truncate(item, 22) for item in intro[:5]],
        }
    ]

    if intro:
        slides.append(
            {
                "kind": "bullets",
                "eyebrow": "Article Focus",
                "title": "先把主线看清",
                "items": [truncate(item, 86) for item in intro[:5]],
            }
        )

    for section in sections[:5]:
        items = [truncate(item, 86) for item in section["items"][:5]]
        if not items:
            continue
        slides.append(
            {
                "kind": "bullets",
                "eyebrow": "Key Section",
                "title": section["title"],
                "items": items,
            }
        )

    section_titles = [truncate(section["title"], 26) for section in sections[:6]]
    if section_titles:
        slides.append(
            {
                "kind": "summary",
                "title": "这篇文章适合怎么读",
                "items": section_titles,
                "closing": "先看地图，再按章节深入，能更快把知识串起来。",
            }
        )

    return slides[:8]


def slide_html(slide: dict, index: int, total: int) -> str:
    if slide["kind"] == "cover":
        chips = "".join(f"<span>{html.escape(chip)}</span>" for chip in slide["chips"])
        return f"""
<section class="slide slide-cover" data-index="{index}">
  <div class="top-line"></div>
  <div class="page-no">{index:02d} / {total:02d}</div>
  <div class="cover-grid anim-item">
    <div class="cover-copy">
      <p class="eyebrow an">Article Presentation</p>
      <h1 class="an">{html.escape(slide["title"])}</h1>
      <p class="subtitle an">{html.escape(slide["subtitle"])}</p>
      <div class="tag-row an">{chips}</div>
    </div>
    <div class="shape-panel an">
      <div class="shape-core">PPT</div>
      <span>阅读地图</span>
      <span>关键概念</span>
      <span>章节速览</span>
      <span>结构总结</span>
    </div>
  </div>
</section>
""".strip()

    if slide["kind"] == "summary":
        cards = "".join(f"<div><strong>{html.escape(item)}</strong></div>" for item in slide["items"])
        return f"""
<section class="slide slide-summary" data-index="{index}">
  <div class="top-line"></div>
  <div class="page-no">{index:02d} / {total:02d}</div>
  <p class="eyebrow an">Reading Map</p>
  <h2 class="an">{html.escape(slide["title"])}</h2>
  <div class="summary-grid anim-item">{cards}</div>
  <p class="closing anim-item">{html.escape(slide["closing"])}</p>
</section>
""".strip()

    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in slide["items"])
    return f"""
<section class="slide slide-bullets" data-index="{index}">
  <div class="top-line"></div>
  <div class="page-no">{index:02d} / {total:02d}</div>
  <p class="eyebrow an">{html.escape(slide["eyebrow"])}</p>
  <h2 class="an">{html.escape(slide["title"])}</h2>
  <div class="bullet-panel anim-item">
    <ul>{bullets}</ul>
  </div>
</section>
""".strip()


def render_html(slides: list[dict], title: str) -> str:
    sections = "\n".join(slide_html(slide, i, len(slides)) for i, slide in enumerate(slides, start=1))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} PPT</title>
<style>
:root {{
  --bg: #081510;
  --panel: #10261d;
  --panel-2: #123226;
  --mint: #20c997;
  --cyan: #57d7ff;
  --gold: #f2b56b;
  --text: #eefaf5;
  --muted: #a7c6bb;
  --line: #214a3d;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: #05100d;
  color: var(--text);
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
  overflow: hidden;
}}
.deck {{
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
}}
.slide {{
  display: none;
  position: relative;
  width: min(100vw, 177.78vh);
  height: min(56.25vw, 100vh);
  padding: 5.4% 6%;
  overflow: hidden;
  background:
    radial-gradient(circle at 18% 14%, rgba(32, 201, 151, .14), transparent 28%),
    radial-gradient(circle at 82% 12%, rgba(87, 215, 255, .14), transparent 24%),
    linear-gradient(135deg, #081510 0%, #0b1713 54%, #07120e 100%);
}}
.slide.active {{ display: block; }}
.top-line {{ position: absolute; inset: 0 auto auto 0; width: 100%; height: 8px; background: linear-gradient(90deg, var(--mint), var(--cyan)); }}
.page-no {{ position: absolute; right: 5.8%; bottom: 4.9%; color: var(--cyan); font-size: clamp(11px, 1vw, 15px); }}
.eyebrow {{
  margin: 0 0 10px;
  color: var(--mint);
  font-size: clamp(13px, 1.2vw, 18px);
  font-weight: 900;
  text-transform: uppercase;
}}
h1, h2 {{
  margin: 0;
  line-height: 1.08;
  letter-spacing: 0;
}}
h1 {{ font-size: clamp(42px, 6vw, 84px); max-width: 72%; }}
h2 {{ font-size: clamp(28px, 3.6vw, 48px); max-width: 82%; }}
.subtitle {{
  margin: 18px 0 0;
  max-width: 64%;
  color: var(--muted);
  font-size: clamp(16px, 1.5vw, 23px);
  line-height: 1.55;
}}
.cover-grid {{
  display: grid;
  grid-template-columns: 1.18fr .82fr;
  gap: 5%;
  height: 100%;
  align-items: center;
}}
.tag-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 28px;
}}
.tag-row span,
.shape-panel span {{
  border: 1px solid rgba(87, 215, 255, .4);
  background: rgba(18, 50, 38, .72);
  border-radius: 999px;
  color: var(--cyan);
  padding: 8px 13px;
  font-weight: 800;
}}
.shape-panel {{
  position: relative;
  min-height: 420px;
  border: 1px solid rgba(87, 215, 255, .25);
  border-radius: 24px;
  background: rgba(16, 38, 29, .75);
}}
.shape-core {{
  position: absolute;
  inset: 36% 28%;
  display: grid;
  place-items: center;
  border: 1px solid rgba(32, 201, 151, .24);
  border-radius: 18px;
  color: var(--mint);
  font-size: clamp(34px, 4vw, 56px);
  font-weight: 900;
}}
.shape-panel span:nth-of-type(1) {{ position: absolute; left: 8%; top: 13%; }}
.shape-panel span:nth-of-type(2) {{ position: absolute; right: 8%; top: 15%; }}
.shape-panel span:nth-of-type(3) {{ position: absolute; left: 10%; bottom: 16%; }}
.shape-panel span:nth-of-type(4) {{ position: absolute; right: 10%; bottom: 14%; }}
.bullet-panel {{
  margin-top: 34px;
  max-width: 86%;
  padding: 26px 28px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(16, 38, 29, .82);
}}
.bullet-panel ul {{
  margin: 0;
  padding-left: 24px;
}}
.bullet-panel li {{
  margin: 0 0 16px;
  color: var(--text);
  font-size: clamp(16px, 1.45vw, 22px);
  line-height: 1.62;
}}
.bullet-panel li:last-child {{ margin-bottom: 0; }}
.summary-grid {{
  margin-top: 34px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  max-width: 90%;
}}
.summary-grid div {{
  min-height: 110px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(18, 50, 38, .76);
  display: flex;
  align-items: center;
}}
.summary-grid strong {{
  font-size: clamp(18px, 1.7vw, 26px);
  line-height: 1.4;
}}
.closing {{
  margin-top: 24px;
  color: var(--gold);
  font-size: clamp(18px, 1.65vw, 24px);
  font-weight: 900;
}}
.controls {{
  position: fixed;
  left: 50%;
  bottom: 1rem;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
}}
button {{
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 999px;
  border: 1px solid rgba(87, 215, 255, .35);
  background: rgba(8, 21, 16, .78);
  color: var(--text);
  font-weight: 900;
  cursor: pointer;
}}
.an, .anim-item {{
  opacity: 0;
  transform: translateY(16px);
  animation: fadeUp .55s ease forwards;
}}
.active .an:nth-of-type(2),
.active .anim-item:nth-of-type(2) {{ animation-delay: .08s; }}
.active .an:nth-of-type(3),
.active .anim-item:nth-of-type(3) {{ animation-delay: .16s; }}
@keyframes fadeUp {{
  to {{
    opacity: 1;
    transform: translateY(0);
  }}
}}
.static-export .an,
.static-export .anim-item {{
  opacity: 1 !important;
  transform: none !important;
  animation: none !important;
}}
@media (max-width: 760px) {{
  body {{ overflow: auto; }}
  .deck {{ height: auto; min-height: 100vh; }}
  .slide {{
    width: 100vw;
    height: auto;
    min-height: 100vh;
    padding: 4.2rem 1.2rem 5rem;
  }}
  h1, h2, .subtitle, .bullet-panel, .summary-grid {{
    max-width: 100%;
  }}
  .cover-grid,
  .summary-grid {{
    grid-template-columns: 1fr;
  }}
  .shape-panel {{
    min-height: 300px;
  }}
}}
</style>
</head>
<body>
<main class="deck">
{sections}
</main>
<nav class="controls" aria-label="幻灯片控制">
  <button type="button" id="prev" title="上一页">‹</button>
  <button type="button" id="next" title="下一页">›</button>
</nav>
<script>
const slides = Array.from(document.querySelectorAll(".slide"));
let current = 0;
function resetAnimations(slide) {{
  slide.querySelectorAll(".an, .anim-item, [style*='animation']").forEach(function(item) {{
    const clone = item.cloneNode(true);
    item.parentNode.replaceChild(clone, item);
  }});
}}
function showSlide(index) {{
  current = (index + slides.length) % slides.length;
  slides.forEach((slide, slideIndex) => slide.classList.toggle("active", slideIndex === current));
  resetAnimations(slides[current]);
}}
document.getElementById("prev").addEventListener("click", () => showSlide(current - 1));
document.getElementById("next").addEventListener("click", () => showSlide(current + 1));
document.addEventListener("keydown", (event) => {{
  if (event.key === "ArrowRight" || event.key === " ") showSlide(current + 1);
  if (event.key === "ArrowLeft") showSlide(current - 1);
}});
const hashSlide = Number.parseInt(location.hash.replace("#", ""), 10);
if (new URLSearchParams(location.search).has("static")) {{
  document.documentElement.classList.add("static-export");
}}
showSlide(Number.isFinite(hashSlide) ? hashSlide - 1 : 0);
</script>
</body>
</html>
"""


def relative_clean_route(path: Path, slug: str) -> str:
    route_target = DOCS_DIR / "presentations" / f"{slug}-ppt"
    relative = os.path.relpath(route_target, path.parent)
    relative = relative.replace("\\", "/")
    if not relative.startswith("."):
        relative = "./" + relative
    return relative


def build_presentation_link(path: Path, title: str, slug: str) -> str:
    href = relative_clean_route(path, slug)
    return f"""<a class="presentation-link" href="{href}" target="_blank" rel="noopener">
  <span class="presentation-link__icon" aria-hidden="true">
    <span class="presentation-link__glyph">PPT</span>
  </span>
  <span>
    <strong>打开文章演示版</strong>
    <small>浏览器幻灯片版速览，支持方向键和空格切换</small>
  </span>
</a>"""


def replace_or_insert_link(path: Path, slug: str, title: str) -> None:
    original = path.read_text(encoding="utf-8")
    link_block = build_presentation_link(path, title, slug)
    cleaned = re.sub(r"\n*<a class=\"presentation-link\"[\s\S]*?</a>\s*", "\n\n", original)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    updated = re.sub(
        r"??????????????????????????????\[[^\]]+\]\([^)]+\)??",
        link_block,
        cleaned,
        count=1,
    )

    if updated == cleaned:
        frontmatter, body = strip_frontmatter(cleaned)
        del frontmatter
        if body.startswith("# "):
            first_newline = cleaned.find("\n")
            insert_at = cleaned.find("\n", first_newline + 1)
            if insert_at == -1:
                insert_at = len(cleaned)
            updated = cleaned[: insert_at + 1] + "\n" + link_block + "\n\n" + cleaned[insert_at + 1 :].lstrip("\n")
        else:
            if cleaned.startswith("---\n"):
                parts = cleaned.split("\n---\n", 1)
                if len(parts) == 2:
                    updated = parts[0] + "\n---\n\n" + link_block + "\n\n" + parts[1].lstrip("\n")
                else:
                    updated = link_block + "\n\n" + cleaned
            else:
                updated = link_block + "\n\n" + cleaned

    path.write_text(updated, encoding="utf-8")

def build_route_page(route_src: str) -> str:
    return f"""---
layout: false
---

<iframe
  src="{route_src}"
  title="文章演示版"
  style="position: fixed; inset: 0; width: 100vw; height: 100vh; border: 0; background: #07130f;"
></iframe>
"""


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    ROUTE_DIR.mkdir(parents=True, exist_ok=True)

    targets = []
    for path in iter_markdown_files():
        slug = make_slug(path)
        meta = parse_markdown(path)
        slides = build_slides(meta)
        asset_path = ASSET_DIR / f"{slug}-ppt.html"
        route_path = ROUTE_DIR / f"{slug}-ppt.md"

        asset_path.write_text(render_html(slides, meta["title"]), encoding="utf-8")
        route_src = f"../assets/presentations/{slug}-ppt.html"
        route_path.write_text(build_route_page(route_src), encoding="utf-8")
        replace_or_insert_link(path, slug, meta["title"])

        targets.append(
            {
                "markdown": str(path.relative_to(ROOT)).replace("\\", "/"),
                "slug": slug,
                "asset": str(asset_path.relative_to(ROOT)).replace("\\", "/"),
                "route": str(route_path.relative_to(ROOT)).replace("\\", "/"),
                "routeSrc": route_src,
            }
        )

    CONFIG_PATH.write_text(json.dumps(targets, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for target in targets:
        print(target["markdown"])


if __name__ == "__main__":
    main()
