# Render pages which depend on all posts.
# - latest posts (landing page)
# - index by date
# - index by tag
# - etc

from jinja2 import Environment, FileSystemLoader
from post import read_post
import sys
import os
from datetime import datetime
from common import make_context
import config
from collections import defaultdict

# number of recent posts to render on landing page
MAX_POSTS = 5

# share one Jinja environment
env = Environment(loader=FileSystemLoader("templates"))

def ensure_dir(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def posted_datetime(post):
    return post["posted"]["datetime"]


def tag_index(posts, out):
    idx = defaultdict(list)
    # make a dict tag -> [post]
    for post in filter(lambda p: "tags" in p, posts):
        for tag in post["tags"]:
            tag_name = tag["text"]
            idx[tag_name].append(post)

    # sort each list of posts by date
    map(lambda p: p.sort(key=posted_datetime, reverse=True), idx.values())

    # create one index page per tag
    for tag, posts in idx.items():
        ctx = make_context({ "title": 'Posts tagged "' + tag + '"', "tag": tag,
                "posts": posts })
        html = env.get_template("tag.html").render(ctx).encode("utf-8")

        tagfile = out + config.TAG_PATH % tag
        ensure_dir(tagfile)
        with open(tagfile, "w") as f:
            f.write(html)


def landing_page(posts):
    recent = sorted(posts, key=posted_datetime, reverse=True)[0:MAX_POSTS]
    ctx = make_context({ "title": "Index", "posts": recent })
    print env.get_template("index.html").render(ctx).encode("utf-8")


def escape_html(html):
    "Escape html to make it suitable for an atom <content type='html'> tag."
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def feed(posts, out):
    posts = sorted(posts, key=posted_datetime, reverse=True)
    # escape html
    for post in posts:
        post["content"] = escape_html(post["content"])
        post["abstract"] = escape_html(post["abstract"])
    ctx = make_context({ "posts": posts, "url": config.BLOG["feed"] })
    # use the most recent post's post time as the feed's update time
    ctx["posted"] = posts[0]["posted"]["isotime"]
    html = env.get_template("atom.xml").render(ctx).encode("utf-8")
    with open(out + config.FEED_PATH, "w") as f:
        f.write(html)


def render_index(srcs, urls, out):
    posts = [read_post(src, url) for src, url in zip(srcs, urls)]

    tag_index(posts, out)
    landing_page(posts)

    # mutates posts in-place!
    feed(posts, out)

if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    urls = os.environ['URL'].split()
    out = os.environ['OUT']
    render_index(srcs, urls, out)
