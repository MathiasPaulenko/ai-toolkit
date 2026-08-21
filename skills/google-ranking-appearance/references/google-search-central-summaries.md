# Google Search Central Summaries: Ranking and Search Appearance

> These are extracted English summaries from the official Google Search Central documentation. Always check the linked official pages for the latest guidance.

## Overview of search appearance topics

The topics in this section describe how you can influence how your website appears in Google Search. With structured data, Google can understand the content of the pages it crawls. You can help us by providing concrete information about your site so that it can appear with enhanced features in search results.

## Use structured data

### Features that use structured data

## Early Adopters Program

- Home
- Search Central
- Documentation
- AI features
- Business details
- Byline dates
- Favicons
- Featured snippets

URL: <https://developers.google.com/search/docs/appearance?hl=en>

---

## Influencing your title links in search results

A title link is the title of a search result on Google Search and other properties (for example, Google News) that links to a web page. Google uses a number of different sources to automatically determine the title link, but you can indicate your preferences by following our best practices for influencing title links. Title links are critical to giving users a quick insight into the content of a result and why it's relevant to their query.

## Best practices for influencing title links

## How title links in Google Search are created

## Common issues and how Google manages them

### Half-empty `<title>` elements

### Obsolete `<title>` elements

### Inaccurate `<title>` elements

### Boilerplate text in `<title>` elements

### No clear main title

### The writing system or language used in `<title>` elements doesn't match

### Duplication of the site name in the `<title>` element

- Home
- Search Central
- Documentation
- Make sure every page on your site has a title specified in the `<title>` element.
- Write `<title>` elements that are descriptive and concise. Avoid vague descriptors like "Home" for your home page, or "Profile" for a specific person's profile. Also avoid unnecessarily long or verbose text in your `<title>` elements. While there's no limit on how long a `<title>` element can be, the title link is truncated in Google Search results as needed, typically to fit the device width.
- Avoid keyword stuffing. It's sometimes helpful to have a few descriptive terms in the `<title>` element, but there's no reason to have the same words or phrases appear multiple times. Title text like "Foobar, foo bar, foobars, foo bars" doesn't help the user, and this kind of keyword stuffing can make your results look spammy to Google and to users.

URL: <https://developers.google.com/search/docs/appearance/title-link?hl=en>

---

## Control your snippets in search results

A snippet is the description or summary part of a search result on Google Search and other properties (for example, Google News). Google primarily uses the content on the page to automatically determine the appropriate snippet. We may also use descriptive information in the `<meta>` description element if it describes the page better than other parts of the content. Get everything you need to sew your next pre

## How snippets are created

## How to prevent snippets from showing or adjust their length

## Best practices for creating quality meta descriptions

### Create unique meta descriptions for each page on your site

### Include relevant information about the description content

### Generate descriptions automatically

### Use quality descriptions

## Best practices for "Learn more" deep links in Google Search

- Home
- Search Central
- Documentation
- Make sure the content is immediately visible on the page for a human user (and not hidden behind an accordion or tabbed interface, for example).
- Avoid using JavaScript to control the user's scroll position when the page loads (for example, don't force the user's scroll position to the top of the page).
- If you make calls to the History API or modify window.location.hash when the page loads, make sure you don't remove the URL hash fragment, as this would prevent deep links from working correctly.

URL: <https://developers.google.com/search/docs/appearance/snippet?hl=en>

---

## Structured data markup supported by Google Search

Google uses structured data to understand the content of pages and display it attractively in search results, which is known as rich results. If you want your site to appear as one of these rich results, check the guide for information on how to implement structured data on your site. If you're just starting out, check the article How structured data works. These are news, sports, or blog articles that appear

- Home
- Search Central
- Documentation

URL: <https://developers.google.com/search/docs/appearance/structured-data/search-gallery?hl=en>

---

## SEO best practices for Google Images

Google offers several products and features in Search results so that users can visually discover information on the web, such as text result images, Google Discover, and Google Images. Although each feature and product looks different, the general recommendations for images to appear in them are the same. You can optimize your images to appear in Google search results by following these best practices:

## Help us discover and index your images

### Use HTML image elements to insert images

### Use an image sitemap

### Responsive images

### Use supported image formats

### Optimize speed and quality

## Optimize image landing pages

