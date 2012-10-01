# Render page with a single post.

from jinja2 import Environment, FileSystemLoader
from post import read_post
import sys
import os
from common import make_context

def render_post(src, url):
    ctx = make_context(read_post(src, url))

    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("single_post.html").render(ctx).encode("utf-8")


if __name__ == "__main__":
    src = sys.argv[1]
    url = os.environ['URL']
    render_post(src, url)
