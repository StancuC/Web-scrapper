import json
import requests
import time
import sys
from bs4 import BeautifulSoup
from os.path import exists
from colors import bcolors


reqTime = 2.5

reqUrl = "https://www.emag.ro/search-by-url?source_id=7&templates%5B%5D=full&is_eab344=false&sort%5Bpopularity_total_orders_v1%5D=desc&listing_display_id=2&page%5Blimit%5D=60&page%5Boffset%5D=0&fields%5Bitems%5D%5Bimage_gallery%5D%5Bfashion%5D%5Blimit%5D=2&fields%5Bitems%5D%5Bimage%5D%5Bresized_images%5D=1&fields%5Bitems%5D%5Bresized_images%5D=200x200,350x350,720x720&fields%5Bitems%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbuying_options%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bflags%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bbundles%5D=1&fields%5Bitems%5D%5Boffer%5D%5Bgifts%5D=1&fields%5Bitems%5D%5Bcharacteristics%5D=listing&fields%5Bquick_filters%5D=1&search_id&search_fraze&search_key&url=";
products = set()


with open('http_proxies.txt', 'r') as f:
    proxies = f.readlines()

with open('useragents.txt', 'r') as f:
    userAgents = f.readlines()
    userAgents = [x.replace('\n', '') for x in userAgents]
    userAgentsLen = len(userAgents)
    userAgentsCounter = 0


currentProxy = proxies[int(sys.argv[1])]

proxyObj = {
   'http': currentProxy,
   'https': currentProxy,
}

def ScrapePages(name, maxPages):
    start_time = time.time()

    global reqUrl
    global products
    global proxyObj
    global userAgents
    global userAgentsLen
    global userAgentsCounter
    global reqTime

    pageNr = 1
    pageTotal = 0
    htmlFound = 0
    skipped = False
    products = set()

    
    
    while htmlFound < 2 and pageNr <= maxPages:
        try:
            headers = {
                    'User-Agent': userAgents[int(sys.argv[1])]
                }
            response = requests.get(reqUrl + (f"/{name}/p{pageNr}/c"), headers=headers)
            
            userAgentsCounter += 1

            if response.headers['Content-Type'] == "application/json":
                products.update(ParseJSON(response.text))
            else:
                if htmlFound == 0:
                    parsed = ParseHTML(response.text)
                    products.update(parsed[0])
                    pageTotal = parsed[1]
                    if int(pageTotal) > 300:
                        print(f"Skipping {bcolors.FAIL}{name}{bcolors.ENDC} beacause of {bcolors.FAIL}{maxPages}{bcolors.ENDC} total pages...")
                        time.sleep(1)
                        skipped = True
                        break
                else:
                    break
                htmlFound += 1

            print(f"Scraped Page {bcolors.OKGREEN}{pageNr}{bcolors.ENDC}/{bcolors.OKGREEN}{maxPages}{bcolors.ENDC} of {bcolors.BOLD}{name}{bcolors.ENDC} successfully")
        except:
            print(f"Failed scraping Page {bcolors.FAIL}{pageNr}{bcolors.ENDC}/{bcolors.FAIL}{maxPages}{bcolors.ENDC} of {bcolors.BOLD}{name}{bcolors.ENDC}")

        pageNr += 1
        time.sleep(reqTime)

    time.sleep(reqTime)

    print("Finished %ss\n" % (round(time.time() - start_time, 2)))

    return [] if skipped else list(products)



#############################
def ParseJSON(jsonText):
    items = json.loads(jsonText)["data"]["items"]
    productList = [x["id"] for x in items]

    return productList


#############################
def ParseHTML(html):
    soup = BeautifulSoup(html, 'html.parser')
    btns = soup.find_all("button", {"class": "add-to-favorites btn"})
    ids = [json.loads(x["data-product"])["productid"] for x in btns]

    pages = soup.find_all("a", {"class": "js-change-page hidden-xs hidden-sm"})
    print(pages)
    num = 0
    if len(pages) > 0:
        num = pages[-1]["data-page"]
        print(f"Pages Num: {bcolors.BOLD}{num}{bcolors.ENDC}")

    return (ids, num)


#############################

hrefsFile = open("allHrefs.json", "r")
allHrefs = json.load(hrefsFile)
hrefsFile.close()

start = int(sys.argv[2])
for i in range(start, len(allHrefs)):
    link = allHrefs[i]
    if exists("storage/%s.json" % link) or  exists("storage/%s.skip" % link):
        continue

    print(f"Scraping {bcolors.BOLD}{link}{bcolors.ENDC} {bcolors.OKGREEN}{i}{bcolors.ENDC}/{bcolors.BOLD}{len(allHrefs)}{bcolors.ENDC}...")
    currentItems = ScrapePages(link, int(sys.argv[3]))
    f = open("storage/%s.json" % link, "w")
    f.write(json.dumps(currentItems))
    f.close()