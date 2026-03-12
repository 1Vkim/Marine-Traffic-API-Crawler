# Building a Simple Selenium Website Crawler (with a Local Demo Site)

This short article walks through a tiny, practical Selenium crawler that visits pages, collects visible text, and saves it to local files. It also includes a sample website you can serve locally to test the crawler end‑to‑end.

## Why Selenium for crawling?

Traditional HTTP libraries are fast and lightweight, but they can’t always render dynamic content. Selenium drives a real browser, so you get the same DOM a user would see. That makes it a good fit for pages that depend on JavaScript.

## What this project includes

- A crawler script: [crawl_and_save.py](crawl_and_save.py)
- A sample website: [sample_site/](sample_site/)
- A helper script to serve the site locally: [start_site.sh](start_site.sh)
- A dependency list: [requirements.txt](requirements.txt)

## How the crawler works

At a high level, the crawler follows these steps:

1. Start at a given URL.
2. Load the page in Chrome via Selenium.
3. Wait for the page body to appear.
4. Extract visible text from the page.
5. Save that text to a local file.
6. Find same‑domain links and repeat until the page limit is reached.

This keeps the scope safe and predictable while still demonstrating how a browser-based crawl works.

## Running the demo

1. **Install dependencies**

   ```
   python -m pip install -r requirements.txt
   ```

2. **Start the sample website**

   ```
   ./start_site.sh
   ```

   The site will be available at:
   - http://localhost:8000/sample_site/index.html

3. **Run the crawler**

   ```
   python crawl_and_save.py http://localhost:8000/sample_site/index.html --max-pages 10 --output-dir crawl_output --headless
   ```

4. **Review output**

   The crawler writes one text file per page to the output directory. Each file begins with the page URL followed by the visible text.

## Key implementation ideas

### 1) Same‑domain filtering

The crawler compares each discovered link’s domain to the start URL’s domain. This prevents accidentally crawling external sites and keeps the demo focused.

### 2) Visible text extraction

The script grabs the `<body>` element’s text. It’s a simple, effective way to capture what a user can read without parsing HTML yourself.

### 3) Stable file naming

To avoid collisions, the output filename is derived from the domain and path, plus a short hash for query strings. This keeps filenames readable and unique.

## Tips and extensions

- **Handle dynamic content**: add waits for specific elements or use explicit waits tailored to each site.
- **Save HTML snapshots**: store `driver.page_source` alongside text for debugging.
- **Use a sitemap**: seed the queue with known URLs to avoid missing sections.
- **Throttle requests**: add delays to be polite and avoid overwhelming servers.

## Final thoughts

This mini project provides a clean, safe starting point for Selenium-based crawling. By combining a local demo site with a focused crawler, you can test the entire flow without touching external websites. From here, you can enhance the crawler with richer extraction logic, better queue management, or site-specific rules.
