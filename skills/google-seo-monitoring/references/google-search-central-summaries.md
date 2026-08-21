# Google Search Central Summaries: Monitoring and Debugging

> These are extracted English summaries from the official Google Search Central documentation. They are preserved in English to keep the original source wording. Always check the linked official pages for the latest guidance.

---

## Debugging drops in Google Search traffic

A drop in organic Search traffic can happen for several reasons, and it may not be straightforward to understand what exactly happened to your site. This guide explains how to use the Search Console Performance report and Google Trends to investigate the reasons for the drop in Search traffic and how to address it.

### Main causes for drops in organic Search traffic

To get an idea of what is affecting your Search traffic, look at the main chart in the Performance report and consider the following causes. Also check the Search Console Data Anomalies page to see if the drop might be related to a change in data processing or a logging error.

#### Algorithmic update

Google is always improving how it assesses content and updating its search ranking and serving algorithms accordingly. Core updates and other smaller updates may change how some pages perform in Google Search results. Google posts about notable improvements to its systems on the list of ranking updates page. If you suspect a drop is due to an algorithmic update, review your top pages in Search Console and assess how they were ranking. A small drop in position, for example dropping from position 2 to 4, may just be normal fluctuation. A large drop in position, for example dropping from position 4 to 29, may indicate that you should self-assess your whole website overall to make sure it is helpful, reliable, and people-first.

#### Small drop in position

A small drop in position is a small shift in position in the top results, for example dropping from position 2 to 4 for a search query. In Search Console, you might see a noticeable drop in traffic without a big change in impressions. Small fluctuations can happen at any time, and Google recommends avoiding making radical changes if your page is already performing well.

#### Large drop in position

A large drop in position is a notable drop out of the top results for a wide range of terms, for example dropping from the top 10 results to position 29. In cases like this, self-assess your whole website overall to make sure it is helpful, reliable, and people-first. If you have made changes to your site, it may take time to see an effect. Some changes can take a few days, while others could take several months. There is no guarantee that changes you make will result in a noticeable impact in search results.

#### Technical issues

Technical issues are errors that can prevent Google from crawling, indexing, or serving your pages to users. Examples include server availability, robots.txt fetching, page not found, and others. The issues can be site-wide, for example your website is down, or page-wide, for example a misplaced `noindex` tag. Check the Crawl stats report and Page indexing report to find if there is a corresponding spike in issues detected.

#### Security issues

If your site is affected by a security threat, like malware or phishing, Google may alert users before they reach your site with warnings or interstitial pages, which may decrease Search traffic. Check the Security Issues report to find if Google detected a security threat on your website.

#### Spam issues

Google detects practices that violate Google Search spam policies both through automated systems and, as needed, human review that can result in a manual action. If your site does not comply with the Spam policies for Google web search, your content might rank lower in results or not appear in results at all. If you suspect a drop due to a spam violation, review the spam policies and check the Manual Actions report in Search Console.

#### Seasonality and changing interests

Sometimes changes in user behavior will change the demand for certain queries, either due to a new trend or seasonality throughout the year. This means your traffic may drop as a result of external influences. Find queries that saw a drop in clicks and impressions using the Performance report, then check them on Google Trends to understand if the drop was only for your website or throughout the web.

#### Site moves and migrations

If you change the URLs of existing pages on your site, you may experience ranking fluctuations while Google recrawls and reindexes your site. As a general rule, a medium-sized website can take a few weeks for Google to notice the change; larger sites can take longer. If you see a drop after moving and it is not recovering, check the site move troubleshooting section for common mistakes when migrating a site with URL changes.

### Analyze your Search traffic drop pattern

The best way to understand what happened to your traffic is to look at the main chart in your Search Console Performance report.

