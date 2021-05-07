from flask_restful import Api, Resource, reqparse
import xml.etree.ElementTree as ET
from os import path

class Fecha(Resource):

    def __init__(self):
        self.fecha_model = reqparse.RequestParser()
        self.fecha_model.add_argument("fecha", type=str, help="Se necesita fecha", required=True)

    def get(self):
        base = path.dirname(__file__)
        ruta = path.abspath(path.join(base, '..', '..', 'estadisticas.xml'))
        doc = ET.parse(ruta)
        raiz = doc.getroot()
        fechas = []
        for estadisticas in raiz.findall('ESTADISTICA'):
            fechas.append(estadisticas.find('FECHA').text)
        return {"mensaje": "exito", "fechas": fechas}

    def post(self):
        args = self.fecha_model.parse_args()
        fecha = args['fecha']
        base = path.dirname(__file__)
        ruta = path.abspath(path.join(base, '..', '..', 'estadisticas.xml'))
        doc = ET.parse(ruta)
        raiz = doc.getroot()
        usuarios = []
        mensajes = []
        for estadistica in raiz.findall('ESTADISTICA'):
            if fecha in estadistica.find('FECHA').text:
                reportados = estadistica.find('REPORTADO_POR')
                for usuario in reportados.findall('USUARIO'):
                    usuarios.append(usuario.find('EMAIL').text)
                    mensajes.append(int(usuario.find('CANTIDAD_MENSAJES').text))


        return {"mensaje": "exito", "usuarios": usuarios, "mensajes": mensajes}
