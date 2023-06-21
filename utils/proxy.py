from readabilipy import simple_json_from_html_string
import requests
from bs4 import BeautifulSoup
from utils import _config

def proxy_post(id):
    URL = f"https://news.ycombinator.com/item?id={id}"
    html = requests.get(URL).content.decode()
    
    parsed_html = BeautifulSoup(html, "html.parser")

    article_url = parsed_html.select_one(".title a")["href"]

    article_html = requests.get(
        url=article_url, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:113.0) Gecko/20100101 Firefox/113.0",
            "Accept": "text/html"
        })
    proxy_html = simple_json_from_html_string(article_html.text, use_readability=True)["content"]

    parsed = BeautifulSoup(proxy_html, "html.parser")

    for image in parsed.find_all("img"):
        image["alt"] = f"URL: {image['src']}"
        image["src"] = f"/proxy_image?url={image['src']}"

    proxy_html = str(parsed)

    return proxy_html

def proxy_image(url):
    image = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:113.0) Gecko/20100101 Firefox/113.0",
            "Accept": "image/*"
        },
    ).content

    return image
