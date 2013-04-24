from __future__ import absolute_import, division, print_function, unicode_literals
from commands import sudo
import json
import os
import pwd


class App(object):
    config_file = os.path.join("/etc", "stackful", "node.json")

    def __init__(self, app_user=None):
        config = {}
        with open(App.config_file, "r") as cf:
            config = json.load(cf)

        if not app_user:
            app_user = self.get_current_user()

        self.user = app_user
        self.name = config["stackful-node"]["app-name"]
        self.source = "/home/{user}/{name}.git".format(user=self.user, name=self.name)
        self.target = config["stackful-node"]["app-home"]

    def get_current_user():
        return pwd.getpwuid(os.geteuid()).pw_name

    def run(self, cmd):
        sudo("cd '{}' && {}".format(self.target, cmd), self.user)

    def has_file(self, path):
        return os.path.exists(os.path.join(self.target, path))
