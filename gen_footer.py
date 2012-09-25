from jinja2 import Environment, FileSystemLoader

def render_footer():
    ctx = dict()
    env = Environment(loader=FileSystemLoader("templates"))
    print env.get_template("footer.html").render(ctx).encode("utf-8")


if __name__ == "__main__":
    render_footer()