- Change the date range to include 16 months. This helps you analyze the traffic drop in context and make sure it is not a drop that happens every year due to a festivity or a trend.
- Compare the drop period to a similar period using the Compare tab. This helps you review what exactly changed.
- Analyze different search types separately using the Search type filter. This helps you understand whether the drop happened in web Search, Google Images, or the Video or News tab.
- Monitor your average position in search results, but do not focus too much on absolute position. Impressions and clicks are ultimately the measure of success.
- Look for patterns in the pages affected. Sort the Pages table by Clicks Difference to find pages that lost the most traffic. If it is a site-wide issue, check the Page indexing report. If the drop only affects a group of pages, use the URL Inspection tool.

### Investigate overall trends in your industry

If you want to go the extra mile, use Google Trends to understand whether the drop is a wider trend or if it is just happening for your site. Changes can be caused by two main factors: changing interests, where people start searching for different queries or use their devices for different purposes, and seasonality, where queries naturally lose or gain volume at certain times of the year.

URL: <https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops?hl=en>

---

## Get started with Search Console

Search Console is a tool from Google that can help anyone with a website to understand how they are performing on Google Search, and what they can do to improve their appearance on search to bring more relevant traffic to their websites. Search Console provides information about how Google crawls, indexes, and serves websites, which can help their owners monitor and optimize their performance in Search.

There is no need to sign in to the tool every day. If new issues are found by Google on your site, you will receive an email from Search Console alerting you. You might want to check your account around once every month, or when you make changes to the site's content, to make sure the data is stable.

### Initial steps

1. Verify site ownership. By doing so, you get access to all of the information Search Console offers.
2. Make sure Google can find and read your pages. In the Page indexing report, you can see all the pages on your website that Google has indexed or tried to index. Review the list and try to fix any errors and warnings.
3. Consider submitting a sitemap to Search Console. Google can discover pages on your site even if you do not submit a sitemap, but submitting one can speed up discovery and let you monitor information related to your sitemap.
4. Monitor your site's performance. The Performance report shows the volume of traffic you get from Google Search, broken down by queries, pages, and countries. For each of those breakdowns, you can see trends for impressions, clicks, and other metrics.

### Useful reports for SEO specialists, digital marketing professionals, and site owners

- Learn if your site has any Google Search manual actions. The Manual Actions report shows any issues, the section of your site affected, and where to learn more about it.
- Temporarily hide pages from Google Search. The Removals tool can quickly remove content on your site from Google Search results for about six months.
- Tell Google about a site migration. The Change of Address tool tells Google about your change and helps migrate your Google Search results from your old site to your new site.
- Review issues with your structured data implementation. The Rich result status reports show what structured data Google could or could not read from your site.

### Useful reports for web developers

- Understand site-wide Search indexing issues. The Page indexing report shows which pages have errors, warnings, or are excluded from Search. It also shows the number of impressions the pages accrued, which helps understand how issues might have affected organic traffic.
- Debug page-level Search indexing issues. The URL Inspection tool provides the current index status of website pages and options to test a live URL, ask Google to crawl a specific page, and view detailed information about the page's loaded resources.
- Find and fix threats affecting your site. The Security Issues report shows warnings when Google finds that a website might have been hacked or used in ways that could potentially harm a visitor or their device.
- Make sure your website provides a great page experience. The Core Web Vitals report shows how pages perform based on real-world usage data.

URL: <https://developers.google.com/search/docs/monitor-debug/search-console-start?hl=en>

---

## Using Search Console and Google Analytics data for SEO

Using Search Console and Google Analytics together can give you a more comprehensive picture of how your audience discovers and experiences your website, which can help you make more informed decisions as you work on your site's SEO. This guide explains how to use Looker Studio to monitor Search Console and Google Analytics metrics, visualize the data together, and resolve discrepancies between the tools.

### About Google Analytics and Search Console

Search Console provides data about how your website is performing in Google Search results, such as impressions, clicks, and the queries that bring people to your site. It focuses on activity that happened before a user arrived at your website from Google Search.

Google Analytics provides data about visitors' interactions with your website, such as the pages they visit, how long they stay, and what actions they take. It also shows you where your audience is coming from, which can help you measure the effectiveness of your traffic channels, like email, referrals, social platforms, paid search, and organic search.

### Comparison of Google Analytics and Search Console data

