# Spider-Man Profile — Deploy Guide

## Quick Start

Your profile README lives in a **special GitHub repo** that shares your username.

```
GitHub username:  Robibiruk
Profile repo:    Robibiruk/Robibiruk   (must match exactly)
README file:     README.md              (at repo root)
```

## Step-by-step

### 1. Create the profile repo (if you haven't already)

```
GitHub → New repo → Name: Robibiruk → Public → Initialize with README
```

### 2. Push the spiderman-profile content

```bash
cd spiderman-profile

# Remove the default README GitHub created
git rm README.md

# Copy everything into the repo root
cp -r assets/ .github/ docs/ theme/ tools/ README.md .
rm -rf spiderman-profile  # or just work from the repo root going forward

git add .
git commit -m "🕸️ Spider-Man themed profile"
git push origin main
```

### 3. Verify

Visit `https://github.com/Robibiruk` — you should see the full Spider-Man profile with animated SVGs, stats cards, and contribution visualizations.

## GitHub Actions (auto-refresh)

The workflow `.github/workflows/refresh.yml` runs **twice a week** (Mon + Thu at 06:17 UTC) to regenerate the Web Arsenal, Web Swing, Achievements, Hero Stats, and Web Streak charts with fresh data.

### How it works

1. `generate.py` fetches your repos + languages from the GitHub REST API (no token needed)
2. If a `GITHUB_TOKEN` is available (it is, automatically), it also fetches the real contribution calendar via GraphQL
3. Writes `web-arsenal.svg`, `web-swing.svg`, `achievements.svg`, `hero-stats.svg`, and `streak-stats.svg` to `assets/`
4. Commits and pushes if anything changed

### Manual trigger

Go to **Actions → Refresh Spider-Man Assets → Run workflow** to force a refresh anytime.

### To use real contribution data (not demo)

The `GITHUB_TOKEN` provided by Actions has read-only access. For the contribution calendar to show **real** data (not demo), the token needs `user` scope. Options:

1. **Default GITHUB_TOKEN** (automatic) — works for repos + languages. Contribution calendar may be limited.
2. **Personal Access Token** — create a PAT with `read:user` scope, add it as a repo secret named `PAT`, then update the workflow:
   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.PAT }}
   ```

## Customization

### Change the username

Edit `tools/generate.py` line with `--username` default, or pass it as an argument:

```bash
python tools/generate.py --username YourUsername
```

### Swap themes

The theme config is in `theme/theme.json`. To adapt for another superhero:

1. Copy `theme/theme.json` → `theme/thor.json` (or whatever)
2. Update palette, terminology, and structure
3. Regenerate SVG assets with the new palette constants
4. Update badge colors in `README.md` to match

### Add more SVG assets

All SVGs use SMIL animations (no JavaScript). GitHub renders them inside `<img>` tags. Rules:

- **No `<script>` tags** — GitHub strips them
- **No external fonts** — use system fonts only (Impact, Segoe UI, Consolas)
- **Use `viewBox`** — makes SVGs responsive
- **Add `role="img"` and `aria-label`** — accessibility
- **Test with `--screenshot`** — Edge headless for quick visual checks

## File Structure

```
spiderman-profile/
├── README.md                    # The profile (push to Robibiruk/Robibiruk)
├── assets/
│   ├── hero.svg                 # Animated hero intro (hand-crafted)
│   ├── web-divider.svg          # Section divider with spider (hand-crafted)
│   ├── spider-sense.svg         # Status card (hand-crafted)
│   ├── footer.svg               # Footer quote (hand-crafted)
│   ├── web-arsenal.svg          # Tech stack hub (auto-generated)
│   ├── web-swing.svg            # 52-week activity skyline (auto-generated)
│   ├── achievements.svg         # Spider-Verse comic badges (auto-generated)
│   ├── hero-stats.svg           # Hero stats HUD (auto-generated)
│   └── streak-stats.svg         # Contribution streak HUD (auto-generated)
├── tools/
│   └── generate.py              # Data fetcher + SVG renderer
├── theme/
│   └── theme.json               # Theme plugin config
├── .github/
│   └── workflows/
│       └── refresh.yml          # Auto-refresh schedule
└── docs/
    └── DEPLOY.md                # This file
```

## Troubleshooting

**SVGs not rendering?**
- Check the image path in the `<img>` tag matches the file location
- GitHub serves `assets/` files from raw.githubusercontent.com
- If the repo is private, the images won't load on your public profile page

**Stats cards showing wrong data?**
- The readme-stats service caches data. Wait 30 minutes or try `?cache_bust=1`

**Web Swing shows "DEMO"?**
- The GraphQL query needs a token with `user` scope
- Without it, `generate.py` falls back to deterministic demo data seeded from your username

**Actions workflow failing?**
- Check the Actions tab for error logs
- Ensure Python 3.12 is available (ubuntu-latest has it)
- The workflow uses `secrets.GITHUB_TOKEN` which is automatic — no setup needed
