import node
import os


bundle_dir = os.path.join(".meteor", "stackful")


def detect(app):
    return app.has_file(".meteor")


def delete_conflicting_npm_packages(app):
    app.run("rm -rf node_modules")


def bundle(app):
    app.mkdir(bundle_dir)
    app.run("HOME='{}' mrt bundle '{}/bundle.tar.gz'".format(app.user_home, bundle_dir))


def unbundle(app):
    app.run("cd '{}' && tar zxf bundle.tar.gz".format(bundle_dir))
    app.run("rm -f '{}/bundle.tar.gz'".format(bundle_dir))


def fix_fibers_server_package(app):
    print("Fixing Fibers package installation.")
    app.run(r"""cd '{bundle}/bundle/server' && \
HOME={home} npm uninstall fibers >/dev/null && \
HOME={home} npm install fibers >/dev/null""".format(home=app.user_home, bundle=bundle_dir))


def deploy(app):
    print("Deploying a Meteor app...")
    delete_conflicting_npm_packages(app)
    bundle(app)
    unbundle(app)
    fix_fibers_server_package(app)
    node.restart(app)


def server_command(app):
    executable = "node"
    process_name = "meteor"
    working_dir = os.path.join(bundle_dir, "bundle")
    return (working_dir, executable, [process_name, "main.js"])
