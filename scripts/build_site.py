#!/usr/bin/env python3
"""Render the GitHub Pages site from the CV YAML.

The YAML stays the single source of truth: every string on the page is read
from it. Only the layout and the curated metric labels live here.
"""

from __future__ import annotations

import html
import pathlib
import re
import shutil
import sys
from datetime import date

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# The readout strip. These are chosen, not scraped: they answer the questions a
# hiring manager screens on at Principal level, which no single bullet states on
# its own. `evidence` is the phrase in the CV each one rests on — the build warns
# if it stops matching, so the strip cannot quietly outlive the CV behind it.
READOUTS = [
    ("9+", "years in production ML", r"with 9\+? years"),
    ("3,000", "RPS in production serving", r"handling 3,?000 RPS"),
    ("10-12", "engineers led", r"12-person cross-functional team"),
    ("4", "product areas owned", r"Safety, Driver Signup, Support Automation, and ETA"),
]


def fmt_date(value) -> str:
    text = str(value)
    if text.lower() == "present":
        return "Present"
    m = re.fullmatch(r"(\d{4})-(\d{2})", text)
    if m:
        return f"{MONTHS[int(m.group(2)) - 1]} {m.group(1)}"
    return text


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def readouts(cv: dict) -> list[tuple[str, str]]:
    blob = cv["sections"]["summary"][0] + " " + " ".join(
        h for role in cv["sections"]["experience"] for h in role.get("highlights", [])
    )
    cells = []
    for value, label, evidence in READOUTS:
        if not re.search(evidence, blob):
            print(f"warning: readout {value!r} no longer matches the CV "
                  f"(looked for /{evidence}/)", file=sys.stderr)
        cells.append((value, label))
    return cells


def group_by_company(roles: list[dict]) -> list[dict]:
    """Consecutive roles at one employer become a single block, so a promotion
    reads as a promotion rather than as two unrelated jobs."""
    groups: list[dict] = []
    for role in roles:
        if groups and groups[-1]["company"] == role["company"]:
            groups[-1]["roles"].append(role)
        else:
            groups.append({
                "company": role["company"],
                "location": role.get("location", ""),
                "roles": [role],
            })
    return groups


def render(cv: dict) -> str:
    name = cv["name"]
    current = cv["sections"]["experience"][0]
    summary = cv["sections"]["summary"][0]
    groups = group_by_company(cv["sections"]["experience"])

    links = [("Email", f"mailto:{cv['email']}", cv["email"])]
    if cv.get("phone"):
        tel = str(cv["phone"]).replace("tel:", "")
        links.append(("Phone", f"tel:{tel.replace('-', '')}", tel.replace("-", " ")))
    for net in cv.get("social_networks", []):
        if net["network"] == "LinkedIn":
            links.append(("LinkedIn", f"https://linkedin.com/in/{net['username']}",
                          f"in/{net['username']}"))

    # --- left rail -----------------------------------------------------------
    link_rows = "\n".join(
        f'<li><span class="rail__key">{esc(k)}</span>'
        f'<a class="rail__val" href="{esc(href)}">{esc(text)}</a></li>'
        for k, href, text in links
    )

    # --- readout strip -------------------------------------------------------
    chips = "\n".join(
        f'<div class="readout__cell"><span class="readout__num">{esc(v)}</span>'
        f'<span class="readout__label">{esc(label)}</span></div>'
        for v, label in readouts(cv)
    )

    # --- experience ----------------------------------------------------------
    blocks = []
    for group in groups:
        rows = []
        for role in group["roles"]:
            bullets = "\n".join(
                f"<li>{esc(h)}</li>" for h in role.get("highlights", [])
            )
            rows.append(f"""
          <article class="role">
            <header class="role__head">
              <h3 class="role__title">{esc(role['position'])}</h3>
              <p class="role__dates">{esc(fmt_date(role['start_date']))} &ndash; {esc(fmt_date(role['end_date']))}</p>
            </header>
            <ul class="role__list">
{bullets}
            </ul>
          </article>""")
        blocks.append(f"""
        <section class="employer">
          <div class="employer__id">
            <h2 class="employer__name">{esc(group['company'])}</h2>
            <p class="employer__place">{esc(group['location'])}</p>
          </div>
          <div class="employer__roles">{''.join(rows)}
          </div>
        </section>""")
    experience = "\n".join(blocks)

    # --- skills --------------------------------------------------------------
    skill_rows = "\n".join(
        f"""<div class="skill">
              <h3 class="skill__label">{esc(s['label'])}</h3>
              <ul class="skill__items">{''.join(
                  f'<li>{esc(item.strip())}</li>' for item in s['details'].split(','))}</ul>
            </div>"""
        for s in cv["sections"]["skills"]
    )

    # --- education -----------------------------------------------------------
    edu_rows = "\n".join(
        f"""<div class="edu">
              <h3 class="edu__school">{esc(e['institution'])}</h3>
              <p class="edu__degree">{esc(e['degree'])} in {esc(e['area'])}</p>
              <p class="edu__dates">{esc(fmt_date(e['start_date']))} &ndash; {esc(fmt_date(e['end_date']))}</p>
            </div>"""
        for e in cv["sections"]["education"]
    )

    updated = date.today().strftime("%B %Y")
    pdf = "Soheil_Koohi_CV.pdf"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(name)} &mdash; {esc(current['position'])}</title>
