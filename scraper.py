from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_product(url):
    options = Options()
    options.add_argument('--headless')  # Run in headless mode (no UI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        title = price = weight = "Not found"

        # Title detection
        for tag in ['h1', 'h2', 'title']:
            elements = driver.find_elements(By.TAG_NAME, tag)
            for el in elements:
                text = el.text.strip()
                if text and len(text) > 5:
                    title = text
                    break
            if title != "Not found":
                break

        # Price detection (exclude discount percentages)
        price_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'price') or contains(text(), '$') or contains(text(), 'Rs')]")
        for el in price_elements:
            text = el.text.strip()
            # Only capture valid price formats (skip percentage or 'discount' text)
            if any(char.isdigit() for char in text) and "%" not in text and "discount" not in text.lower() and len(text) < 30:
                price = text
                break

        # Refined Weight detection (exclude shipping details)
        weight_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'kg') or contains(text(), 'g') or contains(text(), 'Weight')]")
        for el in weight_elements:
            text = el.text.strip()
            # Ignore if it's too long or seems like delivery info
            if ('kg' in text.lower() or 'g' in text.lower()) and len(text) < 40 and 'delivering' not in text.lower():
                weight = text
                break

        return title, price, weight

    except Exception as e:
        print("[ERROR]", e)
        return "Error", "Error", "Error"
    finally:
        driver.quit()
