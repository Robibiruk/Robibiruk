#!/usr/bin/env python3
"""
Glassmorphism × Yellow GitHub Contribution Calendar × Contribution Nexus Generator
- assets/hero.svg          : Custom ASCII portrait from assets/og-image.jpg + System HUD
- assets/exhibits.svg      : Project Showcase cards
- assets/instruments.svg   : Categorized Language & AI Models Arsenal with Vector Brand Icons
- assets/missions.svg      : Engineering Trajectory
- assets/telemetry.svg     : Live Telemetry & Language Distribution with Vector Brand Icons
- assets/nexus.svg         : Holographic 4-Axis Contribution Nexus (at the bottom section)
- assets/contributions.svg : Exact GitHub Contribution Calendar structure in Yellow/Gold theme with animations
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import random
import sys
import textwrap
import urllib.request
from collections import deque
from pathlib import Path

from tech_icons import TECH_ICONS, render_icon

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
GQL = "https://api.github.com/graphql"
PALETTE_ASCII = " .,:-~=+*#%@"

FALLBACK_PORTRAIT = [
    "                     .   ..,:;~~==++*#%@@@%#*+=~:.              ",
    "                   .,:;~=+*#%%@@@@@@@@@@@@@@@@@@@%#*=:.         ",
    "                 .:~+*#%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+,.      ",
    "                :;*#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#;.     ",
    "               ~#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+     ",
    "              *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*    ",
    "             +@@@@@@@@@@@@@@@@@#**++====++**#%@@@@@@@@@@@@@@~   ",
    "            .@@@@@@@@@@@@@#+=~::,,........,,::;~+*#@@@@@@@@@#   ",
    "            ;@@@@@@@@@@#+~:,....,,::;;;;;;::,,....,=*@@@@@@@@,  ",
    "            +@@@@@@@@@*:,..,::;~~===++++++===~~;:,..:*@@@@@@@:  ",
    "            *@@@@@@@@+...,:;~==++++++++++++++++==~;:.,+@@@@@@:  ",
    "            #@@@@@@@@:.,:;~==+++**************+++==~;,,#@@@@@   ",
    "            %@@@@@@@%..:;~=++*#%@@@@@%##*+*#%@@@@@#*=;,*@@@@#   ",
    "            @@@@@@@@#.,;~=++#@@@%*++*#%@%++%@#**+#@@@*;;@@@@+   ",
    "            ~@@@@@@@#.:;~=+*@#=:..:*@@*:=@@+..:+#@*+#@+;@@@#    ",
    "             %@@@@@@%.:;~==++~..:;~==+~.:@@~..;~===~+*~*@@@:    ",
    "             .@@@@@@@,.:;~===~~~===+++~.:@@+.:~===++===#@@~     ",
    "              :@@@@@@~.,:;~~======+++*~.:@@*.:~====~~~*@@+      ",
    "               ;@@@@@#..,:;~~~====++*#;.:@@#;:;~~~~~~=@@#       ",
    "                ~@@@@@*..,:;~~~===+*#%@@@%#@@#+=~~~~*@@@.       ",
    "                 ;@@@@@+..,:;~~==+*#%*=~:;~+#@%+=~~+@@@:        ",
    "                  ~@@@@@*..,:;~~=+*#+~===++~:*#+=~*@@@~         ",
    "              .,:~+*@@@@@#:.,:;~~=+*#%@@@@%#*+=~~#@@@*          ",
    "          .,;~+*#%#*=*@@@@@*:,:;~~==++*****++=~+#@@@@#%#*+~:.   ",
    "       .:~*#@@@@@%*+=~+@@@@@@#+~;;;~~~====~~~=*#@@@@@%*#%@@@@#+:",
    "     .;*#@@@@@@%*+==~~~*@@@@@@@%#*+===~~~~==+#@@@@@@@#+=+*#%@@@@",
    "    :#@@@@@@@@%*+===~~~;+@@@@@@@@@@@#*++++*#@@@@@#@@@@%*++++*#@@",
    "   *@@@@@@@@@@@#*+==~~~::*@@@@@@@@@@@@@%%@@@@@@@*;#@@@@@#*++*#@@",
    "  #@@@@@@@@@@@@@%*+=~~~:.:#@@@@@@@@@@@@@@@@@@@@#:,~%@@@@@@###@@@",
    " +@@@@@@@@@@@@@@@%*+=~~:..;@@@@@@@@@@@@@@@@@@@#,...+@@@@@@@@@@@@",
    ".@@@@@@@@@@@@@@@@@@#*+~:,..*@@@@@@@@@@@@@@@@@%:...,,*@@@@@@@@@@@",
    "#@@@@@@@@@@@@@@@@@@@@#*;:,.:#@@@@@@@@@@@@@@@#;..:;%@@@@@@@@@@@@@",
    "@@@@@@@@@@@@@@@@@@@@@@@*;:,,~@@@@@@@@@@@@@@%+. .;#@@%#@@@@@@@@@@",
    "@@@@@@@@@@@@@@@@@@@@@@@@%+;::+@@@@@@@@@@@@@*...,*@@@#*%@@@@@@@@@",
    "@@@@@@@@@@@@@@@@@@@@@@@@@@#*++@@@@@@@@@@@@@+..:+@@@@@%%@@@@@@@@@",
    "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#**#@@@@@@@@@@@@@@@@@"
]


def esc(s: object) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_json(path: Path | str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def http(url: str, token: str | None = None, body: dict | None = None) -> dict | list:
    headers = {
        "User-Agent": "glassmorphism-nexus-readme",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def generate_portrait_ascii(img_path: Path, width: int = 64, height: int = 36) -> list[str]:
    if not img_path.exists():
        return FALLBACK_PORTRAIT
    try:
        from PIL import Image, ImageFilter

        img = Image.open(img_path).convert("RGB")
        w0, h0 = img.size
        crop = img.crop((int(w0 * 0.20), int(h0 * 0.16), int(w0 * 0.84), int(h0 * 0.70)))
        small = crop.resize((width, height), Image.Resampling.LANCZOS)
        edges = small.convert("L").filter(ImageFilter.FIND_EDGES)

        px_rgb = small.load()
        px_ed = edges.load()

        bg_mask = [[False] * width for _ in range(height)]
        q: deque[tuple[int, int]] = deque()

        def is_bg(r: int, c: int) -> bool:
            R, G, B = px_rgb[c, r]
            lum = 0.299 * R + 0.587 * G + 0.114 * B
            warmth = R - B
            ny, nx = r / max(1, height - 1), c / max(1, width - 1)
            in_head = (0.08 <= ny <= 0.55 and 0.30 <= nx <= 0.68)
            in_torso = (ny > 0.52 and 0.12 <= nx <= 0.88)
            if in_head and (lum < 102 or warmth > 24 or (0.16 <= ny <= 0.50 and 0.36 <= nx <= 0.62)):
                return False
            if in_torso and (lum < 112 or warmth > 20 or (0.20 <= nx <= 0.80 and lum < 140)):
                return False
            return lum > 105 and warmth < 32

        for c in range(width):
            if is_bg(0, c):
                bg_mask[0][c] = True
                q.append((0, c))
        for r in range(height):
            for c in (0, width - 1):
                if not bg_mask[r][c] and is_bg(r, c):
                    bg_mask[r][c] = True
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < height and 0 <= nc < width and not bg_mask[nr][nc]:
                    if is_bg(nr, nc):
                        bg_mask[nr][nc] = True
                        q.append((nr, nc))

        rows = []
        for r in range(height):
            line = []
            for c in range(width):
                if bg_mask[r][c]:
                    line.append("." if (c * 23 + r * 41) % 127 == 0 else " ")
                    continue
                R, G, B = px_rgb[c, r]
                lum = (0.299 * R + 0.587 * G + 0.114 * B) / 255.0
                warmth = max(0.0, (R - B) / 255.0)
                ed = px_ed[c, r] / 255.0
                if warmth > 0.09:
                    val = 0.32 + (lum - 0.18) * 1.35 + warmth * 0.42 + ed * 0.18
                else:
                    val = 0.18 + lum * 0.82 + ed * 0.42
                idx = max(1, min(len(PALETTE_ASCII) - 1, int(val * (len(PALETTE_ASCII) - 1))))
                line.append(PALETTE_ASCII[idx])
            rows.append("".join(line))
        return rows
    except Exception as exc:
        print(f"[info] Pillow portrait conversion skipped ({exc}); using embedded portrait matrix.", file=sys.stderr)
        return FALLBACK_PORTRAIT


def demo_weeks_days(username: str) -> list[list[tuple[str, int]]]:
    """Generate 52 weeks of 7 days (Sun..Sat) ending this week, matching GitHub's calendar layout."""
    rng = random.Random(sum(ord(ch) for ch in username))
    today = datetime.date.today()
    # Align start to Sunday 52 weeks ago
    days_since_sun = (today.weekday() + 1) % 7
    end_sun = today - datetime.timedelta(days=days_since_sun)
    start_sun = end_sun - datetime.timedelta(weeks=51)
    weeks = []
    for w in range(52):
        wk = []
        for d in range(7):
            cur_d = start_sun + datetime.timedelta(weeks=w, days=d)
            if cur_d > today:
                cnt = 0
            else:
                # Higher activity in recent months to look realistic like the screenshot
                boost = 1.35 if w > 28 else 0.85
                cnt = 0 if rng.random() < (0.42 / boost) else max(1, int(rng.gauss(3.8 * boost, 2.8)))
            wk.append((cur_d.isoformat(), cnt))
        weeks.append(wk)
    return weeks


