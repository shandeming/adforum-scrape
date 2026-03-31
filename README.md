# AdForum Scraper

## Screenshots
Below are screenshots of the scraped pages and the generated CSV preview:

![AdForum landing page](/adforum_landpage.png)
![AdForum main page](/adforum.png)
![Additional view](/adforum2.png)

## Overview
This repository contains two Python scripts that scrape agency information from **AdForum**:

- `adforum.py` – Uses **Playwright** to drive a headless Chromium browser and interact with the site UI.
- `cffi_adforum.py` – Uses **curl_cffi** together with **BeautifulSoup** to fetch JSON data from the site’s API and extract agency details into a CSV file.

Both scripts collect agency name, location, website, contact person, phone number and email (when available) and save the results to `adforum_agencies.csv`.

## Prerequisites
- Python 3.12 (or newer)
- [Poetry](https://python-poetry.org/) or `pip` for dependency management
- Google Chrome/Chromium (required by Playwright)

## Installation
```bash
# Create a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt  # if a requirements file exists
# Or install directly:
pip install playwright curl_cffi beautifulsoup4 pandas

# Install Playwright browsers
playwright install chromium
```

## Usage
### Playwright version (`adforum.py`)
```bash
python adforum.py
```
The script opens a Chromium window, navigates to the search results page, clicks the *Load more* button, and prints the page title. Adjust the script as needed for further data extraction.

### curl_cffi version (`cffi_adforum.py`)
```bash
python cffi_adforum.py
```
The script iterates through the paginated API, gathers agency details, and writes them to `adforum_agencies.csv` in the project root.


## Output
The resulting CSV (`adforum_agencies.csv`) contains the following columns:
- `agency`
- `location`
- `website`
- `contact`
- `phone`
- `email`

Open the file with any spreadsheet editor or load it into pandas for further analysis.

## License
This project is provided as‑is under the MIT License. Feel free to modify and adapt it to your needs.
