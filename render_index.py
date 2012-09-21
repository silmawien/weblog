# Render page with a single post.

from jinja2 import Environment, FileSystemLoader
from post import read_post
import sys
import os
from datetime import datetime
from common import add_generated_templates

# number of recent posts to render
MAX_POSTS = 5

def created_datetime(post):
    return datetime.strptime(post["created"]["datetime"], "%Y-%m-%d")

def render_index(srcs, dsts):
    posts = [read_post(x, y) for x, y in zip(srcs, dsts)]
    posts = sorted(posts, key=created_datetime, reverse=True)[0:MAX_POSTS]
    ctx = { "title": "Index", "posts": posts }
    add_generated_templates(ctx)
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("index.html").render(ctx).encode("utf-8")


if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    dsts = os.environ['DST'].split()
    render_index(srcs, dsts)
