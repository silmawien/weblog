# Common util functions

from jinja2 import Environment, FileSystemLoader
import os
import config

def make_context(ctx):
    "Create context dict based on ctx, adding globals."
    ctx["blog"] = config.BLOG
    return ctx
