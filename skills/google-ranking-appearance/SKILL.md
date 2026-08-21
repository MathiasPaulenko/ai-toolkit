---
name: google-ranking-appearance
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Practical guide to Google search ranking and appearance: title links, snippets, structured data, rich results, images, videos, Discover, and local features."
tags: [google-search, ranking, search-appearance, structured-data, rich-results]
trigger: When the user asks about Google search ranking, search appearance, title links, snippets, structured data, rich results, images, videos, Google Discover, or page experience.
---

# Google Ranking and Search Appearance

## Description

This skill covers the *Ranking and search appearance* section of Google Search Central. It explains how to influence how a site appears in Google Search results: from title links and snippets to images, videos, structured data, rich results, Google Discover, local features, and page experience.

> The supporting English summaries for this skill are in [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md).

## Usage

### When to invoke

- The user asks how to influence the appearance of search results.
- The user wants to optimize title links or meta descriptions.
- The user needs guidance on structured data and rich results.
- The user wants to optimize images or videos for Google Search.
- The user needs to understand page experience and Core Web Vitals.
- The user wants to appear in Google Discover or local results.
- The user asks about featured snippets, favicons, sitelinks, site names, or publication dates.

### Input

- A specific appearance feature or search result type.
- Optional: a URL, HTML, or structured data markup to review.

### Output

- A structured answer with direct links to the relevant Google Search Central pages.
- Implementation guidance, concrete examples, and common mistakes to avoid.

---

## Core concepts

### 1. Search appearance overview

Search appearance is the way Google presents web pages in search results. It includes the basic title link and text snippet, plus enhanced formats such as images, videos, rich results, favicons, site names, sitelinks, featured snippets, and feed-style surfaces such as Google Discover and AI Overviews.

A site owner can influence appearance by providing clear, accurate, and well-structured information. The most common mistakes are treating appearance features as isolated tricks, ignoring page experience, or adding structured data that is not visible to users.

How to influence it:

1. Publish crawlable, renderable content with important text visible in the HTML.
2. Use structured data that matches the main purpose of the page.
3. Optimize the assets that appear in search results: the `<title>` element, the `<meta name="description">` tag, images, videos, and the favicon.
4. Monitor results with Search Console: the Performance, Rich Results, and URL Inspection reports.

### 2. Title links

A title link is the clickable title shown for a search result on Google Search, Google News, and other Google properties. Google creates title links automatically from sources such as the `<title>` element, visible headings, `og:title` meta tags, and anchor text from other sites. Because the title link is usually the first thing a user reads, it strongly influences click-through rates and relevance.

**How to implement**

1. Include a `<title>` element on every page.
2. Write descriptive and concise text. Avoid vague descriptors such as "Home" or "Profile".
3. Avoid keyword stuffing, such as repeating "Foobar, foo bar, foobars," which looks spammy.
4. Avoid boilerplate text replicated across many pages, such as "Cheap products for sale" on every product page.
5. Brand titles concisely. On most pages place the site name at the beginning or end with a delimiter: `<title>ExampleSocialSite: Sign up for a new account.</title>`.
6. Make the main title visually prominent, for example by placing it in the first visible `<h1>` element.
7. Use the same language and writing system as the primary content, and update the `<title>` when the content changes.

A common issue is an outdated title: a university page with `<title>2020 admissions criteria - University of Awesome</title>` but a visible heading of "2021 admissions criteria" may have its title link replaced by the heading. The fix is to update the `<title>` to match the current content.

| Common issue | Solution |
| --- | --- |
| Half-empty `<title>` | Complete the `<title>` with the main topic. |
| Outdated `<title>` | Update the `<title>` whenever the page is updated. |
| Inaccurate `<title>` | Make the `<title>` reflect the actual page content. |
| Boilerplate `<title>` | Make each title specific to the page. |
| No clear main title | Make the main heading the most prominent on the page. |
| Mismatched language | Match the `<title>` to the primary content language. |

**Common mistakes**

- Using vague or identical `<title>` elements across many pages.
- Keyword stuffing in titles.
- Writing the `<title>` in a different language or script than the visible content.

### 3. Snippets

