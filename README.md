# java-fullstack-blog

一个基于 `VitePress + Markdown + GitHub Pages` 的个人技术博客。

## 本地启动

首次安装依赖后，启动本地开发服务：

```powershell
npm install
npm run docs:dev
```

默认会启动一个本地预览地址，通常是：

```text
http://localhost:5173/
```

## 本地构建与预览

修改文章后，可以先本地构建检查：

```powershell
npm run docs:build
```

如果想用接近生产的方式预览构建结果：

```powershell
npm run docs:preview
```

## 文章发布流程

1. 在 `docs/` 下修改或新增 Markdown 文章
2. 运行 `npm run docs:build` 检查构建是否通过
3. 执行发布脚本提交并推送到 `main`
4. GitHub Actions 自动部署到 GitHub Pages

## 一键发布脚本

项目内置了 PowerShell 发布脚本：

```powershell
npm run deploy -- "docs: 更新 Java 并发文章"
```

它会自动执行：

- `npm run docs:build`
- 只暂存博客发布相关内容：`docs`、`README.md`、`package.json`、`package-lock.json`、`scripts`、`.github`
- `git commit -m "<你的提交信息>"`
- `git push origin main`

推送成功后，GitHub Actions 会自动发布站点。
