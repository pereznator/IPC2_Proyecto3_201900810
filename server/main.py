from flask import Flask, request
from flask_restful import Api, Resource

from controllers.resource import Usuario
from controllers.estadistica import Estadistica

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.rutas()
        if __name__ == "__main__":
            self.app.run(debug=True)

    def rutas(self):
        self.api.add_resource(Estadistica, "/estadistica")
        self.api.add_resource(Usuario, "/usuario/<string:nombre>")

m = Main()