import string
import re
import requests
from utils._config import HEADERS
from bs4 import BeautifulSoup
from urllib.parse import quote

def is_num(n):
    for i in n:
        if i not in string.digits:
            return False
    return True

def next_page(current, url):
    try:
        end = int(current) + 1
    except ValueError:
        end = 1
    if "p=" in url:
        return url.replace(f"p={current}", f"p={end}")
    elif "?" in url:
        return url + f"&p={end}"
    else:
        return url + f"?p={end}"

def get_results(type, page, day="ignore_me", site="ignore_me"):
    URL = f"https://news.ycombinator.com/{type}?p={page}"

    if day != "ignore_me":
        URL += f"&day={day}"
    if site != "ignore_me":
        URL += f"&site={site}"

    html = requests.get(url=URL, headers=HEADERS).content.decode()
    parsed_html = BeautifulSoup(html, "html.parser")
    content = parsed_html.find_all("tr")[4:94]
    # Range of <tr>s that are relevant to the posts. Length == 90, since each page
    # has 30 posts, each one having a title, subline, and a spacer.

    list_of_posts = []
    n = []

    for con in content:
        # Splits array based on if it's a spacer or not.
        if str(con).strip() == "<tr class=\"spacer\" style=\"height:5px\"></tr>":
            list_of_posts.append(n)
            n = []
        else:
            n.append(con)

    posts = []

    for post in list_of_posts:
        id = post[0]["id"]
        rank = post[0].select(".rank")[0].get_text()
        title_line = post[0].select(".titleline a")[0]
        title = title_line.get_text()
        link = title_line["href"]
        site = post[0].find("span", class_="sitestr")

        if site != None:
            site = site.get_text()
        else:
            site = ""

        score = post[1].find("span", "score")
        if score != None:
            score = score.get_text()
        else:
            score = ""
        user_name = post[1].find("a", class_="hnuser")
        if user_name != None:
            user_name = user_name.get_text()
        else:
            user_name = ""
        age = post[1].select(".age")[0].get_text()
        comments = post[1].select(".subline a")

        if comments != []:
            comments = comments[-1].get_text()
        else:
            comments = ""

        posts.append({
            "id": id,
            "rank": rank,
            "rank_len": len(rank),
            "title": title,
            "link": link,
            "site": site,
            "score": score,
            "user_name": user_name,
            "age": age,
            "comments": comments,
        })

    return posts


def get_comments(parsed_html):
    comments = []
    i = 2
    while True:
        for comment in parsed_html.select(".comtr"):
            user = comment.find("a", class_="hnuser").get_text()
            user_href = f"/user?id={user}"
            date = comment.find("span", class_="age").get_text()
            comment_text = comment.find("span", class_="commtext").prettify().replace(" c00", "")
            indent = comment.find("td", class_="ind")["indent"]

            comments.append({
                "user": user,
                "user_href": user_href,
                "date": date,
                "text": comment_text,
                "indent": indent,
            })
        if parsed_html.find("a", class_=".morelink") == None:
            break
        else:
            URL = f"https://news.ycombinator.com/item?id={quote(id)}&p={i}"
            html = requests.get(url=URL, headers=HEADERS).content
            parsed_html = BeautifulSoup(html, "html.parser")
            i += 1
    return comments


def get_post_content(id):
    URL = f"https://news.ycombinator.com/item?id={quote(id)}"
    html = requests.get(url=URL, headers=HEADERS).content
    parsed_html = BeautifulSoup(html, "html.parser")

    title = parsed_html.select(".titleline a")[0]
    link = title["href"]
    title = title.get_text()
    site = parsed_html.find("span", class_="sitestr")
    if site != None:
        site = site.get_text()
    else:
        site = ""
    site_from = f"from?site={site}"
    points = parsed_html.select(".score")[0].get_text()
    points = parsed_html.find("span", class_="score").get_text()
    op = parsed_html.find("a", class_="hnuser").get_text()
    comment_num = parsed_html.select(".subtext a")[-1].get_text()

    comments = get_comments(parsed_html)

    return {
        "id": id,
        "title": title,
        "op": op,
        "points": points,
        "comment_num": comment_num,
        "link": link,
        "site_from": site_from,
        "site": site,
        "comments": comments,
    }

def get_user_comments(user):
    URL = f"https://news.ycombinator.com/threads?id={user}"
    html = requests.get(url=URL, headers=HEADERS).content.decode()
    parsed_html = BeautifulSoup(html, "html.parser")

    return get_comments(parsed_html)


def valid_id(request):
    if "id" in request.args:
        id = re.search("[0-9]{1,9}", request.args.get("id"))[0]
    else:
        id = "1"
    return id

def get_page_num(request):
    if "p" in request.args:
        page_num = re.search("[0-9]{1,}", request.args.get("p"))[0]
    else:
        page_num = "1"
    return page_num
