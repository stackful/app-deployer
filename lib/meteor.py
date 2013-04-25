import node


def detect(app):
    return app.has_file(".meteor")


def update_meteorite(app):
    app.run("HOME='{}' mrt update".format(app.user_home))


def deploy(app):
    update_meteorite(app)
    node.restart(app)


def server_command(app):
    executable = "mrt"
    process_name = "meteor"
    return (executable, [process_name, "run"])
