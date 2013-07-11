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
    format = "%b %d" if datetime.year == thisyear else "%b %d, %Y"
    return datetime.strftime(format).replace(' 0', ' ')


def iso_time(datetime):
    "Mock ISO timestamp with timezone (utc)."
    return datetime.isoformat() + "Z"


def make_date(datestr):
    "Parse datestr and create datetime, display time, html5 <time> string."
    dt = datetime.strptime(datestr, "%Y-%m-%d")
    return { "datetime": dt, "display": pretty_date(dt),
            "htmltime": datestr, "isotime": iso_time(dt)}


metatrans = {
    "tags": lambda x: map(make_tag_link, tagsplit(x)),
    "posted": lambda x: make_date(x),
    "created": lambda x: make_date(x)
}


def read_post(src, dst):
    """Return a dict with metadata and html content of a post.

    src is the source path
    dst is the web-root relative path to view a single post
    """
    post = dict()
    with codecs.open(src, "r", "utf-8") as file:
        contents = file.read()
    meta, body = contents.split('\n\n', 1)
    for m in meta.split('\n'):
        key, value = re.split(u'\s*:\s*', m.strip(), 1)
        key = key.lower()
        if key in metatrans:
            value = metatrans[key](value)
        post[key] = value

    # self-link (for header and abstract [...])
    post["url"] = dst

    # Format with markdown
    post["content"] = markdown(body)

    # Make a nice abstract, also with markdown
    abstract = body.split('<!-- abstract -->', 1)[0]
    post["abstract"] = markdown(abstract)
    return post
