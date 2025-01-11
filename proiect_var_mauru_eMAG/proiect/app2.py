import tkinter as tk
import ttkbootstrap as ttk
import requests
from bs4 import BeautifulSoup
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
from math import ceil
from pathlib import Path
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class IntegratedApp:
    def __init__(self):
        self.window = ttk.Window(themename='cosmo')
        self.window.title('Integrated App')
        self.window.geometry('520x480')

        self.search_var = ttk.StringVar()
        self.result_text = None

        self.initialize_gui()

    def initialize_gui(self):
        # Title
        title_label = ttk.Label(master=self.window, text='Introduceți produsul', font='Calibri 24')
        title_label.pack()

        # Input field
        input_field = ttk.Frame(master=self.window)
        input_field.pack()

        search_entry = ttk.Entry(master=input_field, textvariable=self.search_var)
        search_button = ttk.Button(master=input_field, text='Search', command=self.perform_search)
        product_scraper_button = ttk.Button(master=input_field, text='Scrape Products', command=self.scrape_products_from_json)

        search_entry.pack(side='left', padx=5)
        search_button.pack(side='left')
        product_scraper_button.pack(side='left', padx=5)

        # Output
        self.result_text = tk.Text(master=self.window, font="Calibri 12", wrap="word", height=15, width=50, cursor="arrow")
        self.result_text.pack(pady=20)
        self.result_text.tag_config("link", foreground='blue', underline=1)
        self.result_text.tag_config('title', font="Calibri 12 bold")
        self.result_text.tag_bind("link", "<Enter>", lambda e: self.result_text.config(cursor="hand2"))
        self.result_text.tag_bind("link", "<Leave>", lambda e: self.result_text.config(cursor="arrow"))

    def perform_search(self):
        """Perform a search and display predefined links matching the query."""
        query = self.search_var.get().lower()
        if query:
            print(f"Searching for: {query}")  # Debugging log
            self.display_matching_links(query, "link.txt")
        else:
            self.display_results("Please enter a search term.")

    def display_matching_links(self, query, file_path):
        """Display links from the file that match the search query, including partial matches."""
        try:
            if not os.path.exists(file_path):
                self.display_results(f"Error: '{file_path}' not found.")
                return

            with open(file_path, "r") as file:
                links = file.readlines()

            print(f"Total links loaded: {len(links)}")  # Debugging log

            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)

            query_words = query.split()
            matching_links = [
                link.strip() for link in links
                if all(word in link.lower() for word in query_words)
                ]

            print(f"Matching links: {matching_links}")  # Debugging log

            if matching_links:
                for index, link in enumerate(matching_links):
                    self.result_text.insert(tk.END, f"{link}\n\n", "link")
                    tag_name = f"link_{index}"
                    start_index = self.result_text.index(f"end-{len(link) + 2}c")
                    end_index = f"{start_index}+{len(link)}c"
                    self.result_text.tag_add(tag_name, start_index, end_index)
                    self.result_text.tag_bind(tag_name, "<Button-1>", self.create_callback(link.strip()))
            else:
                self.result_text.insert(tk.END, "No matching links found.\n")
            self.result_text.config(state="disabled")
        except Exception as e:
            print(f"Error processing links: {e}")  # Debugging log
            self.display_results(f"Error reading links: {e}")

    def create_callback(self, link_url):
        """Create a callback function for each link."""
        return lambda e: self.open_link(link_url)

    def display_results(self, results):
        """Display the search results in the GUI."""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, results + "\n")
        self.result_text.config(state="disabled")

    def open_link(self, url):
        """Open a link in the default web browser."""
        webbrowser.open(url)

    def scrape_products_from_json(self):
        """Scrape product details for IDs listed in telefoane.json."""
        file_path = os.path.join(os.path.dirname(__file__), "storage", "telefoane.json")
        with open(file_path, "r") as file:
            product_ids = json.load(file)
        all_products = []
        for product_id in product_ids:
            product_details = self.fetch_product_details(product_id)
            if product_details:
                all_products.append(product_details)
            time.sleep(2.5)  # Rate limit to avoid being blocked
        with open("product_details.json", "w") as outfile:
            json.dump(all_products, outfile, indent=4)
        print("Product details saved to product_details.json")

    def fetch_product_details(self, product_id):
        """Fetch product details from the eMAG API."""
        url = f"https://sapi.emag.ro/recommendations/compared-similar-products?source_id=7&identifier={product_id}&page_type=product"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "product_collection" in data["data"] and len(data["data"]["product_collection"]) > 0:
                    product_data = data["data"]["product_collection"][0]
                    product_details = {
                        'id': product_data.get("id", "N/A"),
                        'name': product_data.get("name", "N/A"),
                        'price': product_data.get("offer", {}).get("price", {}).get("current", "N/A"),
                        'picture': product_data.get("image", {}).get("original", "N/A"),
                        'url': product_data.get("quick_uri", "N/A")
                    }
                    print(product_details)
                    return product_details
                else:
                    print(f"No product data found for ID: {product_id}")
            else:
                print(f"Request failed for ID {product_id} with status code {response.status_code}")
        except Exception as e:
            print(f"Error fetching product {product_id}: {e}")
        return None

if __name__ == "__main__":
    app = IntegratedApp()
    app.window.mainloop()
