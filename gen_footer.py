from jinja2 import Environment, FileSystemLoader
from post import read_post
from datetime import datetime
from common import make_context
import os

MAX_POSTS = 5

# font size bounds for the category list ("tag cloud")
MAX_SCALE = 1.6
MIN_SCALE = 0.75

env = Environment(loader=FileSystemLoader("templates"))


def posted_datetime(post):
    return post["posted"]["datetime"]

def make_tags(posts):
    idx = dict()
    # make a dict tag -> post count
    for post in filter(lambda p: "tags" in p, posts):
        for tag in post["tags"]:
            name = tag["text"]
            if not name in idx:
                # reuse tag ... hmm
                tag["weight"] = 0
                idx[name] = tag

            idx[name]["weight"] += 1

    tags = idx.values();

    # normalize the sizes
    max_weight = max([tag["weight"] for tag in tags])

    for tag in tags:
        # relative weight [0..1]
        rel_weight = (tag["weight"] - 1) / float(max_weight - 1)
        scale = MIN_SCALE + rel_weight * (MAX_SCALE - MIN_SCALE)
        tag["scale"] = scale

    return tags


def render_footer(srcs, urls):
    posts = [read_post(src, url) for src, url in zip(srcs, urls)]
    recent = sorted(posts, key=posted_datetime, reverse=True)[0:MAX_POSTS]
    tags = make_tags(posts)

    ctx = make_context({ "posts": recent, "tags": tags }, False)
    print env.get_template("footer.html").render(ctx).encode("utf-8")


if __name__ == "__main__":
    srcs = os.environ['SRC'].split()
    urls = os.environ['URL'].split()
    render_footer(srcs, urls)
