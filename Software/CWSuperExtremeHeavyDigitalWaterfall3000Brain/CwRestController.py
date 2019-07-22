from flask import Flask, Response


class CwRestController():

    def __init__(self):
        self.app = FlaskAppWrapper('wrap')
        self.app.add_endpoint(endpoint='/helloworld', endpoint_name='helloworld', handler=self.action)
        self.app.run()

    def action(self):
        return 'Hello, World!'


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={}, response='Hello RTCustomz!')

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
