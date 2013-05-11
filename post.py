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
from datetime import datetime
from urllib import quote
from markdown import markdown
import codecs

# number of paragraphs in abstracts
ABSTRACT_SIZE = 1


def make_tag_link(tag):
    "Create href, display-name from a tag name."
    return { "url": config.TAG_URL % quote(tag), "text": tag }


def tagsplit(tags):
    """Split a tag string on either ',' or ' ' as appropriate."""
    if tags.find(",") != -1:
        return [s.strip() for s in tags.split(",")]
    else:
        return tags.split()


def pretty_date(datetime):
    "Convert 2012-09-10 to August 10[, 2012]."
    thisyear = datetime.now().year
    format = "%B %d" if datetime.year == thisyear else "%B %d, %Y"
    return datetime.strftime(format).replace(' 0', ' ')


def iso_time(datetime):
    "Mock ISO timestamp with timezone (utc)."
    return datetime.isoformat() + "Z"


def make_date(datestr):
    "Parse datestr and create datetime, display time, html5 <time> string."
    dt = datetime.strptime(datestr, "%Y-%m-%d")
    return { "datetime": dt, "display": pretty_date(dt),
            "htmltime": datestr, "isotime": iso_time(dt)}


def paragraph_counter(num):
    "Count empty lines and return False after num such lines."
    count = [num] # workaround for strange scoping rules in python 2.x
    done = [False] 
    def counter(line):
        line = line.strip()
        if not line:
            count[0] -= 1
        # include trailing links, ie. [foo]: http://foo.com
        if count[0] <= 0 and line and line[0] != '[':
            done[0] = True
        return not done[0]
    return counter


def read_post(src, dst):
    """Return a dict with metadata and html content of a post.

    src is the source path
    dst is the web-root relative path to view a single post
    """
    post = dict()
    with codecs.open(src, "r", "utf-8") as f:
        for line in f:
            # Metadata section ends with an empty line
            if not line.strip(): break
            # Metadata has the format "key: value"
            key, value = re.split(u"\s*:\s*", line, 1)
            key = key.lower()
            value = value.strip()

            # linkify tags "tags: tag1 tag2"
            if key == "tags":
                post[key] = map(make_tag_link, tagsplit(value))
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
        post["content"] = markdown(md)

        # Make a nice abstract, also with markdown
        abstract = "".join(takewhile(paragraph_counter(ABSTRACT_SIZE), body))
        post["abstract"] = markdown(abstract)
    return post