def fetch_data(username: str, token: str | None, demo: bool) -> dict:
    weeks_default = demo_weeks_days(username)
    flat_days = [item for wk in weeks_default for item in wk]
    data = {
        "real": False,
        "followers": 16,
        "repos": 35,
        "stars": 16,
        "commits": 659,
        "prs": 35,
        "reviews": 7,
        "issues": 0,
        "commit_pct": 94,
        "pr_pct": 5,
        "review_pct": 1,
        "issue_pct": 0,
        "total_contribs": sum(c for _, c in flat_days),
        "langs": [
            ("TypeScript", 36.4),
            ("Python", 31.8),
            ("JavaScript", 15.2),
            ("HTML5", 8.4),
            ("CSS3", 4.8),
            ("Shell", 3.4),
        ],
        "weeks": weeks_default,
        "days": flat_days,
        "created": "2025-07-23",
    }
    if demo:
        return data

    try:
        user = http(f"{API}/users/{username}", token)
        repos, page = [], 1
        while True:
            batch = http(f"{API}/users/{username}/repos?per_page=100&sort=updated&page={page}", token)
            if not isinstance(batch, list):
                break
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1

        own_repos = [r for r in repos if not r.get("fork")]
        lang_bytes: dict[str, int] = {}
        for r in sorted(own_repos, key=lambda x: x.get("pushed_at") or "", reverse=True)[:30]:
            try:
                lmap = http(r["languages_url"], token)
                if isinstance(lmap, dict):
                    for k, v in lmap.items():
                        lang_bytes[k] = lang_bytes.get(k, 0) + int(v)
            except Exception:
                if r.get("language"):
                    lang_bytes[r["language"]] = lang_bytes.get(r["language"], 0) + max(1, r.get("size", 1)) * 1024

        total_b = sum(lang_bytes.values()) or 1
        langs = sorted(((k, v / total_b * 100.0) for k, v in lang_bytes.items()), key=lambda kv: -kv[1])

        data.update({
            "followers": user.get("followers", data["followers"]),
            "repos": len(own_repos) or len(repos),
            "stars": sum(r.get("stargazers_count", 0) for r in repos),
            "langs": langs[:6] if langs else data["langs"],
            "created": (user.get("created_at") or "")[:10],
            "real": True,
        })

        if token:
            q = """
            query($l: String!) {
              user(login: $l) {
                contributionsCollection {
                  totalCommitContributions
                  totalPullRequestContributions
                  totalPullRequestReviewContributions
                  totalIssueContributions
                  restrictedContributionsCount
                  contributionCalendar {
                    totalContributions
                    weeks {
                      contributionDays {
                        date
                        contributionCount
                      }
                    }
                  }
                }
              }
            }
            """
            res = http(GQL, token, {"query": q, "variables": {"l": username}})
            cc = res["data"]["user"]["contributionsCollection"]
            cal = cc["contributionCalendar"]
            gql_weeks = [
                [(d["date"], d["contributionCount"]) for d in w["contributionDays"]]
                for w in cal["weeks"]
            ]
            if gql_weeks:
                data["weeks"] = gql_weeks[-53:]
                data["days"] = [item for wk in data["weeks"] for item in wk]
            data["total_contribs"] = cal.get("totalContributions", sum(c for _, c in data["days"]))
            c_cnt = cc.get("totalCommitContributions", 0) + cc.get("restrictedContributionsCount", 0)
            pr_cnt = cc.get("totalPullRequestContributions", 0)
            rv_cnt = cc.get("totalPullRequestReviewContributions", 0)
            is_cnt = cc.get("totalIssueContributions", 0)
            act_sum = c_cnt + pr_cnt + rv_cnt + is_cnt
            if act_sum > 0:
                data["commits"] = c_cnt
                data["prs"] = pr_cnt
                data["reviews"] = rv_cnt
                data["issues"] = is_cnt
                data["commit_pct"] = max(1, round(c_cnt / act_sum * 100)) if c_cnt else 0
                data["pr_pct"] = max(1, round(pr_cnt / act_sum * 100)) if pr_cnt else 0
                data["review_pct"] = max(1, round(rv_cnt / act_sum * 100)) if rv_cnt else 0
                data["issue_pct"] = round(is_cnt / act_sum * 100) if is_cnt else 0
    except Exception as exc:
        print(f"[warn] live fetch failed ({exc.__class__.__name__}: {exc}); using fallback data", file=sys.stderr)
        data["real"] = False
    return data


def streaks(days: list[tuple[str, int]]) -> tuple[int, int, int]:
    counts = [c for _, c in days]
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    cur = 0
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    return cur, best, sum(counts)


def calc_grade(data: dict) -> tuple[int, str, str]:
    c_score = min(data.get("commits", 300), 500) / 500 * 35
    r_score = min(data.get("repos", 30), 40) / 40 * 20
    s_score = min(data.get("stars", 15), 50) / 50 * 20
    p_score = min(data.get("prs", 5), 25) / 25 * 15
    f_score = min(data.get("followers", 15), 40) / 40 * 10
    total = int(round(c_score + r_score + s_score + p_score + f_score))
    if total >= 82:
        return total, "S+", "ORBITAL ARCHITECT"
    if total >= 70:
        return total, "A+", "PRINCIPAL VANGUARD"
    if total >= 58:
        return total, "A", "SYSTEMS COMMANDER"
    return total, "B+", "FIELD ENGINEER"


# ------------------------------------------------------------------ Glassmorphism SVG Kit
def glass_panel(x: float, y: float, w: float, h: float, rx: float = 14, border_col: str = "#3b82f6",
                border_op: float = 0.45, fill_op: float = 0.58, top_glow: str | None = None) -> str:
    s = (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
        f'fill="#0b1324" fill-opacity="{fill_op}" stroke="{border_col}" stroke-opacity="{border_op}" stroke-width="1.2"/>'
        f'<line x1="{x + rx:.1f}" y1="{y + 0.8:.1f}" x2="{x + w - rx:.1f}" y2="{y + 0.8:.1f}" '
        f'stroke="#ffffff" stroke-opacity="0.20" stroke-width="1"/>'
    )
    if top_glow:
        s += (
            f'<rect x="{x + 1:.1f}" y="{y + 1:.1f}" width="{w - 2:.1f}" height="3" rx="1.5" '
            f'fill="{top_glow}" fill-opacity="0.85"/>'
        )
    return s


def corner_reticles(w: int, h: int, color: str) -> str:
    return (
        f'<path d="M20 20h26M20 20v26M{w - 20} 20h-26M{w - 20} 20v26'
        f'M20 {h - 20}h26M20 {h - 20}v-26M{w - 20} {h - 20}h-26M{w - 20} {h - 20}v-26" '
        f'fill="none" stroke="{color}" stroke-width="1.5" stroke-opacity="0.7"/>'
    )


def particle_field(rng: random.Random, w: int, h: int, n: int, c: dict) -> str:
    out = []
    palette_pts = [c["yellow"], c["primary"], c["secondary"], c["cyan"], c["text"]]
    for _ in range(n):
        x, y = rng.uniform(28, w - 28), rng.uniform(28, h - 28)
        r = rng.choice([0.7, 1.0, 1.4, 1.8])
        col = rng.choice(palette_pts)
        if rng.random() < 0.55:
            out.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}">'
                f'<animate attributeName="opacity" values="0.08;0.85;0.08" dur="{rng.uniform(2.4, 5.4):.1f}s" '
                f'begin="{rng.uniform(0, 3.5):.1f}s" repeatCount="indefinite"/></circle>'
            )
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="0.20"/>')
    return "".join(out)


