from flask import Flask, Response, request

from Settings import Settings


class CwRestController():

    def __init__(self):
        self.app = FlaskAppWrapper('wrap')
        self.app.add_endpoint(endpoint='/settings', endpoint_name='settings',
                              endpoint_action=EndpointAction(self.action))
        self.app.add_endpoint(endpoint='/available_effects', endpoint_name='available_effects',
                              endpoint_action=EndpointActionWithResponse(self.available_effects))
        self.app.add_endpoint(endpoint='/current_settings', endpoint_name='current_settings',
                              endpoint_action=EndpointActionWithResponse(self.current_settings))

    def run(self):
        self.app.run()

    def action(self):
        on_time = request.args.get('on_time')
        off_time = request.args.get('off_time')
        effect_name = request.args.get('effect_name')
        off_time_pause = request.args.get('off_time_pause')

        Settings.on_time = float(on_time) if on_time is not None else Settings.on_time
        Settings.off_time = float(off_time) if off_time is not None else Settings.off_time
        Settings.off_time_pause = float(off_time_pause) if off_time_pause is not None else Settings.off_time_pause

        if effect_name is not None:
            Settings.load_effect(effect_name)
        # Settings.height = float(request.args.get('height'))

    def available_effects(self):
        return Response(
            # response=string.join(Settings.available_effects, ";"),
            response=Settings.available_effects_to_json(),
            status=200,
            mimetype="application/json",
            headers={})

    def current_settings(self):
        return Response(
            response=Settings.to_json(),
            status=200,
            mimetype="application/json",
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
