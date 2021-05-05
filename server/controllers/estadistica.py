from flask_restful import Api, Resource, reqparse
import xml.etree.ElementTree as ET
import xml.dom.minidom
from os import path
import ast

class Estadistica(Resource):

    def __init__(self):

        self.est_post = reqparse.RequestParser()
        self.est_post.add_argument("eventos", action='append',help="Se necesita ruta", required=True)

    def get(self):
        return {"data": "nom"}

    def post(self):
        try:
            args = self.est_post.parse_args()
            base = path.dirname(__file__)
            ruta = path.abspath(path.join(base, '..', '..', 'estadisticas.xml'))
            doc = ET.parse(ruta)
            raiz = doc.getroot()
            eventos = []
            
            for evento in args['eventos']:
                eventos.append(ast.literal_eval(evento))

            for evento in eventos:
                fechaRepetida = False
                for estadistica in raiz.findall('ESTADISTICA'):
                    fecha = evento['fecha']
                    nf = estadistica.find('FECHA').text
                    if fecha in nf:
                        print(fecha+ ' es igual a '+ nf)
                        fechaRepetida = True
                        estadistica.find('CANTIDAD_MENSAJES').text = str(int(estadistica.find('CANTIDAD_MENSAJES').text) + 1)
                        
                        usuarios = estadistica.find('REPORTADO_POR')
                        usuarioRepetido = False
                        for usuario in usuarios.findall('USUARIO'):
                            if usuario.find('EMIAL') == evento['reportadoPor']:
                                usuarioRepetido = True
                                usuario.find('CANTIDAD_MENSAJES').text = str(int(usuario.find('CANTIDAD_MENSAJES').text) + 1)
                        if not usuarioRepetido:
                            usuario = ET.SubElement(usuarios, 'USUARIO')
                            email = ET.SubElement(usuario, 'EMAIL')
                            email.text = evento['reportadoPor']
                            cantidad = ET.SubElement(usuario, 'CANTIDAD_MENSAJES')
                            cantidad.text = '1'
                        
                        afectados = estadistica.find('AFECTADOS')
                        for usuario in evento['usuariosAfectados']:
                            repetido = False
                            for afectado in afectados.findall('AFECTADO'):
                                if usuario in afectado.text:
                                    repetido = True
                            if not repetido:
                                afec = ET.SubElement(afectados, 'AFECTADO')
                                afec.text = usuario
                        
                        errores = estadistica.find('ERRORES')
                        errorRepetido = False
                        for error in errores.findall('ERROR'):
                            evento_codigo = evento['codigo']
                            estadistica_codigo = error.find('CODIGO').text
                            if evento_codigo in estadistica_codigo:
                                error.find('CANTIDAD_MENSAJES').text = str(int(error.find('CANTIDAD_MENSAJES').text) + 1)
                                errorRepetido = True
                        if not errorRepetido:
                            error = ET.SubElement(errores, 'ERROR')
                            codigo = ET.SubElement(error, 'CODIGO')
                            codigo.text = evento['codigo']
                            cantidad = ET.SubElement(error, 'CANTIDAD_MENSAJES')
                            cantidad.text = '1'
                            
                if not fechaRepetida:
                    nuevaEstadistica = ET.SubElement(raiz, 'ESTADISTICA')
                    fecha = ET.SubElement(nuevaEstadistica, 'FECHA')
                    fecha.text = evento['fecha']

                    cantidad_mensajes = ET.SubElement(nuevaEstadistica, 'CANTIDAD_MENSAJES')
                    cantidad_mensajes.text = '1'

                    reportado_por = ET.SubElement(nuevaEstadistica, 'REPORTADO_POR')
                    usuario = ET.SubElement(reportado_por, 'USUARIO')
                    email = ET.SubElement(usuario, 'EMAIL')
                    email.text = evento['reportadoPor']
                    cantidad_usuario = ET.SubElement(usuario, 'CANTIDAD_MENSAJES')
                    cantidad_usuario.text = '1'

                    afectados = ET.SubElement(nuevaEstadistica, 'AFECTADOS')
                    for afectado in evento['usuariosAfectados']:
                        aff = ET.SubElement(afectados, 'AFECTADO')
                        aff.text = afectado

                    errores = ET.SubElement(nuevaEstadistica, 'ERRORES')
                    error = ET.SubElement(errores, 'ERROR')
                    codigo = ET.SubElement(error, 'CODIGO')
                    codigo.text = evento['codigo']
                    cantidad_error = ET.SubElement(error, 'CANTIDAD_MENSAJES')
                    cantidad_error.text = '1'

            dataString = ET.tostring(raiz)
            data = dataString.decode('utf-8')
            final = ''
            aux = False
            for x in range(len(data)):
                final = final + data[x]
                if data[x] in ('/'):
                    aux = True
                if aux == True and data[x] in ('>'):
                    try:
                        if not data[x+1] in ('\n'):
                            final = final + '\n'
                    except:
                        pass
                    aux = False

            with open(ruta, 'w') as newFile:
                newFile.write(final)

            with open('contenido.txt', 'w') as cont:
                cont.write(final)

            return {"mensaje": "Exito"}
        except:
            return {"mensaje": "Error"}

    def put(self, nombre):
        return {"data": "la data"}
