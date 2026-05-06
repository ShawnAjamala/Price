
# Price Scraper + Currency Converter

## What it does

Scrapes book titles and prices from books.toscrape.com, then converts the prices from GBP to any currency you choose.

## How it works

1. **Scraping** – Uses `requests` to download web pages and `BeautifulSoup` to extract book titles and GBP prices from the HTML.
2. **Exchange rate** – Calls a free API (exchangerate-api.com) to get the current rate from GBP to your chosen currency.
3. **Conversion** – Multiplies each price by the exchange rate and rounds to 2 decimal places.
4. **Save** – Writes the results to a CSV file using Python's built-in `csv` module.
5. **Display** – Prints a formatted table in the terminal using simple `print` statements with spacing.

## Files created

- `prices_[CURRENCY].csv` – contains book titles, original GBP price, converted price, and currency code.