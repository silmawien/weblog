# Flags, paths and other config variables

# Make a container for convenient access from templates.
BLOG = {}

# Root path, to create links.
BLOG["root"] = "/mattias"

# Blog url without root path. Can be concatenated with a relative URL to form
# an absolute URL (see atom.xml).
BLOG["base"] = "http://blog.niklewski.com"

# Title
BLOG["title"] = "// My Blog"

# Output tag-specific index here.
TAG_PATH = "/tags/%s.html"

# The corresponding tag URL.
TAG_URL = BLOG["root"] + TAG_PATH

# Output feed here.
FEED_PATH = "/atom.xml"

# Path to feed.
BLOG["feed"] = BLOG["root"] + FEED_PATH
