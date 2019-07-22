from flask import Flask, escape, request

class CwRestController():
    #def __init__(self):
    app = Flask(__name__)

    @app.route('/helloworld')
    def hello(self):
        name = request.args.get("name", "World")
        return 'Hello, World!'
