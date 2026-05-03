# UX 设计要点: blog-foundation

> 用途：为实现阶段提供可执行的 UI/UX 输入，服务于 VitePress 博客首期搭建。

**基于系统设计**: `.adpp/changes/2026-05-02-blog-foundation/design.md`
**状态**: 草稿

## 1. 变更范围

- 功能名称：博客站点首期页面体验设计
- 涉及页面：首页、主栏目专题页、文章页
- 主要用户角色：技术博客读者、Java 学习者、求职者、站点作者本人
- 本次改动目标：建立清晰、稳定、适合长期扩展的博客页面体验

## 2. 设计输入总表

| 页面/模块 | 设计工具 | 链接 / 节点 | 页面用途 | 是否当前可访问 | 截图/导出稿路径 | 备注 |
|---|---|---|---|---|---|---|
| 首页 | 文档设计 | `docs/index.md` | 表达博客定位并分发内容 | 是 | 无 | 首期采用文档驱动设计 |
| 主栏目专题页 | 文档设计 | `docs/java/index.md`、`docs/microservices/index.md`、`docs/ai/index.md`、`docs/vibe-coding/index.md`、`docs/project/index.md`、`docs/career/index.md` | 承接主导航并解释栏目结构 | 是 | 无 | 每个主栏目一页 |
| 文章页 | 文档设计 | `docs/java/basics/java-basics-overview.md`、`docs/ai/llm-basics/llm-basics-overview.md`、`docs/vibe-coding/workflows/vibe-coding-overview.md`、`docs/vibe-coding/trae/trae-overview.md`、`docs/vibe-coding/codex/codex-overview.md`、`docs/vibe-coding/claude/claude-overview.md`、`docs/project/ai-projects/ai-projects-overview.md`、`docs/project/blog-build/blog-build-overview.md` | 承载技术长文阅读 | 是 | 无 | 依托 VitePress 默认阅读模型 |

## 3. 页面级实现说明

### 3.1 首页

- 对应设计输入：`design.md` 中“4.1 首页”
- 页面目标：让用户快速理解博客定位，并进入核心栏目或文章
- 默认态：展示 Hero、方向入口卡片、精选文章、最新文章、关于站点
- 空态：若暂时没有精选或最新文章，显示“内容正在整理中，欢迎先从专题页开始阅读”
- 加载态：静态站点首期不单独设计异步加载态，保持静态直出
- 错误态：若某个推荐区块数据缺失，则隐藏该区块，不影响页面整体浏览
- 成功态：用户可从首页顺利进入栏目页、文章页或关于页

### 3.2 主栏目专题页

- 对应设计输入：`design.md` 中“4.2 主栏目页”
- 页面目标：解释栏目内容范围，并提供子栏目和推荐阅读入口
- 默认态：展示专题简介、子栏目入口、推荐文章列表、学习建议
- 空态：若当前栏目文章较少，显示“该专题正在持续更新，建议先阅读基础入门内容”
- 加载态：静态站点首期不单独设计
- 错误态：若推荐文章未配置，则展示子栏目入口和专题简介
- 成功态：用户能明确知道该栏目讲什么、先看什么、去哪里继续阅读

### 3.3 文章页

- 对应设计输入：`design.md` 中“4.3 文章页”
- 页面目标：承载技术文章阅读，突出结构、代码和可扫读性
- 默认态：展示标题、元信息、目录、正文、代码块、结尾总结
- 空态：理论上不存在；若文章内容未完成，可保留简短占位说明但不应正式发布
- 加载态：静态站点首期不单独设计
- 错误态：若图片或资源失效，不应破坏正文排版，应保留文本可读性
- 成功态：用户可以顺畅阅读、跳转目录、复制代码并回到栏目上下文

## 4. 交互流程

### 首页主流程

1. 用户进入首页
2. 首屏看到博客定位与主方向说明
3. 点击主方向卡片，例如 `AI 与大模型` 或 `Vibe Coding`
4. 系统跳转到对应专题页
5. 用户继续点击推荐文章进入正文页

### 栏目页主流程

1. 用户进入某个主栏目专题页
2. 浏览栏目简介与子栏目说明
3. 点击某个子栏目或推荐文章
4. 系统跳转到对应文章页或专题入口

### 文章页主流程

1. 用户进入文章页
2. 通过目录快速定位到感兴趣章节
3. 阅读正文与代码示例
4. 阅读完后通过文末链接或导航回到专题页继续浏览

### 分支 A：内容较少时

- 首页或栏目页可优先展示专题说明，而不是硬凑大量文章列表

### 分支 B：某栏目尚未积累足够文章时

- 显示“持续更新中”的轻提示，但仍保留该栏目入口，体现结构完整性

## 5. 组件清单

