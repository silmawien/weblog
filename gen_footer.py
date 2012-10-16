from jinja2 import Environment, FileSystemLoader
from post import read_post
from datetime import datetime
from common import make_context
import os

MAX_POSTS = 5

env = Environment(loader=FileSystemLoader("templates"))


def posted_datetime(post):
    return post["posted"]["datetime"]


def render_footer(srcs, urls):
    posts = [read_post(src, url) for src, url in zip(srcs, urls)]
    recent = sorted(posts, key=posted_datetime, reverse=True)[0:MAX_POSTS]

    ctx = make_context({ "posts": recent }, False)
    print env.get_template("footer.html").render(ctx).encode("utf-8")


if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    urls = os.environ['URL'].split()
    render_footer(srcs, urls)
