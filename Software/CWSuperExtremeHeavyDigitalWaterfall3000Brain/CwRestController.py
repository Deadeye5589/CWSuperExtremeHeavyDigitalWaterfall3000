import string

from flask import Flask, Response, request

from Settings import Settings


class CwRestController():

    def __init__(self):
        self.app = FlaskAppWrapper('wrap')
        self.app.add_endpoint(endpoint='/settings', endpoint_name='settings',
                              endpoint_action=EndpointAction(self.action))
        self.available_effects_endpoint_action = EndpointAction(self.available_effects)
        self.app.add_endpoint(endpoint='/available_effects', endpoint_name='available_effects',
                              endpoint_action=self.available_effects_endpoint_action)

    def run(self):
        self.app.run()

    def action(self):
        Settings.on_time = float(request.args.get('on_time'))
        Settings.off_time = float(request.args.get('off_time'))
        Settings.effect_name = request.args.get('effect_name')
        # Settings.height = float(request.args.get('height'))

    def available_effects(self):
        self.available_effects_endpoint_action.response = Response(
            response=string.join(Settings.available_effects, ";"),
            status=200,
            mimetype="text/txt",
            headers={})


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class EndpointActionWithResponse(EndpointAction):

    def __call__(self, *args):
        return self.action()


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run(threaded=True)

    # def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
    #    self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    def add_endpoint(self, endpoint=None, endpoint_name=None, endpoint_action=None):
        self.app.add_url_rule(endpoint, endpoint_name, endpoint_action)
