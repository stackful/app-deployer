from __future__ import absolute_import, division, print_function, unicode_literals
import os
import ast


virtualenv = "/opt/virtualenvs/python-web/"
python = os.path.join(virtualenv, "bin", "python")


def detect(app):
    return app.has_file("manage.py")


def update_django_settings(app):
    if os.getenv("DJANGO_SETTINGS_MODULE"):
        return

    settings_module = find_module_from_managepy(app)
    if not settings_module:
        settings_module = find_module_grep(app)

    if not settings_module:
        settings_module = "settings"

    if settings_module:
        print("Found Django settings module: {}".format(settings_module))
        os.putenv("DJANGO_SETTINGS_MODULE", settings_module)


def find_module_from_managepy(app):
    if not app.has_file("manage.py"):
        return None

    with open(app.full_path("manage.py"), "r") as f:
        source_code = f.read()

    module = ast.parse(source_code)
    for node in ast.walk(module):
        if isinstance(node, ast.Call) and len(node.args) == 2:
            args = node.args
            if isinstance(args[0], ast.Str) and isinstance(args[1], ast.Str):
                if args[0].s == "DJANGO_SETTINGS_MODULE":
                    return args[1].s

    return None


def find_module_grep(app):
    output = app.run("grep --include=*.py -lr INSTALLED_APPS *", output=True)
    lines = [line.strip() for line in output.split("\n")]
    first = lines[0]
    return first.replace("/", ".").replace("\\", ".").rstrip(".py")


def update_environment(app):
    env = app.environment
    for key, value in env.items():
        os.putenv(key, str(value))


def update_virtuelenv(app):
    pip_path = os.path.join(virtualenv, "bin", "pip")
    print("Updating virtualenv with required packages. This can take a while...")
    app.run("{} install -r '{}/requirements.txt'".format(pip_path, app.target))


def manage_py(app, cmdline="", output=False):
    manage_path = app.full_path("manage.py")
    db_vars = " ".join(["{}='{}'".format(k, v) for k, v in app.environment.items() if k.startswith("DB_")])
    return app.run("{db_vars} {python} '{managepy}' {cmdline}".format(db_vars=db_vars, python=python,
                                                     managepy=manage_path, cmdline=cmdline),
            output=output)


def collectstatic(app):
    manage_py(app, "collectstatic --noinput")


def syncdb(app):
    manage_py(app, "syncdb --noinput")


def supports_migrations(app):
    help_text = manage_py(app, output=True)
    return "schemamigration" in help_text


def migrate(app):
    if supports_migrations(app):
        print("Found South migrations support. Migrating database...")
        manage_py(app, "migrate --noinput")
    else:
        print("No South migrations found.")



def deploy(app):
    print("Deploying a Django app...")
    update_environment(app)
    update_virtuelenv(app)
    update_django_settings(app)
    collectstatic(app)
    syncdb(app)
    migrate(app)
    app.restart()


def server_command(app):
    executable = os.path.join(virtualenv, "bin", "gunicorn_django")
    process_name = "gunicorn_django"
    return (None, executable, [process_name, "--config=/etc/stackful/gunicorn.conf.py"])
