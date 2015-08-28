import glob
from post import read_post
import jinja2
import os

blog = { "base": "http://mattias.niklewski.com", "title": "mattias", "feed": "atom.xml" }

env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

def out(path):
    return os.path.join(os.environ["OUT"], path)

def mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def render(template, ctx, dst):
    ctx = ctx.copy()
    ctx["blog"] = blog
    html = env.get_template(template).render(ctx).encode("utf-8")
    mkdir(os.path.dirname(dst))
    with open(dst, "w") as fd:
        fd.write(html)

def entry(post):
    print post["url"]
    dst = out(post["url"] + ".html")
    render("post.html", post, dst)

def index(posts):
    print "index"
    render("index.html", { "posts": posts }, out("index.html"))

def escape_html(html):
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def feed(posts):
    print "feed"
    # escape html
    for post in posts:
        post["content"] = escape_html(post["content"])
    # use the most recent post's post time as the feed's update time
    updated = posts[0]["posted"]["isotime"] 
    ctx = { "posts": posts,"url": blog["feed"], "updated": updated }
    render("atom.xml", ctx, out(blog["feed"]))

if __name__ == "__main__":
    drafts = [ read_post(path, os.path.splitext(path)[0]) for path in glob.glob("drafts/*.txt")]
    map(entry, drafts)
    posts = [ read_post(path, os.path.splitext(path)[0]) for path in glob.glob("posts/*/*/*")]
    posts = sorted(posts, key=lambda p: p["posted"]["datetime"], reverse=True)
    map(entry, posts)
    feed(posts)
    index(posts)