A snippet is the descriptive text shown below the title link. Google primarily creates snippets from page content, but it may also use the `<meta name="description">` tag when that gives a more accurate description. Snippets are query-specific, and a good snippet helps users decide whether to click.

**How to implement**

1. Write a unique `<meta name="description">` for every page.
2. Make the description informative and relevant. Include details such as author, date, price, or location. For example: `<meta name="description" content="Written by A.N. Author, Illustrated by V. Gogh, Price: $17.99, Length: 784 pages">`.
3. Generate descriptions programmatically for large sites, as long as the output is human-readable and varied.
4. Keep descriptions truly descriptive. Do not use long lists of keywords or generic text.
5. Place important content where it is immediately visible, because deep-link snippets work best when content is not hidden behind tabs or accordions.
6. Use `nosnippet` to prevent any snippet, `max-snippet:[number]` to limit length, or `data-nosnippet` to hide specific text.

A good snippet for a sewing supplies shop is `<meta name="description" content="Get everything you need to sew your next garment. Open Monday-Friday 8-5pm, located in the Fashion District.">` instead of a simple list of keywords.

**Common mistakes**

- Relying only on the meta description and ignoring the visible page content.
- Using the same description on every page.
- Writing descriptions that are too short, too vague, or stuffed with keywords.

### 4. Structured data and rich results

Structured data is a standardized format for describing a page and classifying its content. It helps Google understand the meaning of the page and can enable rich results, which are search results with enhanced features such as star ratings, images, prices, and event details. Google case studies show measurable increases in click-through rate for sites that implement structured data correctly.

**How to implement**