def frame(w: int, h: int, body: str, label: str, T: dict, defs: str = "", stars: int = 34, seed: int = 1) -> str:
    c = T["palette"]
    rng = random.Random(seed)
    base_defs = (
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        f'<path d="M 40 0 L 0 0 0 40" fill="none" stroke="{c["border"]}" stroke-width="0.6" stroke-opacity="0.32"/>'
        '</pattern>'
        f'<radialGradient id="ambientBlue" cx="0.2" cy="0.15" r="0.85">'
        f'<stop offset="0" stop-color="{c["primary"]}" stop-opacity="0.14"/>'
        f'<stop offset="0.5" stop-color="{c["secondary"]}" stop-opacity="0.06"/>'
        f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="ambientGold" cx="0.85" cy="0.85" r="0.65">'
        f'<stop offset="0" stop-color="{c["yellow"]}" stop-opacity="0.11"/>'
        f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></radialGradient>'
        '<filter id="softGlow" x="-25%" y="-25%" width="150%" height="150%">'
        '<feGaussianBlur stdDeviation="5" result="blur"/>'
        '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
        f'<defs>{base_defs}{defs}</defs>'
        f'<rect width="{w}" height="{h}" rx="18" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="1.5"/>'
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>'
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#ambientBlue)"/>'
        f'<rect width="{w}" height="{h}" rx="18" fill="url(#ambientGold)"/>'
        f'{corner_reticles(w, h, c["yellow"])}'
        f'{particle_field(rng, w, h, stars, c)}{body}</svg>\n'
    )


def head(T: dict, kicker: str, title: str, tag: str, y: int = 44) -> str:
    c, f = T["palette"], T["fonts"]
    return (
        f'<circle cx="42" cy="{y - 4}" r="3.8" fill="{c["yellow"]}">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>'
        f'<text x="54" y="{y}" font-family="{f["mono"]}" font-size="11" font-weight="600" letter-spacing="3" fill="{c["yellow"]}">{esc(kicker)}</text>'
        f'<text x="38" y="{y + 28}" font-family="{f["display"]}" font-size="24" font-weight="700" fill="{c["text"]}">{esc(title)}</text>'
        f'{glass_panel(822, y - 16, 142, 24, rx=12, border_col=c["yellow"], border_op=0.55, fill_op=0.65)}'
        f'<text x="893" y="{y}" text-anchor="middle" font-family="{f["mono"]}" font-size="9.5" font-weight="600" letter-spacing="2" fill="{c["yellow"]}">{esc(tag)}</text>'
    )


