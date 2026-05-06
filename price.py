

import requests
from bs4 import BeautifulSoup
import csv

# ---------- scrape 10 books from the website ----------
def scrape_books():
    books = []
    page = 1

    # keep going until we have 10 books
    while len(books) < 10:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)

        # if page doesn't load, stop
        if response.status_code != 200:
            break


        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        # each book is inside <article class="product_pod">
        all_books = soup.select('article.product_pod')

        if not all_books:
            break

        for item in all_books:
            # title is in <h3><a title="...">
            title = item.h3.a['title']
            # price is like "£51.77" but sometimes shows as "Â£51.77"
            price_text = item.find('p', class_='price_color').text
            # FIX: remove both £ and Â, then convert to float
            cleaned = price_text.replace('£', '').replace('Â', '').strip()
            price = float(cleaned)

            books.append({'title': title, 'price_gbp': price})

            if len(books) >= 10:
                break

        page += 1

    return books[:10]

# ---------- get exchange rate from free API ----------
def get_rate(to_currency):
    # API gives rates for GBP (base)
    url = "https://api.exchangerate-api.com/v4/latest/GBP"
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return None
        data = resp.json()
        # example: data['rates']['KES'] is the rate
        rate = data['rates'].get(to_currency)
        return rate
    except:
        return None

# ---------- convert all prices ----------
def convert(books, target, rate):
    for b in books:
        converted = b['price_gbp'] * rate
        b['converted_price'] = round(converted, 2)
        b['currency'] = target
    return books

# ---------- save to CSV file ----------
def save_csv(books, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # write headers
        writer.writerow(['Title', 'Price (GBP)', 'Converted Price', 'Currency'])
        for b in books:
            writer.writerow([b['title'], b['price_gbp'], b['converted_price'], b['currency']])
    print(f"Saved to {filename}")

# ---------- print a simple table ----------
def show_table(books):
    print("\n" + "-"*65)
    print(f"{'Title':<40} {'GBP':<8} {'Converted':<10} {'Curr':<5}")
    print("-"*65)
    for b in books:
        # shorten long titles so table doesn't break
        title = b['title'][:37] + ".." if len(b['title']) > 39 else b['title']
        print(f"{title:<40} {b['price_gbp']:<8.2f} {b['converted_price']:<10.2f} {b['currency']:<5}")
    print("-"*65)

# ---------- main ----------
def main():
    print("=== Price Scraper + Converter ===\n")
    
    # ask user which currency they want
    target = input("Convert GBP to (KES, USD, EUR, etc.): ").upper().strip()
    if target == "":
        target = "KES"

    # scrape
    print("\nScraping 10 books...")
    books = scrape_books()
    if not books:
        print("No books found. Check internet.")
        return
    print(f"Got {len(books)} books.")

    # get exchange rate
    print(f"\nFetching GBP -> {target} rate...")
    rate = get_rate(target)
    if rate is None:
        print("Could not get rate. Try again later.")
        return
    print(f"1 GBP = {rate} {target}")

    # convert
    books = convert(books, target, rate)

    # save to CSV
    filename = f"prices_{target}.csv"
    save_csv(books, filename)

    # show table
    show_table(books)

    print("\nDone!")

if __name__ == "__main__":
    main()