1. Choose the right schema.org type for the main content, such as `Article`, `Recipe`, `Event`, `Product`, `LocalBusiness`, `Organization`, `Video`, or `JobPosting`.
2. Use a supported format. Google supports JSON-LD (recommended), Microdata, and RDFa. JSON-LD is usually easiest and can be injected dynamically with JavaScript.
3. Include all required properties for the type. Items missing required properties are not eligible for rich results.
4. Add recommended properties when they are accurate and complete. It is better to provide fewer complete properties than many incomplete ones.
5. Put the structured data on the page it describes. Do not create blank pages just for structured data, and do not mark up information that is not visible to users.
6. Test the markup with the [Rich Results Test](https://search.google.com/test/rich-results?hl=en). After deployment, monitor the Rich result status reports in Search Console.
7. Follow the general structured data guidelines and the specific feature guidelines. Violations can lead to manual actions and loss of rich result eligibility.

A recipe page can include JSON-LD such as:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Non-Alcoholic Piña Colada",
  "author": { "@type": "Person", "name": "Mary Stone" },
  "datePublished": "2024-03-10",
  "description": "This non-alcoholic piña colada is everyone favorite!",
  "recipeIngredient": ["400ml of pineapple juice", "100ml cream of coconut", "ice"]
}
</script>
```

**Common mistakes**

- Using structured data that does not match the visible content.
- Marking up fake reviews, hidden content, or unrelated entities.
- Missing required properties for a feature.
- Adding structured data to blank or empty pages.
- Blocking the structured data page with `robots.txt` or `noindex`.

### 5. Images

Images appear in text results, Google Images, Google Discover, and other visual features. High-quality, relevant images improve the visual appeal of a result and increase the likelihood of a click. Because images are a major contributor to page size, optimizing them also improves page speed and Core Web Vitals.

**How to implement**

1. Use standard HTML `<img>` elements. Google finds images in the `src` attribute, even inside a `<picture>` element, and does not index CSS background images.
2. Provide descriptive `alt` text. For example, `<img src="puppy.jpg" alt="Dalmatian puppy playing fetch" />` is better than `<img src="puppy.jpg" alt="puppy dog baby dog pup pups" />`.
3. Use supported image formats: BMP, GIF, JPEG, PNG, WebP, SVG, and AVIF. Match the filename extension to the file type.
4. Use responsive images with `srcset` or `<picture>`, and always provide a fallback `src`.
5. Submit an image sitemap, which can include URLs from other domains such as a CDN.
6. Optimize for speed and quality with modern image formats and compression.
7. Specify a preferred image with `primaryImageOfPage` in `WebPage` structured data, or with `og:image`.
8. Place images near relevant text and use descriptive filenames such as `my-new-black-kitten.jpg` instead of `IMG00023.JPG`.

A blog post can specify a preferred image with JSON-LD: `{ "@context": "https://schema.org", "@type": "BlogPosting", "mainEntityOfPage": "https://example.com/url", "image": "https://example.com/images/cat.png" }`.

**Common mistakes**

- Using `<div style="background-image:url(puppy.jpg)">` instead of an `<img>` tag.
- Leaving `alt` attributes empty or stuffing them with keywords.
- Using generic filenames like `image1.jpg`.
- Serving extremely large or unoptimized images.

### 6. Videos

Videos can appear in the main search results page, the video search tab, Google Images, and Discover. Video results are highly visible and can drive significant traffic, and they can also appear as video previews, key moments, and the LIVE badge.

**How to implement**

1. Use HTML elements that Google recognizes: `<video>`, `<embed>`, `<iframe>`, or `<object>`. Do not use URL fragments to load the video.
2. Create a dedicated watch page for each video when it makes sense. A watch page's main purpose is to show a single video.
3. Use a supported video file type. Google can process many formats, including MP4, WebM, MOV, MPEG, AVI, and MKV. See the [video SEO guide](https://developers.google.com/search/docs/appearance/video?hl=en) for the full list.
4. Use stable URLs for watch pages and for video files. Quickly expiring URLs can prevent indexing.
5. Provide a high-quality thumbnail, at least 60x30 pixels, through the `<video>` `poster` attribute, a video sitemap, structured data, or Open Graph.
6. Add `VideoObject` structured data with consistent and unique values for `thumbnailUrl`, `name`, and `description`.
7. Enable key moments with `Clip` or `SeekToAction` structured data.
8. Allow Google to fetch the video files. Do not block the streaming URL with `robots.txt` or `noindex`.
9. Monitor performance with Search Console: the Video indexing report, the Video rich result report, and the Videos filter in the Performance report.

A watch page should distinguish between the watch page URL (`<loc>` in the sitemap), the player URL (`VideoObject.embedUrl` or `<video:player_loc>`), and the video file URL (`VideoObject.contentUrl` or `<video:content_loc>`).

**Common mistakes**

- Embedding a video only inside a blog post or product page without a dedicated watch page.
- Using unstable or expiring URLs for thumbnails or video files.
- Blocking the video file with `robots.txt` or login requirements.
- Providing inconsistent information in structured data, sitemaps, and Open Graph.

### 7. Favicons

A favicon is a small icon that can appear next to the site name in Google Search results. It helps users identify the site and improves brand recognition.

**How to implement**

1. Create a favicon that represents the site. It must be a square image with a 1:1 aspect ratio, at least 8x8 pixels. A size larger than 48x48 pixels is recommended.
2. Add a `<link>` tag to the `<head>` of the home page: `<link rel="icon" href="/path/to/favicon.ico">`.
3. Google supports the following `rel` values: `icon`, `shortcut icon`, `apple-touch-icon`, and `apple-touch-icon-precomposed`.
4. The `href` can be a relative or absolute URL, and may be hosted on a CDN.
5. Allow Googlebot and Googlebot-Image to crawl the favicon and the home page.
6. Wait for Google to recrawl and process the change, which can take from several days to several weeks.

**Common mistakes**

- Trying to set a favicon for a subdirectory. Google Search supports one favicon per hostname.
- Using an inappropriate favicon, such as one containing pornography or hate symbols.
- Changing the favicon URL frequently.
- Blocking the favicon or home page from crawlers.

### 8. Page experience and Core Web Vitals

Google's core ranking systems seek to reward content that provides a good page experience. Page experience includes Core Web Vitals, mobile friendliness, HTTPS, the absence of intrusive interstitials, and the ability of users to find and consume the main content. It is not a single signal, and when many pages could answer a query, pages with a better experience are more likely to be rewarded. However, Google always seeks to show the most relevant content first.

#### Core Web Vitals

| Metric | What it measures | Target |
| --- | --- | --- |
| Largest Contentful Paint (LCP) | Loading performance of the main content | Less than 2.5 seconds |
| Interaction to Next Paint (INP) | Responsiveness to user interactions | Less than 200 milliseconds |
| Cumulative Layout Shift (CLS) | Visual stability of the page | Less than 0.1 |

**How to implement**

1. Measure Core Web Vitals with Search Console, PageSpeed Insights, and other tools.
2. Improve LCP by reducing server response times, optimizing images and videos, and removing render-blocking resources.
3. Improve INP by minimizing long JavaScript tasks.
4. Improve CLS by reserving space for images, ads, and embeds before they load.
5. Serve the site over HTTPS and make sure content displays well on mobile devices.
6. Avoid excessive ads and intrusive interstitials.

**Common mistakes**

- Chasing a perfect score while neglecting content quality.
- Treating page experience as the only ranking factor.
- Ignoring mobile usability or HTTPS.
- Adding large, unoptimized images that hurt LCP.
- Inserting content that causes layout shifts after the page loads.

### 9. Google Discover

Google Discover is a feed that shows users content related to their interests, based on their Web and App Activity. Any content in Google's index that complies with Discover's content policies is eligible to appear. No special tags or structured data are required. Discover can drive significant traffic from users who are not actively searching, but that traffic is less predictable than keyword-driven search traffic.

**How to implement**

1. Avoid clickbait and misleading details in titles, snippets, or images.
2. Use titles and headings that reflect the essence of the content.
3. Avoid sensationalism, such as exploiting morbid curiosity or outrage.
4. Provide timely, well-written, or unique information.
5. Include attractive, high-quality images. Google recommends images that are at least 1200 pixels wide, with high resolution and a 16:9 aspect ratio.
6. Enable large image previews with `max-image-preview:large` or by using AMP.
7. Specify a large, relevant image with `og:image` or structured data.
8. Provide a great page experience overall.

**Common mistakes**

- Using clickbait headlines that do not match the content.
- Using small, generic, or text-heavy images as the featured image.
- Expecting stable, dependable traffic from Discover.
- Publishing content not suitable for an interest-based feed, such as job applications or petitions without context.

### 10. Featured snippets

Featured snippets are special search result boxes where the descriptive snippet appears first, often at the top of the results. They can also appear within the "People also ask" group. Google automatically determines which page to feature, and a featured snippet can drive high visibility and traffic.

#### How to influence them

There is no way to mark a page as a featured snippet. Google systems determine whether a page would make a good featured snippet for a query. To increase the chance of selection, structure the content clearly and answer questions directly.

1. Identify clear questions the page answers.
2. Place the answer near the top, in a concise paragraph, list, or table.
3. Use a logical heading structure with `<h1>`, `<h2>`, and `<h3>` tags.
4. Provide additional context and related questions further down the page.
5. Make sure the content is accurate and directly visible to users.

To block all snippets, use the `nosnippet` robots meta tag. To block only featured snippets while keeping regular snippets, experiment with a low `max-snippet:[number]` value. If a guaranteed solution is needed, use `nosnippet`.

**Common mistakes**

- Trying to force a featured snippet with hidden or manipulative content.
- Structuring answers in a way that is hard to extract, such as inside large blocks of JavaScript or images.
- Not providing a concise, direct answer to the question.

### 11. Site names and sitelinks

The site name is the name of the site shown near the title link in search results. It is different from the per-page title link. Sitelinks are additional links to important sections of the same site, shown under a text result. A clear site name helps users recognize the source, and sitelinks help users navigate directly to important pages.

**How to implement**

For site names:

1. Add `WebSite` structured data to the home page with the `name` and `url` properties. Include `alternateName` if the site is commonly known by an acronym.
2. Use a unique, concise, and commonly recognized name. For example, use "Google" instead of "Google, Inc."
3. Avoid generic names such as "Best Dentists In Iowa" unless that is a well-recognized brand.
4. Use the same site name consistently across the home page, including in `og:site_name`, `<title>`, headings, and structured data.
5. Place the structured data on the domain or subdomain home page. Subdirectories cannot have their own site name.

For sitelinks:

1. Use informative and compact page titles and headings.
2. Create a logical site structure that is easy to navigate.
3. Link to important pages from other relevant pages within the site.
4. Use concise and relevant anchor text for internal links.
5. Avoid repetitive content.

A home page can set the site name with JSON-LD: `{ "@context": "https://schema.org", "@type": "WebSite", "name": "Example Company", "alternateName": "EC", "url": "https://example.com/" }`.

**Common mistakes**

- Trying to set a site name for a subdirectory such as `https://example.com/news`.
- Using a long, generic, or misleading site name.
- Creating multiple `WebSite` structured data blocks on the home page.
- Removing sitelinks by `noindex`-ing important pages instead of improving site structure.

