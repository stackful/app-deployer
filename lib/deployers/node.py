from __future__ import absolute_import, division, print_function, unicode_literals


def update_npm(app):
    # Pass the HOME folder so that npm writes its .npm dir somewhere it can
    # Ignore errors
    app.run("HOME='{}' npm install || true".format(app.user_home))


def detect(app):
    return app.has_file("package.json") and not app.has_file(".meteor")


def deploy(app):
    print("Deploying a vanilla Node.js/npm app...")
    update_npm(app)
    app.restart()


def server_command(app):
    executable = "node"
    process_name = "node"
    return (None, executable, [process_name, "app.js"])