Comparing Search Console performance data with Google Analytics organic traffic can be particularly helpful when attributing conversions to Google Search traffic. However, these tools use different metrics and systems, so the data will not match completely.

The most comparable metrics are Search Console Clicks and Google Analytics Sessions. A click happens when a person clicks on a link in a Google Search result leading to your website. A session is a period of time during which a user interacts with your website or app. Clicks and sessions are calculated differently, so when you compare the data, you will likely see different numbers.

### Monitor Google organic Search traffic in Looker Studio

Using Looker Studio, you can visualize your site's organic search traffic from both Search Console and Google Analytics in one view. To start monitoring with your own data, you can use the Google organic Search traffic dashboard template.

#### Set up the dashboard

1. Open the dashboard template and click Use my own data.
2. Configure your data sources. Connect to Search Console and choose URL Impression in the Tables panel. Connect to Google Analytics.
3. Continue connecting each chart to its relevant data source.

#### Understanding the dashboard

The dashboard shows Google Analytics and Search Console data side by side. Orange is used for Google Analytics and blue for Search Console. The Google Analytics data is already filtered to include only sessions from `Session source = google` and `Session medium = organic`.

The dashboard includes filters and data controls for property, country, device, and date range. The metrics in the dashboard are:

- Sessions (Google Analytics): a period of time during which a user interacts with your website.
- Engagement rate (Google Analytics): the percentage of sessions that had a key event, lasted longer than 10 seconds, or had 2 or more page views.
- Returning users (Google Analytics): the percentage of users who have initiated at least one previous session and came back.
- Clicks (Search Console): the total number of clicks from Google Search results leading to your site.
- Click-through rate (Search Console): clicks divided by impressions.

The dashboard also includes charts for organic sessions and engagement rate over time, percentage of organic search traffic over time, clicks and CTR over time, top pages and queries by click and CTR, and top countries tables.

### Investigate the data more deeply in Google Analytics and Search Console

The source of truth for Search performance will always be Search Console, while the source of truth for behavior inside your site will be Google Analytics. The dashboard can help you monitor your search traffic, but for debugging and finding solutions you should access each tool directly.

In Google Analytics, the Traffic acquisition report and Landing page report with a filter for google organic are particularly useful.

In Search Console, the Performance reports are the most useful for understanding traffic fluctuations.

### Data discrepancies between Google Analytics and Search Console

When comparing the data between these tools, even the most similar metrics, sessions and clicks, will not match exactly. Small discrepancies are normal. If the difference is considerable, the following reasons may apply:

- Implementation in Google Analytics: the Analytics tag may be missing on some pages or misconfigured.
- Cookies or tracking: if your site asks users to accept tracking and users opt out, that can skew Google Analytics data.
- Timezone: Google Analytics lets you choose a timezone, but Search Console uses Pacific Time.
- Attribution: Google Analytics has attribution models, while Search Console counts every click in Google Search.
- Canonical URLs: Search Console reports only on the Google Search canonical URL, while Google Analytics reports on any URL that includes the tracking code.
- Traffic breakdowns: Search Console breaks down traffic by web, image, video, news, and Discover, which are different in Google Analytics.
- Non-HTML pages: PDFs and other non-HTML pages may be counted in Search Console but not in Google Analytics unless enhanced measurement is enabled.
- Bot traffic: Google Analytics automatically excludes traffic from known bots, while Search Console does not necessarily filter them out.

URL: <https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console?hl=en>

---

## Get started with Google Trends

Google Trends can help you better understand how people find information on Google Search, which can help you to develop your content strategy and refine how you talk to your audience. Google Trends provides a random sample of aggregated, anonymized, and categorized Google and YouTube searches. It lets you analyze the interest a query or specific topic has generated worldwide or in a particular city.

### About Google Trends

Google Trends has two main tools:

- Explore tool: for custom terms and topics, checking regional interest, and seeing related topics over time.
- Trending now tool: for current trends, including an approximate search volume, a timeline, and related news articles.

### Monitor rising trends

You can use the Trending Now page to monitor what has been trending recently, and the Explore page to check rising or top terms and topics for different locations, date ranges, categories, and Google properties.

