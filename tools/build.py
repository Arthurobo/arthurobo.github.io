"""Stamp the shared <head>, header and footer around each page body.

Input:  pages/<name>.html, each starting with a small header block:
          ---
          out: work/parallel/index.html
          title: Parallel
          description: ...
          section: work          (body class s-<section>; home for the home page)
          nav: work              (which nav item is current; blank for none)
          ---
        followed by the contents of <main>.
Output: the finished page in the site directory. Plain HTML, nothing to build
        for the person who deploys it.
"""
import os, re, sys, html as H

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
ORIGIN = "https://arthurobo.github.io"

NAV = [("work", "amber", "/work/", "Work"),
       ("projects", "coral", "/projects/", "Projects"),
       ("resume", "mint", "/resume/", "Resume"),
       ("hire", "violet", "/hire/", "Hire")]

PALETTES = ["graphite", "midnight", "terminal", "ember", "daylight"]

def chips():
    return ('<span class="palette-chips" aria-hidden="true">'
            + "".join(f'<i data-hue="{h}"></i>' for h in ("amber", "coral", "mint", "cyan", "violet"))
            + "</span>")

def header(current):
    items = []
    for key, hue, href, label in NAV:
        cur = ' aria-current="page"' if key == current else ""
        items.append(f'        <li><a data-hue="{hue}" href="{href}"{cur}>{label}</a></li>')
    return f"""  <header class="site-header">
    <div class="wrap wrap--wide">
      <a class="mark" href="/" aria-label="Arthur Obo-Nwakaji, home"><span class="mark-glyph" aria-hidden="true">a</span></a>
      <nav class="site-nav" aria-label="Main">
        <ul>
{chr(10).join(items)}
        </ul>
      </nav>
    </div>
  </header>"""

def footer():
    opts = "\n".join(
        f'          <button class="palette-option" type="button" data-palette="{p}" aria-pressed="{"true" if i == 0 else "false"}">{chips()} {p.capitalize()}</button>'
        for i, p in enumerate(PALETTES))
    return f"""  <footer class="site-footer">
    <div class="wrap wrap--wide">
      <p>No framework, no build step. The only script is the palette picker. <a href="https://github.com/Arthurobo" target="_blank" rel="noopener">Read the source</a>.</p>
      <details class="palette-picker">
        <summary>{chips()} Palette<span class="visually-hidden">: <span class="palette-current">Graphite</span></span></summary>
        <div class="palette-menu">
{opts}
        </div>
      </details>
    </div>
  </footer>"""

def new_tab(html_text):
    """External links and PDFs open in a new tab; navigation inside the site stays put."""
    def fix(m):
        tag = m.group(0)
        if 'target=' in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener">'
    return re.sub(r'<a\s[^>]*href="(?:https?://[^"]*|[^"]*\.pdf)"[^>]*>', fix, html_text)

def page(meta, body):
    body = new_tab(body)
    title = meta["title"]
    full = "Arthur Obo-Nwakaji" if meta.get("section") == "home" else f"{title} · Arthur Obo-Nwakaji"
    desc = H.escape(meta.get("description", ""), quote=True)
    path = "/" + meta["out"].replace("index.html", "")
    section = meta.get("section", "")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{H.escape(full)}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{ORIGIN}{path}">
  <meta property="og:title" content="{H.escape(full, quote=True)}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{ORIGIN}{path}">
  <meta property="og:site_name" content="Arthur Obo-Nwakaji">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <script>try{{var p=localStorage.getItem("palette");if(p)document.documentElement.classList.add("p-"+p)}}catch(e){{}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=JetBrains+Mono:wght@400..800&display=swap">
  <link rel="stylesheet" href="/assets/palettes.css">
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body class="s-{section}">
  <a class="skip-link" href="#main">Skip to content</a>
{header(meta.get("nav", ""))}
  <main id="main">
{body.rstrip()}
  </main>
{footer()}
  <script src="/assets/palette.js" defer></script>
</body>
</html>
"""

def main():
    built = []
    for name in sorted(os.listdir(PAGES)):
        if not name.endswith(".html"):
            continue
        src = open(os.path.join(PAGES, name), encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)\Z", src, re.S)
        if not m:
            sys.exit(f"{name}: missing header block")
        meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        out = os.path.join(SITE, meta["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(page(meta, m.group(2)))
        built.append(meta["out"])
    print("built:", ", ".join(built))

if __name__ == "__main__":
    main()
