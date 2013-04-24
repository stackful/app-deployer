from __future__ import absolute_import, division, print_function, unicode_literals
import os
from commands import mkdir_p, sudo


class GitDeploy(object):
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
                self.app_run("rm -rf * .* || true")

            self.app_run("git init")
            self.app_run("git remote add origin '{}'".format(self.source_repo))

    def pull_latest(self):
        self.app_run("git fetch -f origin master")
        self.app_run("git reset --hard FETCH_HEAD")

    def update_npm(self):
        # Pass the HOME folder so that npm writes its .npm dir somewhere it can
        # Ignore errors
        self.app_run("HOME='{}' npm install || true".format(self.app.target))

    def restart(self):
        print("Restarting: {} ...".format(self.app.name))
        # Ignore stop errors -- usually because the app hasn't been started
        sudo("stop {0} || true".format(self.app.name))
        sudo("start {0}".format(self.app.name))

    def app_run(self, cmd):
        sudo("cd '{}' && {}".format(self.app.target, cmd), self.app.user)

    def deploy(self):
        self.ensure_repo()
        self.pull_latest()
        self.update_npm()
        self.restart()
