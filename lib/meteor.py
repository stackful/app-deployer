# curl https://install.meteor.com | /bin/sh

def detect(app):
    return app.has_file(".meteor")
