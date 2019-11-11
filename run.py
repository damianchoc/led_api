from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import led

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(led.change_color, "/changeColor/<string:color>")
api.add_resource(led.brightness, "/brightness/<int:percent>")
api.add_resource(led.switch_on, "/switchOn")
api.add_resource(led.switch_off, "/switchOff")
api.add_resource(led.status, "/status")
api.add_resource(led.get_color, "/getColor")
api.add_resource(led.html_color, "/htmlColor/<string:color>")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4040, debug=True);
