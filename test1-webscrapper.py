# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# # URL-ul pe care vrei să îl accesezi
# website = 'https://mta.ro/'

# # Creează un obiect Service folosind WebDriver Manager
# service = Service(ChromeDriverManager().install())

# # Inițializează WebDriver-ul cu serviciul configurat
# driver = webdriver.Chrome(service=service)

# # Accesează website-ul
# driver.get(website)


# #buton= driver.find_element_by_xpath('//div[@class="menuTop__text"]')
# #buton.click()


# driver.quit()



# import requests
# from bs4 import BeautifulSoup as BS
# import requests, webbrowser, re, json
# import pprint
# import urllib3

# urllib3.disable_warnings()


#produs=str(input("Introdu produsul pe care il doresti: "))
# produs='iphone 16'
# produs = produs.replace(' ','+')
    
# url=f"https://emag.ro/search/{produs}/"

#print(produs)

# r=requests.get(url,verify=False)
# print(r.status_code)
# webbrowser.open(url)

# for h in r.headers.items():
#     print(h)

# date=BS(r.content,'r.parser')
# print(date.prettify())
# lista_scripturi=[]
# lista_scripturi=date.find_all("script")
# print(lista_scripturi)
# j=json.loads(html.decode())
# pprint.pprint(j)
#print(html)


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  # Dezactivează accelerarea hardware
chrome_options.add_argument('--disable-software-rasterizer')

produs='iphone 16'
produs = produs.replace(' ','+')
    
url=f"https://emag.ro/search/{produs}/"

service = Service(ChromeDriverManager().install())

# Inițializează WebDriver-ul cu serviciul configurat
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get(url)
# Browserul va rămâne deschis până închizi manual fereastra
print("Browserul rămâne deschis. Închide-l manual când termini.")
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Ieșire...")


#element = driver.find_element(By.ID, "passwd-id")

# Închide browserul dacă optezi să închei manual
driver.quit()