### 12. Local features and business details

Local features include business details shown in Google Search and Google Maps, such as addresses, phone numbers, opening hours, and reviews. The knowledge panel can also show information about an organization, including the official site, logo, and social profiles. For businesses with a physical presence, local results are often the most important search appearance.

**How to implement**

1. Claim and verify the Business Profile on Google to manage appearance on Maps and Search.
2. Verify website ownership in Search Console.
3. Add `Organization` structured data to the official site to specify the preferred logo.
4. Add `BreadcrumbList` structured data to show the page's position in the site hierarchy.
5. Use `LocalBusiness` structured data when the page represents a local business.
6. Keep business information consistent across the website, Business Profile, and third-party directories.
7. If you are an official representative, use the knowledge panel feedback tools to correct information.

**Common mistakes**

- Having inconsistent business information across the site, Business Profile, and other listings.
- Not verifying the site in Search Console or the Business Profile.
- Forgetting to add structured data that identifies the official website and logo.

### 13. Publication dates

Google can display a byline date in search results when it can determine the publication or significant update date of a page or video. A visible date can influence whether a user clicks, and Google uses date signals as part of its freshness systems, which show fresher content for queries where recency is expected.

**How to implement**

1. Add a user-visible date to the page and label it clearly, such as "Posted Feb 4, 2019" or "Last updated: Feb 14, 2018".
2. Use a subtype of `CreativeWork` structured data, such as `Article`, `BlogPosting`, or `VideoObject`, and specify `datePublished` and `dateModified`.
3. Make the user-visible date and the structured data date consistent, including time and time zone when provided.
4. Do not specify future dates or the date of an event described on the page. The date must describe the page's own publication or update.
5. Minimize other dates on the page if the wrong date is being selected.

