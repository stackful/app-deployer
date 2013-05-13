from __future__ import absolute_import, division, print_function, unicode_literals
import os, errno, subprocess


def run(cmd):
    return subprocess.check_call(cmd, shell=True)

def run_output(cmd):
    return subprocess.check_output(cmd, shell=True)


def sudo(cmd, user="root", output=False):
    escaped_quotes = cmd.replace('"', '\\"')
    sudo_cmd = "sudo -u {} sh -c \"{}\"".format(user, escaped_quotes)
    if not output:
        return run(sudo_cmd)
    else:
        return run_output(sudo_cmd)


def mkdir_p(path, root=False):
    if not root:
        run("mkdir -p '{}'".format(path))
    else:
        sudo("mkdir -p '{}'".format(path))
