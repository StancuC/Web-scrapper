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


#citeste README
