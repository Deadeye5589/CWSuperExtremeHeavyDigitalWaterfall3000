from flask import Flask, Response, request

from CwEffect import CwEffect


class CwRestController:

    def __init__(self, queue):
        self.queue = queue
        self.app = FlaskAppWrapper('wrap')
        self.app.add_endpoint(endpoint='/change_effect', endpoint_name='change_effect',
                              endpoint_action=EndpointAction(self.change_effect))
        ''''self.app.add_endpoint(endpoint='/available_effects', endpoint_name='available_effects',
                              endpoint_action=EndpointActionWithResponse(self.available_effects))
        self.app.add_endpoint(endpoint='/current_settings', endpoint_name='current_settings',
                              endpoint_action=EndpointActionWithResponse(self.current_settings))'''

    def run(self):
        self.app.run()

    def to_float(self, value):
        if value is not None:
            return float(value)
        else:
            return None

    def change_effect(self):
        effect = CwEffect()
        effect.on_time = self.to_float(request.args.get('on_time'))
        effect.off_time = self.to_float(request.args.get('off_time'))
        effect.off_time_pause = self.to_float(request.args.get('off_time_pause'))
        effect.effect_name = request.args.get('effect_name')
        self.queue.put(effect)

    '''@staticmethod
    def to_json():
        return '{"off_time": ' + str(
            Settings.off_time) + ',' + '"on_time": ' + str(
            Settings.on_time) + ',' + '"effect_name": "' + Settings.effect_name + '"}'

    @staticmethod
    def available_effects_to_json():
        return '["' + string.join(Settings.available_effects, '","') + '"]'

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
            
            '''


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

    def add_endpoint(self, endpoint=None, endpoint_name=None, endpoint_action=None):
        self.app.add_url_rule(endpoint, endpoint_name, endpoint_action)
