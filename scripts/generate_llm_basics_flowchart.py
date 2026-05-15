from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "presentations"
HTML_PATH = OUT_DIR / "llm-basics-overview-flowchart.html"


def build_html():
    html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>大模型基础入门流程图</title>
<style>
:root {
  --bg: #07130f;
  --panel: #0d211a;
  --panel-2: #102a22;
  --line: #1e4d40;
  --mint: #06d6a0;
  --cyan: #22d3ee;
  --amber: #f59e0b;
  --rose: #fb7185;
  --text: #eafbf5;
  --muted: #9cc7b8;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 12% 18%, rgba(6, 214, 160, .12), transparent 28%),
    radial-gradient(circle at 84% 10%, rgba(34, 211, 238, .14), transparent 30%),
    linear-gradient(135deg, #07130f 0%, #0b1713 54%, #06100d 100%);
  color: var(--text);
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", Arial, sans-serif;
}
.page {
  width: min(1440px, 100vw);
  min-height: 900px;
  margin: 0 auto;
  padding: 46px 56px 28px;
  position: relative;
  overflow: hidden;
}
.top-line {
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 8px;
  background: linear-gradient(90deg, var(--mint), var(--cyan));
}
.header {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: end;
  gap: 28px;
  margin-bottom: 24px;
}
.kicker {
  margin: 0 0 8px;
  color: var(--mint);
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
}
h1 {
  margin: 0;
  font-size: 44px;
  line-height: 1.08;
  letter-spacing: 0;
}
.subtitle {
  margin: 9px 0 0;
  max-width: 820px;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.55;
}
.legend {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: flex-end;
  flex-wrap: wrap;
}
.legend span {
  border: 1px solid rgba(34, 211, 238, .45);
  background: rgba(16, 42, 34, .72);
  border-radius: 999px;
  padding: 8px 12px;
  color: var(--cyan);
  font-size: 12px;
  font-weight: 800;
}
.canvas {
  display: grid;
  grid-template-columns: 1.04fr .88fr 1.04fr;
  gap: 26px;
  align-items: stretch;
}
.lane {
  border: 1px solid rgba(30, 77, 64, .95);
  background: rgba(13, 33, 26, .74);
  border-radius: 10px;
  padding: 20px;
  min-height: 585px;
  position: relative;
}
.lane-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 18px;
}
.icon {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  border: 1px solid rgba(34, 211, 238, .55);
  display: grid;
  place-items: center;
  color: var(--cyan);
  font-weight: 900;
  font-size: 13px;
}
.lane-title h2 {
  margin: 0;
  font-size: 20px;
  letter-spacing: 0;
}
.lane-title p {
  margin: 3px 0 0;
  color: var(--muted);
  font-size: 12px;
}
.node {
  position: relative;
  border: 1px solid var(--line);
  background: rgba(16, 42, 34, .86);
  border-radius: 8px;
  padding: 15px 16px 15px 58px;
  min-height: 70px;
  margin-bottom: 24px;
}
.node:last-child { margin-bottom: 0; }
.node::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -20px;
  width: 2px;
  height: 16px;
  background: linear-gradient(var(--cyan), var(--line));
}
.node:last-child::after { display: none; }
.num {
  position: absolute;
  left: 16px;
  top: 14px;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: rgba(6, 214, 160, .12);
  border: 1px solid rgba(6, 214, 160, .66);
  color: var(--mint);
  display: grid;
  place-items: center;
  font-weight: 900;
  font-size: 12px;
}
.node strong {
  display: block;
  color: var(--text);
  font-size: 17px;
  margin-bottom: 4px;
}
.node p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.45;
}
.center {
  display: grid;
  grid-template-rows: auto 1fr auto;
  gap: 18px;
}
.hub {
  border: 1px solid rgba(6, 214, 160, .5);
  background:
    radial-gradient(circle at 50% 30%, rgba(6, 214, 160, .16), transparent 38%),
    rgba(13, 33, 26, .82);
  border-radius: 14px;
  padding: 24px 22px;
  text-align: center;
  min-height: 172px;
}
.hub small {
  display: block;
  color: var(--cyan);
  font-weight: 900;
  margin-bottom: 8px;
  text-transform: uppercase;
}
.hub h2 {
  margin: 0;
  color: var(--mint);
  font-size: 32px;
}
.hub p {
  margin: 8px auto 0;
  max-width: 280px;
  color: var(--muted);
  line-height: 1.5;
  font-size: 13px;
}
.system {
  border: 1px solid var(--line);
  background: rgba(13, 33, 26, .64);
  border-radius: 10px;
  padding: 18px;
}
.system h3 {
  margin: 0 0 14px;
  color: var(--cyan);
  font-size: 17px;
}
.stack {
  display: grid;
  gap: 10px;
}
.stack div {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 11px 13px;
  border: 1px solid rgba(30, 77, 64, .86);
  background: rgba(16, 42, 34, .74);
  border-radius: 8px;
}
.stack b {
  font-size: 13px;
}
.stack span {
  color: var(--muted);
  font-size: 12px;
}
.merge {
  border: 1px solid rgba(245, 158, 11, .45);
  background: rgba(245, 158, 11, .08);
  border-radius: 10px;
  padding: 16px;
  color: var(--amber);
  font-weight: 900;
  text-align: center;
  line-height: 1.45;
}
.bridge {
  position: absolute;
  z-index: 0;
  pointer-events: none;
  inset: 0;
}
.bridge line {
  stroke: rgba(34, 211, 238, .42);
  stroke-width: 2;
  stroke-dasharray: 8 9;
  animation: dash 2.4s linear infinite;
}
.bridge path {
  stroke: rgba(6, 214, 160, .5);
  stroke-width: 2;
  fill: none;
  stroke-dasharray: 9 10;
  animation: dash 2.8s linear infinite;
}
.footer {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 18px;
  align-items: center;
  color: var(--muted);
  font-size: 13px;
}
.formula {
  border: 1px solid var(--line);
  background: rgba(16, 42, 34, .78);
  border-radius: 999px;
  padding: 10px 16px;
  color: var(--cyan);
  font-family: Consolas, "Microsoft YaHei", monospace;
}
.anim-item {
  opacity: 0;
  transform: translateY(14px);
  animation: fadeUp .6s ease forwards;
}
.anim-item:nth-child(2) { animation-delay: .08s; }
.anim-item:nth-child(3) { animation-delay: .16s; }
.anim-item:nth-child(4) { animation-delay: .24s; }
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}
@keyframes dash {
  to { stroke-dashoffset: -34; }
}
.static-export .anim-item {
  opacity: 1 !important;
  transform: none !important;
  animation: none !important;
}
@media (max-width: 920px) {
  .page {
    min-height: auto;
    padding: 40px 18px;
  }
  .header,
  .canvas,
  .footer {
    grid-template-columns: 1fr;
  }
  h1 { font-size: 34px; }
  .lane { min-height: auto; }
  .legend { justify-content: flex-start; }
}
</style>
</head>
<body>
<main class="page">
  <div class="top-line"></div>
  <header class="header anim-item">
    <div>
      <p class="kicker">LLM Basics Flowchart</p>
      <h1>大模型应用从概念到闭环</h1>
      <p class="subtitle">先建立概念地图，再跑通最小 RAG 闭环，最后把工具调用和 MCP 接入真实应用。</p>
    </div>
    <div class="legend">
      <span>学习路线</span>
      <span>RAG 链路</span>
      <span>工具生态</span>
    </div>
  </header>

  <section class="canvas">
    <div class="lane anim-item">
      <div class="lane-title">
        <div class="icon">A</div>
        <div>
          <h2>概念学习路线</h2>
          <p>先理解模型如何回答，再扩展外部能力</p>
        </div>
      </div>
      <div class="node">
        <span class="num">1</span>
        <strong>LLM 与 Prompt</strong>
        <p>理解概率生成器，并用清晰目标、上下文和格式约束输出。</p>
      </div>
      <div class="node">
        <span class="num">2</span>
        <strong>Embedding 与向量检索</strong>
        <p>把文本映射到语义空间，找到意思接近但字面不同的内容。</p>
      </div>
      <div class="node">
        <span class="num">3</span>
        <strong>RAG</strong>
        <p>先找知识，再把相关片段作为上下文交给模型生成回答。</p>
      </div>
      <div class="node">
        <span class="num">4</span>
        <strong>Function Calling</strong>
        <p>让模型用结构化格式表达调用工具的意图和参数。</p>
      </div>
      <div class="node">
        <span class="num">5</span>
        <strong>Agent 与 MCP</strong>
        <p>让模型围绕任务推进，并用标准协议连接外部工具生态。</p>
      </div>
    </div>

    <div class="center anim-item">
      <div class="hub">
        <small>Core Mental Model</small>
        <h2>先稳，再扩</h2>
        <p>先让回答基于可靠上下文，再让模型调用工具完成更多动作。</p>
      </div>
      <div class="system">
        <h3>AI 应用核心拼装</h3>
        <div class="stack">
          <div><b>用户问题</b><span>输入意图</span></div>
          <div><b>检索上下文</b><span>私有知识</span></div>
          <div><b>Prompt 编排</b><span>任务边界</span></div>
          <div><b>模型生成</b><span>可读答案</span></div>
          <div><b>工具执行</b><span>真实动作</span></div>
        </div>
      </div>
      <div class="merge">关键判断：多数项目先把 RAG 做稳，再考虑复杂 Agent。</div>
    </div>

    <div class="lane anim-item">
      <div class="lane-title">
        <div class="icon">B</div>
        <div>
          <h2>最小 RAG 闭环</h2>
          <p>以 Java 学习知识库问答为例</p>
        </div>
      </div>
      <div class="node">
        <span class="num">1</span>
        <strong>准备文档</strong>
        <p>收集 Java 基础、并发编程、Spring Boot 常见问题等内容。</p>
      </div>
      <div class="node">
        <span class="num">2</span>
        <strong>切片与向量化</strong>
        <p>把长文切成片段，再为每个片段生成 Embedding。</p>
      </div>
      <div class="node">
        <span class="num">3</span>
        <strong>存入向量库</strong>
        <p>保留原始文档，同时增加语义检索能力。</p>
      </div>
      <div class="node">
        <span class="num">4</span>
        <strong>问题检索 Top-K</strong>
        <p>用户提问时先找最相关片段，而不是让模型裸答。</p>
      </div>
      <div class="node">
        <span class="num">5</span>
        <strong>拼接 Prompt 并生成</strong>
        <p>把问题和检索结果一起发给模型，得到基于知识库的答案。</p>
      </div>
    </div>
  </section>

  <footer class="footer anim-item">
    <div>Prompt 表达任务，Embedding 找到知识，RAG 增强回答，Function Calling 与 MCP 连接真实工具。</div>
    <div class="formula">documents -> chunks -> vectors -> retrieve -> prompt -> answer</div>
  </footer>
</main>
<script>
if (new URLSearchParams(location.search).has("static")) {
  document.documentElement.classList.add("static-export");
}
</script>
</body>
</html>
"""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    HTML_PATH.write_text(html, encoding="utf-8")
    print(HTML_PATH)


if __name__ == "__main__":
    build_html()
