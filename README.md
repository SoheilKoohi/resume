# Resume

Single source of truth: **`Soheil_Koohi_CV.yaml`**.

Everything else (PDF, HTML, PNG, Markdown) is generated from it by
[RenderCV](https://rendercv.com) and is **not** committed — edit the YAML, push,
and the GitHub Action rebuilds it.

## Edit

Change `Soheil_Koohi_CV.yaml`. The theme is set at the bottom:

```yaml
design:
  theme: engineeringresumes
```

Other built-in themes: `classic`, `ember`, `engineeringclassic`, `harvard`,
`ink`, `moderncv`, `opal`, `sb2nov`.

## Build locally

One-time setup (installs a pinned RenderCV with [uv](https://docs.astral.sh/uv/)):

```bash
make install
```

Then:

```bash
make build   # render + assemble site/
make open    # build, then open the PDF (macOS)
make watch   # re-render on every save
make clean   # delete rendercv_output/ and site/
```

Output lands in `rendercv_output/`:

| File | What |
| --- | --- |
| `Soheil_Koohi_CV.pdf` | the resume |
| `Soheil_Koohi_CV.html` | HTML version (paste-friendly) |
| `Soheil_Koohi_CV.md` | Markdown version |
| `Soheil_Koohi_CV_*.png` | one image per page |
| `Soheil_Koohi_CV.typ` | intermediate Typst source |

`scripts/build.sh` also assembles `site/`, the exact folder that gets published
to GitHub Pages.

No `uv`? `pipx install "rendercv[full]==2.8"` works too — `scripts/build.sh`
uses whatever `rendercv` it finds on `PATH`.

## CI

`.github/workflows/render.yml` runs on every push to `main`:

1. Renders the YAML.
2. Uploads `rendercv_output/` as a workflow artifact named **resume**
   (Actions run page → Artifacts).
3. Publishes `site/` to GitHub Pages.

Pull requests build and upload the artifact but do not deploy.

### One-time repo setup

GitHub Pages must be switched on once: **Settings → Pages → Build and
deployment → Source: GitHub Actions**. After that the resume is live at
`https://soheilkoohi.github.io/resume/`, with the PDF at
`https://soheilkoohi.github.io/resume/Soheil_Koohi_CV.pdf`.