A news article can show the visible text "Posted Tuesday, July 20, 2021" and JSON-LD with `"@type": "NewsArticle"`, `"datePublished": "2021-07-20T08:00:00+08:00"`, and `"dateModified": "2021-07-20T09:20:00+08:00"`.

**Common mistakes**

- Providing inconsistent dates between visible text and structured data.
- Specifying future dates or event dates instead of the page's publication or update date.
- Including many unrelated dates on the page.

### 14. Preferred sources

Preferred sources allow users to select a site as a preferred source in Google Search. When a user selects a site, its content is more likely to appear in Top Stories and can be highlighted with a "preferred" badge in AI Mode and AI Overviews. For news and content publishers, this creates a direct relationship with readers.

**How to implement**

1. Check whether the site is eligible in the source preferences tool. Only domain-level and subdomain-level sites are eligible.
2. Add an interactive "Add to Preferred Sources" button. Load the library with `<script async src="https://news.google.com/swg/js/v1/publisher.js?hl=en"></script>` and add `<div google-add-preferred-source-btn></div>` where the button should appear.
3. Customize the button with `data-theme="dark"` or `data-lang="en"`.
4. If JavaScript is not possible, use a deeplink such as `https://www.google.com/preferences/source?q=example.com&hl=en`.
5. Promote the option in posts, newsletters, and social media.

**Common mistakes**

- Trying to use the feature for a subdirectory rather than a domain or subdomain.
- Adding the button without testing that the site appears in the source preferences tool.
- Overpromoting the button in a way that distracts from the content.

### 15. Ranking systems and updates

Google uses many automated ranking systems to present relevant, useful results. They work on a page level using a variety of signals, and site-wide signals also contribute. Understanding them helps avoid SEO myths and focus on what actually matters.

#### Key systems

