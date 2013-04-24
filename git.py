from __future__ import absolute_import, division, print_function, unicode_literals
import os
from commands import mkdir_p, sudo


class Deploy(object):
    def __init__(self, app):
        self.app = app

    def ensure_repo(self):
        if not os.path.exists(self.app.target):
            mkdir_p(self.app.target)
            sudo("chown {} '{}'".format(self.app.user, self.app.target))

        git_dir = os.path.join(self.app.target, ".git")
        if not os.path.exists(git_dir):
            print("Setting up a mirror Git repository at '{}'.".format(self.app.target))
            if os.path.exists(os.path.join(self.app.target, "stackful-demo.txt")):
                print("Wiping demo web app in '{}'...".format(self.app.target))
                self.app.run("rm -rf * .* || true")

            self.app.run("git init")
            self.app.run("git remote add origin '{}'".format(self.source_repo))

    def pull_latest(self):
        self.app.run("git fetch -f origin master")
        self.app.run("git reset --hard FETCH_HEAD")

    def deploy(self):
        self.ensure_repo()
        self.pull_latest()
