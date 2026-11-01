# Observatory README: guide

## Use it (2 minutes)
1. Click **Use this template** and name the repo exactly `YOUR-USERNAME/YOUR-USERNAME`.
2. Edit `readme.config.json` (name, tagline, missions, exhibits, instruments, socials).
3. Go to **Actions → Refresh profile → Run workflow**. Your `README.md` and `assets/*.svg` are generated and committed. It then re-runs every 6 hours.

Optional: add a `PROFILE_TOKEN` repo secret (a PAT with `read:user`) so private contributions count.

## Run locally
```bash
python3 tools/generate.py --demo           # offline, demo data
python3 tools/generate.py --username you   # live public data
GITHUB_TOKEN=ghp_xxx python3 tools/generate.py --username you
```
Python 3.9+, no dependencies.

## Switch or add a theme
`--theme spiderman` (or set `"theme"` in the config) re-skins everything.
To make your own: copy `themes/observatory/` to `themes/mine/`, change the `palette`,
`fonts`, and `labels` in `theme.json`. Labels rename every section, so a theme can change the
whole vocabulary (missions → cases, streak → web streak). Open a PR to share it.

## Add a module
Each section is a function `render_x(cfg, T, data) -> svg string` in `tools/generate.py`,
registered in `RENDERERS`. Add one, then reference `assets/x.svg` from `templates/README.md.tmpl`.

## Notes
- GitHub renders README images without JavaScript. All motion here is SMIL animation inside SVG.
- Web fonts can't load inside `<img>` SVGs, so every font has a system fallback.
- Images are cached by GitHub's proxy; updates can take a few minutes to appear.