| 类型 | 名称 | 新增/复用 | 来源 | 备注 |
|---|---|---|---|---|
| 页面 | 首页 | 新增 | VitePress 页面 | 自定义内容布局 |
| 页面 | 主栏目专题页 | 新增 | Markdown 页面 | 每个主栏目一页 |
| 页面 | 文章页 | 复用 | VitePress 默认文章页 | 以默认主题为主 |
| 组件 | Hero 区块 | 新增 | 首页定制 | 可用 Markdown + 少量样式实现 |
| 组件 | 方向入口卡片 | 新增 | 首页/专题页复用 | 承载主栏目入口 |
| 组件 | 推荐文章列表 | 新增 | 页面级内容模块 | 首期可先静态配置 |
| 组件 | 关于站点模块 | 新增 | 首页内容模块 | 轻量介绍即可 |
| 组件 | 目录侧栏 | 复用 | VitePress 默认能力 | 文章页核心体验 |
| 组件 | 代码块展示 | 复用 | VitePress 默认能力 | 重点依赖默认高亮 |

## 6. 视觉约束

- 布局：首页采用纵向单页分区布局，专题页和文章页以单栏正文为主，桌面端可带辅助侧边信息
- 间距：大区块之间保留明显呼吸感，推荐 32px 到 56px；卡片之间保持 16px 到 24px 间距
- 对齐：正文与标题优先左对齐；首页 Hero 内容可局部居中，但下方内容区保持左对齐更利于阅读
- 字体层级：页面主标题明显大于区块标题；区块标题明显大于正文；代码字体单独区分
- 颜色语义：主色建议蓝青系；强调色用于链接和按钮；弱信息用中性色；避免高饱和大面积撞色
- 圆角 / 阴影 / 边框：卡片可有轻圆角与轻边框，阴影要克制，整体偏技术文档感
- 图标：可以少量使用线性图标辅助栏目识别，但不要依赖图标承担主要信息表达

## 7. 表单与校验规则

本次范围不涉及表单交互。

## 8. 响应式要求

- 桌面端：首页展示完整分区，专题页可同时展示专题说明和推荐内容，文章页可保留目录侧栏
- 平板端：保留正文优先，缩减卡片并压缩首页模块密度
- 移动端：Hero 简化、卡片改单列、目录不应压缩正文阅读区域
- 必须折叠或改单列的模块：首页方向卡片区、精选/最新文章区、专题页子栏目列表

## 9. 文案与语气

- 关键按钮文案：`开始阅读`、`查看专题`、`进入栏目`、`继续阅读`
- 空态文案：`内容正在持续整理中，欢迎先从这个专题开始阅读。`
- 错误提示文案：`部分内容暂时不可用，但你仍然可以继续浏览其他文章。`
- 成功提示文案：本期静态站点不需要显式成功反馈
- 统一语气要求：专业、清晰、克制，不用过度营销化表达

## 10. 实现注意事项

- 不可偏离的设计点：首页必须体现 `Java + AI + Vibe Coding` 的复合定位
- 不可偏离的设计点：内容可读性优先于炫技展示
- 可以工程化调整的点：卡片样式、Hero 视觉、推荐区排序方式
- 已知未定项：精选文章和最新文章是否同时首期上线
- 已知未定项：关于我模块是放首页还是单独 about 页面优先
- 需要后续确认的点：是否在首期就加入文章封面图策略
- 当前已落地的首批文章入口：
  `docs/java/basics/java-basics-overview.md`
  `docs/java/collections/java-collections-overview.md`
  `docs/java/concurrency/java-concurrency-overview.md`
  `docs/java/jvm/jvm-overview.md`
  `docs/java/spring/spring-overview.md`
  `docs/java/spring-boot/spring-boot-overview.md`
  `docs/java/mysql/mysql-overview.md`
  `docs/microservices/redis/redis-overview.md`
  `docs/microservices/spring-cloud-alibaba/spring-cloud-alibaba-overview.md`
  `docs/ai/llm-basics/llm-basics-overview.md`
  `docs/ai/ai-app-dev/ai-app-dev-overview.md`
  `docs/java/build-tools/maven-gradle-overview.md`
  `docs/java/dev-tools/git-dev-tools-overview.md`
  `docs/project/java-projects/java-projects-overview.md`
  `docs/project/ai-projects/ai-projects-overview.md`
  `docs/project/blog-build/blog-build-overview.md`
  `docs/career/interview/interview-overview.md`
  `docs/career/learning-path/learning-path-overview.md`
  `docs/vibe-coding/trae/trae-overview.md`
  `docs/vibe-coding/codex/codex-overview.md`
  `docs/vibe-coding/claude/claude-overview.md`
  `docs/vibe-coding/workflows/vibe-coding-overview.md`

## 11. 交付前核对清单

- [x] 设计输入已补全为文档化说明
- [x] 关键交互流程已写清
- [x] 组件新增/复用关系已写清
- [x] 响应式要求已写清
- [x] 视觉约束已写清
