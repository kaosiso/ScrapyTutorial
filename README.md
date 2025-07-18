# ScrapyTutorial

A comprehensive, beginner-friendly walkthrough for building, customizing, and running a Scrapy spider that scrapes book data and stores it (e.g., CSV, database) for learning and experimentation.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Spider Details](#spider-details)
6. [Storage & Pipelines](#storage--pipelines)
7. [Output](#output)
8. [Customization](#customization)
9. [Contributing](#contributing)
10. [License](#license)

## Overview

**ScrapyTutorial** is a personal project designed to consolidate everything learned about [Scrapy](https://docs.scrapy.org/), a Python framework for web scraping and crawling. The repository includes example spiders (focusing on scraping books), data models, pipelines, and comprehensive instructions to help beginners and intermediate users master web scraping in Python.

## Installation

### Requirements

- Python 3.x
- [Scrapy](https://scrapy.org/)

### Steps

```bash
git clone https://github.com/kaosiso/ScrapyTutorial.git
cd ScrapyTutorial

# (Optional) Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install scrapy
```

## Usage

Run the included spider(s) to scrape data:

```bash
cd bookscraper
scrapy crawl books
```

- Replace `books` with the actual spider name defined in your project.
- Sample scraped data will typically be output to the console or to files (e.g., CSV) as configured.

## Project Structure

```text
ScrapyTutorial/
├── scrapy.cfg
├── bookscraper/
│   ├── spiders/
│   │   └── books_spider.py
│   ├── items.py
│   ├── pipelines.py
│   └── settings.py
└── README.md
```

### Key Components

- `spiders/`: Contains spider scripts for scraping data.
- `items.py`: Defines data models (e.g., BookItem).
- `pipelines.py`: Post-processes scraped data (e.g., store in files or databases).
- `settings.py`: Project configuration, throttle, user-agent, etc.

## Spider Details

- **Example Spider**: `books_spider.py`
- **Target**: Book listing website (e.g., [Books to Scrape](http://books.toscrape.com/))
- **Extracted Fields**:
  - Title
  - Price
  - UPC
  - Image URL
  - Product Page URL

- **Features**:
  - Recursive crawling for paginated content
  - Data extraction using CSS/XPath selectors
  - Structured data output

## Storage & Pipelines

### Supported Output

- **CSV file**: Store scraped items in a structured spreadsheet.
- **Database**: Integrate with MySQL, PostgreSQL, or MongoDB (customize pipeline).
- **JSON**: Output as line-delimited JSON (change feed exporter settings).

### Modifying Pipelines

- Edit `pipelines.py` to add new storage backends or extend post-processing.
- Configure `ITEM_PIPELINES` in `settings.py`.

## Output

Typical outputs include:

- `books.csv`: Contains scraped book data.
- `books.json`: Optional, for JSON-formatted output.

Customize filename and format using Scrapy command-line options, e.g.:

```bash
scrapy crawl books -o books.csv
scrapy crawl books -o books.json
```

## Customization

- **Target Different Sites**: Update `start_urls` in spider script.
- **Change Fields**: Modify selectors in the `parse()` method.
- **Pipelines**: Add/modify pipelines in `pipelines.py` for extra processing (cleaning, database storage, etc.).
- **Settings**: Tune concurrency, delays, user-agent strings, or proxies in `settings.py`.
- **New Spiders**: Use
  ```bash
  scrapy genspider name domain.com
  ```
  to scaffold additional spiders.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes
4. Submit a pull request with a clear description

Suggestions for improvements, bugfixes, or new spiders are welcome!

## License

This repository is for educational purposes and learning Scrapy. See the repository for full license details.

*Created as a personal collection for Scrapy learning—a work in progress and open for contribution from the community and fellow learners.*
