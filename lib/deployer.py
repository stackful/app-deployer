from __future__ import absolute_import, division, print_function, unicode_literals
import sys
from config import App
import git
from deployers import node, meteor, python


class Deployer(object):
    def __init__(self, app_user, skip_update):
        self.app_user = app_user
        self.skip_update = skip_update
        self.app = App(self.app_user)

    def update_app(self):
        if not self.skip_update:
            git.update(self.app)

    def get_deployers(self):
        available = [meteor, node, python]
        appropriate = [deployer for deployer in available if deployer.detect(self.app)]
        if not appropriate:
            print("No suitable deployer found for app. Giving up.")
            sys.exit(0)
        return appropriate

    def run(self):
        self.update_app()

        for deployer in self.get_deployers():
            deployer.deploy(self.app)