There are two main approaches to monitoring rising trends:

- General trends: use the Explore tool and leave the search box empty. This shows the top terms and topics trending. You can apply country, date, category, and property filters.
- Specific trends: compile a list of terms you are already interested in and search for them using the Explore tool. This can help you plan products and content.

### Keyword research

Keyword research is the practice of identifying the words and phrases your audience uses to search for information you offer. To identify and analyze your terms' search interest, follow these steps:

1. Visit the Explore tool and add up to five terms to the search box.
2. If you are targeting multiple countries, check the card that shows where your terms are most popular.
3. Check the related topics and related queries cards. Choose Top for the most popular terms and Rising for terms gaining attention.
4. Check if there are related topics and terms in other languages, which can help if you are considering translating your content.

### Create a content calendar

Google Trends can help you not only get ideas on what to write, but also prioritize when to publish. Find seasonal trends in the data and plan ahead to have high-quality content available on your site a little before people are searching for it. Keep the location of your audience in mind, because trends can differ across countries.

### Industry comparisons

Google Trends can help you assess how you are performing in comparison to your industry. If you are experiencing a traffic increase or decrease, try to identify whether it corresponds to a change in overall search activity for the industry or if it is related only to your website. You can also add competitor names to compare brand interest.

### Brand awareness and sentiment

To monitor what people are saying about your brand, enter your business name in the Explore tool and change the time range to the past 30 or 90 days. In the related search terms section, go through both the Rising and Top terms, and make sure to paginate using the arrows below the table. You can download this data regularly to monitor how sentiment around your brand is changing over time.

URL: <https://developers.google.com/search/docs/monitor-debug/trends-start?hl=en>

---

## Overview of Google search operators

Google Search supports several search operators that you can use to refine or target your searches. The following search operators may also be useful for debugging your website. For example, the `site:` search operator may be useful to monitor comment spam on your website, and the image search `imagesize:` operator may be helpful to find images on your site that are small.

Because search operators are bound by indexing and retrieval limits, the URL Inspection tool in Search Console is more reliable for debugging purposes.

The following search operators can be used to inspect different aspects of your pages in Search:

- `filetype:`: find search results in a specific file type, for example `filetype:rtf galway`.
- `imagesize:`: find pages that contain images of a specific dimension in Google Images, for example `imagesize:1200x800`.
- `site:`: find search results from a particular domain, URL, or URL prefix, for example `site:example.com/products`.
- `src:`: find pages that reference a particular image URL in the `src` attribute, for example `src:https://www.example.com/images/peanut-butter.png`.

URL: <https://developers.google.com/search/docs/monitor-debug/search-operators?hl=en>

---

## `site:` search operator

A `site:` query is a search operator that allows you to request search results from the particular domain, URL, or URL prefix specified in the operator. For example, `site:example.com` shows results only from the `example.com` domain, including `www.example.com` and `recipes.example.com`. The `site:` search operator is available in all Google Search properties.

If a URL is indexed in Google, it can show up in search results for `site:` queries that are related to the URL, but it is not guaranteed. If a URL does not show in a `site:` query, use the URL Inspection tool to make sure the URL can be indexed and to submit the URL to indexing. Also double-check the query is correct; `site:https://www.example.com` does not return the same results as `site:https://example.com/`.

### Uses for site owners

- `site:example.com` returns a list of indexed and serving URLs. The list is not always exhaustive, and bigger sites should not expect to see all their URLs in the results. A more specific prefix may yield more results than broader prefixes.
- `site:https://example.com/recipes/tsukemen.html` may help you understand whether a specific URL is indexed and served.
- `site:example.com viagra casino` helps with identifying and monitoring spam problems on your site.
- `site:https://example.com/ lemon` shows which URLs on the site can show up for the term `lemon`.
- `site:https://example.com/recipes/tsukemen.html lemon` shows whether the specific URL is indexed for the term `lemon`.

### Limitations of the `site:` operator

