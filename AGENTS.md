<!-- ADPP-CODEX:START -->
## ADPP / Codex 工作流

- 优先读取 `.adpp/config.yaml`、`.adpp/spec/`、`.adpp/references/doc-closeout.md`
- 优先使用仓库自动发现的 repo skills：`$adpp-init`、`$adpp-prd`、`$adpp-design`、`$adpp-ux`、`$adpp-implement`、`$adpp-test`、`$adpp-deploy`、`$adpp-closeout`、`$adpp-status`
- 根据用户意图加载 `.adpp/skills/*.md`
- 如果用户直接输入“初始化项目 / 写 PRD / 系统设计 / 前端设计 / 编码实现 / 测试 / 部署 / 收口”，应优先匹配上述 ADPP repo skills
- 如果项目尚未初始化，但已运行 `adpp setup --target codex`，则回退读取 `.codex/adpp-skills/*.md`
- Codex 的 repo skill 自动发现目录为 `.agents/skills/`
- 初始化阶段的模板回退目录为 `.codex/adpp-templates/`
- 若用户要求“本轮完成”或“收口”，先执行 closeout 流程，再宣称完成
- Codex 侧的补充说明见 `.codex/ADPP-CODEX.md`
<!-- ADPP-CODEX:END -->

# Agent 工作规范 - java全栈

本项目遵循 ADPP 模式。所有 agent 必须：

1. 编码前读取对应的阶段文档，默认是 `.adpp/changes/<feature>/tasks.md`；如涉及界面或主题，还要读取 `ux-notes.md`
2. 遵守 `.adpp/spec/` 下的编码、文档、测试规范
3. 不得执行危险操作，参考 `.adpp/config.yaml` 中的 `danger_operations`
4. 所有实质性改动都应有对应验证，当前项目最低验证门槛是 `npm run docs:build`
5. 声称“本轮完成”前，先执行 ADPP closeout 流程
6. 模型选择与密钥配置由外部运行环境管理，不写入项目配置

项目技术栈：`VitePress + Markdown + GitHub Pages`
项目定位：分享 Java 知识的个人博客站点
