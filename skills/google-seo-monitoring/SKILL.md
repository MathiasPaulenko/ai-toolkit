---
name: google-seo-monitoring
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Practical guide to Google SEO monitoring and debugging: Search Console, Google Analytics, Google Trends, search operators, traffic drops, security, spam, and malware."
tags: [google-search, search-console, google-analytics, google-trends, monitoring]
trigger: When the user asks about monitoring SEO, Google Search Console, Google Analytics, Google Trends, debugging traffic drops, search operators, security issues, spam, malware, or social engineering on a site.
---

# Google SEO Monitoring and Debugging

## Description

This skill covers the *Monitoring and debugging* section of Google Search Central. It explains how to use Search Console, Google Analytics, Google Trends, and search operators to monitor and debug a site's SEO, plus how to prevent and handle spam, malware, and social engineering.

> The supporting English summaries for this skill are in [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md).

## Usage

### When to invoke

- The user needs to start with Google Search Console or Google Analytics.
- The user reports a traffic drop and wants to debug it.
- The user wants to use Google Trends for content strategy.
- The user asks about search operators for debugging.
- The user needs to prevent or respond to spam, malware, or security issues.
- The user wants to monitor Core Web Vitals, indexing, or search performance.

### Input

- A specific monitoring or debugging question.
- Optional: Search Console data, analytics reports, or a site URL.

### Output

- A structured answer with direct links to the relevant Google Search Central pages.
- Step-by-step debugging or monitoring instructions.

---

## Core concepts

### 1. Debugging traffic drops

A drop in organic Search traffic can happen for several reasons, and it may not be straightforward to understand what happened. This section explains how to use the Search Console Performance report and Google Trends to investigate the reasons for a drop and how to address it.

**Why this matters**

Traffic is the main bridge between your content and your audience. A sudden or sustained drop can mean lost revenue, leads, or visibility. Diagnosing it quickly prevents wasted effort and helps you fix the right thing rather than guessing.

#### Main causes of a traffic drop

| Cause | What to look for |
| --- | --- |
| Algorithmic update | A broad change across many queries around the time of a known ranking update. |
| Small ranking drop | A shift in the top results, for example from position 2 to 4. Impressions may be stable while clicks fall. |
| Large ranking drop | A notable drop out of the top results for a wide range of terms, for example from position 4 to 29. |
| Technical issues | Crawl errors, server availability problems, a misplaced `<meta name="robots" content="noindex">`, or failed robots.txt fetches. |
| Security issues | Malware, phishing, or other security threats detected by Google. |
| Spam issues | Manual actions or automated detection of scaled content, link spam, or other violations of spam policies. |
| Seasonality or changing interests | Recurring yearly patterns or new trends that reduce demand for certain queries. |
| Site moves or migrations | URL or hosting changes that cause ranking fluctuations while Google recrawls and reindexes the site. |

#### Steps to diagnose a traffic drop

1. Open the **Performance** report in Search Console and change the date range to **Last 16 months**. This puts the drop in context and shows whether the same dip happens every year due to a festivity or trend.
2. Use the **Compare** tab to compare the drop period to a similar period, either the previous 3 months or the same 3 months last year. Click through the query, page, country, device, and search appearance tabs to find where the change is concentrated.
3. Check the **Search Console Data Anomalies page** and the **list of ranking updates** to see if the timing aligns with a known algorithmic change or a data processing issue.
4. Analyze the pattern of the drop. If both **impressions and clicks dropped**, investigate algorithmic, technical, security, spam, or migration issues. If **impressions are stable but clicks dropped**, your `<title>`, meta description, or snippet may not be compelling, or a competitor may have a richer result.
5. Review the **Pages** table below the chart and sort by **Clicks Difference** to find pages that lost the most traffic. If the drop is site-wide, check the **Page indexing report**. If it affects a group of pages, inspect individual URLs with the **URL Inspection tool**.
6. Use the **Crawl stats report** and **Page indexing report** to find spikes in issues that could explain a technical cause.
7. Check the **Security Issues** and **Manual Actions** reports to rule out malware, social engineering, or spam penalties.
8. Use Google Trends to test whether the drop is due to changing interests or seasonality. Filter the Performance report to one query at a time, then check the same query in Trends to see if the drop is web-wide or only on your site.

**Common mistakes**