# ------------------------------------------------------------------ 1. HERO (ASCII Portrait + Glass HUD)
def render_hero(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    W, H = 1000, 460
    portrait_rows = generate_portrait_ascii(ROOT / cfg.get("portrait_path", "assets/og-image.jpg"), 64, 36)
    cur_streak, best_streak, _ = streaks(data["days"])
    score, grade, rank_title = calc_grade(data)

    defs = (
        f'<linearGradient id="goldBlueGrad" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{c["yellow"]}"/><stop offset="0.5" stop-color="{c["primary"]}"/><stop offset="1" stop-color="{c["violet"]}"/></linearGradient>'
        f'<linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c["yellow"]}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{c["yellow"]}" stop-opacity="0.22"/>'
        f'<stop offset="1" stop-color="{c["primary"]}" stop-opacity="0"/></linearGradient>'
        '<clipPath id="portraitClip"><rect x="36" y="64" width="416" height="360" rx="12"/></clipPath>'
    )

    ascii_tspans = []
    for idx, row in enumerate(portrait_rows):
        y_pos = 92 + idx * 9.2
        row_color = c["yellow"] if idx in (12, 13, 14) else (c["info"] if idx > 26 else c["text"])
        ascii_tspans.append(f'<tspan x="48" y="{y_pos:.1f}" fill="{row_color}">{esc(row)}</tspan>')

    portrait_panel = (
        f'{glass_panel(36, 40, 416, 384, rx=14, border_col=c["yellow"], border_op=0.5, fill_op=0.68)}'
        f'<rect x="37" y="41" width="414" height="26" rx="13" fill="#0f1b33" fill-opacity="0.85"/>'
        f'<circle cx="54" cy="54" r="4" fill="#ff5f56"/><circle cx="68" cy="54" r="4" fill="#ffbd2e"/><circle cx="82" cy="54" r="4" fill="#27c93f"/>'
        f'<text x="102" y="58" font-family="{f["mono"]}" font-size="9.5" letter-spacing="1.5" fill="{c["muted"]}">PORTRAIT // ASSETS/OG-IMAGE.JPG</text>'
        f'<text x="438" y="58" text-anchor="end" font-family="{f["mono"]}" font-size="9" font-weight="600" fill="{c["yellow"]}">ASCII·64x36</text>'
        f'<g clip-path="url(#portraitClip)">'
        f'<text font-family="{f["mono"]}" font-size="8.4" xml:space="preserve" opacity="0.94">{"".join(ascii_tspans)}</text>'
        f'<rect x="36" y="64" width="416" height="34" fill="url(#scanGrad)">'
        f'<animate attributeName="y" values="64;390;64" dur="6.5s" repeatCount="indefinite"/></rect>'
        f'</g>'
        f'{glass_panel(48, 396, 392, 20, rx=6, border_col=c["yellow"], border_op=0.4, fill_op=0.75)}'
        f'<text x="58" y="409" font-family="{f["mono"]}" font-size="8.5" letter-spacing="1.5" fill="{c["yellow"]}">BIOMETRIC ASCII RENDER // ACTIVE</text>'
        f'<text x="430" y="409" text-anchor="end" font-family="{f["mono"]}" font-size="8.5" fill="{c["ok"]}">● SYNCED</text>'
    )

    live_badge = "LIVE PAT TELEMETRY" if data["real"] else "SYNTHETIC TELEMETRY"
    tagline_lines = textwrap.wrap(cfg["tagline"], 46)[:2]
    tagline_svg = "".join(
        f'<text x="484" y="{212 + i * 22}" font-family="{f["display"]}" font-size="15" fill="{c["muted"]}">{esc(ln)}</text>'
        for i, ln in enumerate(tagline_lines)
    )

    hud_cards = [
        ("TOTAL SIGNALS", f"{data['total_contribs']:,}", c["yellow"]),
        ("ACTIVE STREAK", f"{cur_streak}d (BEST {best_streak}d)", c["primary"]),
        ("REPOS / STARS", f"{data['repos']} / ★ {data['stars']}", c["cyan"]),
        ("NEXUS RATING", f"{grade} · {score}/100", c["violet"]),
    ]
    cards_svg = ""
    for i, (k_label, val, col) in enumerate(hud_cards):
        cx = 484 + (i % 2) * 244
        cy = 262 + (i // 2) * 58
        cards_svg += (
            f'{glass_panel(cx, cy, 232, 48, rx=10, border_col=col, border_op=0.5, fill_op=0.55)}'
            f'<rect x="{cx}" y="{cy}" width="3.5" height="48" rx="1.7" fill="{col}"/>'
            f'<text x="{cx + 15}" y="{cy + 18}" font-family="{f["mono"]}" font-size="8.5" letter-spacing="1.5" fill="{c["muted"]}">{esc(k_label)}</text>'
            f'<text x="{cx + 15}" y="{cy + 38}" font-family="{f["display"]}" font-size="16" font-weight="700" fill="{c["text"]}">{esc(val)}</text>'
        )

    right_panel = (
        f'<circle cx="492" cy="56" r="4" fill="{c["yellow"]}">'
        f'<animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/></circle>'
        f'<text x="504" y="60" font-family="{f["mono"]}" font-size="10" letter-spacing="2.5" fill="{c["yellow"]}">{esc(live_badge)}  ·  {esc(cfg["location"])}</text>'
        f'<text x="484" y="120" font-family="{f["display"]}" font-size="54" font-weight="700" letter-spacing="1" fill="{c["text"]}">{esc(cfg["name"])}</text>'
        f'<rect x="484" y="136" width="476" height="2.5" rx="1.2" fill="url(#goldBlueGrad)"/>'
        f'<text x="484" y="162" font-family="{f["mono"]}" font-size="11.5" font-weight="600" letter-spacing="2" fill="{c["yellow"]}">{esc(cfg.get("role", "FULL-STACK & AI ENGINEER"))}</text>'
        f'{tagline_svg}'
        f'{cards_svg}'
        f'<rect x="484" y="388" width="232" height="36" rx="18" fill="{c["yellow"]}">'
        f'<animate attributeName="opacity" values="1;0.84;1" dur="2.8s" repeatCount="indefinite"/></rect>'
        f'<text x="600" y="411" text-anchor="middle" font-family="{f["mono"]}" font-size="11.5" font-weight="700" letter-spacing="1.5" fill="#050816">{esc(L["cta"])}</text>'
        f'{glass_panel(728, 388, 232, 36, rx=18, border_col=c["primary"], border_op=0.6, fill_op=0.6)}'
        f'<text x="844" y="411" text-anchor="middle" font-family="{f["mono"]}" font-size="10.5" font-weight="600" letter-spacing="1.5" fill="{c["yellow"]}">RANK: {esc(rank_title)}</text>'
    )

    return frame(W, H, portrait_panel + right_panel, f"{cfg['name']} — Hero ASCII HUD", T, defs, 38, 7)


# ------------------------------------------------------------------ 2. EXHIBITS (Project Showcase)
def render_exhibits(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    ex = cfg["exhibits"]
    rows = (len(ex) + 1) // 2
    W, H = 1000, 104 + rows * 142 + 16
    body = head(T, L["exhibits_kicker"], L["exhibits_title"], f"{len(ex)} SHIPPED")
    accent_cycle = [c["yellow"], c["primary"], c["violet"], c["cyan"]]
    for i, e in enumerate(ex):
        x, y = 38 + (i % 2) * 468, 98 + (i // 2) * 142
        live = bool(e.get("live"))
        k = accent_cycle[i % len(accent_cycle)]
        badge_col = c["yellow"] if i == 0 else (c["ok"] if live else c["warn"])
        body += (
            f'<g>'
            f'{glass_panel(x, y, 456, 128, rx=14, border_col=k, border_op=0.5, fill_op=0.6, top_glow=k)}'
            f'<circle cx="{x + 20}" cy="{y + 24}" r="3.5" fill="{badge_col}">'
            f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>'
            f'<text x="{x + 32}" y="{y + 28}" font-family="{f["mono"]}" font-size="9" font-weight="600" letter-spacing="2" fill="{badge_col}">{esc(L["live"] if live else L["flight"])}</text>'
            f'<text x="{x + 436}" y="{y + 28}" text-anchor="end" font-family="{f["mono"]}" font-size="9" fill="{c["muted"]}">0{i + 1} // EXHIBIT</text>'
            f'<text x="{x + 20}" y="{y + 56}" font-family="{f["display"]}" font-size="20" font-weight="700" fill="{c["text"]}">{esc(e["name"])}</text>'
        )
        for j, ln in enumerate(textwrap.wrap(e["desc"], 58)[:2]):
            body += f'<text x="{x + 20}" y="{y + 78 + j * 16}" font-family="{f["display"]}" font-size="12" fill="{c["muted"]}">{esc(ln)}</text>'
        px = x + 20.0
        for tag in e.get("stack", [])[:4]:
            tw = len(tag) * 6.8 + 32
            body += (
                f'<rect x="{px:.1f}" y="{y + 98}" width="{tw:.1f}" height="21" rx="10.5" fill="#060b18" stroke="{k}" stroke-opacity="0.5"/>'
                f'{render_icon(tag, px + 12, y + 108.5, scale=0.48, default_col=k)}'
                f'<text x="{px + 22:.1f}" y="{y + 112}" font-family="{f["mono"]}" font-size="8.8" fill="{c["text"]}">{esc(tag)}</text>'
            )
            px += tw + 6
        body += "</g>"
    return frame(W, H, body, "Project Showcase", T, "", 26, 5)


# ------------------------------------------------------------------ 3. INSTRUMENTS (Expanded Tech & Language Models with Icons)
def render_instruments(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    cols = [c["yellow"], c["primary"], c["violet"], c["cyan"], c["ok"]]
    y = 104
    out = ""
    total_tools = sum(len(v) for v in cfg["instruments"].values())
    for gi, (group, items) in enumerate(cfg["instruments"].items()):
        col = cols[gi % len(cols)]
        out += (
            f'<rect x="38" y="{y + 5}" width="4" height="20" rx="2" fill="{col}"/>'
            f'<text x="50" y="{y + 19}" font-family="{f["mono"]}" font-size="10.5" font-weight="700" letter-spacing="2" fill="{c["text"]}">{esc(group.upper())}</text>'
        )
        x = 240.0
        for it in items:
            w = len(it) * 7.5 + 42
            if x + w > 962:
                x, y = 240.0, y + 38
            out += (
                f'{glass_panel(x, y, w, 30, rx=9, border_col=col, border_op=0.5, fill_op=0.62)}'
                f'{render_icon(it, x + 16, y + 15, scale=0.62, default_col=col)}'
                f'<text x="{x + 30:.1f}" y="{y + 19}" font-family="{f["mono"]}" font-size="11" font-weight="600" fill="{c["text"]}">{esc(it)}</text>'
            )
            x += w + 8
        y += 48
    H = y + 18
    body = head(T, L["instruments_kicker"], L["instruments_title"], f"{total_tools} MODELS & TOOLS") + out
    return frame(1000, H, body, "Instruments & Language Models", T, "", 24, 9)


# ------------------------------------------------------------------ 4. MISSIONS (Trajectory)
def render_missions(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    ms = cfg["missions"]
    n = len(ms)
    W, H = 1000, 390
    xs = [100 + i * (800.0 / max(1, n - 1)) for i in range(n)] if n > 1 else [500]
    ys = [126 + 18 * math.sin(i * 1.25) for i in range(n)]
    d = f"M {xs[0]:.1f},{ys[0]:.1f}"
    for i in range(1, n):
        mx = (xs[i - 1] + xs[i]) / 2
        d += f" C {mx:.1f},{ys[i - 1]:.1f} {mx:.1f},{ys[i]:.1f} {xs[i]:.1f},{ys[i]:.1f}"
    col = {"complete": c["primary"], "current": c["yellow"], "future": c["muted"]}
    body = head(T, L["missions_kicker"], L["missions_title"], f"{n} MILESTONES")
    body += f'<path d="{d}" fill="none" stroke="{c["yellow"]}" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="4 6"/>'
    body += f'<circle r="4.5" fill="{c["yellow"]}" filter="url(#softGlow)"><animateMotion dur="11s" repeatCount="indefinite" path="{d}"/></circle>'
    cw = min(154.0, 800.0 / max(1, n - 1) - 10)
    for i, m in enumerate(ms):
        k = col.get(m.get("status", "complete"), c["primary"])
        x, y = xs[i], ys[i]
        pulse = ""
        if m.get("status") == "current":
            pulse = (
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="none" stroke="{k}" stroke-width="1.8">'
                f'<animate attributeName="r" values="12;28" dur="2s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.9;0" dur="2s" repeatCount="indefinite"/></circle>'
            )
        cy0 = 174
        body += (
            f'{pulse}<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#070d1f" stroke="{k}" stroke-width="2"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{k}"/>'
            f'<line x1="{x:.1f}" y1="{y + 11:.1f}" x2="{x:.1f}" y2="{cy0}" stroke="{k}" stroke-opacity="0.4"/>'
            f'{glass_panel(x - cw / 2, cy0, cw, 186, rx=12, border_col=k, border_op=0.5, fill_op=0.6, top_glow=k)}'
            f'<text x="{x - cw / 2 + 12:.1f}" y="{cy0 + 22}" font-family="{f["mono"]}" font-size="9" letter-spacing="1.5" fill="{c["muted"]}">{esc(L["mission"])} {esc(m["id"])}</text>'
            f'<text x="{x - cw / 2 + 12:.1f}" y="{cy0 + 40}" font-family="{f["mono"]}" font-size="11" font-weight="700" fill="{k}">{esc(m["year"])}</text>'
        )
        for j, ln in enumerate(textwrap.wrap(m["title"], 15)[:3]):
            body += (
                f'<text x="{x - cw / 2 + 12:.1f}" y="{cy0 + 62 + j * 16}" font-family="{f["display"]}" font-size="12.5" font-weight="700" fill="{c["text"]}">{esc(ln)}</text>'
            )
        tags = " · ".join(m.get("tags", [])[:2])
        body += f'<text x="{x - cw / 2 + 12:.1f}" y="{cy0 + 136}" font-family="{f["mono"]}" font-size="8.5" fill="{c["muted"]}">{esc(tags)}</text>'
        lab = L["current"] if m.get("status") == "current" else L["complete"]
        body += (
            f'<rect x="{x - cw / 2 + 12:.1f}" y="{cy0 + 150}" width="{cw - 24:.1f}" height="20" rx="10" fill="#060b18" stroke="{k}" stroke-opacity="0.7"/>'
            f'<text x="{x:.1f}" y="{cy0 + 163}" text-anchor="middle" font-family="{f["mono"]}" font-size="8" font-weight="600" letter-spacing="1" fill="{k}">{esc(lab)}</text>'
        )
    return frame(W, H, body, "Engineering Trajectory", T, "", 30, 3)


# ------------------------------------------------------------------ 5. TELEMETRY & LANGUAGES (With Embedded Brand Icons)
def render_telemetry(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    W, H = 1000, 410
    cur, best, _ = streaks(data["days"])
    score, grade, rank_title = calc_grade(data)
    tag = "LIVE GRAPHQL" if data["real"] else "DEMO MODE"
    body = head(T, L["telemetry_kicker"], L["telemetry_title"], tag)

    tiles = [
        (f"{data['total_contribs']:,}", L["commits"], c["yellow"]),
        (f"{cur} DAYS", L["streak"], c["primary"]),
        (f"{data['commits']:,}", "COMMITS PUSHED", c["secondary"]),
        (f"{best} DAYS", L["best"], c["violet"]),
        (f"{data['repos']}", L["repos"], c["cyan"]),
        (f"★ {data['stars']} · {data['prs']} PRs", "STARS & PULL REQS", c["ok"]),
    ]
    for i, (val, lab, col) in enumerate(tiles):
        x = 38 + (i % 2) * 234
        y = 96 + (i // 2) * 88
        body += (
            f'{glass_panel(x, y, 220, 76, rx=12, border_col=col, border_op=0.5, fill_op=0.6)}'
            f'<rect x="{x}" y="{y}" width="3.5" height="76" rx="1.7" fill="{col}"/>'
            f'<text x="{x + 16}" y="{y + 36}" font-family="{f["display"]}" font-size="25" font-weight="700" fill="{c["text"]}">{esc(val)}</text>'
            f'<text x="{x + 16}" y="{y + 58}" font-family="{f["mono"]}" font-size="8.8" letter-spacing="1.8" fill="{c["muted"]}">{esc(lab)}</text>'
        )

    x0 = 516
    body += (
        f'{glass_panel(x0, 96, 446, 266, rx=14, border_col=c["yellow"], border_op=0.5, fill_op=0.62)}'
        f'<text x="{x0 + 20}" y="122" font-family="{f["mono"]}" font-size="10.5" font-weight="700" letter-spacing="2.2" fill="{c["yellow"]}">{esc(L["fuel"])}</text>'
        f'<text x="{x0 + 426}" y="122" text-anchor="end" font-family="{f["mono"]}" font-size="9.5" fill="{c["muted"]}">GRADE: {esc(grade)} ({score}/100)</text>'
    )

    cols = [c["yellow"], c["primary"], c["violet"], c["cyan"], c["ok"], "#f472b6"]
    sx = x0 + 20.0
    total_w = 406.0
    for i, (name, pct) in enumerate(data["langs"][:6]):
        seg_w = max(4.0, total_w * (pct / 100.0))
        if sx + seg_w > x0 + 426:
            seg_w = max(0.0, (x0 + 426) - sx)
        body += f'<rect x="{sx:.1f}" y="134" width="{seg_w:.1f}" height="8" rx="2" fill="{cols[i % len(cols)]}"/>'
        sx += seg_w + 1.5

    max_pct = max((pct for _, pct in data["langs"][:6]), default=1.0)
    for i, (name, pct) in enumerate(data["langs"][:6]):
        y = 166 + i * 33
        col = cols[i % len(cols)]
        wbar = 216.0 * (pct / max(1.0, max_pct))
        body += (
            f'<rect x="{x0 + 18}" y="{y - 14}" width="22" height="22" rx="6" fill="#060b18" stroke="{col}" stroke-opacity="0.5"/>'
            f'{render_icon(name, x0 + 29, y - 3, scale=0.58, default_col=col)}'
            f'<text x="{x0 + 48}" y="{y + 1}" font-family="{f["mono"]}" font-size="11" font-weight="600" fill="{c["text"]}">{esc(name)}</text>'
            f'<rect x="{x0 + 160}" y="{y - 9}" width="204" height="10" rx="5" fill="#060b18" stroke="{c["border"]}"/>'
            f'<rect x="{x0 + 161}" y="{y - 8}" width="{wbar * 202 / 216:.1f}" height="8" rx="4" fill="{col}">'
            f'<animate attributeName="width" from="0" to="{wbar * 202 / 216:.1f}" dur="1.1s" begin="{0.2 + i * 0.12:.2f}s" fill="freeze"/></rect>'
            f'<text x="{x0 + 426}" y="{y + 1}" text-anchor="end" font-family="{f["mono"]}" font-size="11" font-weight="700" fill="{col}">{pct:.1f}%</text>'
        )

    body += (
        f'<text x="38" y="386" font-family="{f["mono"]}" font-size="9.5" letter-spacing="2" fill="{c["muted"]}">'
        f'TELEMETRY STATUS: {esc(rank_title)}  ·  NETWORK CREW: {data["followers"]} FOLLOWERS</text>'
    )
    return frame(W, H, body, "Live Telemetry & Language Models", T, "", 28, 13)


# ------------------------------------------------------------------ 6. CONTRIBUTION NEXUS (Placed near bottom right before Calendar)
def render_nexus(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    W, H = 1000, 520
    cx, cy = 500, 292

    c_pct = data.get("commit_pct", 94)
    p_pct = data.get("pr_pct", 5)
    r_pct = data.get("review_pct", 1)
    i_cnt = data.get("issues", 0)
    total_c = data.get("total_contribs", 701)

    col_commits = "#3b82f6"   # Dominant Electric Blue
    col_prs = "#8b5cf6"       # Violet
    col_reviews = "#06b6d4"   # Cyan
    col_issues = "#6366f1"    # Indigo
    col_yellow = c["yellow"]  # Luminous Yellow (#facc15)

    defs = (
        f'<radialGradient id="nexusCoreGlow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{col_commits}" stop-opacity="0.55"/>'
        f'<stop offset="0.45" stop-color="{col_issues}" stop-opacity="0.22"/>'
        f'<stop offset="0.8" stop-color="{col_yellow}" stop-opacity="0.08"/>'
        f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="beamLeft" x1="1" y1="0" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{col_yellow}"/><stop offset="0.25" stop-color="{col_commits}"/><stop offset="1" stop-color="{col_commits}" stop-opacity="0.35"/></linearGradient>'
        f'<linearGradient id="beamBottom" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{col_prs}"/><stop offset="1" stop-color="{col_prs}" stop-opacity="0.3"/></linearGradient>'
        f'<linearGradient id="beamTop" x1="0" y1="1" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{col_reviews}"/><stop offset="1" stop-color="{col_reviews}" stop-opacity="0.25"/></linearGradient>'
        f'<linearGradient id="beamRight" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{col_issues}"/><stop offset="1" stop-color="{col_issues}" stop-opacity="0.22"/></linearGradient>'
    )

    tag = "LIVE NEXUS HUD" if data["real"] else "HOLOGRAPHIC HUD"
    body = head(T, L["nexus_kicker"], L["nexus_title"], tag)
    body += glass_panel(34, 88, 932, 404, rx=16, border_col=col_yellow, border_op=0.45, fill_op=0.50)

    body += (
        f'<g opacity="0.85">'
        f'<circle cx="{cx}" cy="{cy}" r="185" fill="url(#nexusCoreGlow)">'
        f'<animate attributeName="r" values="175;198;175" dur="4.5s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="148" fill="none" stroke="{c["border"]}" stroke-width="1" stroke-dasharray="3 8" opacity="0.6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="112" fill="none" stroke="{col_commits}" stroke-width="1" stroke-dasharray="18 10 4 10" stroke-opacity="0.35">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="36s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="82" fill="none" stroke="{col_yellow}" stroke-width="1.2" stroke-dasharray="8 14" stroke-opacity="0.5">'
        f'<animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="24s" repeatCount="indefinite"/></circle>'
        f'<path d="M {cx - 148} {cy} A 148 148 0 0 1 {cx} {cy - 148}" fill="none" stroke="{col_commits}" stroke-width="1.5" stroke-opacity="0.35" stroke-dasharray="6 6"/>'
        f'<path d="M {cx - 148} {cy} A 148 148 0 0 0 {cx} {cy + 148}" fill="none" stroke="{col_prs}" stroke-width="1.3" stroke-opacity="0.30" stroke-dasharray="5 7"/>'
        f'<path d="M {cx} {cy - 148} A 148 148 0 0 1 {cx + 148} {cy}" fill="none" stroke="{col_reviews}" stroke-width="1" stroke-opacity="0.22" stroke-dasharray="3 9"/>'
        f'<path d="M {cx + 148} {cy} A 148 148 0 0 1 {cx} {cy + 148}" fill="none" stroke="{col_issues}" stroke-width="1" stroke-opacity="0.22" stroke-dasharray="3 9"/>'
        f'</g>'
    )

    # 1) LEFT BEAM: COMMITS (94%)
    path_left = f"M {cx - 56},{cy} L 266,{cy}"
    path_left_curve1 = f"M {cx - 52},{cy - 10} Q 370,{cy - 34} 266,{cy - 6}"
    path_left_curve2 = f"M {cx - 52},{cy + 10} Q 370,{cy + 34} 266,{cy + 6}"
    body += (
        f'<path d="{path_left}" fill="none" stroke="{col_commits}" stroke-width="14" stroke-opacity="0.18" stroke-linecap="round"/>'
        f'<path d="{path_left_curve1}" fill="none" stroke="{col_commits}" stroke-width="1.5" stroke-opacity="0.55" stroke-dasharray="240" stroke-dashoffset="240">'
        f'<animate attributeName="stroke-dashoffset" from="240" to="0" dur="0.9s" begin="0.15s" fill="freeze"/></path>'
        f'<path d="{path_left_curve2}" fill="none" stroke="{col_yellow}" stroke-width="1.2" stroke-opacity="0.45" stroke-dasharray="240" stroke-dashoffset="240">'
        f'<animate attributeName="stroke-dashoffset" from="240" to="0" dur="1.0s" begin="0.25s" fill="freeze"/></path>'
        f'<path d="{path_left}" fill="none" stroke="url(#beamLeft)" stroke-width="5" stroke-linecap="round" stroke-dasharray="220" stroke-dashoffset="220" filter="url(#softGlow)">'
        f'<animate attributeName="stroke-dashoffset" from="220" to="0" dur="0.8s" begin="0.1s" fill="freeze"/></path>'
        f'<circle cx="266" cy="{cy}" r="6" fill="{col_commits}" filter="url(#softGlow)">'
        f'<animate attributeName="r" values="5;8;5" dur="1.8s" repeatCount="indefinite"/></circle>'
        f'<circle cx="266" cy="{cy}" r="2.8" fill="{col_yellow}"/>'
        f'<circle r="4" fill="{col_yellow}" filter="url(#softGlow)">'
        f'<animateMotion dur="1.6s" begin="0.3s" repeatCount="indefinite" path="{path_left}"/></circle>'
        f'<circle r="3.2" fill="#ffffff">'
        f'<animateMotion dur="1.6s" begin="0.85s" repeatCount="indefinite" path="{path_left_curve1}"/></circle>'
        f'<circle r="2.8" fill="{col_commits}">'
        f'<animateMotion dur="1.6s" begin="1.3s" repeatCount="indefinite" path="{path_left_curve2}"/></circle>'
    )

    # 2) BOTTOM BEAM: PULL REQUESTS (5%)
    path_bottom = f"M {cx},{cy + 56} L {cx},414"
    body += (
        f'<path d="{path_bottom}" fill="none" stroke="{col_prs}" stroke-width="7" stroke-opacity="0.12" stroke-linecap="round"/>'
        f'<path d="{path_bottom}" fill="none" stroke="url(#beamBottom)" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="100">'
        f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="0.8s" begin="0.35s" fill="freeze"/></path>'
        f'<circle cx="{cx}" cy="414" r="4.2" fill="{col_prs}"/>'
        f'<circle r="3" fill="{col_prs}" filter="url(#softGlow)">'
        f'<animateMotion dur="2.4s" begin="0.5s" repeatCount="indefinite" path="{path_bottom}"/></circle>'
    )

    # 3) TOP BEAM: CODE REVIEWS (1%)
    path_top = f"M {cx},{cy - 56} L {cx},170"
    body += (
        f'<path d="{path_top}" fill="none" stroke="url(#beamTop)" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="100">'
        f'<animate attributeName="stroke-dashoffset" from="100" to="0" dur="0.8s" begin="0.55s" fill="freeze"/></path>'
        f'<circle cx="{cx}" cy="170" r="3.5" fill="{col_reviews}"/>'
        f'<circle r="2.4" fill="{col_reviews}">'
        f'<animateMotion dur="3.2s" begin="0.7s" repeatCount="indefinite" path="{path_top}"/></circle>'
    )

    # 4) RIGHT BEAM: ISSUES
    path_right = f"M {cx + 56},{cy} L 734,{cy}"
    body += (
        f'<path d="{path_right}" fill="none" stroke="url(#beamRight)" stroke-width="1.5" stroke-dasharray="4 4" stroke-linecap="round" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="0.75" dur="0.8s" begin="0.75s" fill="freeze"/></path>'
        f'<circle cx="734" cy="{cy}" r="3.5" fill="{col_issues}"/>'
        f'<circle r="2.2" fill="{col_issues}">'
        f'<animateMotion dur="3.8s" begin="0.9s" repeatCount="indefinite" path="{path_right}"/></circle>'
    )

    # CENTRAL HOLOGRAPHIC REACTOR CORE
    body += (
        f'<g>'
        f'<circle cx="{cx}" cy="{cy}" r="62" fill="{col_commits}" fill-opacity="0.12">'
        f'<animate attributeName="r" values="58;68;58" dur="3.2s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="54" fill="#070d1f" stroke="{col_commits}" stroke-width="2.2" filter="url(#softGlow)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{col_yellow}" stroke-width="1.4" stroke-dasharray="10 6" stroke-opacity="0.85">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="18s" repeatCount="indefinite"/></circle>'
        f'<text x="{cx}" y="{cy - 14}" text-anchor="middle" font-family="{f["mono"]}" font-size="8.5" font-weight="700" letter-spacing="2" fill="{col_yellow}">NEXUS CORE</text>'
        f'<text x="{cx}" y="{cy + 12}" text-anchor="middle" font-family="{f["display"]}" font-size="26" font-weight="700" fill="{c["text"]}">{total_c:,}</text>'
        f'<text x="{cx}" y="{cy + 28}" text-anchor="middle" font-family="{f["mono"]}" font-size="7.5" letter-spacing="1.5" fill="{c["muted"]}">SIGNALS</text>'
        f'</g>'
    )

    # Floating Glass Cards
    body += (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.35s" fill="freeze"/>'
        f'{glass_panel(56, cy - 44, 198, 88, rx=12, border_col=col_commits, border_op=0.85, fill_op=0.72, top_glow=col_commits)}'
        f'<circle cx="76" cy="{cy - 18}" r="4" fill="{col_yellow}">'
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>'
        f'<text x="88" y="{cy - 14}" font-family="{f["mono"]}" font-size="10" font-weight="700" letter-spacing="2" fill="{c["text"]}">COMMITS</text>'
        f'<text x="238" y="{cy - 14}" text-anchor="end" font-family="{f["mono"]}" font-size="8.5" fill="{col_yellow}">PRIMARY</text>'
        f'<text x="72" y="{cy + 20}" font-family="{f["display"]}" font-size="32" font-weight="700" fill="{col_commits}">{c_pct}%</text>'
        f'<text x="238" y="{cy + 18}" text-anchor="end" font-family="{f["mono"]}" font-size="9.5" fill="{c["muted"]}">{data["commits"]:,} pushed</text>'
        f'<rect x="72" y="{cy + 30}" width="166" height="4" rx="2" fill="#060b18"/>'
        f'<rect x="72" y="{cy + 30}" width="{166 * min(100, c_pct) / 100:.1f}" height="4" rx="2" fill="{col_commits}"/>'
        f'</g>'
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.65s" fill="freeze"/>'
        f'{glass_panel(cx - 105, 102, 210, 58, rx=11, border_col=col_reviews, border_op=0.55, fill_op=0.65, top_glow=col_reviews)}'
        f'<circle cx="{cx - 86}" cy="124" r="3.2" fill="{col_reviews}"/>'
        f'<text x="{cx - 76}" y="128" font-family="{f["mono"]}" font-size="9.5" font-weight="600" letter-spacing="1.8" fill="{c["text"]}">CODE REVIEWS</text>'
        f'<text x="{cx + 88}" y="136" text-anchor="end" font-family="{f["display"]}" font-size="22" font-weight="700" fill="{col_reviews}">{r_pct}%</text>'
        f'<text x="{cx - 86}" y="147" font-family="{f["mono"]}" font-size="8.5" fill="{c["muted"]}">PEER AUDIT CHANNEL</text>'
        f'</g>'
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.5s" fill="freeze"/>'
        f'{glass_panel(cx - 105, 422, 210, 58, rx=11, border_col=col_prs, border_op=0.65, fill_op=0.65, top_glow=col_prs)}'
        f'<circle cx="{cx - 86}" cy="444" r="3.5" fill="{col_prs}"/>'
        f'<text x="{cx - 76}" y="448" font-family="{f["mono"]}" font-size="9.5" font-weight="600" letter-spacing="1.8" fill="{c["text"]}">PULL REQUESTS</text>'
        f'<text x="{cx + 88}" y="456" text-anchor="end" font-family="{f["display"]}" font-size="22" font-weight="700" fill="{col_prs}">{p_pct}%</text>'
        f'<text x="{cx - 86}" y="467" font-family="{f["mono"]}" font-size="8.5" fill="{c["muted"]}">{data["prs"]} MERGED STREAMS</text>'
        f'</g>'
    )

    issue_sub = f"{i_cnt} TRACKED" if i_cnt > 0 else "STANDBY CHANNEL"
    body += (
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="0.85s" fill="freeze"/>'
        f'{glass_panel(746, cy - 38, 196, 76, rx=12, border_col=col_issues, border_op=0.45, fill_op=0.58, top_glow=col_issues)}'
        f'<circle cx="766" cy="{cy - 14}" r="3.2" fill="{col_issues}"/>'
        f'<text x="778" y="{cy - 10}" font-family="{f["mono"]}" font-size="10" font-weight="600" letter-spacing="2" fill="{c["text"]}">ISSUES</text>'
        f'<text x="766" y="{cy + 14}" font-family="{f["display"]}" font-size="16" font-weight="600" fill="{col_issues}">{esc(issue_sub)}</text>'
        f'<text x="766" y="{cy + 30}" font-family="{f["mono"]}" font-size="8" letter-spacing="1.2" fill="{c["muted"]}">SIGNAL RESOLUTION</text>'
        f'</g>'
        f'<text x="52" y="476" font-family="{f["mono"]}" font-size="8.5" letter-spacing="1.5" fill="{c["muted"]}">'
        f'BEAM INTENSITY = PROPORTIONAL SIGNAL WEIGHT</text>'
        f'<text x="948" y="476" text-anchor="end" font-family="{f["mono"]}" font-size="8.5" letter-spacing="1.5" fill="{col_yellow}">'
        f'NEXUS ENGINE v2.6 // ACTIVE</text>'
    )

    return frame(W, H, body, "Contribution Nexus — Holographic Activity Scanner", T, defs, 42, 19)


# ------------------------------------------------------------------ 7. GITHUB CONTRIBUTION CALENDAR IN YELLOW THEME (Replaces Constellation)
def render_contributions(cfg: dict, T: dict, data: dict) -> str:
    """
    Exact GitHub Contribution Calendar layout (from user's reference image) upgraded with:
    - Yellow/Gold heatmap palette (#111827 -> #422006 -> #854d0e -> #eab308 -> #facc15/#fef08a)
    - Header: "<N> contributions in the last year" + compact streak & active-day badges
    - Inner rounded calendar border with Jan..Dec month labels and Mon / Wed / Fri row labels
    - Bottom-left: "Learn how we count contributions" + Bottom-right: "Less [5 yellow squares] More"
    - Subtle golden scanline sweep + animated wave glow along the bottom
    """
    c, f, L = T["palette"], T["fonts"], T["labels"]
    W, H = 1000, 340
    weeks = data.get("weeks", demo_weeks_days(cfg["username"]))[-52:]
    flat_days = [item for wk in weeks for item in wk]
    cur_streak, best_streak, _ = streaks(flat_days)
    total_c = data.get("total_contribs", sum(cnt for _, cnt in flat_days))

    defs = (
        f'<linearGradient id="calScan" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{c["yellow"]}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{c["yellow"]}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{c["yellow"]}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="goldWaveFill" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c["yellow"]}" stop-opacity="0.16"/>'
        f'<stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></linearGradient>'
        '<clipPath id="calClip"><rect x="38" y="82" width="924" height="226" rx="12"/></clipPath>'
    )

    # Top Headline matching GitHub's native header: "701 contributions in the last year"
    body = (
        f'<circle cx="46" cy="48" r="4" fill="{c["yellow"]}">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>'
        f'<text x="60" y="55" font-family="{f["display"]}" font-size="22" font-weight="600" fill="{c["text"]}">'
        f'{total_c:,} contributions in the last year</text>'
        # Compact glassmorphic streak pills on the top right
        f'{glass_panel(640, 34, 152, 28, rx=14, border_col=c["yellow"], border_op=0.55, fill_op=0.65)}'
        f'<text x="716" y="52" text-anchor="middle" font-family="{f["mono"]}" font-size="9.5" font-weight="700" fill="{c["yellow"]}">'
        f'⚡ STREAK: {cur_streak}d</text>'
        f'{glass_panel(804, 34, 158, 28, rx=14, border_col=c["primary"], border_op=0.55, fill_op=0.65)}'
        f'<text x="883" y="52" text-anchor="middle" font-family="{f["mono"]}" font-size="9.5" font-weight="600" fill="{c["text"]}">'
        f'BEST: {best_streak}d ORBIT</text>'
    )

    # Inner Calendar Container Box (Exact match to screenshot's bordered inner container)
    body += glass_panel(38, 82, 924, 226, rx=12, border_col="#334155", border_op=0.75, fill_op=0.68)

    # Subtle Animated Golden Wave + Scanline inside the calendar box
    wave_path = (
        "M -400,292 "
        "C -250,274 -150,310 0,292 "
        "C 150,274 250,310 400,292 "
        "C 550,274 650,310 800,292 "
        "C 950,274 1050,310 1200,292 "
        "C 1350,274 1450,310 1600,292 "
        "L 1600,315 L -400,315 Z"
    )
    body += (
        f'<g clip-path="url(#calClip)">'
        f'<g><path d="{wave_path}" fill="url(#goldWaveFill)" stroke="{c["yellow"]}" stroke-opacity="0.35" stroke-width="1.2"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-400 0" dur="10s" repeatCount="indefinite"/></g>'
        f'<rect x="38" y="82" width="120" height="226" fill="url(#calScan)">'
        f'<animate attributeName="x" values="38;962;38" dur="9s" repeatCount="indefinite"/></rect>'
        f'</g>'
    )

    # Grid geometry
    gx0 = 104.0
    gy0 = 132.0
    pitch = 15.8
    cell_s = 12.0

    # Day-of-week labels on the left: Mon (row 1), Wed (row 3), Fri (row 5)
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for r_idx, d_str in day_labels:
        ly = gy0 + r_idx * pitch + 9.5
        body += f'<text x="60" y="{ly:.1f}" font-family="{f["display"]}" font-size="12" fill="{c["text"]}">{d_str}</text>'

    # Month labels across the top (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
    month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = None
    last_mx = -100.0
    for w_idx, wk in enumerate(weeks):
        if not wk:
            continue
        first_date_str = wk[0][0]
        try:
            m_num = int(first_date_str[5:7])
        except Exception:
            continue
        mx = gx0 + w_idx * pitch
        if m_num != last_month and (mx - last_mx) >= 34.0:
            body += f'<text x="{mx:.1f}" y="118" font-family="{f["display"]}" font-size="12.5" fill="{c["text"]}">{month_names[m_num]}</text>'
            last_month = m_num
            last_mx = mx

    # 5-Level Yellow/Gold Heatmap Cells
    # Level 0: #111827 (empty dark slate)
    # Level 1: #422006 (deep bronze)
    # Level 2: #854d0e (amber gold)
    # Level 3: #eab308 (vibrant yellow)
    # Level 4: #facc15 / #fef08a (luminous peak yellow)
    rng = random.Random(42)
    cells_svg = []
    for w_idx, wk in enumerate(weeks):
        for d_idx, (_, cnt) in enumerate(wk[:7]):
            cx = gx0 + w_idx * pitch
            cy = gy0 + d_idx * pitch
            if cnt <= 0:
                fill_c, stroke_c = "#111827", "#1e293b"
                anim = ""
            elif cnt <= 2:
                fill_c, stroke_c = "#422006", "#713f12"
                anim = ""
            elif cnt <= 5:
                fill_c, stroke_c = "#854d0e", "#a16207"
                anim = ""
            elif cnt <= 8:
                fill_c, stroke_c = "#eab308", "#facc15"
                anim = (
                    f'<animate attributeName="opacity" values="0.8;1;0.8" '
                    f'dur="{rng.uniform(2.5, 4.5):.1f}s" begin="{rng.uniform(0, 2):.1f}s" repeatCount="indefinite"/>'
                ) if rng.random() < 0.25 else ""
            else:
                fill_c, stroke_c = "#facc15", "#fef08a"
                anim = (
                    f'<animate attributeName="opacity" values="0.72;1;0.72" '
                    f'dur="{rng.uniform(1.8, 3.4):.1f}s" begin="{rng.uniform(0, 2):.1f}s" repeatCount="indefinite"/>'
                )
            cells_svg.append(
                f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell_s}" height="{cell_s}" rx="2.8" '
                f'fill="{fill_c}" stroke="{stroke_c}" stroke-width="0.7">{anim}</rect>'
            )

    body += "".join(cells_svg)

    # Bottom row inside calendar container:
    # Left: "Learn how we count contributions"
    # Right: "Less [5 yellow squares] More"
    legend_cols = [
        ("#111827", "#1e293b"),
        ("#422006", "#713f12"),
        ("#854d0e", "#a16207"),
        ("#eab308", "#facc15"),
        ("#facc15", "#fef08a"),
    ]
    lx0 = 816.0
    legend_squares = "".join(
        f'<rect x="{lx0 + k * 16:.1f}" y="271" width="12" height="12" rx="2.8" fill="{fc}" stroke="{sc}" stroke-width="0.7"/>'
        for k, (fc, sc) in enumerate(legend_cols)
    )
    body += (
        f'<text x="104" y="281" font-family="{f["display"]}" font-size="12" fill="{c["muted"]}">'
        f'Learn how we count contributions</text>'
        f'<text x="{lx0 - 8:.1f}" y="281" text-anchor="end" font-family="{f["display"]}" font-size="12" fill="{c["muted"]}">Less</text>'
        f'{legend_squares}'
        f'<text x="{lx0 + len(legend_cols) * 16 + 6:.1f}" y="281" font-family="{f["display"]}" font-size="12" fill="{c["muted"]}">More</text>'
    )

    return frame(W, H, body, "365-Day Contribution Calendar Heatmap", T, defs, 28, 17)


# ------------------------------------------------------------------ 8. FOOTER
def render_footer(cfg: dict, T: dict, data: dict) -> str:
    c, f, L = T["palette"], T["fonts"], T["labels"]
    wave_chars = []
    for col in range(88):
        v = math.sin(col * 0.22) * math.cos(col * 0.07)
        idx = max(0, min(len(PALETTE_ASCII) - 1, int((v * 0.5 + 0.5) * (len(PALETTE_ASCII) - 1))))
        wave_chars.append(PALETTE_ASCII[idx])
    wave_str = "".join(wave_chars)
    body = (
        f'{glass_panel(34, 22, 932, 108, rx=14, border_col=c["yellow"], border_op=0.45, fill_op=0.55)}'
        f'<text x="500" y="46" text-anchor="middle" font-family="{f["mono"]}" font-size="10" font-weight="600" letter-spacing="4" fill="{c["yellow"]}">{esc(L["footer_kicker"])}</text>'
        f'<text x="500" y="66" text-anchor="middle" font-family="{f["mono"]}" font-size="10" fill="{c["primary"]}" opacity="0.85">{esc(wave_str)}</text>'
        f'<text x="500" y="96" text-anchor="middle" font-family="{f["display"]}" font-size="24" font-weight="700" fill="{c["text"]}">{esc(L["footer"])}</text>'
        f'<text x="500" y="116" text-anchor="middle" font-family="{f["mono"]}" font-size="10.5" letter-spacing="2" fill="{c["muted"]}">{esc(L["footer_sub"])}</text>'
    )
    return frame(1000, 152, body, "Footer", T, "", 24, 23)


RENDERERS = {
    "hero": render_hero,
    "exhibits": render_exhibits,
    "instruments": render_instruments,
    "missions": render_missions,
    "telemetry": render_telemetry,
    "nexus": render_nexus,
    "contributions": render_contributions,
    "footer": render_footer,
}


def exhibit_rows(cfg: dict, user: str) -> str:
    rows = [
        "| PROJECT | ARCHITECTURE & IMPACT | STACK | LINKS |",
        "|:--|:--|:--|:--|",
    ]
    for e in cfg["exhibits"]:
        links = []
        if e.get("repo"):
            links.append(f"[`Source ↗`](https://github.com/{user}/{e['repo']})")
        if e.get("live"):
            links.append(f"[`Live Demo ↗`]({e['live']})")
        stack_badges = " ".join(f"`{s}`" for s in e.get("stack", []))
        rows.append(f"| **{e['name']}** | {e['desc']} | {stack_badges} | {' · '.join(links)} |")
    return "\n".join(rows)


def intro_markdown(cfg: dict, data: dict) -> str:
    bullets = "\n".join(f"- ⚡ {b}" for b in cfg.get("intro_bullets", []))
    top_langs = ", ".join(f"**{n}** ({p:.1f}%)" for n, p in data["langs"][:4])
    return (
        f"### `00 // OPERATOR BRIEFING`\n\n"
        f"{bullets}\n"
        f"- 🛰️ **Live Language Telemetry:** {top_langs}"
    )


def socials(cfg: dict) -> str:
    s = cfg.get("socials", {})
    return " &nbsp;·&nbsp; ".join(f"[{k.upper()}]({v})" for k, v in s.items() if v)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate Glassmorphism × Yellow Contribution Calendar & Nexus README.")
    ap.add_argument("--config", default=str(ROOT / "readme.config.json"))
    ap.add_argument("--theme", default=None)
    ap.add_argument("--username", default=None)
    ap.add_argument("--out", default=str(ROOT))
    ap.add_argument("--demo", action="store_true", help="skip network and use deterministic fallback data")
    args = ap.parse_args()

    cfg = load_json(args.config)
    theme_name = args.theme or cfg.get("theme", "observatory")
    T = load_json(ROOT / "themes" / theme_name / "theme.json")
    user = args.username or cfg["username"]
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    data = fetch_data(user, token, args.demo)

    out = Path(args.out)
    (out / "assets").mkdir(parents=True, exist_ok=True)
    for name, fn in RENDERERS.items():
        (out / "assets" / f"{name}.svg").write_text(fn(cfg, T, data), encoding="utf-8")
        print(f"wrote assets/{name}.svg")

    tmpl = (ROOT / "templates" / "README.md.tmpl").read_text(encoding="utf-8")
    readme = (
        tmpl.replace("{{USERNAME}}", user)
        .replace("{{NAME}}", cfg["name"])
        .replace("{{WEBSITE}}", cfg.get("website", "https://robelbiruk.tech"))
        .replace("{{INTERACTIVE_URL}}", cfg.get("interactive_url", "https://robibiruk.github.io/"))
        .replace("{{CTA}}", T["labels"]["cta"])
        .replace("{{BIO}}", cfg.get("bio", ""))
        .replace("{{INTRO_SECTION}}", intro_markdown(cfg, data))
        .replace("{{EXHIBIT_TABLE}}", exhibit_rows(cfg, user))
        .replace("{{SOCIALS}}", socials(cfg))
        .replace("{{TEMPLATE_REPO}}", cfg.get("template_repo", "https://github.com/Robibiruk/observatory-readme"))
    )
    (out / "README.md").write_text(readme, encoding="utf-8")
    print(f"wrote README.md (theme={theme_name}, data={'live' if data['real'] else 'demo'})")


if __name__ == "__main__":
    main()