The `site:` operator was designed primarily for search users, so it has restrictions that site owners might find limiting. It does not necessarily return all the URLs that are indexed under a prefix. A `site:` operator without a query, for example `site:example.com`, does not rank results. It will generally show the shortest URL for the prefix at the top, but the other results are relatively random.

URL: <https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site?hl=en>

---

## Google Images search operators

Similarly to web search, Google Images supports dedicated search operators, namely `src:` and `imagesize:`. These operators only work on Google Images; they have no effect on other Google properties.

### `src:` search operator

The `src:` search operator returns pages that reference the image URL in the `src` attribute that is provided in the operator. For example: `src:https://example.com/media/carrot.jpg`.

The operator returns pages from any domain, not just the domain of the URL specified in the operator. This may be helpful to learn which images you are hosting on your site are hotlinked by other sites.

### `imagesize:` search operator

The `imagesize:` search operator returns images of the dimension specified in the operator. You must specify the dimension in `width x height` format. For example: `imagesize:1500x1000`.

This operator can be helpful in conjunction with `src:` and `site:`. For example, you can find an image of a certain size that was indexed on your site: `src:https://example.com/media/carrot.jpg imagesize:500x1200`. Using `imagesize:` with the `site:` operator, you can find images of the exact size: `site:https://example.com/ imagesize:500x1200`.

### Limitations of image search operators

Because image search operators are bound by indexing and retrieval limits, you might not see all of the results that may appear for a standard search query.

URL: <https://developers.google.com/search/docs/monitor-debug/search-operators/image-search?hl=en>

---

## Preventing and monitoring abuse on your site

The following topics describe how you can prevent and monitor abuse on your site:

- Prevent user-generated spam on your site or platform.
- Malware and unwanted software.
- Prevent a malware infection.
- Social engineering, phishing, and deceptive sites.
- Google Safe Browsing Repeat Offenders Policy.

URL: <https://developers.google.com/search/docs/monitor-debug/security?hl=en>

---

## Prevent user-generated spam on your site and platform

Spammers often take advantage of open comment forms and other user generated content inputs and generate spammy content on an unsuspecting victim site. Hosting platforms may be similarly open to abuse. Spammers may create a large number of sites that violate the spam policies and add little or no value to the web.

Preventing abuse on your platform or site is usually not hard. Even simple deterrents, such as an unusual challenge users have to complete before interacting with your property, may discourage spammers.

### Tell users that you do not allow spam

Publish a clear abuse policy and communicate it to your users, for example during the sign-up process. Allow trusted users to report content on your property that they consider spammy.

### Identify spammy accounts

Keep a record of signups and other user interactions and try to identify typical spam patterns, such as:

- Form completion time.
- Number of requests sent from the same IP address range.
- User agents used during registration.
- Usernames and other values submitted with the registration form.

These signals may help you create a user reputation system. Since many comment spammers want their content in search engines, consider adding a `noindex` robots meta tag on posts from new users without reputation. After they gain reputation, allow their content to be indexed. Since spammers are often motivated by leaving a link to their site, consider adding `nofollow` or `ugc` rel attributes to links in untrusted content.

### Use manual approval for suspicious user interactions

Manual approval or moderation for certain interactions can decrease spam by preventing spammers from instantly creating content. Moderation adds overhead, but it is a very effective way of fighting spam.

### Use a blocklist

Once you find a single spammy profile, make it simple to remove any others. If several spammy profiles come from the same IP address, you can add that IP to a permanent ban list. For CMSes like WordPress, plugins such as Akismet can help, and adding the IP to your firewall's deny list can also be effective.

### Block automated account creation

Use reCAPTCHA or similar verification tools on sign-up forms to only allow human submissions and prevent automated scripts from creating accounts.

### Monitor your service for abuse

Monitor your property for spam signals such as redirects, large numbers of ad sections, spam-related keywords, and large sections of encoded JavaScript. The `site:` search operator or Google Alerts can help. Keep an eye on your webserver log files for sudden traffic spikes. Monitor your property for phishing and malware-infected pages, for example using the Google Safe Browsing API.

URL: <https://developers.google.com/search/docs/monitor-debug/prevent-abuse?hl=en>

