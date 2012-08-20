# Convert a markdown post with metadata into html.

from jinja2 import Environment, FileSystemLoader
import re
from subprocess import Popen, PIPE
import sys

def markdown(source):
    "Run markdown on source and return the resulting html."
    p = Popen(["markdown"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = p.communicate(source)
    return stdoutdata

def read_post(path):
    "Return a dict with metadata and html content of a post."
    post = dict()
    with open(path) as f:
        for line in f:
            # Metadata section ends with an empty line
            if not line.strip(): break
            # Metadata has the format "key: value"
            [key, value] = re.split("\s*:\s*", line)
            post[key.lower()] = value.strip()
        
        # The remainder is markdown-content
        md = "".join([line for line in f])
        post["content"] = markdown(md)
    return post
    
if __name__ == "__main__":
    ctx = read_post(sys.argv[1])
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("post.html").render(ctx)
