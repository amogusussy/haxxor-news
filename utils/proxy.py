from utils.config import HEADERS
from readabilipy import simple_json_from_html_string
import requests
from bs4 import BeautifulSoup


def proxy_post(id):
    URL = f"https://news.ycombinator.com/item?id={id}"
    html = requests.get(URL).content.decode()

    parsed_html = BeautifulSoup(html, "html.parser")

    article_url = parsed_html.select_one(".title a")["href"]

    article_html = requests.get(
        url=article_url,
        headers=HEADERS
    )
    proxy_html = simple_json_from_html_string(
        article_html.text,
        use_readability=True
    )["content"]

    parsed = BeautifulSoup(proxy_html, "html.parser")

    for image in parsed.find_all("img"):
        image["alt"] = f"URL: {image['src']}"
        image["src"] = f"/proxy_image?url={image['src']}"

    proxy_html = str(parsed)

    return proxy_html


def proxy_image(url):
    image = requests.get(
        url=url,
        headers=HEADERS
    ).content

    return image