---

## Malware and unwanted software

Google checks websites to see whether they host software or downloadable executables that negatively affect the user experience. Malware and unwanted software are either downloadable binaries or applications that run on a website and affect site visitors. You can see a list of any suspected files hosted on your site in the Security Issues report.

### What is malware

Malware is any software or mobile app specifically designed to harm a computer, a mobile device, the software it is running, or its users. Malware exhibits malicious behavior that can include installing software without user consent and installing harmful software such as viruses. Website owners sometimes do not realize that their downloadable files are considered malware, so these binaries might be hosted inadvertently.

### What is unwanted software

Unwanted software is an executable file or mobile app that engages in behavior that is deceptive, unexpected, or that negatively affects the user's browsing or computing experience. Examples include software that switches your home page or other browser settings to ones you do not want, or apps that leak private and personal information without proper disclosure.

In the Security Issues report, Malware refers to web-based malware that operates without explicit user action. Harmful downloads refers to malware or unwanted software downloads that must be explicitly downloaded by the user.

### Fix the problem

Ensure that your site or application follows the guidelines, then request a review in the Security Issues report. If your mobile application is showing warnings, you can file an appeal.

### Guidelines

Do not misrepresent yourself. Accurately inform users of a software's purpose and intent. Users must be able to download the software intentionally by clicking on an accurate advertisement that clearly informs them of what will be downloaded. Behave as advertised and explicitly explain what browser and system changes will be made. Use endorsements only when authorized. Do not scare the user with false claims about security states or infections.

Software guidelines include using the Chrome Settings API if your program changes Chrome settings, allowing browser and OS dialogues to alert the user, signing your code, not degrading TLS/SSL protections, protecting user data, not breaking the browser's reset functionality, not bypassing UI controls, using extensions to change Chrome functionality, and making uninstallation findable and complete.

Chrome extension guidelines require that all extensions be disclosed and installed in Chrome, hosted in the Chrome Web Store, and installed using the authorized flow. Instruct users on how to remove a Chrome extension.

Mobile application guidelines include informing users of data collection, not impersonating other brands or apps, keeping content within the context of the app, delivering on advertised functionality, and keeping behavior transparent.

URL: <https://developers.google.com/search/docs/monitor-debug/security/malware?hl=en>

---

## Preventing malware infection

The price of freedom from malware is eternal vigilance. This article contains tips and pointers for preventing malware infection. However, it is by no means exhaustive, and Google encourages website owners to conduct more thorough research as well.

### Monitoring a site's health

Many Search Console features can help you identify potential problems:

- Try a Google search with the `site:` operator to see what pages Google has found on your site. Do this periodically to check whether anyone has added unexpected pages.
- The Security Issues report shows any hacked pages that Google has identified on your site and includes instructions for fixing the issue.
- If Google detects malware on your site, a notification appears in the Search Console message panel. Have messages forwarded to your email account to be notified quickly.

### Security checklist

All website owners should:

- Choose strong passwords.
- Pick third-party content providers very carefully.
- Contact your hosting company or publishing platform for support.
- Keep all computers safe with up-to-date software and anti-virus.

Website owners with server access should:

- Check server configuration, including directory permissions, authentication, and encryption.
- Make a backup copy of your `.htaccess` file before making changes.
- Stay up to date with the latest software updates and patches.
- Keep an eye on log files for unfamiliar URL parameters or spikes in traffic to redirect URLs.
- Check your site for common vulnerabilities such as open permissions, XSS, and SQL injection.
- Use secure protocols such as SSH and SFTP instead of telnet or FTP.
- Keep up to date on the latest security news.

URL: <https://developers.google.com/search/docs/monitor-debug/security/prevent-malware?hl=en>

---

## Social engineering (phishing and deceptive sites)

Social engineering is content that tricks visitors into doing something dangerous, such as revealing confidential information or downloading software. If Google detects that your website contains social engineering content, Chrome may display a "Deceptive site ahead" warning. You can check if any pages on your site are suspected of containing social engineering attacks in the Security Issues report.

