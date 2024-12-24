import os
import json
import requests
import time
from pathlib import Path

STORAGE_DIR = "storage"
OUTPUT_FILE = "product_details.json"
REQ_TIME = 2.5

paths = sorted(Path(STORAGE_DIR).iterdir(), key=os.path.getmtime)
paths = [x.__str__() for x in paths]

products = {}

def fetch_product_details(product_id):
    """Fetch product details from the API."""
    global products
    url = f"https://sapi.emag.ro/recommendations/compared-similar-products?source_id=7&identifier={product_id}&page_type=product"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            if "data" in data and "product_collection" in data["data"] and len(data["data"]["product_collection"]) > 0:
                product_data = data["data"]["product_collection"][0]

                products[product_id] = {
                    'id': product_data.get("id", "N/A"),
                    'name': product_data.get("name", "N/A"),
                    'price': product_data.get("offer", {}).get("price", {}).get("current", "N/A"),
                    'picture': product_data.get("image", {}).get("original", "N/A"),
                    'url': product_data.get("quick_uri", "N/A")
                }

                print(products[product_id])
                return products[product_id]
            else:
                print(f"No product data found for ID: {product_id}")
        else:
            print(f"Request failed for ID {product_id} with status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")

    return None

if __name__ == "__main__":
    all_product_details = []

    for path in paths:
        with open(path, 'r') as file:
            try:
                product_ids = json.load(file)
                print(f"Processing {len(product_ids)} products from file: {os.path.basename(path)}")
            except json.JSONDecodeError as e:
                print(f"Error reading file {path}: {e}")
                continue

            for product_id in product_ids:
                print(f"Fetching details for product ID: {product_id}")
                product_details = fetch_product_details(product_id)
                if product_details:
                    all_product_details.append(product_details)
                time.sleep(REQ_TIME)

    with open(OUTPUT_FILE, "w") as outfile:
        json.dump(all_product_details, outfile, indent=4)

    print(f"Finished! Product details saved to {OUTPUT_FILE}")
