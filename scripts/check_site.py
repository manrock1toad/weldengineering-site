#!/usr/bin/env python3
"""Check the built site (_site/) and compare it with the live WordPress site.

Run by .github/workflows/check.yml after every build. Writes SITE_CHECK.md:
  1. Broken links: every href/src/url() in the built pages (popup JavaScript
     included) must point at a real file in _site/. Matching is
     case-sensitive, like the real server. Clean page URLs (/sd) count as
     their .html file (sd.html), the way Cloudflare Pages serves them.
  2. Missing anchors: links like /tb#HAMX-26 must land on a name/id.
  3. SEO checks: sitemap.xml is valid and every URL in it is a real page whose
     canonical matches; robots.txt points at the sitemap and doesn't block the
     site; each page has one title, one <h1>, a description, a canonical,
     social tags, lang, no noindex, and alt text on every image.
  4. Deployed site: real requests to the site Cloudflare is serving
     (DEPLOYED_URL, default https://we-site.pages.dev). Sitemap pages return
     200, robots.txt and noindex are right for a test or production site, every
     _redirects rule returns its code and target, unknown URLs return a real
     404, and PDFs are served as PDFs.
  5. Live vs. built: for each page, the visible text, links, and images on
     www.weldengineering.com are compared with the built copy.
Only the Python standard library is used. Exit code is always 0; read the report.
"""
import difflib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
LIVE = "https://www.weldengineering.com"
DEPLOYED = os.environ.get("DEPLOYED_URL", "https://we-site.pages.dev").rstrip("/")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
PAGES = ["index", "new", "sd", "hd", "pf", "ham", "ro", "tb", "calc", "mission", "map"]
SLUGS = "new|sd|hd|tb|pf|ham|ro|calc|mission|map"
CATALOG = {"sdo": "catalog/Prod_Sel_Pgs_w_Index/#p=30", "hdo": "catalog/Prod_Sel_Pgs_w_Index/#p=57"}
SKIP = re.compile(r"^(https?:|//|mailto:|tel:|javascript:|data:|#|$)", re.I)

ATTR_RE = re.compile(r"""\b(?:href|src|background)\s*=\s*(["'])(.*?)\1""", re.I | re.S)
ESC_ATTR_RE = re.compile(r"""\b(?:href|src)=\\(["'])(.*?)\\\1""", re.I)  # inside JS strings
CSS_URL_RE = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""", re.I)


def links_in(text):
    found = [m.group(2) for m in ATTR_RE.finditer(text)]
    found += [m.group(2).replace("\\/", "/") for m in ESC_ATTR_RE.finditer(text)]
    found += [m.group(2) for m in CSS_URL_RE.finditer(text)]
    return [html.unescape(u.strip()) for u in found]


def resolve(base_file, url):
    """Return (path in _site, fragment) or None for external/skip."""
    if SKIP.match(url):
        return None
    path, _, frag = url.partition("#")
    path = urllib.parse.unquote(path.split("?")[0])
    if not path:
        return None
    if path.startswith("/"):
        target = SITE / path.lstrip("/")
    else:
        target = base_file.parent / path
    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    elif not target.suffix and not target.exists():
        # Clean page URL: /sd is served from sd.html
        target = target.with_name(target.name + ".html")
    return target, frag


def exists_exact(p):
    """Case-sensitive existence check, even on case-insensitive disks."""
    try:
        rel = p.resolve().relative_to(SITE.resolve())
    except ValueError:
        return p.exists()
    cur = SITE.resolve()
    for part in rel.parts:
        if not cur.is_dir() or part not in {c.name for c in cur.iterdir()}:
            return False
        cur = cur / part
    return True


def anchors_in(text):
    return set(re.findall(r"""\b(?:name|id)\s*=\s*["']([^"']+)["']""", text, re.I))


def check_links():
    broken, bad_anchor, checked = {}, {}, 0
    files = sorted(SITE.glob("*.html"))
    css = sorted(SITE.glob("assets/**/*.css")) + sorted(SITE.glob("includes/**/*.css"))
    cache = {}
    for f in files + css:
        text = f.read_text(encoding="utf-8", errors="replace")
        if 'http-equiv="refresh"' in text:  # sdo.html / hdo.html forwarding stubs
            continue
        for url in links_in(text):
            r = resolve(f, url)
            if r is None:
                continue
            target, frag = r
            checked += 1
            if not exists_exact(target):
                broken.setdefault(url, set()).add(f.name)
                continue
            # catalog/...#p=30 is a flipbook page number handled by its JavaScript, not an anchor
            if frag and target.suffix == ".html" and not frag.startswith("p="):
                if target not in cache:
                    cache[target] = anchors_in(target.read_text(encoding="utf-8", errors="replace"))
                if frag not in cache[target] and 'http-equiv="refresh"' not in target.read_text(errors="replace"):
                    bad_anchor.setdefault(url, set()).add(f.name)
    return checked, broken, bad_anchor


SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
NOINDEX_RE = re.compile(r"""<meta\s+name=["']robots["']\s+content=["'][^"']*noindex""", re.I)
IMG_RE = re.compile(r"""<img\b[^>]*>""", re.I)
JS_IMG_RE = re.compile(r"""<img\b[^>]*?src=\\["'][^>]*>""", re.I)  # <img src=\"...\"> inside JS strings
LDJSON_RE = re.compile(r"""<script type="application/ld\+json">(.*?)</script>""", re.S)


