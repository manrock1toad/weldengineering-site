// Build-time SEO fixes for the converted WordPress pages.
// The page files in src/ stay as close to the old site's markup as possible (so
// they're easy to compare with it). These run on the built HTML instead:
//   - alt text from src/_data/alt.json
//   - one <h1> per page (the existing page heading, same look)
//   - lang="en-US" on <html>
import { readFileSync } from "node:fs";

export const ALT = JSON.parse(readFileSync(new URL("./src/_data/alt.json", import.meta.url), "utf8"));

const escAttr = (s) =>
  String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// "/images/x.png", "./images/x.png" and "images/x.png" are the same image
export const altKey = (src) => String(src).replace(/^(\.\/|\/)+/, "").split(/[?#]/)[0];

// Set alt text for every <img> listed in alt.json (alt.json wins over the page).
// An empty string marks a decorative image (alt="").
// Images inside JavaScript strings (product popups) already have alt text and are left alone.
export function applyAltText(html, map = ALT) {
  return html.replace(/<img\b[^>]*>/gi, (tag) => {
    const m = tag.match(/\ssrc\s*=\s*(["'])(.*?)\1/i);
    if (!m) return tag;
    const key = altKey(m[2]);
    if (!Object.prototype.hasOwnProperty.call(map, key)) return tag;
    const alt = ` alt="${escAttr(map[key])}"`;
    const existing = /\salt\s*=\s*(["'])[\s\S]*?\1/i;
    return existing.test(tag) ? tag.replace(existing, alt) : tag.replace(/^<img\b/i, "<img" + alt);
  });
}

// The old pages use <font face="Arial Black" size="4"><strong>Title</strong></font>
// as the visible page heading. Wrap it in <h1 class="pagetitle"> (styled to look
// exactly the same). On the home page the company tagline under the logo is the heading.
const PAGE_HEADING = /<font face="Arial Black" size="4">\s*<strong>[\s\S]*?<\/strong>\s*<\/font>/i;
const TAGLINE = /<span class="text11ptblackbolditalic">[\s\S]*?<\/span>/i;

export function fixHeadings(html, isHome) {
  if (/<h1\b/i.test(html)) return html;
  if (isHome) return html.replace(TAGLINE, (m) => `<h1 class="pagetitle">${m}</h1>`);
  return html.replace(PAGE_HEADING, (m) => `<h1 class="pagetitle">${m}</h1>`);
}

export function addLang(html) {
  return html.replace(/<html(?![^>]*\blang\s*=)([^>]*)>/i, '<html lang="en-US"$1>');
}

export function seoMarkup(html, outputPath) {
  const out = String(outputPath || "");
  if (!out.endsWith(".html")) return html;
  if (/http-equiv=["']refresh["']/i.test(html)) return html; // forwarding stubs
  const isHome = /(^|[\/\\])index\.html$/.test(out) && !/[\/\\]catalog[\/\\]/.test(out);
  return addLang(fixHeadings(applyAltText(html), isHome));
}
