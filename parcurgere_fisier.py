import web_Scrapper 

fisier_linkuri=open("link.txt","r")

# for link in fisier_linkuri:
#     print(link)
links=[]
links=fisier_linkuri.readlines()

web_Scrapper.produs.replace(" ", "-")
for link in links:
    if link == f"^https://www.emag.ro/telefon-mobil-apple-{web_Scrapper.produs}" :
        print(link)