# Common util functions

from jinja2 import Environment, FileSystemLoader
import os

def add_generated_templates(ctx):
    "Add generated templates from environ['TMP'] to ctx."
    env = Environment(loader=FileSystemLoader("."))
    for tmp in os.environ['TMP'].split():
        # use name "footer" for "gen/footer.html"
        name = os.path.splitext(os.path.basename(tmp))[0]
        ctx[name] = env.get_template(tmp)


