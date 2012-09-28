# Run markdown and wrap the result in a jinja template.
# Metadata is read from the top of the input file.

import jinja2
import os.path
import re
from subprocess import Popen, PIPE

# Output files are written here
SITEROOT = "/var/www/blog.niklewski.com"

def gen_feed_info():
    "Generate triplets of Title, Link, Content for an xml feed."
    # TODO get real info
    yield ("A title1", "http://example.com/1", "content1")
    yield ("A title2", "http://example.com/2", "content2")

def make_feed():
    names = ["title", "link", "content"]
    posts = []
    for info in gen_feed_info():
        posts.append(dict(zip(names, info)))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    return env.get_template("templates/feed.xml").render(items=posts)

def output(path, contents):
    "Generate an output file at SITEROOT/path a print contents to it."
    with open(os.path.join(SITEROOT, path), 'w') as f:
        f.write(contents)

def markdown(source):
    "Run markdown on source and return the resulting html."
    p = Popen(["markdown"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = p.communicate(source)
    return stdoutdata

def get_post(path):
    "Return a dict with metadata and html content of a post."
    post = dict()
    post["meta"] = dict()
    with open(path) as f:
        for line in f:
            # Metadata section ends with an empty line
            if not line.strip(): break
            # Metadata has the format "key: value"
            [key, value] = re.split("\s*:\s*", line)
            post["meta"][key.lower()] = value.strip()

        # The remainder is markdown-content
        md = "\n".join([line for line in f])
        post["content"] = markdown(md)
    return post

def get_posts():
    for root, dirs, files in os.walk("posts"):
        for name in files:
            yield get_post(os.path.join(root, name))

def generate():
    "Generate the complete site."
    # Get all post html / metadata
    for post in get_posts():
        print post["meta"]

    # Individual posts

    # Posts index / landing page

    # Posts feed
    output("feed.xml", make_feed())

    # Book listing ?

if __name__ == "__main__":
    print sys.argv[1]

