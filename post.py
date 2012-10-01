# Post interface.
#
# A post consists of metadata and contents.
# read_post() returns a dict of all metadata plus the contents,
# formatted as html.

import re
from subprocess import Popen, PIPE
import sys
import os.path
from itertools import takewhile
import config

# number of paragraphs in abstracts
ABSTRACT_SIZE = 1

def filter(program, source):
    "Run program on source and return the resulting output."
    p = Popen([program], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = p.communicate(source)
    return stdoutdata


def markdown(source):
    "Run markdown + smartypants on source and return the output."
    return filter("SmartyPants.pl", filter("markdown", source))


def make_tag_link(tag):
    "Create href, display-name from a tag name."
    return { "href": config.TAG_URL % tag, "text": tag }


english_months = ['january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december']


def pretty_date(datestr):
    "Convert 2012-09-10 to August 10, 2012."
    (year, month, day) = datestr.split("-")
    try:
        month = english_months[int(month) - 1].capitalize()
    except IndexError:
        sys.exit("Invalid date string: " + datestr)
    return "{0} {1}, {2}".format(month, int(day), year)


def make_date(datestr):
    "Create datetime and display time for a html5 <time> element."
    return { "datetime": datestr, "display": pretty_date(datestr) }

def paragraph_counter(num):
    "Count empty lines and return False after num such lines."
    count = [num] # workaround for strange scoping rules in python 2.x
    def counter(line):
        if not line.strip():
            count[0] -= 1
        return count[0] > 0
    return counter


def read_post(src, dst):
    """Return a dict with metadata and html content of a post.

    src is the source path
    dst is the web-root relative path to view a single post
    """
    post = dict()
    with open(src) as f:
        for line in f:
            # Metadata section ends with an empty line
            if not line.strip(): break
            # Metadata has the format "key: value"
            key, value = re.split(u"\s*:\s*", unicode(line, "utf-8"))
            key = key.lower()
            value = value.strip()

            # linkify tags "tags: tag1 tag2"
            if key == "tags":
                post[key] = map(make_tag_link, value.split())
            elif key == "posted" or key == "created":
                post[key] = make_date(value)
            else:
                post[key] = value

        # self-link (for header and abstract [...])
        post["url"] = dst

        # The remainder is markdown-content
        body = [line for line in f]

        # Format with markdown
        md = "".join(body)
        post["content"] = unicode(markdown(md), "utf-8")

        # Make a nice abstract, also with markdown
        abstract = "".join(takewhile(paragraph_counter(ABSTRACT_SIZE), body))
        post["abstract"] = unicode(markdown(abstract), "utf-8")
    return post
