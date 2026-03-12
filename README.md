# Selenium Crawler Demo

This workspace contains:
- A simple Selenium crawler script.
- A small sample website to crawl.

## Files
- [crawl_and_save.py](crawl_and_save.py): Selenium crawler that saves visible text to local files.
- [requirements.txt](requirements.txt): Python dependencies.
- [sample_site/](sample_site/): Demo website with a few linked pages.
- [start_site.sh](start_site.sh): Helper script to run a local web server.

## Requirements
- Python 3.9+
- Google Chrome installed
- ChromeDriver available on PATH (matching your Chrome version)
- Selenium installed

Install dependencies:
```
python -m pip install -r requirements.txt
```

## Start the sample website
From the project root:
```
./start_site.sh
```
This starts a local server at:
- http://localhost:8000

Open this URL in a browser to confirm it loads:
- http://localhost:8000/sample_site/index.html

## Run the crawler
Use the local site as the start URL:
```
python crawl_and_save.py http://localhost:8000/sample_site/index.html --max-pages 10 --output-dir crawl_output --headless
```

### How it works
1. The crawler opens the start URL in Chrome.
2. It waits for the page body to load.
3. It extracts visible text from the page and saves it to a local file.
4. It gathers same-domain links and continues until it hits the page limit.

## Output
Saved text files are written to the folder you pass in `--output-dir`.
Each file begins with the URL and then the visible text content.