| System | What it does |
| --- | --- |
| BERT | Understands how combinations of words express different meanings and intent. |
| RankBrain | Understands how words relate to concepts. |
| Freshness systems | Shows newer content for queries where recency is expected. |
| PageRank and link analysis | Uses links between pages to understand relevance and helpfulness. |
| Original content systems | Surfaces original content prominently, including original reporting. |
| Reviews system | Rewards high-quality reviews with insightful analysis and research. |
| Spam detection, including SpamBrain | Deals with content and behaviors that violate spam policies. |
| Site diversity | Generally limits the top results to no more than two listings from the same site. |
| Passage ranking | Identifies individual sections of a page to understand their relevance. |

Google regularly improves ranking systems and announces major updates. Core updates can affect traffic broadly, while spam updates target content that violates spam policies. The reviews system update focuses on review content quality. When traffic changes after an update, review the relevant guidance before making major changes.

**Common mistakes**

- Believing there is a single "page experience signal" or a magic ranking factor.
- Trying to optimize for one specific system while ignoring overall content quality.
- Assuming a drop after an update means the site has been penalized.
- Building low-quality links or creating content primarily for search engines.

### 16. AI features

AI features in Google Search, such as AI Overviews and AI Mode, surface relevant links to help users find information quickly and explore content they might not have discovered otherwise. They can display a wider and more diverse set of helpful links than classic web search because they may issue multiple related searches across subtopics and data sources.

#### How to appear

There are no additional requirements to appear in AI Overviews or AI Mode. The same SEO best practices apply: ensure the page is indexed, follow Search policies, create helpful and people-first content, make content findable through internal links, provide a great page experience, keep important content in textual form, support it with high-quality images and videos, make sure structured data matches the visible text, and keep Merchant Center and Business Profile information up to date.

**Common mistakes**

- Creating new machine-readable files, AI text files, or special schema.org markup for AI features. None are required.
- Believing that AI features replace the need for solid SEO fundamentals.
- Blocking content with `nosnippet` or `noindex` without understanding that this also affects classic search.

---

## Additional appearance and ranking topics