def page_file_for(path):
    """Built file for a clean URL path: / -> index.html, /sd -> sd.html."""
    path = path.split("#")[0].strip("/")
    if not path:
        return SITE / "index.html"
    f = SITE / path
    if f.is_dir():
        return f / "index.html"
    return f if f.suffix else SITE / (path + ".html")


def images_without_alt(text):
    missing = []
    for m in IMG_RE.finditer(text):
        tag = m.group(0)
        if "src=\\" in tag:  # JS string; checked below
            continue
        if not re.search(r"\salt\s*=", tag, re.I):
            src = re.search(r"""\ssrc\s*=\s*["']([^"']+)""", tag, re.I)
            missing.append(src.group(1) if src else tag[:60])
    for m in JS_IMG_RE.finditer(text):
        if "alt=" not in m.group(0):
            src = re.search(r"""src=\\["']([^"'\\]+)""", m.group(0))
            missing.append((src.group(1) if src else m.group(0)[:60]) + " (in JavaScript)")
    return sorted(set(missing))


def seo_checks():
    """Return (table rows, problems) for the SEO section of the report."""
    problems, rows, seen_titles = [], [], {}
    locs = []
    sm = SITE / "sitemap.xml"
    if not sm.exists():
        problems.append("`sitemap.xml` is missing.")
    else:
        try:
            locs = [(e.text or "").strip() for e in ET.parse(sm).getroot().iter(SM_NS + "loc")]
        except ET.ParseError as e:
            problems.append(f"`sitemap.xml` is not valid XML: {e}")
    if len(set(locs)) != len(locs):
        problems.append("`sitemap.xml` lists a URL more than once.")
    for loc in locs:
        if not loc.startswith(LIVE + "/"):
            problems.append(f"Sitemap URL `{loc}` is not on {LIVE}.")
            continue
        f = page_file_for(loc[len(LIVE):])
        if not f.exists():
            problems.append(f"Sitemap URL `{loc}` has no built page.")
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        canon = re.findall(r'<link rel="canonical" href="([^"]+)"', t)
        if canon != [loc]:
            problems.append(f"Sitemap URL `{loc}`: the page's canonical is {canon or 'missing'}.")
        if NOINDEX_RE.search(t) or 'http-equiv="refresh"' in t or f.name == "404.html":
            problems.append(f"Sitemap URL `{loc}` is a noindex, redirect, or error page.")

    robots = SITE / "robots.txt"
    if not robots.exists():
        problems.append("`robots.txt` is missing.")
    else:
        rt = robots.read_text(encoding="utf-8", errors="replace")
        if f"Sitemap: {LIVE}/sitemap.xml" not in rt:
            problems.append(f"`robots.txt` doesn't declare `Sitemap: {LIVE}/sitemap.xml`.")
        if re.search(r"(?im)^\s*Disallow:\s*/\s*$", rt):
            problems.append("`robots.txt` blocks the whole site (`Disallow: /`).")

    for f in sorted(SITE.glob("*.html")):
        t = f.read_text(encoding="utf-8", errors="replace")
        if "<html" not in t.lower() or 'http-equiv="refresh"' in t:
            continue  # verification file, forwarding stubs
        name, is404 = f.name, f.name == "404.html"
        issues = []
        titles = re.findall(r"(?is)<title>(.*?)</title>", t)
        title = html.unescape(re.sub(r"\s+", " ", titles[0])).strip() if titles else ""
        if len(titles) != 1:
            issues.append(f"{len(titles)} <title> tags")
        if len(title) > 70:
            issues.append(f"title is {len(title)} characters (Google shows about 60)")
        if title and title in seen_titles:
            issues.append(f"same title as {seen_titles[title]}")
        seen_titles.setdefault(title, name)
        h1 = len(re.findall(r"(?i)<h1\b", t))
        if h1 != 1:
            issues.append(f"{h1} <h1> headings (want 1)")
        if not re.search(r"(?i)<html[^>]*\blang\s*=", t):
            issues.append("no lang on <html>")
        desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t)
        canon = len(re.findall(r'<link rel="canonical"', t))
        social = all(f'property="og:{k}"' in t for k in ("title", "description", "url", "image"))
        noindex = bool(NOINDEX_RE.search(t))
        if is404:
            if not noindex:
                issues.append("error page should be noindex")
        else:
            if not desc:
                issues.append("no meta description")
            elif len(html.unescape(desc.group(1))) > 160:
                issues.append(f"description is {len(html.unescape(desc.group(1)))} characters (keep under ~160)")
            if canon != 1:
                issues.append(f"{canon} canonical tags")
            if not social:
                issues.append("missing og: social tags")
            if noindex:
                issues.append("marked noindex (would drop out of Google)")
        for block in LDJSON_RE.findall(t):
            try:
                json.loads(block)
            except ValueError as e:
                issues.append(f"structured data is not valid JSON: {e}")
        no_alt = images_without_alt(t)
        if no_alt:
            issues.append(f"{len(no_alt)} images without alt: " + ", ".join(f"`{u}`" for u in no_alt[:10])
                          + (" ..." if len(no_alt) > 10 else ""))
        rows.append(f"| {name} | {len(title)} | {h1} | {'yes' if desc else 'no'} | {canon} | "
                    f"{'yes' if social else 'no'} | {len(LDJSON_RE.findall(t))} | {len(no_alt)} |")
        problems += [f"{name}: {i}" for i in issues]
    return rows, problems


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # report redirects instead of following them
        return None


