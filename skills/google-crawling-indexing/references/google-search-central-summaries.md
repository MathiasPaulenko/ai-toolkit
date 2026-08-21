# Google Search Central Summaries: Crawling and Indexing

> These are extracted English summaries from the official Google Search Central documentation. They are preserved in English to keep the original source wording. Always check the linked official pages for the latest guidance. All URLs below include `?hl=en` to force the English version.

## Overview of crawling and indexing topics

The topics in this section describe how you can control Google's ability to find and parse your content in order to show it in Search and other Google properties, as well as how to prevent Google from crawling specific content on your site.

Google Search has three overlapping stages: crawling, indexing, and serving. Crawling is the automated discovery of pages, usually by Googlebot following links and sitemaps. After a page is fetched, Googlebot renders it with an evergreen version of Chromium so that client-side JavaScript content can be analyzed. Indexing is the process of evaluating the rendered content and, if appropriate, storing it in the index. Serving is selecting relevant pages from the index and ranking them for a query.

Key pages in this section:

- [Crawling and indexing overview](https://developers.google.com/search/docs/crawling-indexing?hl=en)
- [How Google Search works](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en)
- [File types Google can index](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types?hl=en)
- [URL structure](https://developers.google.com/search/docs/crawling-indexing/url-structure?hl=en)
- [Crawlable links](https://developers.google.com/search/docs/crawling-indexing/links-crawlable?hl=en)

---

## Learn about sitemaps

A sitemap is a file where you provide information about the pages, videos, and other files on your site, and the relationships between them. Search engines like Google read this file to crawl your site more efficiently. A sitemap tells search engines which pages and files you think are important in your site, and also provides valuable information about these files, for example when the page was last updated and any alternate language versions of the page.

You probably need a sitemap if:

- Your site is large. On large sites it is more difficult to make sure that every page is linked by at least one other page on the site, so it is more likely Googlebot might not discover some new pages.
- Your site is new and has few external links. Googlebot and other web crawlers access URLs found in previously crawled pages, so if no other sites link to yours, some pages may not be discovered.
- You have rich media, news, or localized content that can benefit from the extra metadata sitemaps provide.

URL: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=en>

---

## Build and submit a sitemap

This page describes how to build a sitemap and make it available to Google. If you are new to sitemaps, read the introduction first.

Google supports the sitemap formats defined by the sitemaps protocol. Each format has its own benefits and shortcomings; choose the one that is most appropriate for your site and setup. Google does not have a preference. The supported formats are XML, RSS, mRSS, Atom 1.0, and plain text.

- XML sitemaps are the most versatile. They are extensible and can supply additional data about images, video, and news content, as well as localized versions of your pages. Most CMSes automatically generate XML sitemaps or have plugins that do so. The trade-off is that they can be cumbersome to work with and complex to maintain on large or frequently changing sites.
- RSS, mRSS, and Atom 1.0 sitemaps are similar in structure to XML sitemaps and are often the easiest to provide because CMSes automatically create RSS and Atom feeds. Besides HTML and other indexable textual content, they can provide information about videos, but not images or news.
- Text sitemaps are the simplest format and can only list URLs to HTML and other indexable pages. They are simple to do and maintain, especially on large sites.

Best practices:

- A single sitemap file must not be larger than 50 MB uncompressed and must not contain more than 50,000 URLs. If you have a larger file or more URLs, break the sitemap into multiple files and use a sitemap index file.
- The sitemap file must be UTF-8 encoded.
- You can host your sitemap anywhere on your site, but unless you submit the sitemap through Search Console, a sitemap only affects descendants of the parent directory. For this reason, it is recommended to post sitemaps at the site root.
- Use fully-qualified, absolute URLs. Google will attempt to crawl the URLs exactly as listed, so do not use relative URLs such as `/mypage.html`; use `https://www.example.com/mypage.html`.
- Include only canonical URLs that you want to see in search results.
- If you have separate URLs for mobile and desktop versions of a page, point to only one version in the sitemap, or annotate the URLs to indicate the desktop and mobile versions.

A very basic XML sitemap looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/foo.html</loc>
    <lastmod>2022-06-04</lastmod>
  </url>
</urlset>
```

URL: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=en>

---

## Sitemap extensions and large sitemaps

Sitemap index files let you split a very large sitemap into multiple files and then list them in one place. You can submit the single index file to Google instead of submitting each sitemap individually. This is useful when you want to track the search performance of each individual sitemap in Search Console.

Image, video, and news extensions allow you to give Google additional metadata:

- An image sitemap entry can include the location of images included in a page. This is useful for images that are loaded by JavaScript or that otherwise might not be easily discovered.
- A video sitemap entry can specify the video running time, rating, and age-appropriateness rating.
- A News sitemap entry can include the article title and publication date. News sitemaps should contain only news articles published in the last two days and are intended for sites approved for Google News.
- You can combine extensions in a single sitemap, but you must follow the namespace and child-element rules of the sitemaps protocol.

When a sitemap grows beyond the 50 MB or 50,000 URL limit, split it. For example, a site with 100,000 URLs would have at least two separate sitemap files and one sitemap index file that lists them.

URLs:

- [Manage sitemaps with a sitemap index file](https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps?hl=en)
- [Image sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps?hl=en)
- [News sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap?hl=en)
- [Video sitemaps and alternatives](https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps?hl=en)
- [Combining sitemap extensions](https://developers.google.com/search/docs/crawling-indexing/sitemaps/combine-sitemap-extensions?hl=en)

---

## Introduction to robots.txt

A robots.txt file tells search engine crawlers which URLs the crawler can access on your site. This is used mainly to avoid overloading your site with requests; it is not a mechanism for keeping a web page out of Google. To keep a web page out of Google, block indexing with `noindex` or password-protect the page.

If you use a CMS, such as Wix or Blogger, you might not need to (or be able to) edit your robots.txt file directly. Instead, your CMS might expose a search settings page or some other mechanism to tell search engines whether or not to crawl your page.

Main uses:

- Prevent the site from being overloaded by crawler requests.
- Block crawling of non-public or irrelevant sections.

Important limitations:

- robots.txt is not a security mechanism. Malicious crawlers may ignore it.
- robots.txt does not prevent indexing. Use `noindex` or a password for that.
- Each crawler may interpret the syntax differently.

URL: <https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=en>

---

## How Google interprets the robots.txt specification

Google's automated crawlers support the Robots Exclusion Protocol (REP). Before crawling a site, Google's crawlers download and parse the site's robots.txt file to extract information about which parts of the site may be crawled. The REP is not applicable to Google's crawlers that are controlled by users, such as feed subscriptions, or to crawlers used to increase user safety, such as malware analysis.

A robots.txt file is a text file containing rules about which crawlers may access which parts of a site. It consists of one or more groups. Each group begins with a `User-agent` line and contains one or more `Disallow` or `Allow` rules. Crawlers process groups from top to bottom and a user agent matches only the first, most specific group. If there are multiple groups for the same user agent, the groups are combined before processing.

Key rules:

- The default assumption is that a user agent can crawl any page or directory not blocked by a `Disallow` rule.
- Rules are case-sensitive. For example, `Disallow: /file.asp` applies to `https://www.example.com/file.asp` but not to `https://www.example.com/File.asp`.
- The file must be placed in the top-level directory of the site. The rules apply only to the host, protocol, and port number where the robots.txt file is hosted.
- For Google Search, supported protocols are HTTP, HTTPS, and FTP. On HTTP and HTTPS, crawlers fetch robots.txt with an HTTP non-conditional `GET` request.
- A `Sitemap:` directive can point to a sitemap file. It is not required, but it is a good way to help Google discover the sitemap.

URL: <https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec?hl=en>

---

## How to specify a canonical URL with rel="canonical" and other methods

To specify a canonical URL for duplicate or very similar pages to Google Search, you can indicate your preference using a number of methods. These are, in order of how strongly they can influence canonicalization:

1. **Redirects.** A strong signal that the target of the redirect should become canonical.
2. **`<link rel="canonical">` annotations.** A strong signal that the specified URL should become canonical.
3. **Sitemap inclusion.** A weak signal that helps the URLs that are included in a sitemap become canonical.

Keep in mind that these methods can stack and thus become more effective when combined. Using two or more methods increases the chance that your preferred canonical URL appears in search results.

Reasons to specify a canonical URL include:

- Indicate the URL you want to show in search results. For example, if you have a page where green dresses are sold, you might prefer people to reach it through `https://www.example.com/dresses/green/green-dress.html` rather than `https://example.com/dresses/cocktail?gclid=ABCD`.
- Consolidate signals for similar or duplicate pages. It helps search engines consolidate the signals they have for the individual URLs, such as links to them, into a single preferred URL.

You can implement a canonical annotation as an HTML element:

```html
<link rel="canonical" href="https://www.example.com/dresses/green/green-dress.html" />
```

Or as an HTTP header:

```
Link: <https://www.example.com/dresses/green/green-dress.html>; rel="canonical"
```

URL: <https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=en>

---

## Redirects and Google Search

Redirecting URLs is the practice of resolving an existing URL to a different one, effectively telling your visitors and Google Search that a page has a new location. Redirects are particularly useful in the following circumstances:

- You have moved your site to a new domain and want to make the transition seamless.
- People access your site through several different URLs. If your home page can be reached in multiple ways, pick one as the preferred destination and use redirects to send traffic from the other URLs to the preferred one.
- You are merging two websites and want to make sure that links to outdated URLs are redirected to the correct pages.
- You removed a page and want to send users to a new page.

Key redirect types:

- **301 / 308 (permanent server-side redirects).** Show the new redirect target in search results. These are the best choice for permanent URL changes.
- **302 / 307 (temporary server-side redirects).** Keep the original URL in the index while temporarily serving another page.
- **Meta refresh and JavaScript `location` redirects.** Avoid if possible; they are less reliable and may take longer for Google to process.
- **Crypto redirects.** Displaying a message that a page has moved without a real HTTP redirect is not recommended as the primary solution.

URL: <https://developers.google.com/search/docs/crawling-indexing/301-redirects?hl=en>

---

## Understand the JavaScript SEO basics

JavaScript is an important part of the web platform because it provides many features that turn the web into a powerful application platform. Making your JavaScript-powered web applications discoverable via Google Search can help you find new users and re-engage existing users. Google Search runs JavaScript with an evergreen version of Chromium.

How Google processes JavaScript:

1. Googlebot crawls the initial HTML.
2. Googlebot queues the page for rendering.
3. Google renders the page, including JavaScript, using an evergreen Chromium.
4. The rendered content is then processed for indexing.

Best practices:

- Describe pages with unique titles and snippets.
- Define the canonical URL and avoid relying on JavaScript to inject it.
- Write compatible code and use meaningful HTTP status codes.
- Avoid soft 404 errors in single-page apps.
- Use the History API instead of URL fragments for client-side navigation.
- Use robots `meta` tags carefully; avoid injecting or changing them with JavaScript when possible.
- Use long-term caching for static assets.

URL: <https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=en>

---

## Lazy loading and dynamic rendering

Lazy loading is a technique that defers loading of non-critical resources until they are needed, such as images below the fold. Googlebot can process lazy-loaded content, but the content must be visible in the rendered HTML without requiring complex user interactions. Use the native `loading="lazy"` attribute or `IntersectionObserver` and avoid hiding primary content behind clicks, swipes, or scrolls that Googlebot cannot easily trigger.

Dynamic rendering is a workaround for sites that rely heavily on JavaScript and have difficulty getting their content indexed. With dynamic rendering, a server detects Googlebot and serves a pre-rendered version of the page, while users receive the normal JavaScript experience. Google no longer recommends dynamic rendering as the default solution; instead, use server-side rendering, static rendering, or hydration.

URLs:

- [Fix lazy-loaded content](https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading?hl=en)
- [Fix search-related JavaScript problems](https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript?hl=en)
- [Dynamic rendering as a workaround](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering?hl=en)

---

## Meta tags and attributes that Google supports

`meta` tags are HTML tags used to provide additional information about a page to search engines and other clients. Clients process the `meta` tags and ignore those they do not support. `meta` tags are added to the `<head>` section of your HTML page.

Key supported tags:

- `description` may be used as the snippet in search results.
- `robots` and `googlebot` control indexing and display directives such as `noindex`, `nofollow`, `noarchive`, `nosnippet`, `max-snippet`, `max-image-preview`, `max-video-preview`, `notranslate`, and `nopagereadaloud`.
- `google-site-verification` is used for Search Console ownership verification.
- `Content-Type` and `charset` declare the document encoding.
- `viewport` is essential for mobile-friendly pages.
- `rating` can indicate the maturity rating of the page.

Important notes:

- Google can read both HTML and XHTML-style `meta` tags.
- The HTML code in the `<head>` section must be valid and parent tags must be closed as appropriate.
- Except for `google-site-verification`, `meta` tags are usually not case-sensitive.
- Google ignores `meta` tags it does not support.
- Avoid using JavaScript to inject or change `meta` tags when possible.

URL: <https://developers.google.com/search/docs/crawling-indexing/special-tags?hl=en>

---

## Robots meta tag, data-nosnippet, and X-Robots-Tag

This document details how page-level and text-level settings can be used to adjust how Google presents your content in search results. You can specify page-level settings by including a `meta` tag on HTML pages or in an HTTP response header. The `X-Robots-Tag` is useful for non-HTML files such as PDFs and images.

Common directives:

- `noindex` prevents the page from appearing in search results.
- `nofollow` prevents Google from following links on the page.
- `nosnippet` prevents a snippet from being shown.
- `noarchive` prevents a cached copy from being shown.
- `max-snippet`, `max-image-preview`, and `max-video-preview` control the length or size of the snippet and media preview.

The `data-nosnippet` attribute lets you mark specific parts of a page that should not appear in a snippet. Apply it to `span`, `div`, or `section` elements.

URL: <https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=en>

---

## Block Search indexing with noindex

`noindex` is a rule set with either a `meta` tag or HTTP response header and is used to prevent indexing content by search engines that support the `noindex` rule, such as Google. When Googlebot crawls that page and extracts the tag or header, Google will drop that page from its search results.

To implement `noindex`:

- HTML: `<meta name="robots" content="noindex">`
- HTTP header: `X-Robots-Tag: noindex`

For `noindex` to work, the page must be crawlable. If the page is blocked by `robots.txt`, Googlebot cannot see the `noindex` directive and the URL may still appear in search results.

URL: <https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=en>

---

## Control what you share with Google

Google supports a variety of ways that allow site owners to control what shows up in Google's search results. While most people focus on getting their pages indexed, sometimes it is important to do the opposite: prevent content from appearing in Search.

How to block content:

- Remove or update the content on your page. This is the most secure way to prevent your information from appearing in search engines that might not respect the `noindex` tag.
- Password-protect your files. Limiting access to your page enables the right users to view it while preventing Googlebot and other crawlers from accessing it.
- Add a `noindex` tag to your page. A `noindex` tag only blocks your page from showing up in Google search results. Users and other search engines that do not support `noindex` can still access it.
- Block crawling with `robots.txt`. This prevents Google from crawling the page, but it does not prevent the URL from appearing in search results.

To remove a page from Google quickly, use the Removals tool in Search Console. Protect or remove all variations of the URL for the content that you want to remove, including case, parameters, and trailing slashes.

URL: <https://developers.google.com/search/docs/crawling-indexing/control-what-you-share?hl=en>

---

## Remove a page hosted on your site from Google

If you want to quickly remove (within a day) a page hosted on your site from Google Search results, use the Removals tool. Protect or remove all variations of the URL for the content that you want to remove. In many cases, different URLs can point to the same page, for example `example.com/puppies`, `example.com/PUPPIES`, and `example.com/petchooser?pet=puppies`.

To make a removal permanent:

- Remove or update the content on the page.
- Password-protect the page.
- Add a `noindex` tag.

Removing images or information from other Google properties may require separate steps, such as using Google Business Profile or Google Shopping controls.

URL: <https://developers.google.com/search/docs/crawling-indexing/remove-information?hl=en>

---

## Ask Google to recrawl your URLs

If you have recently added or made changes to a page on your site, you can request that Google re-index your page using the URL Inspection tool for a few URLs or by submitting a sitemap for many URLs at once. You cannot request indexing for URLs that you do not manage.

Crawling can take anywhere from a few days to a few weeks. Be patient and monitor progress using either the Page Indexing report or the URL Inspection tool. For hosted CMS platforms such as Blogger or WordPress, new content is often submitted to search engines automatically.

URL: <https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=en>

---

## Overview of Google crawlers and fetchers

Google uses crawlers and fetchers to perform actions for its products, either automatically or triggered by user request. A crawler is a generic term for any program that is used to automatically discover and scan websites. A fetcher acts like a program such as `wget` that typically makes a single request on behalf of a user.

Google's clients fall into three categories:

- **Common crawlers**, such as Googlebot, which respect `robots.txt` rules for automatic crawls.
- **Special-case crawlers**, which are used by specific products where there is an agreement between the crawled site and the Google product. For example, `AdsBot` ignores the global `robots.txt` user agent (`*`) with the ad publisher's permission.
- **User-triggered fetchers**, which are part of tools and product functions where the end user triggers a fetch, such as Google Site Verifier.

Google's crawlers and fetchers support HTTP/1.1 and HTTP/2. They support gzip, deflate, and Brotli content encodings. By default, Google's crawlers only crawl the first 15 MB of a file, and any content beyond that limit is ignored; individual projects may set different limits. Google also supports heuristic HTTP caching through `ETag`, `If-None-Match`, `Last-Modified`, and `If-Modified-Since` headers.

URL: <https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=en>

---

## Googlebot

Googlebot is the generic name for Google's web crawler. It is used for both desktop and mobile indexing. For mobile-first indexing, Googlebot uses a smartphone user agent. Googlebot discovers pages by following links and reading sitemaps. It then renders the page using an evergreen version of Chromium and sends the rendered content for indexing.

The user-agent token `Googlebot` in `robots.txt` affects Google Search, Google Images, Google Video, Google News, and Google Discover. If you need to target only image search, you can use the `Googlebot-Image` token, and for video search, the `Googlebot-Video` token.

URL: <https://developers.google.com/search/docs/crawling-indexing/googlebot?hl=en>

---

## Reduce the Google crawl rate

Google's crawler infrastructure has sophisticated algorithms to determine the optimal crawl rate for a site. The goal is to crawl as many pages as possible without overwhelming the server. If Google's crawling is causing a critical load on your infrastructure, you can reduce it.

In an emergency, for a short period of time such as a couple of hours or one to two days, you can return `500`, `503`, or `429` HTTP response status codes instead of `200`. Google will reduce the crawl rate for the whole hostname. This is not recommended for longer than a couple of days, because the affected URLs may eventually be dropped from the index.

For exceptional cases, you can file a special request through Search Console to report an unusually high crawl rate. You cannot request an increase in crawl rate.

URL: <https://developers.google.com/search/docs/crawling-indexing/reduce-crawl-rate?hl=en>

---

## Verify Googlebot and other Google crawlers

You can verify if a request to your server really is from Google. This is useful if you are concerned that spammers or other troublemakers are accessing your site while claiming to be from Google.

There are two methods:

1. **Manual verification.** Run a reverse DNS lookup on the accessing IP address, verify that the domain is `googlebot.com`, `google.com`, or `googleusercontent.com`, then run a forward DNS lookup and verify that it resolves to the same IP.
2. **Automatic verification.** Match the crawler's IP address against the published JSON files for common crawlers, special-case crawlers, and user-triggered fetchers.

Common Googlebot hostnames resolve to `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`.

URL: <https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot?hl=en>

---

## Managing crawling of faceted navigation URLs

Faceted navigation is a common feature that allows visitors to filter items such as products, articles, or events. The most common implementation uses URL parameters and can generate infinite URL spaces. This causes overcrawling, because crawlers cannot determine whether a URL is useful without first crawling it, and it slows the discovery of new, useful URLs.

A typical faceted navigation URL looks like:

```
https://example.com/items.shtm?products=fish&color=radioactive_green&size=tiny
```

If you do not need faceted navigation URLs indexed, prevent crawling with `robots.txt` by disallowing the filter parameters. If you need them potentially indexed, follow best practices:

- Use the standard URL parameter separator `&`.
- If filters are encoded in the URL path, keep the logical order of filters the same and avoid duplicate filters.
- Return an HTTP `404` status code when a filter combination returns no results.

You can also use `rel="canonical"` and `rel="nofollow"` as supporting signals, but they are generally less effective than `robots.txt` or fragment-based filters.

URL: <https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation?hl=en>

---

## Optimize your crawl budget

This guide describes how to optimize Google's crawling of very large and frequently updated sites. If your site does not have a large number of pages that change rapidly, or if your pages seem to be crawled the same day they are published, you do not need to read this guide.

Crawl budget is the set of URLs that Google can and wants to crawl. It is determined by crawl capacity and crawl demand. Crawl capacity is how much load your server can handle; it goes up if the site is fast and stable, and down if the site returns server errors or becomes slow. Crawl demand is based on the site's size, update frequency, page quality, and popularity.

Best practices:

- Consolidate duplicate content so Google does not waste time crawling the same content under many URLs.
- Block unimportant or infinite URL spaces with `robots.txt`. Do not use `noindex` for this purpose, because Google still requests the page.
- Return `404` or `410` for permanently removed pages.
- Eliminate soft 404s.
- Keep sitemaps up to date.
- Avoid long redirect chains.
- Make pages efficient to load and support `304 Not Modified` caching.

URL: <https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget?hl=en>

---

## HTTP status codes and network errors

The HTTP status code returned for a page tells Google how to treat that URL. The most important codes for crawling and indexing are:

- `200 OK` — the page was fetched successfully and can be indexed.
- `301 / 308` — permanent redirect; the target URL becomes canonical.
- `302 / 307` — temporary redirect; the original URL stays in the index.
- `404 / 410` — not found or gone; Google will eventually stop crawling the URL.
- `500 / 503 / 429` — server errors or rate limiting; Google will reduce crawling.
- `304 Not Modified` — the page has not changed; Google can reuse the cached version.

DNS and network errors can also affect crawling. If DNS cannot resolve the host, Google cannot crawl it. If the server does not respond, the crawl may be retried later.

URL: <https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=en>

---

## Mobile site and mobile-first indexing best practices

Google uses the mobile version of a site's content, crawled with the smartphone agent, for indexing and ranking. This is called mobile-first indexing. It is not required to have a mobile version to be included in search results, but it is strongly recommended.

Best practices:

- Use responsive web design so the same HTML and URL are served to all devices.
- Make sure Google can access and render your mobile content.
- Keep content the same on desktop and mobile, including metadata and structured data.
- Check where ads appear on mobile and ensure they do not obstruct content.
- Check visual content such as images and videos.

If you use dynamic serving, rely on user-agent sniffing and the `Vary: user-agent` HTTP response header. If you use separate URLs for mobile, use equivalent `rel="alternate"` and `rel="canonical"` annotations.

URL: <https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing?hl=en>

---

## URL structure and crawlable links

To make sure Google Search can crawl your site effectively, use a crawlable URL structure. Good URLs are short, meaningful, and use a logical hierarchy. Avoid using session IDs or unnecessary parameters in URLs that need to be indexed, and avoid relying on fragments for navigation.

Google uses links as a signal for relevancy and to discover new pages. To make links crawlable:

- Use an `<a>` tag with an `href` attribute pointing to a real URL.
- Do not rely on non-standard elements or JavaScript events alone for navigation.
- Provide descriptive anchor text that gives users and Google context about the target page.

URL structure URL: <https://developers.google.com/search/docs/crawling-indexing/url-structure?hl=en>
Crawlable links URL: <https://developers.google.com/search/docs/crawling-indexing/links-crawlable?hl=en>

---

## Page metadata, rel attributes, and indexable file types

Valid page metadata helps Google understand and present your content. Keep your `<head>` section valid, place `meta` tags and canonical links in the `<head>`, and make sure the content is equivalent on mobile and desktop.

`rel` attributes on links help Google understand the relationship between pages:

- `rel="canonical"` marks the preferred version of duplicate content.
- `rel="nofollow"` tells Google not to pass quality signals.
- `rel="sponsored"` marks paid or advertising links.
- `rel="ugc"` marks user-generated content links.

Google can index many file types, including HTML, PDF, Microsoft Word and Excel, text files, and several image and video formats. Some rich media and proprietary formats may not be indexed.

URLs:

- [Page metadata](https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata?hl=en)
- [rel attributes and qualifying outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links?hl=en)
- [Indexable file types](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types?hl=en)

---

## Site moves, A/B testing, and temporarily pausing a website

When you move a site to new hosting without changing the URL, Google can usually continue crawling as long as the DNS and server configuration are correct. If you move to a new domain or change the URL structure, use `301` redirects from the old URLs to the new ones, update canonical tags and sitemaps, and use the Change of Address tool in Search Console.

For A/B testing, use `302` redirects or JavaScript to serve different versions to users, and use `rel="canonical"` to point to the original page so Google does not get confused by duplicate content.

If you need to temporarily pause or disable a website, return `503 Service Unavailable` status codes for the pages you want to take offline. Do not use `404` if the outage is temporary, because `404` signals that the content is gone.

URLs:

- [Changing your hosting](https://developers.google.com/search/docs/crawling-indexing/site-move-no-url-changes?hl=en)
- [Move a site with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes?hl=en)
- [A/B testing](https://developers.google.com/search/docs/crawling-indexing/website-testing?hl=en)
- [Temporarily pause or disable a website](https://developers.google.com/search/docs/crawling-indexing/pause-online-business?hl=en)

---

## AMP on Google Search

AMP is a web component framework that can create fast-loading pages. Google Search supports AMP and can show AMP pages in carousels and other rich result formats. To use AMP, create valid AMP HTML, enhance the content with structured data and metadata, validate the pages with the AMP validator, and monitor the AMP report in Search Console.

If you decide to remove AMP, redirect the AMP URLs to the canonical non-AMP versions and remove the AMP references from the canonical pages.

URLs:

- [About AMP on Google Search](https://developers.google.com/search/docs/crawling-indexing/amp?hl=en)
- [Enhance AMP content](https://developers.google.com/search/docs/crawling-indexing/amp/enhance-amp?hl=en)
- [Validate AMP content](https://developers.google.com/search/docs/crawling-indexing/amp/validate-amp?hl=en)
- [Remove AMP content](https://developers.google.com/search/docs/crawling-indexing/amp/remove-amp?hl=en)

---

## Image removals and redacted information

If you want to prevent images from appearing in Google Search results, you can either remove the image from the page, block the image URL with `robots.txt`, or add a `noindex` rule. For images hosted on other sites, you can use the Remove Outdated Content tool.

If redacted information still appears in search results, it is usually because the information is still present on the page or in the cached copy. Remove the content from the page, request a cache removal through Search Console, and make sure the content is not available through any other URL.

URLs:

- [Remove an image from search results](https://developers.google.com/search/docs/crawling-indexing/prevent-images-on-your-page?hl=en)
- [Keep redacted information out of Google Search](https://developers.google.com/search/docs/crawling-indexing/keep-redacted-information-out?hl=en)

---

## Other useful references

- [How Google Search works](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en) — high-level explanation of crawling, indexing, and ranking.
- [Search Console](https://search.google.com/search-console?hl=en) — submit sitemaps, request indexing, and monitor coverage.
- [Google Search Central blog](https://developers.google.com/search/blog?hl=en) — announcements about crawling and indexing changes.
