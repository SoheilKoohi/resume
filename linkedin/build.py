"""Render the LinkedIn profile copy to a standalone page.

The copy lives in content.py; this file is only layout. Run:
    python3 linkedin/build.py linkedin/preview.html
"""

import html, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import content as c

E = lambda s: html.escape(str(s), quote=True)


def field(label, limit, text, note=""):
    used = len(text)
    pct = min(100, round(used / limit * 100))
    state = "over" if used > limit else ("tight" if pct > 90 else "ok")
    note_html = f'<p class="field__note">{note}</p>' if note else ""
    return f"""
<section class="field">
  <header class="field__head">
    <h2 class="field__label">{E(label)}</h2>
    <div class="meter" role="img" aria-label="{used} of {limit} characters used">
      <span class="meter__count" data-state="{state}">{used:,} / {limit:,}</span>
      <span class="meter__track"><span class="meter__fill" style="width:{pct}%"></span></span>
    </div>
  </header>
  {note_html}
  <div class="copyblock">
    <button class="copyblock__btn" type="button" data-copy>Copy</button>
    <pre class="copyblock__text">{E(text)}</pre>
  </div>
</section>"""


role_sections = []
for title, meta, intro, bullets in c.ROLES:
    body = intro + "\n\n" + "\n".join("- " + b for b in bullets)
    used = len(body)
    pct = min(100, round(used / 2000 * 100))
    role_sections.append(f"""
  <article class="role">
    <header class="role__head">
      <div>
        <h3 class="role__title">{E(title)}</h3>
        <p class="role__meta">{E(meta)}</p>
      </div>
      <div class="meter">
        <span class="meter__count" data-state="{'tight' if pct > 90 else 'ok'}">{used:,} / 2,000</span>
        <span class="meter__track"><span class="meter__fill" style="width:{pct}%"></span></span>
      </div>
    </header>
    <div class="copyblock">
      <button class="copyblock__btn" type="button" data-copy>Copy</button>
      <pre class="copyblock__text">{E(body)}</pre>
    </div>
  </article>""")

skills_text = "\n".join(c.SKILLS)
chips = "".join(
    f'<li{" class=\"is-top\"" if s in c.TOP3 else ""}>{E(s)}</li>' for s in c.SKILLS
)

checklist = [
    ("Headline", "Paste the headline. It is the single highest-weighted field in recruiter search."),
    ("About", "Paste the About text. Only the first ~300 characters show before &ldquo;see more&rdquo;, so the opening line is doing the work."),
    ("Experience", "Add the two-sentence role intro above the bullets. LinkedIn shows the intro in previews; your CV bullets do not have one."),
    ("Skills", "Add all 50. Pin Machine Learning, MLOps and Technical Leadership as your top three."),
    ("Open to work", "Set job titles to Principal / Staff Machine Learning Engineer and choose <em>Recruiters only</em> if you do not want the public badge."),
    ("Custom URL", "You already have linkedin.com/in/soheilkoohi. Nothing to change."),
    ("Featured", "Link the CV site and the PDF. Nothing else on your profile shows the 3,000 RPS and ~1M events/sec numbers at a glance."),
    ("Recommendations", "Ask the Director of Engineering at Snapp! and one of the engineers you mentored. Two strong ones beat six generic ones."),
]
check_html = "".join(
    f'<li><h3>{E(t)}</h3><p>{d}</p></li>' for t, d in checklist
)