### What is social engineering

A social engineering attack tricks a web user into doing something dangerous online. Types include:

- Phishing: the site tricks users into revealing personal information by pretending to be a trusted entity, such as a browser, operating system, bank, or government.
- Deceptive content: the content tries to trick users into doing something they would only do for a trusted entity, such as sharing a password, calling tech support, or downloading software. It can also include ads that falsely claim device software is out of date.
- Insufficiently labeled third-party services: a third party operates a site or service on behalf of another entity without making the relationship clear.

Social engineering can also appear in embedded content, usually ads, on otherwise benign websites. This is a policy violation for the host page, whether visible directly or delivered through pop-ups, pop-unders, or other redirection.

### Fixing the problem

1. Verify that you own your site in Search Console and that no new, suspicious owners have been added.
2. Check the Security Issues report to see if your site is listed as containing deceptive content. If sample URLs are provided, visit them from a computer outside your site's network.
3. Remove all deceptive content from your pages.
4. Check the third-party resources included in your site, such as ads, images, and payment services. Refresh pages a few times and test both mobile and desktop views.
5. For any third-party service, make sure the third-party brand is clearly displayed and the relationship with the first party is explicitly stated.
6. Request a security review in the Security Issues report. Reviews can take several days.

URL: <https://developers.google.com/search/docs/monitor-debug/security/social-engineering?hl=en>

---

## Improving SEO with a Search Console bubble chart

Analyzing Search performance data is always a challenge, but even more so when you have plenty of long-tail queries, which are harder to visualize and understand. A bubble chart can help you understand which queries are performing well on your site and which could improve. You can connect your data to Looker Studio to play with the chart settings.

### Interpreting the chart

The bubble chart uses the Site Impression table from the Search Console data source, which includes Search performance data aggregated by site and queries.

There are five customization options:

1. Data control: choose the Search Console property you want to analyze.
2. Time period: choose the date range you want to see. By default, the last 28 days are shown.
3. Query: include or exclude the queries you want to focus on.
4. Country: include or exclude countries.
5. Device: include or exclude device categories.

The axes in the chart are average position (y-axis) and site CTR (x-axis). The y-axis is reversed so position 1 is at the top. A logarithmic scale is used for both axes. Reference lines help highlight values above or below a threshold.

Each bubble represents a single query. The bubble size is the number of clicks, and the bubble color is the device category.

### Analyzing the data

The chart is split into quadrants by the average reference lines:

- Top position, high CTR: these queries are doing well.
- Low position, high CTR: these queries are relevant to users even though they rank lower. Focus on improving SEO for these queries.
- Low position, low CTR: look at bubble sizes to find queries that still drive significant traffic. Related queries are easier to optimize than unrelated ones.
- Top position, low CTR: check whether competitors have rich results, whether the query is a good match for your site, or whether users already found the answer.

### Improving SEO for specific queries

Once you find queries worth the effort, optimize or create pages related to those queries. Create a query filter in Search Console or a pivot table in Looker Studio to see the pages receiving traffic for a specific query. Then ensure titles, descriptions, and alt attributes are descriptive and specific, use headings to create a clear hierarchy, and add relevant structured data.

URL: <https://developers.google.com/search/docs/monitor-debug/bubble-chart-analysis?hl=en>

---

## Google Safe Browsing Repeat Offenders Policy

Google Safe Browsing helps protect users by showing warnings on dangerous sites or dangerous download files. Safe Browsing also notifies website owners when their websites are compromised by malicious actors and helps them diagnose and resolve the problem so that their visitors stay safer.

Sites that repeatedly switch between compliant and noncompliant behavior within a short window of time will be classified as Repeat Offenders.

When a site is established as a Repeat Offender, the website owner will be notified via email to their registered Search Console email address. Once Safe Browsing has designated a site as a Repeat Offender, the website owner will be unable to request additional reviews via Search Console. Repeat Offender status persists for 30 days, after which the website owner will be able to request a review.

URL: <https://developers.google.com/search/docs/monitor-debug/security/safe-browsing-repeat-offenders?hl=en>