NO_REDIRECT = urllib.request.build_opener(_NoRedirect)


def http_get(url):
    """One request, redirects not followed: (status, headers, body bytes)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with NO_REDIRECT.open(req, timeout=30) as r:
            return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()
    except Exception as e:  # noqa: BLE001
        return f"no answer ({type(e).__name__})", {}, b""


def location_of(headers):
    """Redirect target as path#fragment, whatever host Cloudflare puts in front."""
    loc = urllib.parse.urlparse(headers.get("Location") or "")
    return loc.path + ("#" + loc.fragment if loc.fragment else "")


def smoke_checks():
    """Request the deployed site; return (report lines, problems)."""
    production = (urllib.parse.urlparse(DEPLOYED).hostname or "").endswith("weldengineering.com")
    lines, problems = [], []

    def ok(msg):
        lines.append(f"- OK: {msg}")

    def bad(msg):
        lines.append(f"- **Problem:** {msg}")
        problems.append(msg)

    status, _, body = http_get(DEPLOYED + "/sitemap.xml")
    locs = []
    if status != 200:
        bad(f"`/sitemap.xml` returned {status}.")
    else:
        try:
            locs = [(e.text or "").strip() for e in ET.fromstring(body).iter(SM_NS + "loc")]
            ok(f"`/sitemap.xml` returns 200 and is valid XML ({len(locs)} URLs).")
        except ET.ParseError as e:
            bad(f"`/sitemap.xml` is not valid XML: {e}")
    not_200 = []
    for loc in locs:
        path = urllib.parse.urlparse(loc).path or "/"
        status, _, _ = http_get(DEPLOYED + path)
        if status != 200:
            not_200.append(f"`{path}` ({status})")
    if not_200:
        bad("Sitemap pages that don't return 200: " + ", ".join(not_200))
    elif locs:
        ok(f"All {len(locs)} sitemap pages return 200.")

    status, _, body = http_get(DEPLOYED + "/robots.txt")
    blocks_all = bool(re.search(r"(?im)^\s*Disallow:\s*/\s*$", body.decode("utf-8", "replace")))
    if status != 200:
        bad(f"`/robots.txt` returned {status}.")
    elif production and blocks_all:
        bad("`robots.txt` blocks all crawlers on the production site.")
    elif production:
        ok("`robots.txt` allows crawling.")
    elif blocks_all:
        ok("`robots.txt` blocks all crawlers (right for a test site).")
    else:
        bad("`robots.txt` on the test site doesn't block crawlers.")

    status, headers, body = http_get(DEPLOYED + "/")
    noindex = ("noindex" in (headers.get("X-Robots-Tag") or "").lower()
               or bool(NOINDEX_RE.search(body.decode("utf-8", "replace"))))
    if status != 200:
        bad(f"The home page returned {status}.")
    elif production and noindex:
        bad("The production home page is marked noindex.")
    elif production:
        ok("The home page returns 200 and can be indexed.")
    elif noindex:
        ok("The home page returns 200 and is marked noindex (right for a test site).")
    else:
        bad("The test site's home page isn't marked noindex.")

    rules = []
    redirects = SITE / "_redirects"
    if redirects.exists():
        for ln in redirects.read_text(encoding="utf-8").splitlines():
            parts = ln.split()
            if len(parts) >= 2 and not parts[0].startswith("#"):
                rules.append((parts[0], parts[1], int(parts[2]) if len(parts) > 2 else 302))
    wrong = []
    for src, dest, code in rules:
        status, headers, _ = http_get(DEPLOYED + src)
        got = location_of(headers)
        if status != code or got != dest:
            wrong.append(f"`{src}` gave {status} to `{got or 'nowhere'}` (want {code} to `{dest}`)")
            continue
        status, _, _ = http_get(DEPLOYED + dest.split("#")[0])
        if status != 200:
            wrong.append(f"`{src}` goes to `{dest}`, which returns {status}")
    if not rules:
        bad("No `_redirects` file in the build.")
    elif wrong:
        bad(f"{len(wrong)} of {len(rules)} old addresses don't redirect correctly: " + "; ".join(wrong))
    else:
        ok(f"All {len(rules)} old addresses in `_redirects` return their redirect code and land on a page that returns 200.")

    for path in ("/no-such-page-" + os.environ.get("GITHUB_SHA", "check")[:7], "/wp-login.php"):
        status, _, _ = http_get(DEPLOYED + path)
        if status == 404:
            ok(f"`{path}` returns a real 404.")
        else:
            bad(f"`{path}` returned {status} instead of 404.")

    status, headers, _ = http_get(DEPLOYED + "/catalog/PT-100-LIT.pdf")
    ctype = headers.get("Content-Type") or ""
    if status == 200 and "application/pdf" in ctype:
        ok("Literature PDFs are served as PDFs (`/catalog/PT-100-LIT.pdf`).")
    else:
        bad(f"`/catalog/PT-100-LIT.pdf` returned {status} with type `{ctype or 'none'}`.")
    return lines, problems


