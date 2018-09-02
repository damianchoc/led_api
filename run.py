from flask import Flask, request
from flask_restful import Resource, Api
import led

app = Flask(__name__)
api = Api(app)

api.add_resource(led.Test, "/")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=4040, debug=True);
