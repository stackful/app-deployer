from __future__ import absolute_import, division, print_function, unicode_literals
import os
from commands import mkdir_p, sudo


def ensure_repo(app):
    if not os.path.exists(app.target):
        mkdir_p(app.target)
        sudo("chown {} '{}'".format(app.user, app.target))

    git_dir = os.path.join(app.target, ".git")
    if not os.path.exists(git_dir):
        print("Setting up a mirror Git repository at '{}'.".format(app.target))
        if os.path.exists(os.path.join(app.target, "stackful-demo.txt")):
            print("Wiping demo web app in '{}'...".format(app.target))
            app.run("rm -rf * .* || true")

        app.run("git init")
        app.run("git remote add origin '{}'".format(source_repo))

def pull_latest(app):
    app.run("git fetch -f origin master")
    app.run("git reset --hard FETCH_HEAD")


def update(app):
    ensure_repo(app)
    pull_latest(app)