def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001
        return f"__FETCH_FAILED__ {type(e).__name__}: {e}"


def normalize_live(text):
    """Make live WordPress URLs comparable with the built site's clean URLs."""
    text = re.sub(r"https?:(\\?/)\1(?:www\.)?weldengineering\.com", "", text, flags=re.I)
    text = re.sub(r"(?<![\w./\\-])(\\?/)?index\.php\b", lambda m: m.group(1) or "/", text)
    text = re.sub(r"(?<![\w./\\-])(\\?/)?(sdo|hdo)\.php(?!\w)",
                  lambda m: (m.group(1) or "") + CATALOG[m.group(2)], text)
    text = re.sub(r"(?<![\w./\\-])(\\?/)?(" + SLUGS + r")\.php(?!\w)",
                  lambda m: (m.group(1) or "") + m.group(2), text)
    return text


def body_of(text):
    """The part between the nav bar and the footer: what the page is about."""
    m = re.search(r'class="navbar".*?</table>', text, re.S)
    start = m.end() if m else 0
    e = re.search(r'<table[^>]*class="bottom"', text[start:])
    return text[start:start + e.start()] if e else text[start:]


def visible_lines(fragment):
    t = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1>", " ", fragment)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</(p|li|td|tr|div|h\d|table)>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("\xa0", " ")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in t.splitlines()]
    return [ln for ln in lines if ln and ln not in ("|",)]


