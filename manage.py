#!/usr/bin/env python

from flask.ext.script import Manager

from dialtone.app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def init():
    pass


if __name__ == "__main__":
    manager.run()
