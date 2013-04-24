from __future__ import absolute_import, division, print_function, unicode_literals
from commands import sudo


class Deploy(object):
    def __init__(self, app):
        self.app = app

    def update_npm(self):
        # Pass the HOME folder so that npm writes its .npm dir somewhere it can
        # Ignore errors
        self.app.run("HOME='{}' npm install || true".format(self.app.target))

    def restart(self):
        print("Restarting: {} ...".format(self.app.name))
        # Ignore stop errors -- usually because the app hasn't been started
        sudo("stop {0} || true".format(self.app.name))
        sudo("start {0}".format(self.app.name))

    def deploy(self):
        self.update_npm()
        self.restart()
