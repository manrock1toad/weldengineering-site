# weldengineering.com (static site)

The public site is plain HTML built with [Eleventy](https://www.11ty.dev/). There's no
PHP or database, so nothing on the server can be exploited the way WordPress could.

## Layout

```
src/        page content + templates (Eleventy builds these)
public/     files copied into the site as-is: images, PDFs, catalog, diagrams, CSS/JS
scripts/    site checker used by the GitHub Actions workflow
_site/      the built site (created by the build, not stored in git)
```

## Where things live

| What you want to change | Edit this |
| --- | --- |
| Address, phone, email, tagline, top nav, bottom links, banner message | `src/_data/site.json` |
| Search descriptions (the snippet under each Google result) | `src/_data/descriptions.json` |
| Search titles (the Google headline), when it should differ from the page title | `src/_data/titles.json` |
| Image alt text | `src/_data/alt.json` (wins over the page's own alt) |
| Company facts for Google (Organization data), share image | `org` and `shareImage` in `src/_data/site.json` |
| Header (logo, marquees, earth) | `src/_includes/partials/header.njk` |
| Top nav markup | `src/_includes/partials/nav.njk` |
| Footer / copyright | `src/_includes/partials/footer.njk` |
| `<head>`: CSS, JS, slider setup | `src/_includes/partials/head.njk` |
| CSS/JS file locations | `src/_data/assets.json` |
| A page's content | `src/<page>.html` (everything below the `---` front matter) |
| Product photos, thumbnails | `public/images/` |
| Literature PDFs, catalog flipbook | `public/catalog/` |
| System diagrams | `public/tb708/`, `public/tbmm708/` |
| Site CSS/JS, slider files | `public/assets/` |
| Old `.php` URL redirects | `public/_redirects` (Cloudflare) and `public/.htaccess` (Apache) |
| Security headers, keep test URLs out of Google | `public/_headers` (Cloudflare) |
| What search engines may crawl | `public/robots.txt` (`sitemap.xml` is generated; test builds block all crawlers) |

Each page file starts with front matter:

```yaml
---
layout: "layouts/base.njk"
title: "Standard Duty Submerged Arc Flux Recovery Equipment"   # "" on the home page
nav: "sd"          # top-nav item to highlight (a key from site.json), or null
pageKey: "sd"      # bottom-link item marked as current
bodyClass: "..."   # kept from WordPress so the old CSS still matches
permalink: "sd.html"
---
```

## URLs and SEO

- Pages are served at clean URLs (`/sd`, not `/sd.html`), the way Cloudflare Pages does it.
  Canonical tags, `sitemap.xml`, and links between pages all use that format. The build
  rewrites page links automatically, so `href="sd.html#DC-30"` in a page file is fine.
- Catalog shortcuts (`sdo.html`, `hdo.html`) are rewritten to link straight to the flipbook page.
- Every page needs a search description in `src/_data/descriptions.json`, keyed by its clean
  URL. Keep it to about 150 characters and describe what's actually on the page.
- The build fails if a page is missing its description, or if canonicals and the sitemap
  ever disagree.
- Titles are `<page title> | <titleSuffix>` (`homeTitle` in `site.json` on the home page), the
  same as the WordPress site. `titles.json` can override a page's front matter title.
- `seo.js` fixes the old WordPress markup in the built pages without touching `src/`: alt
  text from `alt.json`, one `<h1>` per page (the existing page heading, same look; on the
  home page it's the tagline), and `lang="en-US"`.
- Every page gets social sharing tags (`og:`); the home page also gets Organization
  structured data built from `org` in `site.json`. Error pages are `noindex` with no canonical.
- The site check (Actions → **Check site**) has an **SEO checks** section: sitemap, robots.txt,
  titles, `<h1>`, descriptions, canonicals, social tags, structured data, and missing alt text.

To show a banner on every page (e.g. "See us at FABTECH Booth #1234!"), set
`"announcement"` in `site.json`. Clear it to hide.

**Add a page:** copy an existing `src/*.html`, change the front matter and content,
add a description to `descriptions.json`, then add it to `bottomLinks` (and `nav` if
needed) in `site.json`. If it's a top-level page, add its name to `PAGES` in
`eleventy.config.js`. If it replaces an old `.php` page, add a line to both
`public/_redirects` and `public/.htaccess`.

## Building (no terminal needed)

Every push to `main` builds a downloadable copy of the site:

1. Edit files right on GitHub (pencil icon) and commit.
2. Open the **Actions** tab, click the newest **Build site** run.
3. Under **Artifacts**, download **weldengineering-site** (a ZIP of the finished site).

On a computer with Node.js you can also run `npm install` once, then `npm start` for a
live preview at http://localhost:8080 or `npm run build` to write `_site/`.

## Hosting on Cloudflare Pages (recommended)

Cloudflare builds and publishes the site on every push. `main` is the live site;
every other branch gets its own test site.

Settings (Workers & Pages → Create application → Pages → Import an existing Git repository):

| Setting | Value |
| --- | --- |
| Framework preset | Eleventy |
| Production branch | `main` |
| Build command | `npx @11ty/eleventy` |
| Build output directory | `_site` |
| Node version | from `.node-version` (22) |

Then in **Settings → Builds → Branch control**, set Preview branch to **Custom branches**:
include `*`, exclude `site-preview` (the site checker force-pushes that branch and it
isn't a buildable site).

### Making changes (branch → test site → merge)

1. Work on the `dev` branch (GitHub branch menu → `dev`, then edit and commit there).
2. Cloudflare builds it at `https://dev.<project>.pages.dev` within a minute or two.
3. Check it. Optional: Actions → **Check site** → Run workflow → pick `dev` for the
   link check and live comparison.
4. Open a pull request from `dev` into `main` and merge it. Cloudflare publishes `main`
   to the live domain.

Test sites are kept out of search engines three ways: Cloudflare's own
`X-Robots-Tag: noindex` on preview deployments, the `*.pages.dev` rule in
`public/_headers`, and the build itself (any Cloudflare build that isn't `main` writes a
`robots.txt` that blocks all crawlers and puts `noindex, nofollow` on every page).

Notes:
- Pages ignores `.htaccess`. Redirects live in `public/_redirects`, headers in `public/_headers`.
- `/404.html` is shown for any missing page.
- Add the custom domain under **Custom domains** once the test site checks out. Do this
  in the same Cloudflare account that holds the weldengineering.com DNS so the record
  is created for you.

## Deploying to an Apache/cPanel server (fallback)

The ZIP is the **whole** site: pages, `.htaccess`, images, PDFs, catalog, and diagrams.
The `.htaccess` gives Apache the same clean URLs and redirects as Cloudflare.

First time only:
1. Back up `public_html` (cPanel → File Manager → Compress, then download it).
2. Move everything in `public_html` to a folder **outside** it. Do `wp-config.php`
   first; it holds the database password.
3. Upload the contents of the ZIP into the empty `public_html` (FileZilla: turn on
   *Server → Force showing hidden files* so `.htaccess` goes too).
4. Spot-check `/`, `/sd.php` (should redirect to `/sd`), a product popup, a
   print button, the calculator, a literature PDF, and the catalog flipbook.

After that, just upload the files that changed.

## History

The pages were saved from the old WordPress site and converted into `src/` with a
one-time migration script. The old WordPress files and migration scripts are not part
of this repository.
