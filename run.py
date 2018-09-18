from flask import Flask, request
from flask_restful import Resource, Api
import led

app = Flask(__name__)
api = Api(app)

api.add_resource(led.ChangeColor, "/changeColor/<string:color>")
api.add_resource(led.Brightness, "/brightness/<int:percent>")
api.add_resource(led.SwitchOn, "/switchOn")
api.add_resource(led.SwitchOff, "/switchOff")
api.add_resource(led.Status, "/status")
api.add_resource(led.HtmlColor, "/htmlColor/<string:color>")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4040, debug=True);
