from flask_restful import Api, Resource, reqparse
import xml.etree.ElementTree as ET
from os import path

class Error(Resource):

    def __init__(self):
        self.error_model = reqparse.RequestParser()
        self.error_model.add_argument("codigo", type=str, help="Se necesita codigo", required=True)

    def get(self):
        base = path.dirname(__file__)
        ruta = path.abspath(path.join(base, '..', '..', 'estadisticas.xml'))
        doc = ET.parse(ruta)
        raiz = doc.getroot()
        codigos = []
        for estadisticas in raiz.findall('ESTADISTICA'):
            errores = estadisticas.find('ERRORES')
            for error in errores.findall('ERROR'):
                codigos.append(error.find('CODIGO').text)
        codigos = list(dict.fromkeys(codigos))
        return {"mensaje": "exito", "codigos": codigos}

    def post(self):
        args = self.error_model.parse_args()
        print(args['codigo'])
        base = path.dirname(__file__)
        ruta = path.abspath(path.join(base, '..', '..', 'estadisticas.xml'))
        doc = ET.parse(ruta)
        raiz = doc.getroot()

        cant_mensajes = []
        fechas = []

        for estadistica in raiz.findall('ESTADISTICA'):
            errores = estadistica.find('ERRORES')
            for error in errores.findall('ERROR'):
                if args['codigo'] in error.find('CODIGO').text:
                    cant_mensajes.append(int(error.find('CANTIDAD_MENSAJES').text))
                    fechas.append(estadistica.find('FECHA').text)
        return {"mensaje": "exito", "fechas": fechas, "mensajes": cant_mensajes}

