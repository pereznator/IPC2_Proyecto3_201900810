from flask_restful import Api, Resource, reqparse


class Usuario(Resource):

    def __init__(self):
        self.usuario_model = reqparse.RequestParser()
        self.usuario_model.add_argument("edad", type=int, help="Se necesita edad", required=True)
        self.usuario_model.add_argument("nombre", type=str, help="Se necesita nombre", required=True)
        self.usuario_model.add_argument("activo", type=bool, help="Se necesita activo", required=True)

    def get(self, nombre):
        return {"data": nombre}

    def post(self, nombre):
        return {"data": nombre}

    def put(self, nombre):
        args = self.usuario_model.parse_args()
        return {"data": args}
