# Deploy Record - blog-foundation

## Target

- Platform: GitHub Pages
- Build source: GitHub Actions
- Site generator: VitePress

## Changes

- Added GitHub Pages workflow at `.github/workflows/deploy.yml`
- Updated `docs/.vitepress/config.mjs` to auto-detect the correct `base` during GitHub Actions builds
- Kept local preview base as `/` so local development remains unchanged

## Pre-Deploy Verification

- `npm.cmd run docs:build` passed locally
- Key routes verified in local preview:
  - `/`
  - `/java/`
  - `/ai/`
  - `/vibe-coding/`
  - `/java/basics/java-basics-overview`
  - `/vibe-coding/codex/codex-overview`

## Release Notes

- If the GitHub repository name is not `<username>.github.io`, the production build will publish under `/<repository>/`
- If the repository name is `<username>.github.io`, the production build will publish at `/`

## Manual Follow-Up

- In repository settings, set `Pages > Build and deployment > Source` to `GitHub Actions`
- Push to the `main` branch to trigger the workflow
- Confirm the generated site URL after the first successful deployment

## Risks

- The current workspace is not a Git repository, so remote URL and default branch could not be auto-detected locally
- The workflow currently deploys on `main`; if the actual default branch is different, update `.github/workflows/deploy.yml`

## Deployment Attempt - 2026-05-03

- Commit pushed to `main`: `3678f17 chore: add GitHub Pages deployment workflow`
- Repository detected successfully:
  - Remote: `https://github.com/LordVoldemt/java-fullstack-blog.git`
  - Default branch: `main`
  - Visibility: `public`
- Local verification:
  - `npm.cmd run docs:build` passed before push
- GitHub Actions result:
  - Run URL: `https://github.com/LordVoldemt/java-fullstack-blog/actions/runs/25267948576`
  - Build job status: `failure`
  - Failed step: `Setup Pages`
- GitHub repository metadata:
  - `has_pages: false`
- Published site check:
  - `https://lordvoldemt.github.io/java-fullstack-blog/` returned `404`

## Next Action

- Open GitHub repository settings and enable `Pages`
- Set `Build and deployment > Source` to `GitHub Actions`
- Re-run the failed workflow or push a new commit to `main`

## Deployment Attempt - 2026-05-13

- Commit pushed to `main`: `1be7e41 docs: add java basics presentation`
- Scope:
  - Added the Java basics dynamic HTML presentation at `docs/public/presentations/java-basics-dynamic-presentation.html`
  - Added an article entry link in `docs/java/basics/java-basics-overview.md`
  - Added presentation link styles in `docs/.vitepress/theme/custom.css`
- Local verification:
  - `npm run docs:build` passed before push
  - Local presentation URL returned `200`: `/presentations/java-basics-dynamic-presentation.html`
- Publish command:
  - `.\scripts\deploy.ps1 -Message "docs: add java basics presentation"`
- Push result:
  - `main` pushed to `https://github.com/LordVoldemt/java-fullstack-blog.git`
- Production check immediately after push:
  - Existing article URL returned `200`
  - New presentation URL still returned `404`, likely because GitHub Actions / Pages deployment had not completed yet
- Notes:
  - `npm run deploy -- --Message ...` failed locally because `powershell` was not available on `PATH`; direct PowerShell script execution succeeded
