# Convert a markdown post with metadata into html.

from jinja2 import Environment, FileSystemLoader
import re
from subprocess import Popen, PIPE
import sys

def filter(program, source):
    "Run program on source and return the resulting output."
    p = Popen([program], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = p.communicate(source)
    return stdoutdata

def markdown(source):
    return filter("SmartyPants.pl", filter("markdown", source))

def make_tag_link(tagname):
    "Create href, display-name from a tag name."
    return { "href": "/tags/" + tagname, "name": tagname }

english_months = ['january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december']

def pretty_date(datestr):
    "Convert 2012-09-10 to August 10, 2012."
    (year, month, day) = datestr.split("-")
    try:
        month = english_months[int(month)].capitalize()
    except IndexError:
        sys.exit("Invalid date string: " + datestr)
    return "{0} {1}, {2}".format(month, int(day), year)

def make_date(datestr):
    "Create datetime and display time for a html5 <time> element."
    return { "datetime": datestr, "display": pretty_date(datestr) }

def read_post(path):
    "Return a dict with metadata and html content of a post."
    post = dict()
    with open(path) as f:
        for line in f:
            # Metadata section ends with an empty line
            if not line.strip(): break
            # Metadata has the format "key: value"
            [key, value] = re.split(u"\s*:\s*", unicode(line, "utf-8"))
            key = key.lower()

            # split keys that appear to be plural
            if key[-1] == "s":
                post[key] = map(make_tag_link, value.split())
            elif key == "created":
                post[key] = make_date(value)
            else:
                post[key] = value.strip()

        # The remainder is markdown-content
        md = "".join([line for line in f])
        post["content"] = unicode(markdown(md), "utf-8")
    return post
    
def mm(src):
    ctx = read_post(src)
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("post.html").render(ctx).encode("utf-8")

if __name__ == "__main__":
    mm(sys.argv[1])
