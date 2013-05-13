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

        self.environment = config["stackful-environment"]
        stack_name = self.environment["STACK_NAME"]
        stack_config = config[stack_name]
        git_config = config["stackful-git"]

        self.user = app_user
        self.name = stack_config["app-name"]
        deploy_user = git_config["deploy-user"]
        self.source = "/home/{deploy_user}/{name}.git".format(deploy_user=deploy_user, name=self.name)
        self.target = stack_config["app-home"]

    def get_current_user(self):
        return pwd.getpwuid(os.geteuid()).pw_name

    def run(self, cmd, output=False):
        return sudo("cd '{}' && {}".format(self.target, cmd), self.user, output=output)

    def mkdir(self, path):
        self.run("mkdir -p '{}'".format(path))

    def has_file(self, path):
        return os.path.exists(os.path.join(self.target, path))

    def full_path(self, relative_path):
        return os.path.join(self.target, relative_path)

    def restart(self):
        print("Restarting: {} ...".format(self.name))
        # Ignore stop errors -- usually because the app hasn't been started
        sudo("stop {0} || true".format(self.name))
        sudo("start {0}".format(self.name))

    @property
    def user_home(self):
        return "/home/{}".format(self.user)