- Blaming an algorithm update before checking technical and security data.
- Making radical changes for a small position fluctuation, especially if the page is already performing well.
- Ignoring the Search Console Data Anomalies page and assuming the drop is real.
- Looking only at the total line on the chart and not segmenting by query, page, or search type.

---

### 2. Getting started with Search Console

Search Console is a tool from Google that helps anyone with a website understand how they are performing on Google Search and what they can do to improve their appearance on search to bring more relevant traffic to their site.

**Why this matters**

Search Console provides information about how Google crawls, indexes, and serves your site. Without it, you are flying blind on indexing errors, security issues, and search performance. It also alerts you by email when Google finds new issues, so you do not have to check every day.

#### Initial setup steps

1. **Verify site ownership** to access all the information Search Console makes available. Google offers several verification methods, including DNS records, HTML files, Google Analytics, and Google Tag Manager.
2. **Make sure Google can find and read your pages** by reviewing the **Page indexing** report. This report shows all the pages Google has indexed or tried to index, along with errors and warnings.
3. **Submit a sitemap** through the **Sitemaps report**. Google can discover pages without a sitemap, but submitting one can speed up discovery and lets you monitor its status.
4. **Monitor your site's performance** in the **Performance** report, which shows how much traffic you get from Google Search broken down by queries, pages, and countries.

#### Useful reports

| Report | What it tells you |
| --- | --- |
| Performance | Impressions, clicks, average position, click-through rate, and breakdowns by query, page, country, device, and search appearance. |
| Page indexing | Which pages are indexed, excluded, or have errors and warnings. |
| Sitemaps | The status of submitted sitemaps and any errors in them. |
| Core Web Vitals | How pages perform based on real-world usage data. |
| Security Issues | Warnings about malware, hacked content, or social engineering. |
| Manual Actions | Any manual penalties issued against the site. |
| Rich result status | Errors and warnings for structured data implementation. |
| URL Inspection | The current index status of a specific URL and a live test option. |

#### Reports for different roles

For SEO specialists, digital marketers, and site administrators, the most useful reports include **Manual Actions**, the **Removals tool**, the **Change of Address tool**, and the **Rich result status reports**.

For web developers, the most useful reports include the **Page indexing** report for site-wide indexing issues, the **URL Inspection tool** for page-level debugging, the **Security Issues** report for threats, and the **Core Web Vitals** report for page experience data.

**Common mistakes**

- Verifying only one property variant and missing data for `http` vs `https` or `www` vs non-`www`.
- Checking Search Console only during a crisis instead of reviewing it regularly.
- Not submitting a sitemap or not keeping it up to date.
- Ignoring the email alerts that Search Console sends.

---

### 3. Using Search Console and Google Analytics together

Using Search Console and Google Analytics together can give you a more comprehensive picture of how your audience discovers and experiences your website.

**Why this matters**

Search Console focuses on activity that happened before a user arrived at your site from Google Search. Google Analytics focuses on what visitors do once they are on your site. Combining the two lets you understand the full journey from query to conversion and helps you make more informed decisions.

#### What each tool measures

| Tool | What it measures |
| --- | --- |
| **Search Console** | Impressions, clicks, queries, and how your site appears in Google Search results. |
| **Google Analytics** | Pages visited, sessions, engagement, conversions, and traffic sources across all channels. |

The two most comparable metrics are **Search Console Clicks** and **Google Analytics Sessions**. A click is a click on a Google Search result leading to your site. A session is a period of time during which a user interacts with your site. Because they are calculated differently, the numbers will not match exactly, but the trends should be similar.

#### How to build a combined Looker Studio dashboard

