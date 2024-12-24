from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from math import ceil

 # Configurare opțiuni pentru Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rulează fără interfață grafică
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options=chrome_options)

  
# Determinarea nr de pagini in functie de nr total de produse... numarul se regaseste in partea de jos a paginii
def numarPagini(url):
    driver.get(url)
    time.sleep(5)
    try:
        elem= driver.find_element(By.XPATH, '//div[@class="text-center mt-1"]')
        nr_prod=int(''.join(filter(str.isdigit,elem.text)))         #toata treaba cu join(...) preia doar textul cu cifre de acolo care mai apoi este convertit in nr integer
    except Exception as e:
        print(f"Eroare la extragerea unui produs: {e}")
    return ceil(nr_prod/48)            #48 de produse are o pagina completa cu produse pe altex




def scrape_altex_products(url, i):
    # Acceseaza pagina i 
    driver.get(url)
    time.sleep(5)  # Așteaptă să se încarce complet pagina

    products = []
    try:
        # Găsește toate produsele
        product_cards = driver.find_elements(By.CLASS_NAME, 'Products-item')
        for card in product_cards:
            try:
                # Extrage numele produsului
                name = card.find_element(By.CLASS_NAME, 'Product-name').text.strip()

                # Extrage imaginea
                image_url = card.find_element(By.TAG_NAME, 'img').get_attribute('src')

                # Extrage link-ul produsului
                product_url = card.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # Extrage prețul
                price_integer = card.find_element(By.XPATH, './/div[@class="leading-none text-red-brand -tracking-0.48 lg:-tracking-0.56"]/span/span[@class="Price-int leading-none"]').text.strip() # "." - Caută prețul în cadrul cardului curent.
                price_fractional = card.find_element(By.XPATH, './/div[@class="leading-none text-red-brand -tracking-0.48 lg:-tracking-0.56"]/span/sup[@class="inline-block -tracking-0.33"]').text.strip(",") # strip(",") functioneaza ca un filtru si o sa ia doar sirul de caractere fara ","
                price = f"{price_integer},{price_fractional}" #pretul de pe site cu tot cu partea fractionala

                # Adaugă produsul într-o listă
                products.append({
                    'name': name,
                    'price': price,
                    'image_url': image_url,
                    'product_url': product_url
                })
            except Exception as e:
                # Dacă lipsește vreo informație, continuă cu următorul produs
                print(f"Eroare la extragerea unui produs: {e}")
                continue
    except Exception as e:
            print(f"Eroarea pentru pagina {i}: {e}")
    return products

# Preia categoriile de produse din fisierul "produse_altex.txt" si le adauga intr-un vector 
fisier_produse=open("produse_altex.txt","r")
prod_a=[]
prod_a=fisier_produse.readlines()
# Pentru fiecare categorie de produse, determina nr de pagini, facea partea de scraping si salveaza datele sub forma de json... face un json pentru fiecare pagina a categoriei de produse
for produs in prod_a:
    url_init= f"https://www.altex.ro/{produs.strip()}/cpl/filtru/p/1/"
    nr_pagini=numarPagini(url_init)       
    for i in range(1):              #aici ar trebui sa fie nr_pagini
        url=f"https://www.altex.ro/{produs.strip()}/cpl/filtru/p/{i+1}/"
        # Extrage produsele și salvează într-un fișier JSON
        try:
        
            scraped_products = scrape_altex_products(url, i)

        # Scrie datele într-un fișier JSON extern
            with open(f"{produs.strip()}_altex_scraping_pag{i+1}.json", "w", encoding="utf-8") as json_file:
                json.dump(scraped_products, json_file, ensure_ascii=False, indent=4)

            print(f"Datele au fost salvate în fișierul '{produs.strip()}_altex_scraping_pag{i+1}.json'.")

        except Exception as e:
            print(f"Eroare: {e}")

print("Web scraper-ul si-a terminat treaba!")
driver.quit()