<meta name="description" content="{esc(summary[:180])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --paper:#f5f7f9; --surface:#ffffff; --ink:#0f1519; --slate:#5b6672;
  --hair:#dfe5ea; --accent:#0b5563; --accent-soft:#e4eef0;
  --display:'Archivo',system-ui,sans-serif;
  --body:'Newsreader',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
  --rail:19rem; --gutter:clamp(1.25rem,4vw,3.5rem);
}}
@media (prefers-color-scheme:dark) {{
  :root {{
    --paper:#0c1013; --surface:#141a1e; --ink:#e9eef2; --slate:#8e99a4;
    --hair:#222b31; --accent:#4fb2c6; --accent-soft:#16262b;
  }}
}}
*,*::before,*::after {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
body {{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--body); font-size:1.0625rem; line-height:1.62;
  -webkit-font-smoothing:antialiased;
}}
a {{ color:inherit; }}
:focus-visible {{ outline:2px solid var(--accent); outline-offset:3px; border-radius:2px; }}

.shell {{ display:grid; grid-template-columns:var(--rail) minmax(0,1fr); gap:var(--gutter);
  max-width:76rem; margin:0 auto; padding:var(--gutter); }}

/* ---------- left rail ---------- */
.rail {{ position:sticky; top:var(--gutter); align-self:start; }}
.rail__portrait {{ width:6.5rem; height:6.5rem; border-radius:50%; display:block;
  object-fit:cover; filter:grayscale(1) contrast(1.04);
  box-shadow:0 0 0 1px var(--hair), 0 0 0 6px var(--paper), 0 0 0 7px var(--hair); }}
.rail__name {{ font-family:var(--display); font-weight:700; font-size:1.75rem;
  letter-spacing:-.022em; line-height:1.1; margin:1.5rem 0 .35rem; }}
.rail__role {{ margin:0; color:var(--accent); font-family:var(--display);
  font-weight:600; font-size:.8125rem; letter-spacing:.04em; text-transform:uppercase; }}
.rail__place {{ margin:.5rem 0 0; color:var(--slate); font-size:.9375rem; }}
.rail__links {{ list-style:none; margin:1.75rem 0 0; padding:1.25rem 0 0;
  border-top:1px solid var(--hair); display:grid; gap:.55rem; }}
.rail__links li {{ display:grid; grid-template-columns:4.5rem 1fr; align-items:baseline; }}
.rail__key {{ font-family:var(--mono); font-size:.6875rem; letter-spacing:.06em;
  text-transform:uppercase; color:var(--slate); }}
.rail__val {{ font-size:.9375rem; text-decoration:none; border-bottom:1px solid var(--hair);
  padding-bottom:1px; word-break:break-word; transition:border-color .18s,color .18s; }}
