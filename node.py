from __future__ import absolute_import, division, print_function, unicode_literals
from commands import sudo


def update_npm(app):
    # Pass the HOME folder so that npm writes its .npm dir somewhere it can
    # Ignore errors
    app.run("HOME='{}' npm install || true".format(app.target))


def restart(app):
    print("Restarting: {} ...".format(app.name))
    # Ignore stop errors -- usually because the app hasn't been started
    sudo("stop {0} || true".format(app.name))
    sudo("start {0}".format(app.name))


def detect(app):
    return app.has_file("package.json")


def deploy(app):
    update_npm(app)
    restart(app)
