import json
from bs4 import BeautifulSoup
import requests
import urllib.parse

def get_data(url):
    response = requests.get(url)
    return response.text

def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_products(data):
    return data.find_all(class_="ProductItem__Wrapper")

def format_data(data):
    products = []
    for item in data:
        product = {}
        product["title"] = item.find(class_="ProductItem__Title").text.strip()
        product["price"] = item.find(class_="ProductItem__Price").text
        product["image"] = item.find("noscript").find_all("img")[-1].get("src")
        product["alt"] = item.find("noscript").find_all("img")[-1].get("alt")
        products.append(product)
    return products

url = input("Enter the URL: ")
html_data = get_data(url)
soup_data = parse_data(html_data)
product_wrapper = get_products(soup_data)
product_data = format_data(product_wrapper)

title = urllib.parse.unquote(soup_data.title.text).replace(
    "/n", "").strip().replace(" ", "_")

with open(title + ".json", "w") as f:
    json.dump(product_data, f, indent=4)