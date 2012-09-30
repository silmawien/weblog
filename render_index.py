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
from common import add_generated_templates
import config
from collections import defaultdict

# number of recent posts to render on landing page
MAX_POSTS = 5

def ensure_dir(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def posted_datetime(post):
    return datetime.strptime(post["posted"]["datetime"], "%Y-%m-%d")


def tag_index(posts, out, root):
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
        ctx = { "title": 'Posts tagged "' + tag + '"', "tag": tag,
                "posts": posts }
        add_generated_templates(ctx)
        env = Environment(loader=FileSystemLoader("templates"))
        html = env.get_template("tag.html").render(ctx).encode("utf-8")

        # strip the url root from TAG_URL to find the server path
        server_path = os.path.relpath(config.TAG_URL, root) % tag
        tagfile = os.path.join(out, server_path)
        ensure_dir(tagfile)
        with open(tagfile, "w") as f:
            f.write(html)


def landing_page(posts):
    recent = sorted(posts, key=posted_datetime, reverse=True)[0:MAX_POSTS]
    ctx = { "title": "Index", "posts": recent }
    add_generated_templates(ctx)
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("index.html").render(ctx).encode("utf-8")


def render_index(srcs, urls, out, root):
    posts = [read_post(src, url) for src, url in zip(srcs, urls)]

    tag_index(posts, out, root)
    landing_page(posts)


if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    urls = os.environ['URL'].split()
    out = os.environ['OUT']
    root = os.environ['ROOT']
    render_index(srcs, urls, out, root)