.rail__val:hover {{ color:var(--accent); border-color:var(--accent); }}
.rail__cta {{ display:inline-flex; align-items:center; gap:.5rem; margin-top:1.75rem;
  padding:.7rem 1.15rem; background:var(--ink); color:var(--paper);
  font-family:var(--display); font-weight:600; font-size:.8125rem; letter-spacing:.03em;
  text-decoration:none; border-radius:2px; transition:background .18s,transform .18s; }}
.rail__cta:hover {{ background:var(--accent); transform:translateY(-1px); }}
.rail__nav {{ margin-top:1.75rem; padding-top:1.25rem; border-top:1px solid var(--hair);
  display:grid; gap:.4rem; }}
.rail__nav a {{ font-family:var(--mono); font-size:.75rem; letter-spacing:.04em;
  color:var(--slate); text-decoration:none; transition:color .18s; }}
.rail__nav a:hover {{ color:var(--accent); }}

/* ---------- main ---------- */
.lede {{ font-size:clamp(1.25rem,2.1vw,1.5rem); line-height:1.5; font-weight:300;
  letter-spacing:-.011em; margin:0 0 2.75rem; max-width:52ch; }}

.readout {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(8.5rem,1fr));
  border-top:1px solid var(--hair); border-bottom:1px solid var(--hair); }}
.readout__cell {{ padding:1.1rem 1.1rem 1.1rem 0; border-right:1px solid var(--hair); }}
.readout__cell:last-child {{ border-right:0; }}
.readout__cell + .readout__cell {{ padding-left:1.1rem; }}
.readout__num {{ display:block; font-family:var(--mono); font-weight:500;
  font-size:1.5rem; letter-spacing:-.03em; color:var(--accent); }}
.readout__label {{ display:block; margin-top:.3rem; font-family:var(--display);
  font-size:.6875rem; letter-spacing:.05em; text-transform:uppercase; color:var(--slate); }}

.section {{ margin-top:4rem; }}
.section__title {{ font-family:var(--mono); font-size:.75rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--slate); margin:0 0 1.75rem;
  padding-bottom:.75rem; border-bottom:1px solid var(--hair); }}

.employer {{ display:grid; grid-template-columns:11rem minmax(0,1fr); gap:2rem;
  padding:2rem 0; border-bottom:1px solid var(--hair); }}
.employer:first-child {{ padding-top:.5rem; }}
.employer:last-child {{ border-bottom:0; padding-bottom:0; }}
.employer__id {{ position:sticky; top:var(--gutter); align-self:start; }}
.employer__name {{ font-family:var(--display); font-weight:700; font-size:1.125rem;
  letter-spacing:-.015em; margin:0; }}
.employer__place {{ margin:.3rem 0 0; font-family:var(--mono); font-size:.6875rem;
  letter-spacing:.04em; color:var(--slate); }}
.role + .role {{ margin-top:2rem; padding-top:2rem; border-top:1px dashed var(--hair); }}
.role__head {{ display:flex; flex-wrap:wrap; align-items:baseline; justify-content:space-between;
  gap:.5rem 1.5rem; }}
.role__title {{ font-family:var(--display); font-weight:600; font-size:1.0625rem;
  letter-spacing:-.008em; margin:0; }}
.role__dates {{ margin:0; font-family:var(--mono); font-size:.75rem; color:var(--slate);
  white-space:nowrap; }}
.role__list {{ margin:1rem 0 0; padding:0; list-style:none; display:grid; gap:.85rem; }}
.role__list li {{ position:relative; padding-left:1.35rem; max-width:68ch; }}
.role__list li::before {{ content:""; position:absolute; left:0; top:.72em; width:.5rem;
  height:1px; background:var(--accent); }}

.skills {{ display:grid; gap:1.5rem; }}
.skill {{ display:grid; grid-template-columns:11rem minmax(0,1fr); gap:2rem; align-items:baseline; }}
.skill__label {{ font-family:var(--display); font-weight:600; font-size:.875rem; margin:0; }}
.skill__items {{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:.4rem; }}
.skill__items li {{ font-family:var(--mono); font-size:.75rem; letter-spacing:.01em;
  padding:.28rem .55rem; background:var(--accent-soft); color:var(--accent); border-radius:2px; }}

