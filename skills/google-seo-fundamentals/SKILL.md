---
name: google-seo-fundamentals
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Practical guide to Google Search SEO fundamentals: Search Essentials, technical requirements, spam policies, helpful content, generative AI guidelines, and site maintenance."
tags: [google-search, seo-fundamentals, search-essentials, helpful-content, ai-seo]
trigger: When the user asks about Google SEO fundamentals, Search Essentials, technical requirements, spam policies, helpful content, generative AI guidelines, or the SEO starter guide.
---

# Google SEO Fundamentals

## Description

This skill covers the *SEO fundamentals* section of Google Search Central. It explains how Google Search works, what it takes to appear and perform well, how to create people-first content, the role of generative AI, and how to maintain a site's SEO over time.

> The supporting English summaries for this skill are in [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md).

## Usage

### When to invoke

- The user wants to understand how Google Search works (crawling, indexing, serving).
- The user asks about the basic requirements to appear on Google.
- The user needs guidance on creating useful, reliable, people-first content.
- The user asks about Google's spam policies and what to avoid.
- The user wants to optimize for generative AI features in Google Search.
- The user is evaluating whether to hire an SEO specialist or use third-party SEO tools.

### Input

- A specific question, page, or topic from the *SEO fundamentals* section of Google Search Central.
- Optional: a URL or content the user wants to review against Google's fundamentals.

### Output

- A concise, structured answer with direct links to the relevant Google Search Central pages.
- Actionable next steps and common pitfalls to avoid.

---

## Core concepts

### 1. Google Search Essentials

