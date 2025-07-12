from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime

def scrape_alibaba_rfq():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=False to see it live
        page = browser.new_page()
        page.goto("https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y")

        page.wait_for_timeout(5000)  # Wait for full load

        # Scroll to trigger loading
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

        # Try to collect visible RFQ cards
        titles = page.locator(".title span").all_inner_texts()
        buyers = page.locator(".user-name span").all_inner_texts()

        print("Found titles:", len(titles))
        print("Found buyers:", len(buyers))

        records = []
        for i in range(min(len(titles), len(buyers))):
            records.append({
                "Title": titles[i],
                "Buyer Name": buyers[i],
                "Inquiry Date": datetime.today().strftime('%d-%m-%Y'),
                "Scraping Date": datetime.today().strftime('%d-%m-%Y')
            })

        df = pd.DataFrame(records)
        df.to_csv("alibaba_rfq_output_playwright.csv", index=False, encoding="utf-8-sig")
        print("Done. Data saved to 'alibaba_rfq_output_playwright.csv'")
        browser.close()

if __name__ == '__main__':
    scrape_alibaba_rfq()