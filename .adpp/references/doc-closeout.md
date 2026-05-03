# Closeout Reference - java全栈

> 本项目是一个基于 `VitePress + Markdown + GitHub Pages` 的 Java 知识博客。
> closeout 的核心是说明本轮改动影响了哪些内容、结构、主题和发布验证。

## 1. Source Of Truth Docs

- `.adpp/changes/<feature>/prd.md`
- `.adpp/changes/<feature>/design.md`
- `.adpp/changes/<feature>/ux-notes.md`
- `docs/**` 正式文章与页面内容
- `.vitepress/config.*` 站点结构与导航配置

说明：

- 文章内容、导航结构和主题实现变更时，相关事实源文档必须同步更新
- README、首页概述等派生文档不能替代事实源文档

## 2. Derived Docs

- `README.md`
- `docs/index.md`
- 导航描述文案
- 发布说明或阶段总结

## 3. Trigger Matrix Notes

### 内容结构改动

- 命中条件：`docs/**` 或专题目录结构变化
- 必须更新：对应 `design.md`、必要时更新 `ux-notes.md` 和 `README.md`
- 必跑命令：`npm run docs:build`

### 主题或配置改动

- 命中条件：`.vitepress/config.*`、`.vitepress/theme/**`、样式或首页布局变化
- 必须更新：`design.md`、`tasks.md`、必要时更新 `README.md`
- 必跑命令：`npm run docs:build`
- 建议补充：人工检查首页、正文页和移动端显示

### 仅文案微调

- 命中条件：不影响目录结构和主题，仅局部文字修改
- 必须更新：按需更新本轮 `closeout-note.md`
- 必跑命令：`npm run docs:build`

## 4. Verification Layers

### Base

- `npm run docs:build`

### Module-specific

- 首页或主题改动后，人工检查首页和至少一篇正文页
- 导航改动后，检查顶部导航和侧边栏跳转

### Release / Deployment

- 发布到 GitHub Pages 前后，检查站点入口、静态资源和关键文章页

## 5. Evidence Directories

- `dist/`
- `output/`

说明：

- `dist/` 用于保存构建输出
- `output/` 可用于截图、发布验证记录或其他交付证据

## 6. Progress / Closeout Note Convention

- 每轮改动建议在 `.adpp/changes/<feature>/closeout-note.md` 记录
- 如果本轮涉及发布，可附带 `deploy-record.md`
- closeout 里至少写清：范围、更新文档、验证命令、证据路径、剩余风险
