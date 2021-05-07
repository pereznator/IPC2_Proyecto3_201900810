import re

class Automata:

    def verEntrada(self, nombre):
        self.entrada = ''

        with open('media/'+nombre) as entrada:
            texto = entrada.read()
            for x in range(len(texto) - 1):
                if not texto[x] in ('<', '>', '\"'):
                    self.entrada = self.entrada + texto[x]
                else:    
                    try:
                        if texto[x+1] in ('E', '/'):
                            self.entrada = self.entrada + texto[x]
                        elif texto[x-1] in ('O', 'S'):
                            self.entrada = self.entrada + texto[x]
                    except:
                        pass


    def afd(self, texto):
        '''with open('media/'+self.nombre) as doc:
            lineas = doc.readlines()
            contenido = []
            for linea in lineas:
                lin = ''
                for x in range(len(linea)):
                    if not linea[x] in ('\t', '\n', '<', '>', '\"'):
                        lin = lin + linea[x]
                palabras = re.split(' ', lin)

                for pal in palabras:
                    contenido.append(pal)'''
        contenido = []
        for linea in re.split('\n', texto):
            lin = ''
            for x in range(len(linea)):
                if not linea[x] in ('\t', '\r'):
                    lin = lin + linea[x]
            palabras = re.split(' ', lin)
            for pal in palabras:
                contenido.append(pal)

        enEvento = False
        eventos = []
        e = 0
        evento = {"fecha": "", "reportadoPor": "", "usuariosAfectados": [], "error": "", "codigo": ""}
        for x in range(len(contenido)):
            if enEvento:
                if e == 0:
                    if not contenido[x] in ("Reportado"):
                        if not contenido[x] in ("Guatemala,"):
                            evento["fecha"] = evento["fecha"] + contenido[x]
                    else:
                        e = 1
                elif e == 1:
                    if not contenido[x] in ("Usuarios"):
                        if not contenido[x] in ("por:"):
                            evento["reportadoPor"] = contenido[x]
                    else:
                        e = 2
                elif e == 2:
                    if not contenido[x] in ("Error:"):
                        if not contenido[x] in ("afectados:"):
                            afectado = ''
                            for i in range(len(contenido[x])):
                                if not contenido[x][i] in (','):
                                    afectado = afectado + contenido[x][i]
                            evento["usuariosAfectados"].append(afectado)
                    else:
                        e = 3
                elif e == 3:
                    if not contenido[x] in ("-"):
                        evento["codigo"] = contenido[x]
                    else:
                        e = 4
                elif e == 4:
                    if not contenido[x] in ("</EVENTO>"):
                        evento["error"] = evento["error"] + " " + contenido[x]
                    else:
                        e = 0
                        enEvento = False
                        eventos.append(evento)
                        evento = {"fecha": "", "reportadoPor": "", "usuariosAfectados": [], "error": ""}

            else:
                if contenido[x] in ("<EVENTO>"):
                    enEvento = True
        return eventos
                


                     