HTML = f"""<title>Koohi LinkedIn Rewrite</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Newsreader:opsz,wght@6..72,300;6..72,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {{
  --paper:#f4f6f8; --surface:#ffffff; --ink:#0f1519; --slate:#5b6672;
  --hair:#dde4e9; --accent:#0b5563; --accent-soft:#e3eef0; --warn:#9a6b1f;
  --display:'Archivo',system-ui,sans-serif;
  --body:'Newsreader',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,monospace;
}}
@media (prefers-color-scheme:dark) {{
  :root:not([data-theme="light"]) {{
    --paper:#0c1013; --surface:#141a1e; --ink:#e9eef2; --slate:#8e99a4;
    --hair:#222b31; --accent:#4fb2c6; --accent-soft:#16262b; --warn:#d9a441;
  }}
}}
:root[data-theme="dark"] {{
  --paper:#0c1013; --surface:#141a1e; --ink:#e9eef2; --slate:#8e99a4;
  --hair:#222b31; --accent:#4fb2c6; --accent-soft:#16262b; --warn:#d9a441;
}}
*,*::before,*::after {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--body); font-size:1.0625rem; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:52rem; margin:0 auto; padding:clamp(1.5rem,5vw,4rem) clamp(1.25rem,4vw,2rem) 5rem;
  display:flex; flex-direction:column; gap:3rem; }}
:focus-visible {{ outline:2px solid var(--accent); outline-offset:3px; border-radius:3px; }}

.masthead {{ display:flex; flex-direction:column; gap:.75rem;
  padding-bottom:1.75rem; border-bottom:2px solid var(--ink); }}
.masthead__eyebrow {{ font-family:var(--mono); font-size:.6875rem; letter-spacing:.16em;
  text-transform:uppercase; color:var(--accent); margin:0; }}
.masthead h1 {{ font-family:var(--display); font-weight:700; font-size:clamp(1.9rem,4.5vw,2.6rem);
  letter-spacing:-.025em; line-height:1.05; margin:0; text-wrap:balance; }}
.masthead p {{ margin:0; color:var(--slate); max-width:60ch; }}

.field, .roles, .skills, .checklist {{ display:flex; flex-direction:column; gap:1rem; }}
.field__head, .role__head {{ display:flex; flex-wrap:wrap; align-items:flex-end;
  justify-content:space-between; gap:.75rem 1.5rem; }}
.field__label {{ font-family:var(--mono); font-size:.75rem; letter-spacing:.14em;
  text-transform:uppercase; color:var(--slate); margin:0; }}
.field__note {{ margin:0; color:var(--slate); font-size:.9375rem; max-width:62ch; }}

.meter {{ display:flex; align-items:center; gap:.6rem; }}
.meter__count {{ font-family:var(--mono); font-size:.6875rem; font-variant-numeric:tabular-nums;
  color:var(--slate); white-space:nowrap; }}
.meter__count[data-state="tight"] {{ color:var(--warn); }}
.meter__count[data-state="over"] {{ color:#b3261e; font-weight:500; }}
.meter__track {{ display:block; width:5rem; height:3px; background:var(--hair); border-radius:2px; overflow:hidden; }}
.meter__fill {{ display:block; height:100%; background:var(--accent); }}

.copyblock {{ position:relative; background:var(--surface); border:1px solid var(--hair);
  border-radius:3px; }}
.copyblock__text {{ margin:0; padding:1.35rem 1.35rem 1.5rem; font-family:var(--body);
  font-size:1rem; line-height:1.62; white-space:pre-wrap; word-wrap:break-word;
  overflow-x:auto; max-width:100%; }}
.copyblock__btn {{ position:absolute; top:.6rem; right:.6rem; z-index:1;
  font-family:var(--mono); font-size:.6875rem; letter-spacing:.06em; text-transform:uppercase;
  padding:.35rem .7rem; color:var(--slate); background:var(--paper);
  border:1px solid var(--hair); border-radius:2px; cursor:pointer;
  transition:color .15s, border-color .15s, background .15s; }}
.copyblock__btn:hover {{ color:var(--accent); border-color:var(--accent); }}
.copyblock__btn[data-done] {{ color:var(--accent); border-color:var(--accent); background:var(--accent-soft); }}

.section-title {{ font-family:var(--display); font-weight:700; font-size:1.4rem;
  letter-spacing:-.02em; margin:0; }}
.section-intro {{ margin:0; color:var(--slate); max-width:62ch; }}

.role {{ display:flex; flex-direction:column; gap:.85rem; padding-top:1.75rem;
  border-top:1px solid var(--hair); }}
.role__title {{ font-family:var(--display); font-weight:600; font-size:1.0625rem; margin:0; }}
.role__meta {{ font-family:var(--mono); font-size:.6875rem; color:var(--slate); margin:.25rem 0 0; }}

.chips {{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:.4rem; }}
.chips li {{ font-family:var(--mono); font-size:.75rem; padding:.3rem .6rem;
  background:var(--accent-soft); color:var(--accent); border-radius:2px; }}
.chips li.is-top {{ background:var(--accent); color:var(--surface); font-weight:500; }}

.checklist ol {{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; }}
.checklist li {{ display:grid; grid-template-columns:9rem minmax(0,1fr); gap:1.5rem;
  padding:1.1rem 0; border-top:1px solid var(--hair); align-items:baseline; }}
.checklist li h3 {{ font-family:var(--display); font-weight:600; font-size:.9375rem; margin:0; }}
.checklist li p {{ margin:0; color:var(--slate); font-size:.9375rem; }}

.foot {{ font-family:var(--mono); font-size:.6875rem; color:var(--slate);
  padding-top:1.5rem; border-top:1px solid var(--hair); }}

@media (max-width:38rem) {{
  .checklist li {{ grid-template-columns:1fr; gap:.35rem; }}
}}
@media (prefers-reduced-motion:reduce) {{ * {{ transition-duration:.01ms !important; }} }}
</style>

<div class="wrap">

  <header class="masthead">
    <p class="masthead__eyebrow">Rewritten from Soheil_Koohi_CV.yaml</p>
    <h1>LinkedIn, rebuilt from the CV</h1>
    <p>Every block below is ready to paste into the matching LinkedIn field. The counter on each
      one is the field&rsquo;s real character limit, so nothing here will be truncated.</p>
  </header>

{field("Headline", c.LIMITS["headline"], c.HEADLINE,
       "The highest-weighted field in recruiter search. Front-loads the title recruiters type, then the stack, then the numbers that make it concrete.")}

{field("About", c.LIMITS["about"], c.ABOUT,
       "Only the first ~300 characters show before &ldquo;see more&rdquo;. The opening line has to earn the click on its own, so it leads with the hardest constraint in your work rather than a job title.")}

  <div class="roles">
    <h2 class="section-title">Experience</h2>
    <p class="section-intro">Your CV bullets already work here, so they are reused unchanged. What is new is the
      two-sentence role intro above each set: LinkedIn surfaces it in previews and search results, and a CV has no
      equivalent field.</p>
{''.join(role_sections)}
  </div>

  <div class="skills">
    <h2 class="section-title">Skills</h2>
    <p class="section-intro">All 50 slots used, in LinkedIn&rsquo;s own naming so the entries match its taxonomy and
      autocomplete. The three filled chips are the ones to pin at the top.</p>
    <ul class="chips">{chips}</ul>
    <div class="copyblock">
      <button class="copyblock__btn" type="button" data-copy>Copy list</button>
      <pre class="copyblock__text">{E(skills_text)}</pre>
    </div>
  </div>

  <div class="checklist">
    <h2 class="section-title">Everything else</h2>
    <p class="section-intro">Fields that are not copy, ordered by how much they move recruiter search.</p>
    <ol>{check_html}</ol>
  </div>

  <p class="foot">Generated from the CV at github.com/SoheilKoohi/resume &middot; character limits current as of Aug 2026</p>
</div>

<script>
document.querySelectorAll('[data-copy]').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var text = btn.parentElement.querySelector('.copyblock__text').textContent;
    var label = btn.textContent;
    navigator.clipboard.writeText(text).then(function () {{
      btn.textContent = 'Copied';
      btn.setAttribute('data-done', '');
      setTimeout(function () {{ btn.textContent = label; btn.removeAttribute('data-done'); }}, 1600);
    }}).catch(function () {{
      btn.textContent = 'Select and copy';
      setTimeout(function () {{ btn.textContent = label; }}, 2200);
    }});
  }});
}});
</script>
"""

pathlib.Path(sys.argv[1]).write_text(HTML, encoding="utf-8")
print("written", sys.argv[1], len(HTML), "bytes")
