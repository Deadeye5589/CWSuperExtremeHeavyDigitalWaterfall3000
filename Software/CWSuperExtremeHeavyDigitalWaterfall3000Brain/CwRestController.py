from flask import Flask, Response, request

from Settings import Settings


class CwRestController():

    def __init__(self):
        self.app = FlaskAppWrapper('wrap')
        self.app.add_endpoint(endpoint='/set_timing', endpoint_name='set_timing', handler=self.action)

    def run(self):
        self.app.run()

    def action(self):
        Settings.on_time = float(request.args.get('on_time'))
        Settings.off_time = float(request.args.get('off_time'))


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))
