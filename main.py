#!/usr/bin/env python3
from datetime import datetime
from flask import Flask, request, render_template
from utils._config import PORT
from utils import helpers, proxy

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def home():
    page_num = helpers.get_page_num(request)

    return render_template(
        "index.html",
        posts=helpers.get_results("", page_num),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/front")
def front():
    page_num = helpers.get_page_num(request)

    if "day" in request.args:
        day = request.args.get("day", "")
    else:
        day = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        "index.html",
        posts=helpers.get_results("front", page_num, day=day),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/ask")
def ask():
    page_num = helpers.get_page_num(request)

    return render_template(
        "index.html",
        posts=helpers.get_results("ask", page_num),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/newest")
def new():
    page_num = helpers.get_page_num(request)

    return render_template(
        "index.html",
        posts=helpers.get_results("newest", page_num),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/show")
def show():
    page_num = helpers.get_page_num(request)

    return render_template(
        "index.html",
        posts=helpers.get_results("show", page_num),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/from")
def from_site():
    page_num = helpers.get_page_num(request)

    if "site" in request.args:
        site = request.args.get("site", "").strip()
    else:
        site = "ignore_me"

    return render_template(
        "index.html",
        posts=helpers.get_results("from", page_num, site=site),
        next_page=helpers.next_page(page_num, request.path)
    )

@app.route("/item")
def item():
    return render_template(
        "item.html",
        content=helpers.get_post_content(helpers.valid_id(request))
    )

@app.route("/threads")
def threads():
    # page_num = helpers.get_page_num(request)

    return "TODO"

@app.route("/proxy")
def _proxy():
    return render_template(
        "proxy.html",
        content=proxy.proxy_post(helpers.valid_id(request))
    )

@app.route("/proxy_image")
def _proxy_image():
    if "url" in request.args:
        url = request.args.get("url")
        return proxy.proxy_image(url)


if __name__ == "__main__":
    app.run(threaded=True, port=PORT)
