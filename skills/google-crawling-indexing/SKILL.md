---
name: google-crawling-indexing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Practical guide to Google crawling and indexing: sitemaps, robots.txt, meta tags, canonical URLs, redirects, JavaScript, removals, and crawler management."
tags: [google-search, crawling, indexing, robots-txt, sitemaps]
trigger: When the user asks about Google crawling and indexing, sitemaps, robots.txt, meta tags, canonical URLs, redirects, JavaScript SEO, mobile indexing, or removing content from Google.
---

# Google Crawling and Indexing

## Description

This skill covers the *Crawling and indexing* section of Google Search Central. It explains how Google discovers, crawls, renders, and indexes web content, and it gives you practical controls you can use to guide each stage of that process. The guidance here is built directly on the official English Google Search Central documentation, so the focus is on actions that work: building and submitting sitemaps, writing a correct `robots.txt` file, using `meta` robots tags and canonical links, implementing server-side redirects, optimizing JavaScript sites, managing crawl budget, and removing content safely.

> The supporting English summaries for this skill are in [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md), and a structured index of every page is in [`references/google-search-central-toc.md`](references/google-search-central-toc.md).

## Usage

### When to invoke

- The user asks how Google crawls, renders, and indexes pages.
- The user needs to create, validate, or submit a sitemap.
- The user wants to configure `robots.txt` or `meta` robots tags.
- The user has duplicate content and needs canonical URLs.
- The user is migrating a site or renaming URLs and needs redirects.
- The user needs SEO guidance for a JavaScript site, single-page app, or lazy-loaded content.
- The user wants to remove or block content from Google.
- The user needs to request a recrawl, manage crawl budget, or fix crawl errors.

### Input

- A specific topic or problem from the crawling and indexing section.
- Optional: a site URL, a `robots.txt` file, a sitemap, or page markup to review.

### Output

- A structured answer with direct links to the relevant Google Search Central pages.
- Step-by-step actions and concrete examples.
- Common pitfalls to avoid and how to verify the fix.

---

## Core concepts

### 1. Crawling and indexing overview

Google Search has three overlapping stages: crawling, indexing, and serving search results. Understanding the difference between them is the foundation of every technical SEO decision.

**Crawling** is the automated discovery process. Googlebot, which uses a smartphone user agent for mobile-first indexing, starts from a list of known URLs and follows links and sitemaps to find new pages. It also handles rendering: Googlebot fetches the HTML, then runs JavaScript with an evergreen version of Chromium so that client-side content can be analyzed. Crawling is governed primarily by `robots.txt`, by the availability and crawlability of links, and by the site's crawl budget.

**Indexing** is the analysis and storage stage. After a page is crawled and rendered, Google processes the content, evaluates quality and relevance, and may add it to the index. A page that is crawled is not necessarily indexed, and a page that is indexed is not necessarily shown for any given query. To prevent a page from being indexed, use a `noindex` rule or password protection; `robots.txt` alone does not prevent indexing.

**Serving** is the result-selection stage. When a user searches, Google retrieves relevant pages from the index and ranks them. Ranking is influenced by relevance, authority, structured data, page experience, and many other signals, but those are outside the scope of this skill. What matters here is that only publicly accessible, properly canonicalized, and technically sound pages can compete.

Key principles to keep in mind:

1. Google only indexes public, accessible pages. If a page requires authentication, Googlebot generally cannot see it.
2. `robots.txt` controls which URLs Googlebot may crawl, but it does not prevent a URL from appearing in search results if other sites link to it.
3. `noindex` prevents a page from being shown in search results, but for it to work, the page must be crawlable so that Google can see the directive.
4. Duplicate or near-duplicate content should be canonicalized so that signals such as links are consolidated on the preferred URL.
5. Google uses the mobile version of a page's content for indexing, so desktop and mobile users should see the same core content and metadata.