1. Open the [Google organic Search traffic dashboard template](https://lookerstudio.google.com/reporting/408e669d-07d1-4353-a1dc-94f06bde27ef/page/Hqrp/preview?hl=en) and click **Use my own data**.
2. Connect **Search Console** and choose **URL Impression** in the Tables panel.
3. Connect **Google Analytics**.
4. Continue connecting each chart to its relevant data source. The dashboard uses orange for Google Analytics and blue for Search Console.
5. Apply the same country and device filters to both data sources so the comparison is fair.
6. Choose a date range that fits your analysis. The default is last 28 days, but Search Console data can be delayed by a couple of days.

#### Key metrics in the dashboard

| Metric | What it means |
| --- | --- |
| Sessions (Google Analytics) | The volume of traffic on your website attributed to organic search. |
| Engagement rate (Google Analytics) | The percentage of sessions that had a key event, lasted longer than 10 seconds, or had 2 or more page views. |
| Returning users (Google Analytics) | The percentage of users who have initiated at least one previous session and came back. |
| Clicks (Search Console) | The total number of clicks from Google Search results leading to your site. |
| CTR (Search Console) | Clicks divided by impressions, showing how often users who see your site click through. |

#### Main reasons for a large discrepancy between clicks and sessions

| Reason | Why it happens |
| --- | --- |
| Implementation in Google Analytics | The Analytics tag may be missing on some pages or misconfigured. |
| Cookies or consent | Users who opt out of tracking can skew Google Analytics data. |
| Timezone | Google Analytics lets you choose a timezone, but Search Console uses Pacific Time. |
| Attribution | Google Analytics uses attribution models, while Search Console counts every click. |
| Canonical URLs | Search Console reports on the canonical URL, while Analytics reports on any URL with the tracking code. |
| Traffic breakdowns | Search Console breaks down traffic by web, image, video, news, and Discover, which differ from Google Analytics channels. |
| Non-HTML pages | PDFs and other non-HTML pages may be counted in Search Console but missed in Google Analytics unless enhanced measurement is enabled. |
| Bot traffic | Google Analytics excludes known bots, while Search Console does not necessarily filter them out. |

**Common mistakes**

- Expecting clicks and sessions to be identical.
- Comparing different timezones or date ranges without adjusting.
- Not applying the same country or device filters to both data sources.
- Trying to debug traffic issues in the dashboard instead of going back to each tool for deeper investigation.

---

### 4. Getting started with Google Trends

Google Trends can help you better understand how people find information on Google Search, which can help you develop your content strategy and refine how you talk to your audience.

**Why this matters**

Google Trends provides a random sample of aggregated, anonymized, and categorized Google and YouTube searches. It lets you analyze interest in a query or topic worldwide or down to city-level geography. This helps you anticipate demand, plan content timing, and validate whether a traffic change is specific to your site or part of a wider trend.

#### Two main tools

The **Explore tool** is for custom terms and topics, regional interest, and related topics over time. The **Trending now tool** is for current trends, including an approximate search volume, a timeline, and related news articles.

#### Practical applications

**Monitor rising trends.** Use the Explore tool with the search box empty to see top terms and apply country, date, category, and property filters. Use Trending now to find rising terms and related news for context. If you know a term is rising, consider whether it applies to your industry and target audience before creating content.

**Keyword research.** Visit the Explore tool and add up to five terms. Compare their interest over time, check the regional popularity card, and review related topics and queries. Choose **Top** for the most popular terms and **Rising** for terms that are gaining attention. Focus on terms that are connected to your business and where you have expertise.

**Create a content calendar.** Find seasonal trends in the data so you can publish high-quality content a little before people start searching for it. Keep the location of your audience in mind, because trends can differ across countries.

**Benchmark against your industry.** Use Trends to see whether a traffic increase or decrease for a term corresponds to a change in overall search activity or is only on your site. You can also add competitor names to compare brand interest across regions.

**Analyze brand awareness and sentiment.** Enter your business name in the Explore tool and set the range to the past 30 or 90 days. Review the **Rising** and **Top** related terms to see what people search along with your brand. Download this data regularly to monitor how sentiment changes over time.

**Concrete example**

If you run a cheese store, you can compare interest for Brie, Cheddar, Provolone, Parmesan, and Mozzarella. The chart may show that Parmesan has the highest interest and is growing, Brie is highly seasonal around Thanksgiving and the winter holidays, Mozzarella has sustained interest, and Provolone has very little interest. You can use this to plan inventory and content.

**Common mistakes**

- Writing about a topic just because it is trending, without checking that it fits your business and audience.
- Forgetting to filter by country, category, or property.
- Not distinguishing between a search term and a topic. Topics aggregate across languages and include misspellings, variations, and acronyms.
- Ignoring that you should still check Search Console to see which queries already bring traffic to your site.

---

### 5. Debugging with search operators

Google Search supports several search operators that can help you refine or target your searches. These operators can also be useful for debugging your website, although the URL Inspection tool in Search Console is more reliable for definitive answers.

#### Key search operators

| Operator | Use | Example |
| --- | --- | --- |
| `site:` | Find results from a particular domain, URL, or URL prefix. | `site:example.com` |
| `filetype:` | Find results in a specific file type. | `filetype:rtf galway` |
| `imagesize:` | Find images of a specific dimension in Google Images. | `imagesize:1200x800` |
| `src:` | Find pages that reference a specific image URL in Google Images. | `src:https://example.com/media/carrot.jpg` |

#### Using `site:` for debugging

A `site:` query lets you request search results from a particular domain, URL, or URL prefix. It can help you:

- See which pages from your domain are indexed and serving, with `site:example.com`.
- Check whether a specific URL is indexed, with `site:https://www.example.com/recipes/tsukemen.html`.
- Identify spam problems on your site, with `site:example.com viagra casino`.
- See which URLs can show up for a term, with `site:https://example.com/ lemon`.

Because the `site:` operator was designed for search users, it has important limitations. It does not necessarily return all the URLs that are indexed under a prefix, so do not use it to count indexed pages. A `site:` operator without a query does not rank results; it usually shows the shortest URL for the prefix at the top, but the other results are relatively random. If a URL does not show in a `site:` query, use the URL Inspection tool to check its index status and submit it if needed.

#### Google Images operators

In Google Images, `src:` returns pages that reference the image URL in the `src` attribute. This can help you detect hotlinking. `imagesize:` returns images of the dimension you specify in `width x height` format, such as `imagesize:1500x1000`. You can combine these with `site:`, for example `site:https://example.com/ imagesize:500x1200`, to find images of an exact size that are indexed on your site.

**Common mistakes**

- Assuming that `site:` returns every indexed URL.
- Using a `site:` query without a regular query to judge ranking or relevance.
- Forgetting that `site:https://www.example.com` does not return the same results as `site:https://example.com/`.
- Relying on search operators instead of the URL Inspection tool for page-level index status.

---

### 6. Preventing and monitoring user-generated spam

Spammers often take advantage of open comment forms and other user-generated content inputs to generate spammy content on an unsuspecting victim site. Hosting platforms may be similarly open to abuse, with spammers creating large numbers of sites that add little or no value to the web.

**Why this matters**

User-generated spam can violate Google's spam policies, lead to manual actions, damage your reputation, and pollute your site with low-quality links and content. Preventing it is usually not difficult, and even simple deterrents can discourage spammers.

#### How to prevent user-generated spam

1. **Publish a clear abuse policy.** Tell users that spam is not allowed and give trusted users a way to report spammy content.
2. **Identify spammy accounts.** Keep a record of signups and user interactions and look for patterns such as:
   - Form completion time.
   - Number of requests from the same IP address range.
   - User agents used during signup.
   - Usernames or other values chosen during signup.
3. **Use a reputation system for new users.** Consider adding a `<meta name="robots" content="noindex">` tag to posts from new users who have not yet built a reputation. Once they gain reputation, allow their content to be indexed.
4. **Mark untrusted links.** Add `rel="nofollow"` or `rel="ugc"` to links in untrusted content, because many spammers are motivated by leaving followed links to their sites.
5. **Use manual approval for suspicious interactions.** Moderation adds overhead, but it is one of the most effective ways to stop spam before it goes public.
6. **Use a blocklist.** If you see several spammy profiles coming from the same IP address, add that IP to a ban list. For CMSes like WordPress, plugins such as Akismet can help, and adding the IP to your firewall's deny list can also be effective.
7. **Block automated account creation.** Use reCAPTCHA or similar verification tools on sign-up forms to prevent automated scripts from creating accounts.
8. **Monitor your service for abuse.** Look for spam signals such as suspicious redirects, large numbers of ad sections, spam-related keywords, and large sections of encoded JavaScript. The `site:` operator and Google Alerts can help you detect these problems. Monitor server log files for sudden traffic spikes and use the Google Safe Browsing API to test URLs regularly.

**Common mistakes**

- Allowing followed links in comments or forum posts.
- Letting new user content be indexed immediately without any reputation check.
- Not moderating user interactions.
- Ignoring sudden traffic spikes or new pages found through `site:` searches.

---

### 7. Security: malware and unwanted software

Google checks websites to see whether they host software or downloadable executables that negatively affect the user experience. Malware and unwanted software can appear in the **Security Issues** report in Search Console.

#### What is malware

Malware is any software or mobile app specifically designed to harm a computer, a mobile device, the software it is running, or its users. Malware can install software without user consent or install harmful software such as viruses. Website owners sometimes do not realize that their downloadable files are considered malware, so these binaries might be hosted inadvertently.

#### What is unwanted software

Unwanted software is an executable file or mobile app that engages in behavior that is deceptive, unexpected, or that negatively affects the user's browsing or computing experience. Examples include software that changes your home page or other browser settings without your permission, or apps that leak private information without proper disclosure.

In the Security Issues report, "Malware" refers to web-based malware that operates without explicit user action, while "Harmful downloads" refers to malware or unwanted software downloads that must be explicitly downloaded by the user.

#### How to detect malware or unwanted software

- Review the **Security Issues report** in Search Console for a list of suspected files hosted on your site.
- Search with `site:yourdomain.com` to detect unknown pages or content that you did not create.
- Watch the Search Console message panel for malware notifications and have messages forwarded to your email.
- Use the Google Safe Browsing API to test URLs from your service.

#### Steps if your site is infected

1. Review the **Security Issues report** and identify the suspicious files or pages.
2. Search with `site:yourdomain.com` to find any unexpected content.
3. Remove the malware and any hacked pages. Check `.htaccess` or other access control files, restore from a clean backup, and patch the vulnerability that allowed the infection.
4. Strengthen security: choose strong passwords, enable two-factor authentication, keep software and plugins up to date, control server access, and back up regularly.
5. Request a review in the **Security Issues report** after you have cleaned the site.

#### Guidelines for safe software

To avoid being flagged as unwanted software:

- Accurately inform users of a software's purpose and intent. Ads that lead to downloads must clearly identify the software.
- Behave as advertised. If your program collects data or injects ads, disclose that clearly.
- Explicitly explain what browser and system changes the software will make, and let users approve them.
- Use the Chrome Settings Override API if your program changes Chrome settings, and host extensions in the Chrome Web Store.
- Do not degrade TLS/SSL security, intercept traffic, or collect private data beyond the functionality of the app.
- Make the uninstallation process findable, simple, and non-threatening, and remove all components.
- Sign your code with a valid and verified code signature.

**Common mistakes**

- Hosting downloadable binaries without understanding their behavior.
- Bundling unrelated software without clear disclosure.
- Not requesting a review in Search Console after cleaning an infection.
- Using ads that only say "Download" or "Play" without identifying the software.

---

### 8. Social engineering

Social engineering is content that tricks visitors into doing something dangerous, such as revealing confidential information or downloading software. If Google detects that your website contains social engineering content, Chrome may display a "Deceptive site ahead" warning when visitors try to access it.

#### Types of social engineering

- **Phishing.** The site tricks users into revealing personal information such as passwords, phone numbers, or social security numbers by pretending to be a trusted entity like a browser, operating system, bank, or government.
- **Deceptive content.** The content tries to trick users into doing something they would only do for a trusted entity, such as sharing a password, calling tech support, or downloading software. It can also include ads that falsely claim device software is out of date.
- **Insufficiently labeled third-party services.** A third party operates a site or service on behalf of another entity without making the relationship clear. For example, a donation management site used by a charity must clearly identify that it is a third-party platform acting on behalf of that charity.

Social engineering can also appear in embedded content, such as ads, on otherwise benign websites. This is a policy violation for the host page, whether the deceptive content is visible directly or arrives through pop-ups, pop-unders, or redirects.

#### How to fix social engineering issues

1. Verify that you own your site in Search Console and that no new, suspicious owners have been added.
2. Check the **Security Issues report** to see if your site is listed as containing deceptive content. If sample URLs are provided, visit them from a computer outside your site's network, because attackers may disable their attacks for site owners.
3. Remove all deceptive content from your pages.
4. Review third-party resources such as ads, images, and payment services. Refresh pages a few times to see all ad rotations, and test both mobile and desktop views with the **URL Inspection tool**.
5. Make sure any third-party service clearly displays its own brand and, on pages with first-party branding, explicitly states the relationship between the first and third party.
6. Request a security review in the **Security Issues report** after removing all social engineering content. Reviews can take several days.

**Common mistakes**

- Assuming that a site cannot be hacked or used to host deceptive content.
- Allowing ads that look like page buttons, media player updates, or system warnings.
- Not checking third-party resources or ad rotations.
- Failing to request a review after cleaning the issue.

---

### 9. Bubble chart analysis in Search Console

Analyzing Search performance data is challenging when you have many long-tail queries. A bubble chart can help you understand which queries are performing well and which could be improved.

**Why this matters**

A bubble chart lets you see relationships between multiple metrics and dimensions in one view. By plotting click-through rate, average position, clicks, and device together, you can quickly find queries worth investing in and queries that are not a good fit for your site.

#### How to build the chart

You can connect Search Console to Looker Studio and use the **Site Impression** table as the data source. Set the chart as follows:

- **X-axis:** site click-through rate (CTR).
- **Y-axis:** average position. Reverse the y-axis so that position 1 is at the top.
- **Bubble size:** total number of clicks. Larger bubbles drive more traffic.
- **Bubble color:** device category to spot mobile vs desktop differences.
- **Scale:** use a logarithmic scale for both axes to better understand queries at the extremes.
- **Reference lines:** add average or median reference lines to split the chart into quadrants.

The chart has five data controls: Search Console property, date range, query filter, country filter, and device filter. The default date range is the last 28 days.

#### Interpreting the four quadrants

1. **Top position, high CTR.** These queries are doing well. There is usually little you need to do.
2. **Low position, high CTR.** These queries are relevant to users even though they rank lower than your average query. Improving position could have a big impact. Check whether you have a strong page for the query and add content that better addresses the user need.
3. **Low position, low CTR.** Look at the bubble sizes to find queries that still drive significant traffic. If the query is related to your site, it is a good start that it already appears in Search, so prioritize it. If it is unrelated, consider fine-tuning your content or focusing on other queries.
4. **Top position, low CTR.** These queries might have a low CTR because competitors have rich results, the query is not a good match for your site, or users already found the answer in the snippet. Check the largest bubbles and consider improving titles, descriptions, and structured data.

#### Improving SEO for specific queries

Once you find queries worth optimizing, use Search Console or Looker Studio to see all the pages receiving traffic for that query. Then follow SEO best practices: make `<title>` elements and meta descriptions descriptive and specific, use headings to create a clear hierarchy, and add relevant structured data. You can also use Google Trends and the Google Ads Keyword Planner to find related terms and variations.

**Common mistakes**

- Trying to optimize every low-CTR query without checking whether it is relevant to your site.
- Ignoring device differences that the color dimension reveals.
- Treating the bubble chart as the final answer instead of using it to identify queries to investigate in Search Console.

---

## Complete subsections

This skill covers the main monitoring and debugging workflows. For a complete list of every page in the *Monitoring and debugging* section, see [`references/google-search-central-toc.md`](references/google-search-central-toc.md). It includes:

- Debugging traffic drops
- Getting started with Search Console
- Combining Search Console and Google Analytics data
- Search Console bubble-chart analysis
- Google search operators, including `site:` and image operators
- Preventing and monitoring user-generated spam, malware, and social engineering
- Google Trends

---

## Common patterns

### Pattern: Weekly SEO health check

1. Open the Search Console Performance report and compare the last 7 days to the previous period. Look for significant changes in clicks, impressions, and average position.
2. Check the Page indexing report for new indexing errors or warnings that could prevent pages from appearing in Search.
3. Review the Core Web Vitals report for any regressions in page experience.
4. Check the Security Issues and Manual Actions reports for malware, spam, or social engineering warnings.
5. Note any major site changes, deployments, or migrations that could correlate with traffic changes, and document them for future reference.

### Pattern: Diagnosing a traffic drop

1. Segment the Performance report by query, page, country, device, and search appearance to find where the drop is concentrated.
2. Change the date range to the last 16 months and use the Compare tab to see if the drop matches a seasonal or year-over-year pattern.
3. Check the list of ranking updates and the Data Anomalies page to see if an algorithmic change or data issue is involved.
4. Use the `site:` operator to detect spam or unexpected content that you did not create.
5. Review the Page indexing and Security Issues reports for technical or security problems.
6. Use Google Trends to test whether the drop is due to changing interests or seasonality rather than a problem with your site.

---

## Best practices

1. **Verify and revisit Search Console regularly.** Verification is the gateway to all Search Console data. Once verified, review the Performance, Page indexing, Core Web Vitals, and Security reports at least once a month, and whenever you make significant site changes.

2. **Keep an up-to-date sitemap.** Submitting a sitemap helps Google discover your important pages faster and gives you a Sitemaps report to monitor. Remove outdated URLs and add new sections promptly.

3. **Combine Search Console with Google Analytics and Looker Studio.** Search Console shows what happens before a user reaches your site, while Google Analytics shows what happens after. Use Looker Studio to see both in one view, but remember that clicks and sessions are measured differently.

4. **Investigate traffic drops with data, not assumptions.** Segment the Performance report by query, page, country, device, and search type before concluding that an algorithm update is to blame.

5. **Use Google Trends for planning.** Anticipate rising topics, align seasonal content with demand peaks, and compare your traffic changes to industry-wide trends.

6. **Monitor security continuously.** Respond quickly to malware, spam, or social engineering warnings. Clean the issue thoroughly and request a review in Search Console when you are done.

7. **Document site changes.** Keep a record of technical changes, migrations, and content updates so you can correlate them with traffic variations and resolve issues faster.

## Common pitfalls

| Pitfall | Solution |
| --- | --- |
| Blaming an algorithm update without checking technical data first. | Investigate technical, security, and spam issues before assuming an algorithm change. |
| Ignoring Search Console alerts. | Set up email notifications and review them promptly. |
| Using Google Trends without context. | Complement Trends data with Search Console and your own business knowledge. |
| Underestimating user-generated spam. | Implement validation, moderation, and reputation systems for new users. |
| Not requesting a review after cleaning malware or social engineering. | Use the Security Issues report to request a review once the issue is fixed. |
| Expecting Search Console clicks and Google Analytics sessions to match. | Compare trends, not absolute numbers, and understand the differences in measurement. |
| Using `site:` to count all indexed pages. | Use the Page indexing report and URL Inspection tool for accurate index status. |

---

## Examples

### Example 1: Diagnosing a traffic drop

```
User: My organic traffic dropped 30% last week. What should I check?
Assistant: Start with the Search Console Performance report. Change the date range to the last 16 months, use the Compare tab, and segment by query, page, country, and device. If impressions and clicks both dropped, check the list of ranking updates, the Page indexing report for technical errors, and the Security Issues report for malware or social engineering. If impressions are stable but clicks dropped, review your <title> elements and meta descriptions. Use Google Trends to rule out seasonality.
```

### Example 2: Setting up monitoring

```
User: How should I monitor my site's SEO on a regular basis?
Assistant: Verify the site in Search Console, submit a sitemap, and review the Performance, Page indexing, Core Web Vitals, and Security reports weekly or monthly. Connect Search Console and Google Analytics in Looker Studio to see both search and on-site behavior. Set up email alerts in Search Console and use Google Trends for content ideas.
```

### Example 3: Spotting an opportunity with a bubble chart

```
User: I have thousands of long-tail queries in Search Console. How do I decide which ones to optimize?
Assistant: Build a bubble chart in Looker Studio using the Search Console Site Impression data source. Put CTR on the x-axis, average position on the reversed y-axis, clicks on bubble size, and device on color. Focus on the quadrant with low position but high CTR first: these queries are already relevant to users, and a position improvement could have a big impact. Then check the pages receiving traffic for those queries and improve their <title>, headings, and structured data.
```

---

## References

- [`references/google-search-central-summaries.md`](references/google-search-central-summaries.md) — Extracted English summaries from Google Search Central.
- [`references/google-search-central-toc.md`](references/google-search-central-toc.md) — Complete index of all subsections in this documentation area.
- [Debugging traffic drops](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops?hl=en)
- [Getting started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start?hl=en)
- [Search Console and Google Analytics](https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console?hl=en)
- [Getting started with Google Trends](https://developers.google.com/search/docs/monitor-debug/trends-start?hl=en)
- [Search operators overview](https://developers.google.com/search/docs/monitor-debug/search-operators?hl=en)
- [`site:` search operator](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site?hl=en)
- [Google Images search operators](https://developers.google.com/search/docs/monitor-debug/search-operators/image-search?hl=en)
- [Prevent and monitor abuse](https://developers.google.com/search/docs/monitor-debug/security?hl=en)
- [Prevent user-generated spam](https://developers.google.com/search/docs/monitor-debug/prevent-abuse?hl=en)
- [Malware and unwanted software](https://developers.google.com/search/docs/monitor-debug/security/malware?hl=en)
- [Avoid malware infection](https://developers.google.com/search/docs/monitor-debug/security/prevent-malware?hl=en)
- [Social engineering](https://developers.google.com/search/docs/monitor-debug/security/social-engineering?hl=en)
- [Bubble chart analysis](https://developers.google.com/search/docs/monitor-debug/bubble-chart-analysis?hl=en)
