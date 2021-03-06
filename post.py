import re
from datetime import datetime
from markdown import markdown
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.codehilite import CodeHiliteExtension
import codecs

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
    "posted": make_date,
    "created": make_date
}

def read_post(src, dst):
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
    post["content"] = markdown(body, extensions=[
        FootnoteExtension(),
        CodeHiliteExtension(guess_lang=False)
    ])

    # Make a nice abstract
    abstract = body.split('<!-- abstract -->', 1)[0]
    post["abstract"] = markdown(abstract)

    return post
