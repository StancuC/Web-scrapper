from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurări opționale pentru Chrome
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')  
chrome_options.add_argument('--disable-software-rasterizer')

# URL de test
produs = 'iphone 16'
url = f"https://www.emag.ro/search/{produs.replace(' ', '+')}"

# Inițializare ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accesează pagina
driver.get(url)
time.sleep(5)  # Așteaptă pentru încărcarea completă a paginii

# Așteaptă ca toate link-urile să fie disponibile
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

# Extrage și afișează link-urile
fisier=open("link.txt","w")

link_elements = driver.find_elements(By.TAG_NAME, "a")
print(f"Număr de link-uri găsite: {len(link_elements)}")
for link in link_elements:
    href = link.get_attribute("href")
    if href:  # Verifică dacă href nu este None
        #print(href)
        fisier.write(href+"\n")

fisier.close()
driver.quit()


#citeste README