The [Google Search Essentials](https://developers.google.com/search/docs/essentials?hl=en) are the core rules that make web-based content eligible to appear and perform well on Google Search. They are organized around three pillars: technical requirements, spam policies, and key best practices. Think of them as the baseline contract between your site and Google. Meeting the Essentials does not guarantee a top ranking, but violating them can prevent a page from appearing at all.

The first pillar, [technical requirements](https://developers.google.com/search/docs/essentials/technical?hl=en), covers the bare minimum Google needs in order to crawl, index, and serve a page. The second, [spam policies](https://developers.google.com/search/docs/essentials/spam-policies?hl=en), lists behaviors and tactics that can cause a page or an entire site to rank lower or be removed. The third, key best practices, describes the main things that can improve how your site appears in Search. All three pillars work together. A technically perfect page that violates spam policies will still fail, and a high-quality page that Google cannot access will not be shown.

Importantly, appearing in Google Search is free. Google does not accept payment to crawl a site more often or to rank it higher. Any claim to the contrary should be treated as a warning sign.

#### Minimum technical requirements

Google needs only a few technical things from a web page. Most sites that are built normally already pass these requirements without extra work. However, it is worth checking them deliberately because a single misconfiguration can make an entire page invisible.

1. Googlebot must not be blocked. Google only indexes pages that are publicly accessible and that do not block Google's crawler, Googlebot. If a page requires a login, Googlebot cannot crawl it. If `robots.txt` prevents access, the page is unlikely to appear in Search results. To verify access, use the URL Inspection tool in Search Console or the robots.txt tester.

2. The page must work, meaning that Google receives an HTTP `200 (success)` status code. Client errors such as `404` and server errors such as `500` are not indexed. A page that looks fine to a user but returns an error status code to Googlebot will not be indexed. Test the HTTP status with Search Console, a browser network tab, or a command-line tool such as `curl`.

3. The page must contain indexable content. The textual content should be in a file type that Google Search supports, such as HTML, and it must not violate spam policies. In addition, the content should be available without requiring the user to run unsupported plugins or to interact with the page in ways a crawler cannot replicate.

A common point of confusion: `robots.txt` blocks crawling, but a URL may still appear in search results if it is linked from elsewhere. To tell Google not to index a page at all, use a [`<meta name="robots" content="noindex">`](https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=en) tag or an equivalent `X-Robots-Tag` and allow Google to crawl the URL.

#### Major spam policies to avoid

Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies?hl=en) apply to all web search results. Violations can lead to manual actions, ranking demotions, or removal from the index. The following list is not exhaustive, but it covers the most common policy areas that site owners encounter.

- **Cloaking** means presenting different content to users and search engines with the intent to manipulate rankings or mislead users. An example is showing a page about travel destinations to search engines while showing discount-drug content to human visitors. Paywalls and content gating are not considered cloaking if Google can see the same content that any person with access would see and if you follow the [Flexible Sampling guidance](https://developers.google.com/search/docs/appearance/flexible-sampling?hl=en).

- **Doorway abuse** is the creation of pages that rank for specific, similar queries but funnel users to a single intermediate or final destination. Examples include multiple near-duplicate sites with slight URL or homepage variations, many region- or city-targeted domain names that all lead to the same page, or pages that are closer to search results than to a clearly defined, browseable hierarchy.

- **Expired domain abuse** happens when someone buys an expired domain and republishes low-value content primarily to borrow the domain's established signals. Examples include affiliate content on a domain previously used by a government agency, or casino content on a former elementary-school site.

- **Hacked content** is any content placed on a site without permission, often through code injection, page injection, or malicious redirects. If a site is hacked, attackers may use cloaking to hide the attack from the site owner. Site owners should follow Google's guidance on fixing and avoiding hacked sites.

- **Hidden text and link abuse** means placing content on a page solely to manipulate search engines and not to be easily viewable by people. Examples are white text on a white background, text positioned off-screen with CSS, font size or opacity set to zero, or links hidden behind a single small character. Not all hidden content is abusive: accordions, tabs, sliders, and screen-reader-only text that improves user experience are generally acceptable.

- **Keyword stuffing** is filling a page with keywords or numbers in an attempt to manipulate rankings, often in lists or groups that appear unnaturally or out of context. An example is a block of text that repeats the same phrase so often it sounds robotic. It is also keyword stuffing to list cities or phone numbers without substantial added value.

- **Link spam** is the creation of links to or from a site primarily to manipulate rankings. Buying or selling links, excessive link exchanges, automated link-building programs, requiring links in terms of service, advertorials that pass ranking credit, low-quality directory links, and keyword-rich links in widgets, footers, or forum signatures are all examples. Links that are part of normal advertising or sponsorship are acceptable if they are qualified with `rel="nofollow"` or `rel="sponsored"` on the `<a>` tag.



- **Scaled content abuse** is the mass production of unoriginal content that provides little to no value to users, regardless of how it is created. Using generative AI or automation to produce many pages without adding value, scraping feeds or results to generate pages, stitching content from different sources, or creating multiple sites to hide the scaled nature of the work all fall under this policy.

- **Scraping** is taking content from other sites, often through automated means, and hosting it to manipulate rankings. Republishing content without original value or citation, copying and lightly modifying another site's content, or building a site dedicated to embedding other people's media without substantial added value are all examples.

- **Site reputation abuse** is publishing third-party content on a host site mainly because that host site has already earned strong ranking signals. The test is whether the content would rank better on the established host than it could on its own. Coupons, advertorials, and affiliate links can be legitimate if they are clearly presented and treated appropriately, but third-party content that is hosted primarily to manipulate rankings can violate this policy.

#### Key best practices that influence appearance

While the technical requirements are the floor, the following practices are the main things Google recommends for improving how your site appears in Search.

- Create [helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=en). This is the single most important practice. Content should be created to help users, not to manipulate rankings.

- Use words that people would naturally search for and place them in prominent, descriptive locations. These include the `<title>` element, the main heading of the page, image `alt` text, and the visible text of links. This helps Google understand what the page is about and helps users decide whether to click.

- Make your links crawlable. Google discovers pages primarily by following links. If important pages are only reachable through forms, JavaScript events, or non-crawlable navigation, Google may never find them.

- Tell people about your site through legitimate promotion, community engagement, and offline materials. Word-of-mouth discovery remains one of the most effective and lasting ways to build an audience.

- Follow best practices for [images](https://developers.google.com/search/docs/appearance/google-images?hl=en), [videos](https://developers.google.com/search/docs/appearance/video?hl=en), [structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=en), and [JavaScript](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=en) so that Google can understand every part of the page.

- If you have content that should not appear in Search, use the correct method for [controlling how your content appears](https://developers.google.com/search/docs/crawling-indexing/control-what-you-share?hl=en). Do not rely on hope or on obscure tricks.

**Concrete example**

A small bakery launches a page for wedding cakes. The owner places the target keywords in the `<title>` element, the main heading, and image `alt` attributes; the URL is `https://www.example.com/wedding-cakes`; the page returns HTTP 200; the page is linked from the site navigation; and the text describes the bakery's real experience, pricing, and service area. The page is not blocked by `robots.txt` or `noindex`. Because it meets the technical requirements, avoids spam tactics, and follows key best practices, it is eligible to appear when people search for wedding cakes in that area.

**Common mistakes**

- Believing that paying for submission or inclusion will improve rankings, or accidentally allowing staging or test sites to be indexed.
- Using `robots.txt` to try to remove a page from search results, or stuffing footers with city names and phone numbers that add no real value.

### 2. How Google Search works

Google Search is a fully automated search engine. It uses software known as [web crawlers](https://developers.google.com/search/docs/crawling-indexing/googlebot?hl=en) to explore the web regularly, find pages, and add them to the [Google index](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en). The vast majority of pages listed in Google's results are not manually submitted. They are found and added automatically as Google crawls the web.

Understanding the three stages of Search is essential for debugging problems. If a page is not appearing, the cause is usually at one of these stages.

#### The three stages

1. **Crawling**: Google downloads text, images, and videos from pages it has found on the internet. Googlebot discovers URLs in several ways. Some pages are known because Google has already visited them. Others are discovered when Google extracts a link from a known page to a new page, such as when a category page links to a new blog post. Still others are discovered when the site owner submits a [sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=en) listing important pages.

   Once Googlebot discovers a URL, it may visit the page to find out what is on it. Googlebot uses an algorithmic process to determine which sites to crawl, how often, and how many pages to fetch. It also tries not to crawl a site too fast, and it may slow down in response to server errors such as `500`.

   During the crawl, Google renders the page and runs JavaScript using a recent version of Chrome. This is important because many sites rely on JavaScript to bring content into the page. If the JavaScript is blocked or unsupported, Google may not see the content.

2. **Indexing**: After a page is crawled, Google tries to understand what it is about. This stage includes processing and analyzing the textual content and key content tags and attributes, such as `<title>` elements, `alt` attributes, images, and videos. Google also determines whether a page is a duplicate of another page and selects a [canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=en) version to represent a group of similar pages.

   The canonical is the page that may be shown in search results. Other pages in the group may appear in different contexts, such as for mobile users or for very specific queries. Google collects signals about the canonical page and its contents, such as language, country, and usability, and stores the information in the Google index.

3. **Serving search results**: When a user enters a query, Google searches its index for matching pages and returns the results it believes are the highest quality and most relevant. Relevance is determined by hundreds of factors, which can include the user's location, language, and device. The search features that appear on the results page can also change depending on the query. For example, a search for "bicycle repair shops" is likely to show local results, while a search for "modern bicycle" is more likely to show image results.

#### Why it matters

Many site owners assume that if a page is live, it is in Google. In practice, a page must survive all three stages. A page can be crawled but not indexed if the content quality is low or if a `noindex` rule is present. A page can be indexed but not served if it is not relevant to any query or if it is outranked by more helpful pages.

#### How to help Google at each stage

- **Crawling**: Make sure Googlebot is not blocked by `robots.txt`, network issues, or server errors. Make your links crawlable and, if appropriate, submit a sitemap.
- **Indexing**: Provide original, high-quality content. Use descriptive `<title>` elements and `alt` text. Make sure `noindex` is used intentionally, not accidentally. Avoid duplicate content where possible.
- **Serving**: Create content that genuinely answers the queries your audience uses. Focus on relevance, authority, and page experience rather than trying to reverse-engineer a specific ranking formula.

#### Factors that can prevent a page from showing

- Server or network problems.
- `robots.txt` rules blocking Googlebot.
- `noindex` meta tags or `X-Robots-Tag` headers.
- Low-quality or irrelevant content.
- Pages that require a login, cookies, or unsupported interactions to be viewed.

**Concrete example**

A recipe site publishes a new article. It is linked from the homepage and from a category page, so Googlebot discovers it. The page returns HTTP 200, it does not block the crawler, and it uses a descriptive `<title>` and clear headings. After a few days, the page is indexed. However, it does not yet appear for competitive queries because other sites have stronger relevance and authority signals. The site owner continues to improve the content and promote it. After several weeks, the page begins to appear for long-tail queries.

**Common mistakes**

- Blocking CSS or JavaScript in `robots.txt`, or using JavaScript-only navigation that Google cannot follow.
- Assuming that submitting a URL guarantees indexing, or expecting immediate results before discovery and ranking can take effect.

### 3. Creating helpful, reliable, people-first content

Google's automated ranking systems are designed to prioritize helpful, reliable information that is created to benefit people, not content that is created to manipulate search engine rankings. This concept is the heart of modern SEO at Google. If you get it right, most other details become much easier.

#### What "people-first" means

People-first content is content created primarily for people, not to manipulate search engine rankings. It answers real questions, solves real problems, and provides a satisfying experience. Search engine-first content, by contrast, is created mainly to attract visits from search engines. It may be mass-produced, lightly summarize other sources, chase trending topics without expertise, or promise answers to questions that have no confirmed answer.

Google does not oppose SEO. SEO is a helpful activity when it is applied to people-first content. Good SEO helps search engines discover and understand valuable content. Bad SEO tries to make low-value content rank well.

#### Self-assessing content quality

Before publishing or updating a page, ask the following questions. They are grouped into content and quality questions and expertise questions.

- Does the content provide original information, reporting, research, or analysis? A page that merely repeats what is already available elsewhere adds little value. A page that brings new data, original research, a tested method, or a personal experience provides more.

- Does the content provide a substantial, complete, or comprehensive description of the topic? A thin page that touches on a topic without fully addressing it is less likely to succeed than a page that covers the topic in depth.

- Does the content provide insightful analysis or interesting information that is beyond the obvious? Surface-level tips that anyone could write are less valuable than insights drawn from real experience or deep expertise.

- If the content draws on other sources, does it avoid simply copying or rewriting those sources, and instead provide substantial additional value and originality? Citing sources is good; copying them is not.

- Does the main heading or page title provide a descriptive, helpful summary of the content? Titles should accurately describe what is on the page and should avoid exaggeration or shock.

- Is this the sort of page you would want to bookmark, share with a friend, or recommend? If you would not share it, it may not be people-first.

- Would you expect to see this content in or referenced by a printed magazine, encyclopedia, or book? This is a useful sanity check for quality and authority.

- Does the content present information in a way that makes you want to trust it? Clear sourcing, evidence of expertise, background about the author or site, and links to an author page or About page all help.

- Is the content written or reviewed by an expert or enthusiast who demonstrably knows the topic well? For Your Money or Your Life topics, such as health, finance, or safety, strong expertise signals are especially important.

- Does the content have any easily-verified factual errors? Even one obvious error can damage trust.

#### E-E-A-T and "Who, How, and Why"

E-E-A-T stands for Experience, Expertise, Authoritativeness, and Trustworthiness. It is not a single ranking factor. Instead, Google's systems use many factors to identify content that demonstrates these qualities. Trust is the most important of the four. Content does not need to demonstrate all of them, but it should demonstrate enough to earn trust for the topic.

The "Who, How, and Why" framework is a practical way to evaluate content:

- **Who created the content?** It should be self-evident who authored the content. Use bylines where readers would expect them, and link bylines to author pages that provide background and expertise. This helps people intuitively understand the E-E-A-T of the page.

- **How was the content created?** It is helpful to explain how the content was produced. For product reviews, this might include the number of products tested, the test results, and how the tests were conducted, with photographs as evidence. For AI-generated or AI-assisted content, disclose the use of automation when it would be reasonably expected and explain why it was useful.

- **Why was the content created?** The primary reason should be to help people. If the main reason is to attract search engine visits or to manipulate rankings, the content is not aligned with what Google's systems seek to reward.

#### Page experience

Google's core ranking systems look to reward content that provides a good overall page experience. This does not mean optimizing one or two metrics and ignoring the rest. It means providing a fast, mobile-friendly, secure page that is easy to use and that does not bury the main content under distracting ads or intrusive interstitials.

**Concrete example**

A financial blog writes an article about choosing a low-cost index fund. The author is a certified financial planner with a clear byline and bio. The article explains the author's own research methodology, links to authoritative sources, and updates the data quarterly. The page uses a descriptive `<title>`, clear headings, and no misleading claims. Because the content is original, reliable, and people-first, it is more likely to perform well for related queries.

**Common mistakes**

- Writing content mainly to rank for many topics, or using extensive automation without adding value.
- Changing dates without real updates, or adding or removing content only to seem "fresh." This does not work.

### 4. Optimization for generative AI in Search

Generative AI features in Google Search, such as AI Overviews and AI Mode, rely on the same core Search ranking and quality systems as the rest of Google Search. This means the foundational practices described in this skill remain relevant. However, the way generative AI assembles and presents answers creates a few additional priorities and myths worth addressing.

#### How generative AI features use web content

Two key techniques are worth understanding:

- **Retrieval-augmented generation (RAG)**, also known as grounding, improves the quality, accuracy, and freshness of AI responses. It relies on Google's core Search ranking systems to retrieve relevant, up-to-date web pages from the Search index. The systems then review specific information from those pages to generate a reliable response and show prominent, clickable links to the sources.

- **Query fan-out** is a set of concurrent, related queries generated by the model to request more information and fetch additional relevant search results. For example, a query about fixing a lawn full of weeds might trigger fan-out queries about herbicides, removing weeds without chemicals, and preventing weeds. This means a single well-structured, comprehensive page can serve many related questions.

#### What to do

The same principles that help in Google Search overall also help in generative AI features.

- **Create valuable, non-commodity content.** Commodity content is based on common knowledge that could come from anyone, such as "7 Tips for First-Time Homebuyers." Non-commodity content provides a unique expert or experienced take, such as "Why We Waived the Inspection & Saved Money: A Look Inside the Sewer Line." First-hand reviews, original research, and unique perspectives stand out.

- **Organize content for human readers.** Use paragraphs, sections, and clear headings. Write naturally and make the content easy to follow. People-first organization also helps AI systems understand the structure of your content.

- **Add high-quality images and video.** Generative AI features can bring in images and videos, so strong visual content creates additional opportunities for your site to appear.

- **Build and maintain a clear technical structure.** Make sure your content is crawlable, follows JavaScript SEO best practices, reduces duplicate content, and provides a good page experience across devices.

- **Optimize local business and ecommerce details where relevant.** Use [Merchant Center](https://merchants.google.com/?hl=en) and [Google Business Profiles](https://business.google.com/?hl=en) to help your products, services, and business information appear in AI responses and other Google Search results.

- **Monitor visibility.** Use the Generative AI performance report in Search Console to understand how your content is appearing in generative AI features.

#### What not to do

- Do not mass-produce pages with AI without adding value. This can violate the [scaled content abuse](https://developers.google.com/search/docs/essentials/spam-policies?hl=en#scaled-content) spam policy.
- Do not copy or rewrite content already available elsewhere.
- Do not chase every fan-out query by creating a separate page for each variation. A high quantity of pages does not make a site higher quality.
- Do not invest in "AEO" or "GEO" tools that promise to optimize for AI answers without proof. From Google's perspective, optimizing for generative AI search is still SEO, and the same best practices apply.

#### Myths to ignore

Several common claims about generative AI search are not supported by how Google works.

- **LLMs.txt files and other "special" markup.** You do not need to create new machine-readable files, AI text files, or special markup to appear in Google Search. Google Search does not use `llms.txt`. Creating such files for other services is fine, but it will neither help nor harm your Google visibility.

- **"Chunking" content into tiny pieces.** There is no requirement to break content into small chunks for AI to understand it. Google can understand the nuance of multiple topics on a page and show the relevant piece to users. The right page length is whatever serves your audience.

- **Rewriting content just for AI systems.** You do not need to write in a special way for generative AI. Google's systems understand synonyms and general meaning, so you do not need to capture every long-tail keyword variation.

- **Seeking inauthentic mentions.** Generative AI features can show what is being said about products and services across the web, but seeking fake or inauthentic mentions is not helpful. Google's spam systems are designed to detect and block such behavior.

- **Overfocusing on structured data.** Structured data is not required for generative AI search, and there is no special schema.org markup you need to add. Continue using it as part of your overall SEO strategy to be eligible for rich results.

#### Generative AI usage guidelines

If you use generative AI to create content on your site, follow these guidelines.

- Use AI as a research and drafting aid, not as a replacement for original value. AI can help structure original content, but the final page should include human review, fact-checking, and editing.

- Focus on accuracy, quality, and relevance for all automatically generated content. This includes `<title>` elements, meta descriptions, structured data, and image `alt` text.

- Give users context about how content was created. For example, explain how automation was used and add image metadata when it is appropriate for your audience.

- For ecommerce, follow Google Merchant Center policies. AI-generated images must contain metadata with the `DigitalSourceType` `TrainedAlgorithmicMedia` value. AI-generated product data such as titles and descriptions must be specified separately and labeled as AI-generated.

- Confirm that the final content follows the Search Essentials and spam policies. Using AI to produce content primarily to manipulate search rankings is a violation.

**Concrete example**

A software review site writes a detailed guide about project management tools. Instead of summarizing manufacturer descriptions, the reviewer uses each tool for a real project, documents the workflow, includes screenshots, and explains the trade-offs. The page is well-structured, crawlable, and linked from the site's navigation. When users ask generative AI questions about project management tools, this page has a high chance of being cited because it provides a unique, first-hand perspective.

**Common mistakes**

- Publishing AI-generated articles without human review or original value.
- Chasing "GEO" tools or creating thin pages for every query variation, instead of focusing on crawlable, high-quality content.

### 5. Site maintenance and practical decisions

Once a site is on Google, ongoing maintenance helps it perform well over time. Site maintenance is not a one-time task; it involves controlling how Google crawls and indexes the site, helping Google understand the content, following guidelines, and managing the user experience.

#### Controlling how Google crawls and indexes your site

- **Duplicate content.** Understand [canonical pages](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=en) and how Google selects a canonical URL. Having duplicate content is not a spam violation, but it can waste crawl budget and confuse users. Consolidate duplicates with `301` redirects or `<link rel="canonical">` where possible.

- **Resources.** Make sure that images, CSS, JavaScript, and other resources that Google is meant to crawl are accessible. If important resources are blocked, Google may not be able to render the page correctly. Use the URL Inspection tool in Search Console to check how Google sees a page.

- **Robots.txt.** Use `robots.txt` to prevent crawling, not to prevent indexing. `robots.txt` is appropriate for blocking duplicate content, unimportant resources such as small icons, and URLs that change state, such as adding items to a cart. For preventing indexing, use `noindex` or login requirements.

- **Sitemaps.** Submit a sitemap to tell Google which pages are important. Sitemaps are especially useful for large sites, sites with rapidly changing content, and pages that might not be discovered through links alone. Google does not limit crawling to sitemap URLs, but it uses them to prioritize crawling.

- **International or multilingual sites.** Use `hreflang` annotations to tell Google about different language or regional versions of a page. If your site adapts content based on the user's locale, read about how this can affect Google's crawl.

- **Site moves and migrations.** If you move a page permanently, use a `301` redirect. If a move is temporary, use `302`. If you remove a page, return a true `404` or `410` status, not a soft `404` that looks like an error page but returns `200`. For full site moves, implement all redirects and sitemap changes, then tell Google about the move through Search Console.

- **Crawl budget and best practices.** Make your links crawlable. Use `rel="nofollow"` for paid links, links that require login, or untrusted user-submitted content. For very large sites, manage crawl budget by listing the most important or recently updated pages in sitemaps and by using `robots.txt` to hide less important pages.

#### Helping Google understand your site

Put key information in text, not only in images or graphics. While Google can index many file types, text is still the safest way to communicate meaning. If you use non-text content, add [structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data?hl=en) to provide explicit clues about the content. Structured data can also make pages eligible for rich results such as review stars, carousels, and recipe cards.

#### Managing the user experience

A good user experience is a ranking factor. Make your site secure with HTTPS, fast, and mobile-friendly. Google uses a mobile crawler by default for most sites, so mobile usability is essential. Use the [Core Web Vitals report](https://search.google.com/search-console?hl=en) and [PageSpeed Insights](https://pagespeed.web.dev/?hl=en) to identify performance issues. Consider whether intrusive interstitials or distracting ads make it hard for users to reach your main content.

#### Do you need an SEO specialist?

Hiring an SEO specialist can improve visibility, but it also carries risks. A good SEO can help with content and site-structure review, technical advice, content development, keyword research, and online business development campaigns. An irresponsible SEO can damage your site and reputation.

Before hiring, ask useful questions:

- Can the SEO show examples of previous work and share success stories?
- Do they follow the [Google Search Essentials](https://developers.google.com/search/docs/essentials?hl=en)?
- What results do they expect, in what timeframe, and how do they measure success?
- What is their experience in your industry, region, and with international sites?
- How will they communicate changes and recommendations?

Check business references and be wary of unsolicited emails, guaranteed #1 rankings, "special relationships" with Google, or secretive methods. No one can guarantee a top ranking. If an SEO uses a third-party tool, keep in mind that Google does not evaluate or endorse these tools, and they do not have access to Google's internal ranking data.

#### Third-party SEO tools and advice

There are many third-party SEO tools, services, and consultants. Some are helpful; others make unsupported claims or imply that they are "approved" by Google. Google's guidance is to evaluate any external advice against [official Google Search guidance](https://developers.google.com/search/docs?hl=en).

Common third-party offerings include:

- Sitemap generation.
- Indexing directives.
- "SEO-optimized" content generation.
- Ranking improvement advice.
- "AEO" or "GEO" services for AI experiences.

Use these tools if they help your workflow, but verify their claims. No third-party tool has access to Google's internal ranking or AI systems. Google strongly recommends using [Search Console](https://search.google.com/search-console/about?hl=en) as a first-party source of data.

**Concrete example**

An ecommerce site migrates from HTTP to HTTPS and changes its product URL structure. The team sets up `301` redirects from every old URL to the new one, updates the sitemap with the new URLs, and submits the sitemap in Search Console. They also verify that product detail pages return HTTP 200, that `robots.txt` does not block CSS or JavaScript, and that `hreflang` tags are preserved for international product pages. After the move, they monitor indexing and traffic in Search Console and fix any soft `404` errors.

**Common mistakes**

- Using `robots.txt` to prevent indexing, returning soft `404` pages, or blocking render-critical resources.
- Migrating a site without redirects, or believing that a third-party tool can guarantee rankings.

### 6. Search developer guide

The [developer-focused Search guide](https://developers.google.com/search/docs/fundamentals/get-started-developers?hl=en) covers how search fits into the build process. Developers should treat search as a quality requirement from the start, not as an afterthought.

#### What developers should focus on

- Make sure Googlebot can access and render pages. This means using crawlable `<a>` links, building a sitemap, and keeping resources such as CSS and JavaScript accessible.

- Use meaningful HTTP status codes. Return `200` for working pages, `301` or `302` for redirects, `404` or `410` for removed pages, and `500` for server errors. Avoid soft `404` behavior.

- Implement correct `robots`, canonical, and `hreflang` signals. Combining multiple rules can lead to conflicts, so test them carefully.

- Keep content in the DOM. Content added through the CSS `content` property is not part of the DOM and is ignored by Google. Content that requires unsupported plugins, such as Java or Silverlight, is not indexed.

- Test structured data and page experience before launch. Use the [Rich Results Test](https://search.google.com/test/rich-results?hl=en) and [PageSpeed Insights](https://pagespeed.web.dev/?hl=en) to validate markup and performance.

- Keep Google updated when content changes. Submit sitemaps and use the URL Inspection tool to request recrawls when important pages are updated.

**Concrete example**

A team builds a single-page application for a documentation site. They ensure that every major section has its own URL, that navigation uses standard `<a>` elements, and that content is rendered into the DOM before any user interaction. They submit a sitemap with all section URLs and test a sample of pages in the Rich Results Test. As a result, Google can discover, crawl, and index each section independently.

**Common mistakes**

- Relying on JavaScript without verifying rendering, or using `<div>` or `<button>` elements instead of crawlable `<a>` links.
- Returning `200` for "not found" pages, or adding important text through CSS `content` properties.

### 7. SEO starter guide

The [SEO starter guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=en) is designed for beginners, but its principles apply to sites of all sizes. It explains how to help Google find your content, organize your site, create interesting and useful content, and influence how your site looks in Search.

#### Help Google find your content

Most pages are discovered through links. You can also submit a sitemap, especially if your site is large or has pages that are not well linked. Before doing anything, search for your site with the `site:` operator to see whether Google has already indexed it. Use the URL Inspection tool to check whether Google sees the page the same way a user does. If you do not want a page to appear in Search, use the appropriate opt-out method.

#### Organize your site

A logical site structure helps both users and search engines. Use descriptive URLs that include useful words, such as `https://www.example.com/pets/cats.html`, rather than opaque identifiers such as `https://www.example.com/2/6772756D707920636174`. Group topically similar pages in directories, especially if you have many thousands of URLs. Reduce duplicate content by redirecting or canonicalizing alternate versions of the same page.

#### Create interesting and useful content

Compelling, useful content is the single most important influence on search presence. Good content is:

- **Easy to read and well organized**, with natural language, correct spelling and grammar, clear paragraphs, sections, and headings.
- **Unique and original**, based on what you know about the topic, not copied from others.
- **Up to date**, with regular reviews and updates or removal of irrelevant pages.
- **Helpful, reliable, and people-first**, with expert or experienced sources where appropriate.

Think about the words your audience might use. Someone new to a topic may use different terms than an expert. However, you do not need to anticipate every variation; Google's language matching is sophisticated and can understand related queries.

Avoid distracting advertisements and intrusive interstitials that make it difficult for users to read your content.

#### Influence how your site looks in Search

- **Title links.** The title link is the headline of a search result. Google uses the `<title>` element and other headings to generate it. A good title is unique to the page, clear, concise, and accurately describes the content. It may include the site or business name, location, and what the page offers.

- **Snippets.** The snippet is the description shown below the title link. It is usually sourced from the page content, but it may also come from the meta description. A good meta description is short, unique to the page, and summarizes the most relevant points.

- **Images and videos.** Use high-quality images and videos near relevant text. Add descriptive `alt` text to images so that both search engines and users with screen readers can understand them. For videos, use descriptive titles and descriptions and embed videos on dedicated pages with relevant text.

#### Promote your site

Promote new content through social media, community engagement, advertising, word of mouth, and offline materials. Effective promotion leads to faster discovery by interested users and by search engines. Be careful not to overdo it; aggressive promotion can fatigue users and may be perceived as manipulation.

#### Things not to focus on

Several topics generate confusion. Google does not use the keywords meta tag, does not require a specific word count or heading order, does not give special ranking power to keywords in domains or TLDs, and does not penalize duplicate content on your own site (though copying others' content can). PageRank is one of many signals, and E-E-A-T is not a single ranking factor. Subdomains and subdirectories are business decisions, not ranking factors.

**Concrete example**

A local gardening shop creates a guide about growing tomatoes. The URL is `https://www.example.com/guides/growing-tomatoes`, the `<title>` is "Growing Tomatoes: A Beginner's Guide - Example Garden Shop," and the page includes original photography with `alt` text, step-by-step instructions based on the shop's experience, and links to related guides. The shop shares the guide with local gardening groups and links to it from the shop's homepage and newsletter. Over a few weeks, the page begins to appear for queries such as "how to grow tomatoes" and "tomato growing tips."

**Common mistakes**

- Copying descriptions or using vague, duplicate `<title>` elements across many pages.
- Creating pages for every keyword variation, or expecting immediate results. SEO can take weeks or months.

---

## Common patterns

### Pattern 1: Auditing a new page against Search Essentials

1. Confirm the page is publicly accessible and returns HTTP 200. Use Search Console's URL Inspection tool or `curl` to verify.
2. Check that `robots.txt` and any `meta` robots tags allow crawling and indexing. Remember that `robots.txt` blocks crawling, while `noindex` blocks indexing.
3. Verify that the page has a descriptive, unique `<title>` and a clear main heading that accurately describes the content.
4. Review the content for originality and usefulness. Ask whether the page provides value that a user cannot find elsewhere.
5. Check that images have `alt` text, links have descriptive anchor text, and the page is linked from other findable pages.
6. Submit or update the sitemap in Search Console, then request indexing for the URL if it is important.

### Pattern 2: Deciding whether to use AI-generated content

1. Use AI for research, drafting, and structuring, not as the final author.
2. Add original value: personal experience, expert review, original data, or analysis that a generic model could not produce.
3. Fact-check every claim and edit the output for accuracy, clarity, and tone.
4. Disclose automation when it is reasonably expected, especially for product data, product images, or content where readers would ask "how was this created?"
5. Confirm the final content follows the Search Essentials and spam policies, including the scaled content abuse policy.
6. Validate any structured data, `<title>`, and meta description generated with AI before publishing.

### Pattern 3: Fixing a page that is not appearing in Search

1. Search for the page with the `site:` operator to see whether it is indexed at all.
2. If it is not indexed, use the URL Inspection tool to check for crawling or indexing errors.
3. Verify that the page returns HTTP 200, is not blocked by `robots.txt`, and does not have an accidental `noindex` tag.
4. Check that the content is in the DOM and not hidden behind unsupported JavaScript, plugins, or login walls.
5. If the page is indexed but not ranking, evaluate whether the content is relevant, original, and more helpful than competing pages.
6. Improve the content, earn or encourage relevant links, and wait a few weeks for changes to take effect.



---

## Best practices

- Meet the minimum technical requirements before focusing on advanced optimizations. A page that cannot be crawled or indexed will never rank, no matter how good its content is.
- Focus on useful, reliable, people-first content. This is the single most important long-term SEO strategy.
- Keep a clean technical structure with descriptive URLs, an accurate sitemap, a well-maintained `robots.txt`, and correct canonical and `hreflang` signals.
- Make your site secure with HTTPS, fast, and mobile-friendly. Page experience is a ranking factor.
- Use Search Console to monitor performance, indexing, and errors. It is the only first-party source of data from Google Search.
- Be transparent about automation and AI-generated content when users would reasonably expect to know.
- Always verify third-party advice, tools, and services against Google's official guidelines.

---

## Common pitfalls

| Pitfall | Solution |
| --- | --- |
| Thinking Google inclusion costs money. | Appearing on Google is free. Do not pay for "guaranteed inclusion" or "priority submit." |
| Mass-producing AI content without human review. | Add original value, fact-check, and follow the scaled content abuse policy. |
| Copying or rewriting content from other sites. | Create your own content based on real experience, research, or expertise. |
| Ignoring `robots.txt` or `meta` robots rules. | Regularly review what is allowed to crawl and index; use `noindex` for indexing, not `robots.txt`. |
| Hiring SEO help without understanding the risks. | Ask for references, verify official guidance alignment, and never grant full access before you trust the consultant. |
| Chasing "AEO" or "GEO" hacks. | Optimizing for generative AI is still SEO. Focus on non-commodity content and a clear technical structure. |
| Believing in a preferred word count or keyword density. | There is no magical word count. Write naturally and cover the topic adequately. |
| Returning soft `404` pages. | A missing page should return a true `404` or `410` status, not a friendly page with HTTP 200. |

---

## Complete subsections

This skill covers the main concepts above. For a complete, structured list of every page in the *SEO fundamentals* section, see [`references/google-search-central-toc.md`](references/google-search-central-toc.md). It includes:

- Search Essentials (technical requirements, spam policies, key best practices)
- SEO starter guide
- How Google Search works
- Creating helpful, reliable, people-first content
- Generative AI optimization and usage guidelines
- Site maintenance and the Search developer guide
- Hiring SEO specialists and evaluating third-party SEO advice

---

## Examples

### Example 1: Checking a page against Search Essentials

```
User: I wrote a new article. How do I make sure it can appear on Google?
Assistant: First, confirm the page is publicly accessible and returns HTTP 200. Then check that it is not blocked by robots.txt and does not have a noindex meta tag. Make sure the `<title>` and main heading are descriptive and unique, the content provides original value, and images have `alt` text. Finally, make sure the page is linked from other pages on your site and submit or update your sitemap in Search Console.
```

### Example 2: Evaluating AI-generated content

```
User: Can I publish articles created entirely with AI?
Assistant: You can use AI to help create articles, but the final content must provide real value. Use AI for drafting and research, then add original analysis, fact-check every claim, and edit before publishing. Disclose automation when it is reasonably expected, and make sure the content follows the Search Essentials and spam policies. Mass-producing AI pages without added value can violate Google's scaled content abuse policy.
```

### Example 3: Troubleshooting why a page is missing from Search

```
User: My product page has been live for a month but does not show up on Google.
Assistant: Start by using the site: search operator to see if the page is indexed. Then use Search Console's URL Inspection tool to check for crawl or indexing issues. Verify that the page returns HTTP 200, is not blocked by robots.txt, and does not have an accidental noindex tag. Check that key content is visible in the rendered DOM and that the page has descriptive `<title>` and `alt` text. If the page is indexed but not ranking, compare it to competing results and improve the content, user experience, and relevance. Be prepared to wait a few weeks after making changes.
```

---

## References

- [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md) — Extracted English summaries from Google Search Central.
- [`references/google-search-central-toc.md`](references/google-search-central-toc.md) — Complete index of all subsections in this documentation area.
- [Search Essentials](https://developers.google.com/search/docs/essentials?hl=en)
- [Technical requirements](https://developers.google.com/search/docs/essentials/technical?hl=en)
- [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies?hl=en)
- [SEO starter guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=en)
- [How Google Search works](https://developers.google.com/search/docs/fundamentals/how-search-works?hl=en)
- [Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content?hl=en)
- [Optimize for generative AI](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide?hl=en)
- [Generative AI usage guidelines](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content?hl=en)
- [Maintain your site's SEO](https://developers.google.com/search/docs/fundamentals/get-started?hl=en)
- [Do you need an SEO specialist?](https://developers.google.com/search/docs/fundamentals/do-i-need-seo?hl=en)
- [Third-party SEO tools and advice](https://developers.google.com/search/docs/fundamentals/third-party-seo?hl=en)
- [Get started with Search: a developer's guide](https://developers.google.com/search/docs/fundamentals/get-started-developers?hl=en)
