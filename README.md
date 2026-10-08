# arthurobo

The personal site of Arthur Obo-Nwakaji: DevOps / platform engineer, senior
backend engineer, with RAG in production and coding-agent tooling on the side.

Plain HTML and CSS, no framework and no build step. The only script is the
palette picker in the footer (`assets/palette.js`, about 40 lines).

## Pages

| Path | What |
|---|---|
| `/` | Home: who, selected work, what's next, projects, the stack |
| `/work/` | Jobs, side projects, and a table of capabilities with where each was proven |
| `/work/parallel/` | Case study: the AWS platform, CI/CD and services at Parallel |
| `/projects/` | AgentFlow, Saidic, Pennywise, Saidiz and the smaller repos |
| `/projects/agentflow/`, `/projects/saidic/`, `/projects/pennywise/` | Case studies |
| `/resume/` | The web resume (printable) and the three tailored PDFs |
| `/hire/` | What's on offer: platform, backend, RAG, or a full-time role |

## Preview locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

Links are root-relative (`/work/`, `/assets/site.css`), so the site must be
served from the root of a domain: `yourname.dev`, `yourname.github.io`, a
Cloudflare Pages or Netlify site. It will not work from a sub-path such as
`github.io/repo/` without changing the links.

## Deploy

Live at <https://arthurobo.github.io/>, served by GitHub Pages straight from
the `main` branch of the `arthurobo.github.io` repo. Every push to `main`
redeploys in about a minute. `.nojekyll` tells Pages to serve the files as
they are.

To publish a change:

```sh
git add -A && git commit -m "What changed" && git push
```

**Custom domain later:** add a `CNAME` file containing the domain, point the
domain's DNS at GitHub Pages, and change `ORIGIN` in `tools/build.py` before
running the generator so the canonical and og:url tags follow.

## Changing things

- **Colours:** `assets/palettes.css`. One block per palette; every colour on
  the site is a token from there. Keep the contrast contract in the comment at
  the top. The default is Graphite; `:root` carries its values.
- **Fonts:** the Google Fonts `<link>` in each page's `<head>` and the
  `--font` / `--font-code` variables at the top of `assets/site.css`.
- **Section hues:** `.s-work`, `.s-projects`, `.s-resume`, `.s-hire` near the
  top of `assets/site.css`, and the `data-hue` attributes in the nav.
- **Header and footer:** repeated in every page on purpose, so the host needs
  no build step. To change them in one place, edit `tools/build.py` (the
  `<head>`, header and footer live there) and the page bodies in
  `tools/pages/`, then run `python3 tools/build.py` to regenerate every page.
  Editing the generated `.html` files directly also works; just do not run the
  generator afterwards without porting the edit into `tools/pages/`.
- **Resume PDFs:** drop new files over `resume/Arthurobo_*.pdf`; the buttons on
  `/resume/` point at those names.

## Design

The layout and visual system follow the pattern of austn.net (one accent hue
per section, tape labels, tilted squares, dashed rules, a pressed shadow under
anything you can push), reimplemented here with its own palettes and type:
Space Grotesk for text, JetBrains Mono for labels and code.