The full documentation also covers [AI features](https://developers.google.com/search/docs/appearance/ai-features?hl=en), [publication dates](https://developers.google.com/search/docs/appearance/publication-dates?hl=en), [flexible sampling](https://developers.google.com/search/docs/appearance/flexible-sampling?hl=en), [site names](https://developers.google.com/search/docs/appearance/site-names?hl=en) and [sitelinks](https://developers.google.com/search/docs/appearance/sitelinks?hl=en), [business details](https://developers.google.com/search/docs/appearance/establish-business-details?hl=en) and [top places lists](https://developers.google.com/search/docs/appearance/top-places-list?hl=en), [opting out of local results](https://search.google.com/search-console/opt-out?hl=en), [core updates](https://developers.google.com/search/docs/appearance/core-updates?hl=en), [spam updates](https://developers.google.com/search/docs/appearance/spam-updates?hl=en), the [reviews system](https://developers.google.com/search/docs/appearance/reviews-system?hl=en), [translated results](https://developers.google.com/search/docs/appearance/translated-results?hl=en), [ad network translation](https://developers.google.com/search/docs/appearance/ad-network-and-translation?hl=en), [Web Stories](https://developers.google.com/search/docs/appearance/enable-web-stories?hl=en), [package tracking](https://developers.google.com/search/docs/appearance/package-tracking?hl=en), and [structured-data carousels (beta)](https://developers.google.com/search/docs/appearance/structured-data/carousels-beta?hl=en). For the complete list, see [`references/google-search-central-toc.md`](references/google-search-central-toc.md).

---

## Common patterns

### Pattern: Adding rich results to a page

1. Identify the content type (Article, Product, Event, Recipe, Video, etc.).
2. Choose the right schema.org type from the [Search Gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery?hl=en).
3. Implement the markup in JSON-LD, Microdata, or RDFa, with all required properties.
4. Validate with the [Rich Results Test](https://search.google.com/test/rich-results?hl=en).
5. Test the page with the URL Inspection tool in Search Console.
6. Monitor the Rich Results report for errors after deployment.

### Pattern: Optimizing a page for a featured snippet

1. Identify a clear question the page answers.
2. Place the answer near the top, in 40-60 words.
3. Use a list, table, or paragraph format that matches the query.
4. Add related questions and answers for context.
5. Use clear heading structure with `<h2>` or `<h3>` tags for each question.

---

## Best practices

- Create unique, descriptive, and concise `<title>` elements and `<meta name="description">` tags for every page.
- Implement relevant structured data and validate the markup.
- Optimize images and videos for visual search results, including `alt` text, thumbnails, and stable URLs.
- Improve Core Web Vitals and overall page experience.
- Publish useful, timely, people-first content for Google Discover and AI features.
- Maintain consistent business information and structured data for local and organizational features.
- Keep up to date with ranking system updates and Search Console reports.

## Common pitfalls

| Pitfall | Solution |
| --- | --- |
| Duplicate or generic `<title>` elements. | Customize the `<title>` of every page to describe its specific content. |
| Relying only on meta descriptions. | Make sure the page content itself describes the topic well. |
| Incorrect or misleading structured data. | Validate with the Rich Results Test and match markup to visible content. |
| Ignoring Core Web Vitals. | Measure and improve LCP, INP, and CLS. |
| Clickbait in Discover. | Use honest titles and images that reflect the content. |
| Blocking important pages or assets. | Review `robots.txt`, `noindex`, and access controls regularly. |

---

## Examples

### Example 1: Adding structured data for an article

```
User: What structured data should I add to a blog post?

Assistant: Use Article schema with headline, author, datePublished, dateModified,
publisher, and image properties. Validate the markup with the Rich Results Test
and the URL Inspection tool in Search Console. If the article is news, use
NewsArticle and follow the additional Google News guidelines.
```

### Example 2: Improving title links

```
User: My homepage title appears as "Home" in search results. How do I fix it?

Assistant: Update the <title> element to be descriptive and specific, such as
"Acme Tools — Industrial Equipment and Supplies" instead of "Home". Also make
sure the <h1> heading on the page matches the main topic.
```

### Example 3: Optimizing a product page for rich results

```
User: How do I get star ratings and price to show for my product in search results?

Assistant: Add Product structured data with name, image, description, brand, sku,
offers (price, priceCurrency, availability), and aggregateRating if you have
verified reviews. Validate the markup with the Rich Results Test and monitor the
Product snippets report in Search Console.
```

### Example 4: Enabling a video watch page

```
User: My embedded videos don't show up in Google video results. What am I missing?

Assistant: Make sure each video has its own watch page where the video is the main
content. Use <video>, <iframe>, <embed>, or <object> to embed the video. Provide
VideoObject structured data with name, description, thumbnailUrl, and contentUrl.
Use a supported video file type and a stable thumbnail URL. Submit a video sitemap
and check the Video indexing report in Search Console.
```

---

## References

- [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md) — Extracted English summaries from Google Search Central.
- [`references/google-search-central-toc.md`](references/google-search-central-toc.md) — Complete index of all subsections in this documentation area.
- [Search appearance overview](https://developers.google.com/search/docs/appearance?hl=en)
- [Title links](https://developers.google.com/search/docs/appearance/title-link?hl=en)
- [Snippets](https://developers.google.com/search/docs/appearance/snippet?hl=en)
- [Structured data search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery?hl=en)
- [How structured data works](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=en)
- [Structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies?hl=en)
- [Google Images](https://developers.google.com/search/docs/appearance/google-images?hl=en)
- [Videos](https://developers.google.com/search/docs/appearance/video?hl=en)
- [Favicons](https://developers.google.com/search/docs/appearance/favicon-in-search?hl=en)
- [Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals?hl=en)
- [Page experience](https://developers.google.com/search/docs/appearance/page-experience?hl=en)
- [Google Discover](https://developers.google.com/search/docs/appearance/google-discover?hl=en)
- [Featured snippets](https://developers.google.com/search/docs/appearance/featured-snippets?hl=en)
- [Preferred sources](https://developers.google.com/search/docs/appearance/preferred-sources?hl=en)
- [Ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide?hl=en)
- [Site names](https://developers.google.com/search/docs/appearance/site-names?hl=en)
- [Sitelinks](https://developers.google.com/search/docs/appearance/sitelinks?hl=en)
- [Business details](https://developers.google.com/search/docs/appearance/establish-business-details?hl=en)
- [Publication dates](https://developers.google.com/search/docs/appearance/publication-dates?hl=en)
- [AI features](https://developers.google.com/search/docs/appearance/ai-features?hl=en)