### Specify a preferred image with metadata

### Review the title and description of the pages

### Add structured data

- Home
- Search Central
- Documentation
- Help us discover and index your images
- Optimize image landing pages
- Specify the `primaryImageOfPage` property from schema.org with a URL or ImageObject value. `<script type="application/ld+json">`{ "@context": "<https://schema.org>", "@type": "WebPage", "url": "<https://example.com/url>", "primaryImageOfPage": "<https://example.com/images/cat.png>" }`</script>` You can also specify a URL or ImageObject image property and attach it to the main entity (using the schema.org `mainEntity` or `mainEntityOfPage` properties): `<script type="application/ld+json">`{ "@context": "<https://schema.org>", "@type": "BlogPosting", "mainEntityOfPage": "<https://example.com/url>", "image": "<https://example.com/imag>

URL: <https://developers.google.com/search/docs/appearance/google-images?hl=en>

---

## Best practices for video SEO

If you have videos on your site, following these video SEO best practices can help more users find your site through Google video results. Videos can appear in different places on Google, such as the main search results page, Video mode, Google Images, and Discover: Optimize your videos to appear in Google by following these best practices:

## Help Google find your videos

## Make sure your videos can be indexed

### Use a supported video file type

### Use stable URLs

### Create a specific watch page for each video

### Use third-party embedded players

## Distinguish the different URLs

### Provide a high-quality video thumbnail

### Provide unique and consistent information in structured data

## Enable video-specific features

- Home
- Search Central
- Documentation
- Help Google find your videos
- Make sure your videos can be indexed
- Enable video-specific features
- Remove, restrict, or update your videos as needed
- Monitor videos with Search Console

URL: <https://developers.google.com/search/docs/appearance/video?hl=en>

---

## Define a favicon to appear in search results

If your site has a favicon, it can be included in your site's Google Search results. Here's how to make your site eligible to appear with a favicon in Google Search results:

## Implementation

## Guidelines

## Send feedback about favicons in search results

- Home
- Search Central
- Documentation
- Create a favicon that meets the guidelines.
- Add a `<link>` tag to the header of your home page with this syntax: `<link rel="icon" href="/path/to/favicon.ico">` To extract the favicon information, Google relies on the following attributes of the `<link>` element: rel attributes Google supports the following values of the rel attribute to specify a favicon. Use the one that best fits your use case: icon The icon that represents your site, as defined in the HTML standard. For historical reasons, we also support shortcut icon, which is an older alternative version of icon. apple-touch-icon An iOS-compatible icon that represents your site, according to Apple's developer documentation. apple-touch-icon-precomposed An alternative icon for older versions of iOS, according to Apple's developer documentation. href The URL of the favicon. The URL can be a relative path (/smile.ico) or an absolute path (<https://example.com/smile.ico>). The URL does not need to be hosted on your site (for example, your favicon can be hosted on a content delivery network (CDN).
- Wait for some time for Google to recrawl and proce

URL: <https://developers.google.com/search/docs/appearance/favicon-in-search?hl=en>

---

## Core Web Vitals and Google Search results

Core Web Vitals are a set of metrics that measure the real-world experience users have with the loading speed of content, interactivity, and visual stability of pages. We recommend that site owners have good Core Web Vitals to achieve good results in Search and, in general, ensure an optimal user experience. This, along with other aspects of page experience, corresponds to what

## Core Web Vitals

## Optimize Core Web Vitals

## Recent Core Web Vitals news on our blog

- Home
- Search Central
- Documentation
- Largest Contentful Paint (LCP): measures the loading speed of content. To provide a good user experience, try to keep the LCP value below 2.5 seconds.
- Interaction to Next Paint (INP): measures responsiveness. To provide a good user experience, try to keep the INP value below 200 milliseconds.
- Cumulative Layout Shift (CLS): measures visual stability. To provide a good user experience, try to keep the CLS value below 0.1.
- Check the "Core Web Vitals" report in Search Console. This report shows the performance of your pages.
- Check the guide on Core Web Vitals, which includes information on how to measure, debug, and improve them, as well as best practices.

URL: <https://developers.google.com/search/docs/appearance/core-web-vitals?hl=en>

---

## What is page experience in Google Search results

Google's core ranking systems seek to reward content that provides a good page experience. Site owners who want to get good results with our systems shouldn't focus only on one or two aspects of page experience, but should check whether they provide a good overall page experience in many aspects. If you answer yes to the following questions, you're likely in

## Self-assess the page experience of content

## Resources about page experience

## Frequently asked questions

### Is there a single "page experience signal" that Google Search uses for ranking?

### What aspects of page experience are used in ranking?

### Is page experience evaluated across the whole site or on a specific page?

### How important is page experience for ranking?

## Recent page experience news on our blog

- Home
- Search Central
- Documentation
- Do your pages have good Core Web Vitals?
- Are your pages served securely?
- Does your content display correctly on mobile devices?
- Does your content avoid using an excessive amount of ads that distract from or interfere with the main content?
- Do your pages avoid using intrusive interstitials?

URL: <https://developers.google.com/search/docs/appearance/page-experience?hl=en>

---

## Discover and your website

Discover is a part of Google Search that shows users content related to their interests, based on their Web & App Activity. This page explains how content can appear in Discover and the best practices that site owners can keep in mind. Any content that is in Google's index and complies with Discover's content policies can appear in Discover. There is no need to use special tags or structured d

## How content appears in Discover

## Why Discover traffic can change over time

## Monitor performance in Discover

- Home
- Search Central
- Documentation
- Avoid clickbait and similar tactics to artificially increase engagement. For example, don't include misleading or exaggerated information in the parts of your content that users see first (that is, in the title, snippets, or images) to make the page more appealing, and don't hide information needed to understand what the content is about.
- Use titles and page headings that reflect the essence of the content.
- Avoid sensationalism and tactics that seek to manipulate interest, whether by exploiting morbid curiosity, excitement, or outrage.
- Offer content about trending topics, that is well written, or that provides unique information.
- Include attractive, high-quality images in your content that are relevant, especially if they are large, as they are more likely to generate visits in Discover. We recommend that you use images that meet the following specifications: At least 1200 px wide High resolutio

URL: <https://developers.google.com/search/docs/appearance/google-discover?hl=en>

---

## Featured snippets and websites

Featured snippets are special search results displayed in boxes and have the inverted format; that is, they show the descriptive snippet first. They can also appear within a group of related questions (also called "People also ask"). Check more information about how Google featured snippets work. To prevent snippets from a specific page (both featured snippets and regular snippets),

## How can I disable featured snippets?

### Block all snippets

### Block only featured snippets

## How can I mark my page to appear as a featured snippet?

## What happens when users click a featured snippet?

- Home
- Search Central
- Documentation
- Block both featured and regular search snippets
- Block only featured snippets
- Text marked with the HTML `data-nosnippet` attribute won't appear in featured snippets or regular snippets either.
- If both `nosnippet` rules and `data-nosnippet` appear on a page, `nosnippet` takes priority and the snippets for that page won't be shown.

URL: <https://developers.google.com/search/docs/appearance/featured-snippets?hl=en>

---

## Help readers find your site through preferred sources in Google Search

If you're a website owner, you can help your audience find your publication as a preferred source in Google Search. When a user selects your site as a preferred source, your content is more likely to appear in the Top Stories section, highlighted with a "preferred" badge. In AI Mode and AI Overviews, your content can be highlighted with the "preferred" badge for users who have selected your site as a preferred source. The functi

## Feature availability

## How to help users find your site as a preferred source

- Home
- Search Central
- Documentation
- Add the deep link to your posts or promotions on social media. Use the following URL format, which takes users directly to your site in the source preferences tool: <https://google.com/preferences/source?q=Your_Website's_URL&hl=en> For example, if your site is <https://example.com>, use the following URL: <https://google.com/preferences/source?q=example.com&hl=en>
- Add a button to your site alongside other social calls to action (CTAs). You can use your own design or download the button resources that Google provides for some languages. Button resources by language All listed languages Download (all_listed_languages) Danish Download (da) English Download (en) Estonian Download (et) Finnish Download (fi) French Download (fr) German Download (de) Hebrew Download (iw) Hindi Download (hi) Japanese Download (ja) Korean Download (ko) Portuguese (Brazil) Download (pt-br) Russian Download (ru) Spanish Download (es) Swedish Downloa

URL: <https://developers.google.com/search/docs/appearance/preferred-sources?hl=en>
