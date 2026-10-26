// Eleventy config for the static weldengineering.com
// Docs: https://www.11ty.dev/docs/config/
import { writeFile } from "node:fs/promises";
import { join } from "node:path";
import { seoMarkup } from "./seo.js";

// Pages that are served at clean URLs (/sd instead of /sd.html)
const PAGES = "index|new|sd|hd|tb|pf|ham|ro|calc|mission|map";
const CATALOG = {
  sdo: "/catalog/Prod_Sel_Pgs_w_Index/#p=30",
  hdo: "/catalog/Prod_Sel_Pgs_w_Index/#p=57",
};
// href="sd.html#X", href="/sd.html", href=\"sd.html\" (inside popup JS), old absolute URLs
const PAGE_LINK = new RegExp(
  "(href\\s*=\\s*\\\\?[\"'])(?:https?://(?:www\\.)?weldengineering\\.com)?(?:\\./|/)?" +
    "(" + PAGES + "|sdo|hdo)\\.html(#[^\"'\\\\\\s]*)?(?=\\\\?[\"'])",
  "g"
);

export function cleanUrl(value) {
  return String(value || "/")
    .replace(/(^|\/)index\.html$/, "$1")
    .replace(/\.html$/, "") || "/";
}

export function cleanPageLinks(html) {
  return html.replace(PAGE_LINK, (m, pre, slug, frag = "") => {
    if (CATALOG[slug]) return pre + CATALOG[slug];
    return pre + (slug === "index" ? "/" : "/" + slug) + frag;
  });
}

export function missingDescription(html, outputPath) {
  const out = String(outputPath || "");
  if (!out.endsWith(".html") || /(^|[\/\\])404\.html$/.test(out)) return false;
  if (/http-equiv=["']refresh["']/i.test(html)) return false; // sdo/hdo forwarding stubs
  return !/<meta\s+name=["']description["']\s+content=["'][^"']{50,}["']/i.test(html);
}

// Only the live site may be indexed. On Cloudflare Pages, any branch other than
// main is a test site: robots are blocked and every page says noindex.
// Builds outside Cloudflare (GitHub Actions ZIP, your computer) count as live.
export function isIndexable(env = process.env) {
  if (!env.CF_PAGES) return true;
  return (env.CF_PAGES_BRANCH || "") === (env.PRODUCTION_BRANCH || "main");
}

export const TEST_ROBOTS_TXT = "# Test site: not for search engines\nUser-agent: *\nDisallow: /\n";

export default function (eleventyConfig) {
  const indexable = isIndexable();
  eleventyConfig.addGlobalData("indexable", indexable);
  // Everything in public/ is copied into the site as-is: product images, PDFs,
  // the catalog flipbook, diagrams, CSS/JS, favicon, robots.txt, .htaccess
  eleventyConfig.addPassthroughCopy({ public: "/" });

  // {{ year }} for the copyright line
  eleventyConfig.addGlobalData("year", () => new Date().getFullYear());

  // Match Cloudflare Pages' public HTML URLs without changing output filenames.
  // Canonicals, the XML sitemap, and internal links all use this format.
  eleventyConfig.addFilter("cleanUrl", cleanUrl);

  // The saved WordPress pages still carry Cloudflare's email-decoder script tag.
  // Emails are plain mailto: links now, so drop it from the built pages.
  eleventyConfig.addTransform("drop-cloudflare-email-decoder", function (content) {
    const out = (this.page && this.page.outputPath) || "";
    if (!String(out).endsWith(".html")) return content;
    return content.replace(/<script[^>]*cloudflare-static\/email-decode\.min\.js[^>]*><\/script>/g, "");
  });

  // Point links between pages at the clean URLs (/sd, /hd#MV-5) so visitors and
  // Google never hit a redirect. Catalog shortcuts go straight to the flipbook page.
  eleventyConfig.addTransform("clean-page-links", function (content) {
    const out = (this.page && this.page.outputPath) || "";
    if (!String(out).endsWith(".html")) return content;
    return cleanPageLinks(content);
  });

  // Alt text from src/_data/alt.json, one <h1> per page, lang="en-US" (see seo.js)
  eleventyConfig.addTransform("seo-markup", function (content) {
    return seoMarkup(content, this.page && this.page.outputPath);
  });

  // Fail the build if a page is missing its search description
  // (add one in src/_data/descriptions.json, keyed by the page's clean URL).
  eleventyConfig.addTransform("require-meta-description", function (content) {
    const out = (this.page && this.page.outputPath) || "";
    if (missingDescription(content, out)) {
      throw new Error(`Missing meta description for ${this.page.url}. Add it to src/_data/descriptions.json.`);
    }
    return content;
  });

  // Test sites get a robots.txt that blocks everything (replaces public/robots.txt).
  eleventyConfig.on("eleventy.after", async ({ directories, dir }) => {
    if (indexable) return;
    const out = (directories && directories.output) || (dir && dir.output) || "_site";
    await writeFile(join(out, "robots.txt"), TEST_ROBOTS_TXT);
    console.log(`[robots] Test build (branch ${process.env.CF_PAGES_BRANCH}): robots.txt blocks all crawlers`);
  });

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    // Page bodies are the old WordPress HTML (inline JavaScript and all), so
    // .html pages are NOT run through a template engine. Layouts are Nunjucks.
    htmlTemplateEngine: false,
    markdownTemplateEngine: "njk",
  };
}
