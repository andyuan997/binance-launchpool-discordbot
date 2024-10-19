# Binance Launchpool Scraper and Discord Notifier

This Python script is designed to scrape the latest Binance Launchpool announcements and send a notification to a specified Discord channel when new announcements are found. The script compares previously scraped announcements with the current ones to detect any new listings.

## Features

- **Web Scraping**: Uses `requests` and `BeautifulSoup` to scrape Binance Launchpool announcements.
- **JSON Parsing**: Extracts the announcement data using regular expressions.
- **Discord Notification**: Sends new announcements to a Discord channel via a webhook.
- **File Persistence**: Stores and retrieves the last scraped articles in a JSON file for comparison.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `BeautifulSoup`
  - `json`
  - `re`
  - `os`

You can install the required libraries using the following command:

```bash
pip install requests beautifulsoup4