.edu {{ display:grid; grid-template-columns:11rem minmax(0,1fr) auto; gap:2rem; align-items:baseline; }}
.edu__school {{ font-family:var(--display); font-weight:600; font-size:1.0625rem; margin:0; }}
.edu__degree {{ margin:0; }}
.edu__dates {{ margin:0; font-family:var(--mono); font-size:.75rem; color:var(--slate); }}

.colophon {{ margin-top:4rem; padding-top:1.5rem; border-top:1px solid var(--hair);
  font-family:var(--mono); font-size:.6875rem; letter-spacing:.03em; color:var(--slate); }}
.colophon a {{ color:var(--accent); }}

/* ---------- motion ---------- */
.reveal {{ opacity:0; transform:translateY(14px); transition:opacity .6s ease, transform .6s ease; }}
.reveal.is-in {{ opacity:1; transform:none; }}
@media (prefers-reduced-motion:reduce) {{
  html {{ scroll-behavior:auto; }}
  .reveal {{ opacity:1; transform:none; transition:none; }}
  * {{ transition-duration:.01ms !important; }}
}}

/* ---------- responsive ---------- */
@media (max-width:60rem) {{
  .shell {{ grid-template-columns:1fr; }}
  .rail {{ position:static; }}
  .rail__nav {{ display:none; }}
  .employer,.skill,.edu {{ grid-template-columns:1fr; gap:1rem; }}
  .employer__id {{ position:static; }}
  .readout__cell {{ padding-left:0 !important; border-right:0; border-bottom:1px solid var(--hair); }}
  .readout__cell:last-child {{ border-bottom:0; }}
}}
@media print {{
  .rail__cta,.rail__nav,.readout {{ display:none; }}
  body {{ background:#fff; }}
}}
</style>
</head>
<body>
<div class="shell">

  <aside class="rail">
    <img class="rail__portrait" src="profile.jpg" width="720" height="720"
         alt="Portrait of {esc(name)}">
    <h1 class="rail__name">{esc(name)}</h1>
    <p class="rail__role">{esc(current['position'])}</p>
    <p class="rail__place">{esc(cv['location'])}</p>
    <ul class="rail__links">
{link_rows}
    </ul>
    <a class="rail__cta" href="{pdf}" download>Download CV (PDF)</a>
    <nav class="rail__nav" aria-label="Sections">
      <a href="#experience">Experience</a>
      <a href="#skills">Skills</a>
      <a href="#education">Education</a>
    </nav>
  </aside>

  <main>
    <p class="lede reveal">{esc(summary)}</p>

    <div class="readout reveal">
{chips}
    </div>

    <section class="section" id="experience">
      <h2 class="section__title">Experience</h2>
{experience}
    </section>

    <section class="section" id="skills">
      <h2 class="section__title">Skills</h2>
      <div class="skills">
{skill_rows}
      </div>
    </section>

    <section class="section" id="education">
      <h2 class="section__title">Education</h2>
{edu_rows}
    </section>

    <p class="colophon">
      Updated {updated} &middot; generated from a single YAML file with
      <a href="https://rendercv.com">RenderCV</a> &middot;
      <a href="https://github.com/SoheilKoohi/resume">source</a>
    </p>
  </main>

</div>
<script>
  const items = document.querySelectorAll('.section, .reveal');
  items.forEach(el => el.classList.add('reveal'));
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
    const io = new IntersectionObserver((entries) => {{
      entries.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('is-in'); io.unobserve(e.target); }} }});
    }}, {{ rootMargin: '0px 0px -8% 0px' }});
    items.forEach(el => io.observe(el));
  }} else {{
    items.forEach(el => el.classList.add('is-in'));
  }}
</script>
</body>
</html>
"""


def main() -> int:
    cv_file = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "Soheil_Koohi_CV.yaml")
    cv = yaml.safe_load(cv_file.read_text(encoding="utf-8"))["cv"]

    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "index.html").write_text(render(cv), encoding="utf-8")

    portrait = ROOT / "images" / "profile-square.jpg"
    if not portrait.exists():
        print(f"error: {portrait} is missing", file=sys.stderr)
        return 1
    shutil.copy(portrait, SITE / "profile.jpg")
    print(f">> wrote {SITE / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