For a high-level explanation of the whole system, see [How Google Search works](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en). For the crawling and indexing landing page, see [Overview of crawling and indexing topics](https://developers.google.com/search/docs/crawling-indexing?hl=en).

### 2. Sitemaps

A sitemap is a file that tells Google which pages, videos, images, and other files on your site are important, and it can provide metadata such as the last modification date, change frequency, and alternate language versions. Sitemaps are not a requirement for being indexed, but they are especially valuable when:

- Your site is large, making it hard to ensure every page has internal links.
- Your site is new and has few external links.
- You publish rich media, news, or localized content and want to give Google extra metadata.
- You have isolated or deep pages that are not well linked from the rest of the site.

Google supports three sitemap formats, and none is universally preferred; choose the one that fits your publishing workflow:

- **XML sitemaps** are the most versatile. They support extensions for images, video, news, and localized URLs. Most content management systems and plugins generate them automatically. The trade-off is that they can be more complex to maintain on very large or frequently changing sites.
- **RSS, mRSS, and Atom 1.0** feeds are convenient because many CMSes create them automatically. They are useful for frequently updated content and can include video metadata, but they cannot include image or news sitemap data.
- **Plain text sitemaps** are the simplest format: one URL per line. They are easy to maintain but limited to indexable textual content and provide no metadata.

A single sitemap file must be no larger than 50 MB uncompressed and must contain no more than 50,000 URLs. If you exceed either limit, split the file into multiple sitemaps and use a sitemap index file to list them. The sitemap file must be UTF-8 encoded and should use fully qualified, absolute URLs. A sitemap placed at the site root, such as `https://www.example.com/sitemap.xml`, can affect all files on the host, while a sitemap in a subdirectory can only affect descendants of that directory unless it is explicitly submitted through Search Console.

A minimal XML sitemap looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/foo.html</loc>
    <lastmod>2022-06-04</lastmod>
  </url>
  <url>
    <loc>https://www.example.com/bar.html</loc>
    <lastmod>2022-06-04</lastmod>
  </url>
</urlset>
```

Sitemap extensions let you give Google additional metadata beyond the page URL. An [image sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps?hl=en) can list images that might not otherwise be discovered, such as those loaded by JavaScript. A [video sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps?hl=en) can specify the title, description, running time, and age-appropriateness of videos. A [News sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap?hl=en) is for articles approved for Google News and should contain only news articles published in the last two days. You can also list [localized versions of a page](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=en) using `xhtml:link rel="alternate"` entries inside each URL. If you have many sitemaps, create a [sitemap index file](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps?hl=en) that lists each individual sitemap and submit only the index.

Sitemap best practices include:

1. Include only canonical URLs that you want to see in search results.
2. Use image, video, or news extensions when you have that content.
3. Submit the sitemap through the [Sitemaps report in Search Console](https://search.google.com/search-console?hl=en), or reference it in `robots.txt` with a `Sitemap:` directive.
4. Keep sitemaps up to date; remove URLs that no longer exist and use accurate `<lastmod>` values.

Common mistakes with sitemaps include submitting non-canonical URLs, including pages that are blocked by `robots.txt` or marked `noindex`, and allowing the file to grow beyond the size limits. See the official guidance on [Learn about sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=en) and [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=en).

### 3. robots.txt

A `robots.txt` file tells search engine crawlers which URLs they can access. Its primary purpose is to avoid overloading your site with crawler requests; it is **not** a security mechanism and it **does not** keep a page out of Google Search results.

The file must be placed in the top-level directory of the site, on a supported protocol. For Google Search, the supported protocols are HTTP, HTTPS, and FTP. A `robots.txt` file on `https://www.example.com/robots.txt` controls crawling for `https://www.example.com/` only; it does not apply to subdomains, other protocols, or other port numbers. Each rule group begins with a `User-agent` line, followed by `Disallow` and `Allow` lines. The most specific matching rule applies, and groups are processed from top to bottom.

A typical `robots.txt` file looks like this:

```
User-agent: *
Disallow: /includes/

User-agent: Googlebot
Allow: /includes/

Sitemap: https://www.example.com/sitemap.xml
```

In this example, all crawlers are blocked from the `/includes/` directory, but Googlebot is allowed because the more specific group overrides the general one. The `Sitemap:` directive points Google to the sitemap file.

Important limitations to remember:

- `robots.txt` only controls crawling. If a page is blocked but other sites link to it, Google may still index the URL and show a title-only result.
- Malicious crawlers or scrapers may ignore `robots.txt`.
- Different crawlers may interpret the syntax differently, so target the specific user agent when needed.
- Do not block CSS, JavaScript, image, or font files that Googlebot needs to render the page. Blocking critical resources can prevent Google from understanding the page.

To keep sensitive or private content out of Google, use a password, `noindex`, or remove the content entirely. See the [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=en) and [How Google interprets the robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec?hl=en) for the complete syntax.

### 4. Meta tags and attributes

`meta` tags and HTML attributes give you page-level control over how Google indexes and displays content. They live in the `<head>` section of the HTML document, and for automated systems to interpret them correctly, the HTML in the `<head>` must be valid and the relevant parent tags must be closed appropriately.

The most important tags for crawling and indexing are:

- `<meta name="description" content="A useful summary of the page.">` may be used as the snippet in search results; it is not a ranking factor but can influence click-through rate.
- `<meta name="robots" content="noindex">` tells Google not to index the page. Other values include `nofollow`, `noarchive`, `nosnippet`, `max-snippet`, `max-image-preview`, `max-video-preview`, `notranslate`, and `nopagereadaloud`. You can combine them: `<meta name="robots" content="noindex, nofollow">`.
- `<meta name="googlebot" content="...">` is a Google-specific equivalent of the `robots` directive.
- `<meta name="google-site-verification" content="...">` is used to verify ownership in Search Console.
- `<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">` declares the encoding.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` is essential for mobile-friendly pages.

You can also set directives in an HTTP header using the `X-Robots-Tag`. This is useful for non-HTML files such as PDFs or images. For example:

```
X-Robots-Tag: noindex
```

The `data-nosnippet` HTML attribute lets you mark specific parts of a page that should not appear in a search snippet. Apply it to `span`, `div`, or `section` elements:

```html
<p>This text can appear in a snippet.</p>
<p data-nosnippet>This text must not appear in a snippet.</p>
```

`rel` attributes on links are also important:

- `rel="canonical"` marks the preferred version of duplicate or similar pages.
- `rel="nofollow"` tells Google not to pass quality signals through the link.
- `rel="sponsored"` identifies advertising or paid links.
- `rel="ugc"` identifies user-generated content links, such as comments or forum posts.

Common mistakes include injecting or changing `meta` robots tags with JavaScript, which can be unreliable; using `noindex` and then blocking the page with `robots.txt`, which prevents Google from ever seeing the `noindex`; and using `noindex` but allowing the page to be publicly linked, which is safe but wasteful. See the official pages on [meta tags and attributes](https://developers.google.com/search/docs/crawling-indexing/special-tags?hl=en), the [robots meta tag and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=en), and [qualifying outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links?hl=en).

### 5. Canonicalization

Canonicalization is the process of selecting the preferred URL for a set of duplicate or very similar pages. When Google finds the same content accessible through multiple URLs, it tries to consolidate signals such as links onto one canonical URL. If your preferred URL is not clear, Google chooses one, and it may not be the one you want.

Google supports several canonicalization signals, listed from strongest to weakest:

1. **Redirects** are the strongest signal. A permanent `301` redirect tells Google that the target URL should become canonical.
2. **`rel="canonical"` link annotations**, either as a `<link>` element in the HTML `<head>` or as an HTTP header, are a strong signal that the specified URL should be canonical.
3. **Sitemap inclusion** is a weak signal. Including only the canonical URLs in your sitemap helps those URLs be seen as canonical.
4. **Other signals**, such as preferring HTTPS over HTTP, can also influence the choice.

These methods can be combined, which usually makes the preferred canonical more likely to be respected. However, avoid sending conflicting signals: do not canonicalize page A to page B while also redirecting page A to page C, and do not canonicalize to a URL that is itself blocked, noindexed, or inaccessible.

To implement a canonical link, add this inside the `<head>` of every duplicate or parameterized version of the page:

```html
<link rel="canonical" href="https://www.example.com/dresses/green/green-dress.html" />
```

You can also serve it as an HTTP header:

```
Link: <https://www.example.com/dresses/green/green-dress.html>; rel="canonical"
```

Canonicalization is especially important for e-commerce filters, session IDs, tracking parameters such as `?gclid=...`, and pages that are available with and without a trailing slash. When the URL has permanently changed, use a `301` redirect instead of, or in addition to, the canonical annotation. See [What is URL canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization?hl=en), [How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=en), and [Fix canonicalization issues](https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting?hl=en).

### 6. Redirects

A redirect resolves one URL to another, telling both visitors and Google that the page has a new location. Redirects are commonly used when you move a site to a new domain, merge websites, remove a page and send traffic elsewhere, or consolidate multiple home page URLs into one canonical version.

The type of redirect you choose matters:

- **301 (permanent redirect)** is the best choice when a page has moved permanently. It passes the canonical signal to the target and, over time, the target URL is shown in search results.
- **302 and 307 (temporary redirects)** should be used when the move is temporary. They tell Google to keep the original URL in the index while serving the redirect to users.
- **Meta refresh** and **JavaScript `location` redirects** are less reliable than server-side redirects. Google may take longer to process them, and they can create a poor user experience. Use server-side redirects whenever possible.
- **Crypto redirects**, such as displaying a message that a page has moved without a real redirect, are not recommended as a primary solution because they do not pass the same signals.

To migrate a domain or redesign a URL structure, follow these steps:

1. Map every old URL to the most relevant new URL. Avoid blanket redirects to the home page; send users and crawlers to the closest equivalent content.
2. Implement `301` redirects on the server, ideally in the server configuration or `.htaccess` rather than in application code.
3. Update internal links, canonical tags, and sitemaps to point to the new URLs.
4. Submit an updated sitemap in Search Console.
5. Monitor the Page Indexing report and Crawl stats for redirect errors or unexpected drops.

Keep redirect chains short. A chain of two or three redirects is acceptable, but long chains slow crawling and can cause Google to stop following. Also avoid redirect loops, where page A redirects to B and B redirects back to A. See [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects?hl=en) for implementation details.

### 7. JavaScript SEO

Google Search runs JavaScript with an evergreen version of Chromium, so JavaScript-powered sites can be crawled and indexed. However, making a JavaScript site easy for Google to process requires attention to a few specific details.

Best practices for JavaScript sites:

1. **Use unique titles and meta descriptions** for each page. If the title and description are generated by JavaScript, ensure they are present in the rendered HTML.
2. **Define the canonical URL correctly** in the HTML. If you inject `<link rel="canonical">` with JavaScript, test thoroughly, because it can be missed or applied too late.
3. **Use the History API instead of hash fragments** for client-side navigation. Hash-based URLs such as `/#!/products` are harder for Google to treat as separate pages.
4. **Avoid soft 404 errors in single-page apps**. If a route does not exist, return a real `404` HTTP status code or use JavaScript to redirect to a `404` page where the server can return `404`.
5. **Use meaningful HTTP status codes**. Do not return `200 OK` for error pages; return `404` or `410` for missing content.
6. **Inject robots `meta` tags carefully**. Avoid changing `meta` robots tags with JavaScript when possible. If you must, test the rendered HTML to confirm the directive is present.
7. **Use long-term caching** for JavaScript and CSS assets to improve crawling and rendering performance, but make sure the cache does not prevent critical updates from being discovered.

For lazy-loaded content, make sure the content is visible in the rendered HTML without requiring complex user interactions. Use the native `loading="lazy"` attribute or `IntersectionObserver` to lazy-load below-the-fold images, and avoid hiding primary content behind events such as clicks, swipes, or scrolls that Googlebot cannot easily trigger. See [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=en), [Fix search-related JavaScript problems](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript?hl=en), [Lazy loading](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading?hl=en), and [Dynamic rendering](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering?hl=en).

### 8. Controlling what you share with Google

Sometimes the goal is to keep content out of Google rather than to get it indexed. There are several ways to do this, and they are not interchangeable.

The strongest methods:

1. **Remove the content from the site** or move it behind a login. This is the safest option and applies to all search engines.
2. **Password-protect the page**. Googlebot and other crawlers cannot access content that requires a password.
3. **Add a `noindex` rule** using either `<meta name="robots" content="noindex">` in the HTML or an `X-Robots-Tag: noindex` HTTP header. This prevents the page from appearing in Google Search, but it does not prevent other search engines or visitors from accessing the page.

Weaker or misunderstood methods:

- **Blocking with `robots.txt`** prevents crawling, but it does not prevent the URL from appearing in search results. In fact, if Google cannot crawl the page, it cannot see a `noindex` directive, so the page may remain indexed.
- **The Removals tool in Search Console** can remove a URL from search results within about a day, but it is temporary unless you also remove or `noindex` the content.

For quick removal of a page hosted on your site, use the [Removals tool](https://search.google.com/search-console?hl=en) and protect or remove all variations of the URL, including different cases, trailing slashes, and query parameters. To make the removal permanent, use `noindex`, delete the content, or require authentication. See the official pages on [Control what you share with Google](https://developers.google.com/search/docs/crawling-indexing/control-what-you-share?hl=en) and [Remove a page from Google](https://developers.google.com/search/docs/crawling-indexing/remove-information?hl=en).

### 9. Crawler management

Crawler management is about helping Google spend its time on your most important pages and avoid wasting resources on duplicate, broken, or low-value URLs.

**Requesting a recrawl** is useful when you add or update content. For a few URLs, use the URL Inspection tool in Search Console and click **Request indexing**. For many URLs, submit or update a sitemap. Crawling can take anywhere from a few days to a few weeks, so be patient and monitor progress in the Page Indexing report.

**Crawl budget** is the set of URLs that Google can and wants to crawl. It is determined by crawl capacity, which is how much load your server can handle, and crawl demand, which is based on the site's size, update frequency, page quality, and popularity. Most small or medium sites do not need to manage crawl budget, but large sites should:

1. Consolidate duplicate content with canonicalization and redirects.
2. Prevent crawling of unimportant or infinite URL spaces, such as faceted navigation, calendars, and sorting parameters, using `robots.txt` or URL design.
3. Return `404` or `410` for permanently removed pages so Google stops recrawling them.
4. Eliminate soft 404s and avoid long redirect chains.
5. Keep sitemaps up to date and use `<lastmod>` accurately.

**Mobile-first indexing** means Google uses the mobile version of a page's content for indexing and ranking. Google recommends responsive web design because it serves the same HTML on the same URL regardless of device. If you use dynamic serving or separate mobile URLs, make sure the content, metadata, and structured data are equivalent on both versions. Google does not require a mobile version to be in the index, but a mobile-friendly experience is strongly recommended.

**Verifying Googlebot** is important if you see unusual traffic claiming to be Googlebot. Use reverse DNS and forward DNS lookups, or match the IP address against the published [common crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=en) and [IP range JSON files](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot?hl=en). For example, a Googlebot IP should resolve to a host ending in `googlebot.com` or `geo.googlebot.com`, and a forward DNS lookup of that host should return the same IP.

**HTTP status codes and crawl errors** shape how and whether Google continues to crawl a URL. A `200 OK` means the page was fetched successfully. A `404 Not Found` tells Google the URL does not exist, while a `410 Gone` is a stronger signal that the resource is permanently removed. A `301` or `308` permanent redirect passes the canonical signal forward; a `302` or `307` temporary redirect keeps the original URL in the index. Server errors such as `500`, `503`, or `429` will cause Google to reduce crawling, so use them only temporarily and not as a long-term indexing strategy. Soft 404s, where an error page returns `200 OK`, waste crawl budget and should be fixed. Monitor these in the Page Indexing report and Crawl stats in Search Console, and use the URL Inspection tool to test live URLs. See [Ask Google to recrawl](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=en), [Mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing?hl=en), [Overview of Google crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=en), and [HTTP status codes and network errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=en).

---

## Additional crawling and indexing topics

The core concepts above cover the most common cases. The complete documentation also includes:

- **Crawlable content basics:** [indexable file types](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types?hl=en), [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure?hl=en), and [crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable?hl=en).
- **Sitemap extensions:** [image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps?hl=en), [News sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap?hl=en), [video sitemaps and alternatives](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps?hl=en), and [combining extensions](https://developers.google.com/search/docs/crawling-indexing/sitemaps/combine-sitemap-extensions?hl=en). For very large sitemaps, see [sitemap index files](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps?hl=en).
- **Crawler management:** the [list of Google crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=en), [Googlebot specifics](https://developers.google.com/search/docs/crawling-indexing/googlebot?hl=en), [reducing crawl rate](https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate?hl=en), [verifying Googlebot](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot?hl=en), [managing faceted navigation URLs](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation?hl=en), [large site crawl budget guide](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget?hl=en), [troubleshooting crawl errors](https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors?hl=en), and [HTTP status codes and network errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=en).
- **Canonicalization troubleshooting:** how to [solve canonical issues](https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting?hl=en).
- **Advanced page metadata:** the [robots meta tag, `data-nosnippet`, and `X-Robots-Tag`](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=en), [`noindex`](https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=en), and [qualifying outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links?hl=en).
- **Content removal:** [removing images](https://developers.google.com/search/docs/crawling-indexing/prevent-images-on-your-page?hl=en) and [redacted information](https://developers.google.com/search/docs/crawling-indexing/keep-redacted-information-out?hl=en).
- **Site moves and testing:** changing hosting, moving a site with URL changes, [A/B testing](https://developers.google.com/search/docs/crawling-indexing/website-testing?hl=en), and [temporarily pausing a site](https://developers.google.com/search/docs/crawling-indexing/pause-online-business?hl=en).
- **AMP:** creating, enhancing, validating, and [removing AMP content](https://developers.google.com/search/docs/crawling-indexing/amp/remove-amp?hl=en).

For a complete, structured list of every page, see [`references/google-search-central-toc.md`](references/google-search-central-toc.md).

---

## Common patterns

### Pattern: Launching a new site

1. Make the site publicly accessible and confirm that pages return a `200` status code.
2. Create and validate a sitemap with only canonical, indexable URLs.
3. Submit the sitemap in the [Search Console Sitemaps report](https://search.google.com/search-console?hl=en).
4. Check that `robots.txt` allows Googlebot and does not block CSS, JavaScript, images, or fonts.
5. Add a canonical URL to every page, especially the home page, and implement redirects for alternate home page URLs.
6. Verify that the mobile version has the same content and metadata as the desktop version.
7. Monitor the Page Indexing report and fix coverage errors.

### Pattern: Merging or migrating domains

1. Audit the old site and create a URL mapping from every old URL to the most relevant new URL.
2. Implement `301` redirects from the old URLs to the new URLs on the server side.
3. Update canonical tags, internal links, and navigation to point to the new URLs.
4. Submit the new sitemap through Search Console and remove any old sitemaps that are no longer accurate.
5. Use the Change of Address tool in Search Console if you are moving to a new domain.
6. Monitor Search Console for redirect errors, soft 404s, and indexing drops for several weeks.

### Pattern: Cleaning up duplicate or filtered URLs

1. Choose the canonical URL for each product, category, or article, ignoring tracking parameters and sort order.
2. Add `<link rel="canonical">` to all parameterized and alternate versions.
3. If a filter permanently changes the content, consider a `301` redirect instead of a canonical tag.
4. If the filters create a large number of low-value combinations, block the crawling of those combinations with `robots.txt`.
5. Update the sitemap to include only canonical URLs.

### Pattern: Handling removed or out-of-stock content

1. If the product or page will never return, return a `404` or `410` status code and remove internal links to the URL.
2. If the product will return soon, keep the page live and explain the expected availability; do not redirect it to an unrelated category page.
3. If the product is permanently replaced by another, use a `301` redirect to the new product page.
4. Avoid soft 404s where the server returns `200 OK` for an error message; this wastes crawl budget.
5. Remove the URL from the sitemap once it is gone.

---

## Best practices

- Ensure Google can crawl and index your important public pages; do not rely on hidden or uncrawlable content.
- Use sitemaps for large, new, media-rich, or weakly internally linked sites.
- Keep `robots.txt` clean, place it at the root, and do not block resources needed for rendering.
- Use `noindex` for pages that should not appear in search results, but make sure those pages are not blocked by `robots.txt`.
- Canonicalize duplicate content and redirect obsolete URLs with `301` redirects.
- Optimize JavaScript sites so titles, snippets, canonical tags, and core content are available in the rendered HTML.
- Use the History API for client-side navigation and avoid hash-based routing.
- Implement server-side redirects instead of meta refresh or JavaScript redirects whenever possible.
- Keep desktop and mobile content equivalent, including metadata and structured data.
- Monitor the Page Indexing report, Crawl stats, and Core Web Vitals in Search Console.

## Common pitfalls

| Pitfall | Why it is a problem | Solution |
| --- | --- | --- |
| Using `robots.txt` to hide sensitive content. | `robots.txt` does not prevent indexing and is ignored by many crawlers. | Use password protection or `noindex`. |
| Canonicalizing to an inaccessible URL. | Google cannot follow the canonical signal if the target returns an error or is blocked. | Ensure the canonical URL returns `200` and is not `noindex`ed or blocked. |
| Long redirect chains. | Long chains slow crawling and can cause Google to stop following. | Keep chains to one or two hops. |
| Blocking CSS or JavaScript with `robots.txt`. | Googlebot cannot render the page correctly and may miss content. | Allow crawling of all resources needed for rendering. |
| Relying only on JavaScript redirects. | Google may take longer to process them, and users with JavaScript disabled are left behind. | Use server-side `301` or `302` redirects. |
| Using `noindex` and blocking the page with `robots.txt` at the same time. | Google cannot see the `noindex` if the page is blocked, so the URL may still appear in results. | Allow crawling so Google can read the `noindex`, or remove the content. |
| Letting faceted navigation create infinite URL spaces. | Crawl budget is wasted on useless combinations, slowing discovery of real pages. | Use `robots.txt`, canonicalization, or fragment-based filters. |

---

## Examples

### Example 1: Blocking a staging environment from Google

```
User: How do I prevent Google from indexing my staging environment?

Assistant: The safest approach is to put the staging site behind a password or add a `noindex` rule to every staging page. For example, add the following to the `<head>` of each page:

`<meta name="robots" content="noindex">`

If you use an HTTP header, you can return:

X-Robots-Tag: noindex

Blocking with robots.txt alone is not enough, because robots.txt prevents crawling but does not prevent the URL from appearing in search results if other sites link to it. If you do use robots.txt to stop crawling, make sure the pages are also noindex or password-protected. Finally, remove the staging URLs from any public sitemaps and do not link to the staging site from the production site.
```

### Example 2: Requesting a recrawl after a product update

```
User: I updated my product pages. How do I ask Google to recrawl them?

Assistant: First, make sure the updated pages return a 200 status code and contain the correct canonical URLs. Then take the following steps:

1. Submit an updated sitemap in Google Search Console that lists the canonical product URLs and uses accurate `<lastmod>` dates.
2. For the most important pages, use the URL Inspection tool in Search Console to request indexing individually.
3. If the site is large, prioritize the top category and product pages; Google will discover the rest through the sitemap and internal links.
4. Monitor the Page Indexing report. Crawling and indexing can take anywhere from a few days to a few weeks, so be patient and look for errors.
```

### Example 3: Merging two domains without losing traffic

```
User: We are merging `example-a.com` into `example-b.com`. How do we keep our rankings?

Assistant: A domain merge must be done with server-side 301 redirects and clear canonical signals. Follow this plan:

1. Map every URL on `example-a.com` to the most relevant URL on `example-b.com`. Do not redirect every old page to the new home page.
2. Configure the server to return a 301 redirect from each old URL to its mapped new URL. For example, redirect `www.example-a.com/products/green-dress` to `www.example-b.com/products/green-dress`.
3. Update the canonical tags on `example-b.com` so they point to the new URLs, and update internal links so they no longer point to `example-a.com`.
4. Add the new domain in Search Console, submit the new sitemap, and use the Change of Address tool to tell Google about the move.
5. Keep the old redirects in place for at least a year and monitor the Page Indexing report for redirect errors, soft 404s, and traffic changes.
```

### Example 4: Fixing a JavaScript product gallery that Google is not indexing

```
User: Google Search Console says my product gallery pages are Discovered - currently not indexed. The gallery images only load when the user scrolls. What should I do?

Assistant: The issue is most likely that the gallery content is not visible to Googlebot during the initial render. Lazy loading is fine, but it must not hide primary content behind interactions that Googlebot cannot easily trigger. Take these steps:

1. Use native lazy loading for images with the `loading="lazy"` attribute, or use `IntersectionObserver` to load images as they approach the viewport. Avoid requiring a click or swipe to reveal the main gallery.
2. Confirm that the product titles, descriptions, and canonical URLs are present in the server-rendered or client-rendered HTML by testing with the Search Console URL Inspection tool or the Rich Results Test.
3. Ensure the page uses the History API for any pagination or filtering rather than hash fragments.
4. Submit the updated gallery pages for indexing in Search Console and update the sitemap with accurate `<lastmod>` dates.
```

---

## References

- [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md) — Extracted English summaries from Google Search Central.
- [`references/google-search-central-toc.md`](references/google-search-central-toc.md) — Complete index of all subsections in this documentation area.
- [Crawling and indexing overview](https://developers.google.com/search/docs/crawling-indexing?hl=en)
- [How Google Search works](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en)
- [File types Google can index](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types?hl=en)
- [URL structure best practices](https://developers.google.com/search/docs/crawling-indexing/url-structure?hl=en)
- [Crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable?hl=en)
- [Sitemaps overview](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=en)
- [Build and submit sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=en)
- [Manage sitemaps with a sitemap index file](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps?hl=en)
- [robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=en)
- [How Google interprets the robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec?hl=en)
- [Meta tags and attributes](https://developers.google.com/search/docs/crawling-indexing/special-tags?hl=en)
- [Robots meta tag, data-nosnippet, and X-Robots-Tag](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=en)
- [noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=en)
- [Specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=en)
- [Fix canonicalization issues](https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting?hl=en)
- [Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects?hl=en)
- [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=en)
- [Fix search-related JavaScript problems](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript?hl=en)
- [Lazy loading](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading?hl=en)
- [Dynamic rendering](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering?hl=en)
- [Control what you share with Google](https://developers.google.com/search/docs/crawling-indexing/control-what-you-share?hl=en)
- [Remove a page from Google](https://developers.google.com/search/docs/crawling-indexing/remove-information?hl=en)
- [Request a recrawl](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=en)
- [Overview of Google crawlers](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=en)
- [Googlebot](https://developers.google.com/search/docs/crawling-indexing/googlebot?hl=en)
- [Reduce the Google crawl rate](https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate?hl=en)
- [Verify Googlebot and other Google crawlers](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot?hl=en)
- [Mobile-first indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing?hl=en)
