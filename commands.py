from __future__ import absolute_import, division, print_function, unicode_literals
import os, errno, subprocess


def run(cmd):
    subprocess.check_call(cmd, shell=True)


def sudo(cmd, user="root"):
    escaped_quotes = cmd.replace('"', '\\"')
    sudo_cmd = "sudo -u {} sh -c \"{}\"".format(user, escaped_quotes)
    run(sudo_cmd)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
