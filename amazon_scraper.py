import time
import random
import pickle
import pandas
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import os

#for brand name search
brand = input("Enter Brand Name: ").replace(" ","+")



user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
]

COOKIE_FILE = "amazon_cookies.pkl"


#empty list to store product
product_list = []
# undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument(f"user-agent={random.choice(user_agents)}")

print("Launching browser...")
driver = uc.Chrome(options=options)
driver.get("https://www.amazon.com")


# Load cookies from file if not 
if os.path.exists(COOKIE_FILE):
    try:
        cookies = pickle.load(open(COOKIE_FILE, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        print("Cookies loaded.")
        driver.refresh()
    except Exception as e:
        print("Failed to load cookies:", e)
        driver.quit()
        exit()
else:
    print("No cookies found. Please login manually")
    driver.get("https://www.amazon.com")
    time.sleep(30)  # Wait 30 seconds for manual login
    pickle.dump(driver.get_cookies(), open("amazon_cookies.pkl", "wb"))
    print("Cookies saved successfully")

for page in range(1, 5):
    print(f"Scraping page no. {page}")

    url = f"https://www.amazon.com/s?k={brand}&page={page}"
    driver.get(url)

        #first wait for behave like normal user
    time.sleep(random.uniform(4, 10)) 
        
        #get the page html
    pagehtml = driver.page_source

    soup = BeautifulSoup(pagehtml, "html.parser")
  

        
    products = soup.find_all("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
    prices = [
    price.text.strip() for price in soup.find_all("span", class_="a-offscreen")
    if price.text.strip().startswith("$") and "List:" not in price.text]


    for i in range(min(len(products), len(prices))):
            product_list.append({"Product Name": products[i].text.strip(), "Price": prices[i]})
        

    # Sleep before go to the next page
    time.sleep(random.uniform(3, 6))
driver.quit()
df = pandas.DataFrame(product_list)
df.to_excel("amazon_search_Products.xlsx", index=False)
print("extracted product list and stored in amazon_search_Products.xlsx")



