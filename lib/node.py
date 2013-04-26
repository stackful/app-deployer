from __future__ import absolute_import, division, print_function, unicode_literals
from commands import sudo


def update_npm(app):
    # Pass the HOME folder so that npm writes its .npm dir somewhere it can
    # Ignore errors
    app.run("HOME='{}' npm install || true".format(app.user_home))


def restart(app):
    print("Restarting: {} ...".format(app.name))
    # Ignore stop errors -- usually because the app hasn't been started
    sudo("stop {0} || true".format(app.name))
    sudo("start {0}".format(app.name))


def detect(app):
    return app.has_file("package.json") and not app.has_file(".meteor")


def deploy(app):
    print("Deploying a vanilla Node.js/npm app...")
    update_npm(app)
    restart(app)


def server_command(app):
    executable = "node"
    process_name = "node"
    return (None, executable, [process_name, "app.js"])