def norm_link(u):
    u = html.unescape(u).replace("\\/", "/")
    u = re.sub(r"^/", "", u)
    if "includes/image.php" in u:
        return "(generated thumbnail)"
    return u


def compare(page):
    built_path = SITE / f"{page}.html"
    if not built_path.exists():
        return f"### {page}\n- **Built page missing.**\n"
    built = built_path.read_text(encoding="utf-8", errors="replace")
    live_url = LIVE + ("/" if page == "index" else f"/{page}.php")
    live = fetch(live_url)
    if live.startswith("__FETCH_FAILED__"):
        return f"### {page}\n- Could not fetch {live_url}: {live[17:]}\n"
    live = normalize_live(live)
    bt, lt = visible_lines(body_of(built)), visible_lines(body_of(live))
    ratio = difflib.SequenceMatcher(None, lt, bt).ratio()
    only_live = [ln for ln in lt if ln not in set(bt)]
    only_built = [ln for ln in bt if ln not in set(lt)]
    bl = {norm_link(u) for u in links_in(body_of(built))}
    ll = {norm_link(u) for u in links_in(body_of(live))}
    gen = {u for u in bl if u.startswith("images/generated/")}
    bl -= gen
    out = [f"### {page}  ({ratio:.0%} text match)", f"Live: {live_url}"]
    if only_live:
        out.append("- Text only on the **live** page:")
        out += [f"  - `{ln[:160]}`" for ln in only_live[:15]]
        if len(only_live) > 15:
            out.append(f"  - ...and {len(only_live) - 15} more")
    if only_built:
        out.append("- Text only on the **built** page:")
        out += [f"  - `{ln[:160]}`" for ln in only_built[:15]]
        if len(only_built) > 15:
            out.append(f"  - ...and {len(only_built) - 15} more")
    missing = sorted(u for u in ll - bl if u != "(generated thumbnail)")
    extra = sorted(bl - ll)
    if missing:
        out.append("- Links/images on live but **not** in built: " + ", ".join(f"`{u}`" for u in missing[:25]))
    if extra:
        out.append("- Links/images in built but not on live: " + ", ".join(f"`{u}`" for u in extra[:25]))
    if not (only_live or only_built or missing or extra):
        out.append("- Identical text, links, and images.")
    return "\n".join(out) + "\n"


def main():
    if not (SITE / "index.html").exists():
        print(f"No built site at {SITE}/ (run the build first).")
        return 1
    checked, broken, bad_anchor = check_links()
    rep = ["# Site check", "",
           f"Built by `.github/workflows/check.yml` from the latest `{os.environ.get('GITHUB_REF_NAME', 'main')}`. "
           "Live = the WordPress site at www.weldengineering.com.", "",
           f"## 1. Broken links in the built site ({len(broken)} of {checked} checked)"]
    if broken:
        rep += [f"- `{u}` (on {', '.join(sorted(p))})" for u, p in sorted(broken.items())]
    else:
        rep.append("- None.")
    rep += ["", f"## 2. Links to a missing #anchor ({len(bad_anchor)})"]
    rep += [f"- `{u}` (on {', '.join(sorted(p))})" for u, p in sorted(bad_anchor.items())] or ["- None."]
    seo_rows, seo_problems = seo_checks()
    rep += ["", f"## 3. SEO checks ({len(seo_problems)} problems)",
            "| Page | Title chars | H1 | Description | Canonical | Social tags | Structured data | Images missing alt |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"] + seo_rows + [""]
    rep += [f"- {p}" for p in seo_problems] or ["- None."]
    smoke_lines, smoke_problems = smoke_checks()
    rep += ["", f"## 4. Deployed site: {DEPLOYED} ({len(smoke_problems)} problems)",
            "Real requests to whatever Cloudflare is serving during this run. If Cloudflare's deploy "
            "hadn't finished yet, these results are for the previous version.", ""] + smoke_lines
    rep += ["", "## 5. Live vs. built, page by page",
            "Expected differences: the email shows as plain text instead of Cloudflare's "
            "\"[email protected]\", thumbnails point at `images/generated/` instead of `image.php`, "
            "and page links use clean URLs (`sd`) where live uses `sd.php`.", ""]
    for page in PAGES:
        rep.append(compare(page))
    Path("SITE_CHECK.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
