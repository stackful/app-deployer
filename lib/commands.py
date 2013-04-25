from __future__ import absolute_import, division, print_function, unicode_literals
import os, errno, subprocess


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def sudo(cmd, user="root"):
    escaped_quotes = cmd.replace('"', '\\"')
    sudo_cmd = "sudo -u {} sh -c \"{}\"".format(user, escaped_quotes)
    run(sudo_cmd)


def mkdir_p(path, root=False):
    if not sudo:
        run("mkdir -p '{}'".format(path))
    else:
        sudo("mkdir -p '{}'".format(path))
