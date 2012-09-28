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
        ctx = { "title": 'Posts tagged "' + tag + '"', "tag": tag,
                "posts": posts }
        add_generated_templates(ctx)
        env = Environment(loader=FileSystemLoader("templates"))
        html = env.get_template("tag.html").render(ctx).encode("utf-8")
        outpath = out + config.TAG_URL % tag
        ensure_dir(outpath)
        with open(out + config.TAG_URL % tag, "w") as f:
            f.write(html)


def landing_page(posts):
    recent = sorted(posts, key=posted_datetime, reverse=True)[0:MAX_POSTS]
    ctx = { "title": "Index", "posts": recent }
    add_generated_templates(ctx)
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("index.html").render(ctx).encode("utf-8")


def render_index(srcs, dsts, out):
    posts = [read_post(src, dst_url) for src, dst_url in zip(srcs, dsts)]

    tag_index(posts, out)
    landing_page(posts)


if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    dsts = os.environ['DST'].split()
    out = os.environ['OUT']
    render_index(srcs, dsts, out)
