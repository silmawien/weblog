# Common util functions

from jinja2 import Environment, FileSystemLoader
import os
import config

def add_generated_templates(ctx):
    "Add generated templates from environ['TMP'] to ctx."
    env = Environment(loader=FileSystemLoader("."))
    for tmp in os.environ['TMP'].split():
        # use name "footer" for "gen/footer.html"
        name = os.path.splitext(os.path.basename(tmp))[0]
        ctx[name] = env.get_template(tmp)

def make_context(ctx, templates=True):
    "Create context dict based on ctx, adding globals and generated templates."
    ctx["blog"] = config.BLOG
    if templates:
        add_generated_templates(ctx)
    return ctx
