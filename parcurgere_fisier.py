#import web_Scrapper 

fisier_linkuri=open("link.txt","r")

# for link in fisier_linkuri:
#     print(link)
links=[]
links=fisier_linkuri.readlines()

# web_Scrapper.produs.replace(" ", "-")
# for link in links:
#     if link == f"^https://www.emag.ro/telefon-mobil-apple-{web_Scrapper.produs}" :
#         print(link)


url_nou=links[307]
print(url_nou)



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
chrome_options.add_experimental_option("detach", True)

# Inițializare ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accesează pagina
driver.get(url_nou)


xpath = "/html/body/div[4]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[1]/div/div/div[1]/p[2]"
xpath2= "/html/body/div[3]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[1]/div/div/div[1]/p[2]"
try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath2))
    ) 
    print("Element găsit:", element.text)
except Exception as e:
    print("Eroare la găsirea elementului:", e)

#Elementul poate să nu fie prezent imediat după încărcarea paginii. În acest caz, utilizează o așteptare explicită: e ceva legat de DOM
#trebuie asteptat sa se incarce toate elementele in pagina
#tind sa cred ca asta nu functiona la varianta mea, XPATH-ul fiind corect

# pret=driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/section[3]/div/div[1]/div[2]/div/div[2]/div[2]/form[1]/div[1]/div[1]/div[1]/div/div/div[1]/p[2]")
# print(pret.text)





input("Apasă Enter pentru a închide browser-ul...")
driver.quit()

