from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import random
import requests
from django.core.files.storage import FileSystemStorage
import subprocess

import matplotlib.pyplot as plt
plt.switch_backend('agg')

from main.afd import Automata

url = 'http://127.0.0.1:5000/'

def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def home_view(request):
    cargar = {"cargado": False, "archivo": '', "error": False, "procesado": False, "entrada": '', 'enviado': False}
    if request.method == 'POST':
        if 'cargar' in request.POST:
            archivo = request.FILES['doc']
            if os.path.splitext(archivo.name)[1] == '.xml':
                cargar['archivo'] = archivo
                eventos = {"eventos": []}
                fs = FileSystemStorage()
                name = fs.save(archivo.name, archivo)
                aut = Automata()
                aut.verEntrada(name)
                cargar['entrada'] = aut.entrada
                cargar['cargado'] = True
            else:
                cargar['error'] = True
        elif 'enviar' in request.POST:
            cargar['enviado'] = True
            cargar['cargado'] = True
            cargar['procesado'] = True
            cargar['entrada'] = request.POST['entrada-texto']
            aut = Automata()
            eventos = aut.afd(request.POST['entrada-texto'])
            cuerpo = {"eventos": eventos}
            respuesta = requests.post(url+'estadistica', json=cuerpo)
            print(respuesta.json())
            mensaje = respuesta.json()
            if mensaje['mensaje'] == 'Exito':
                cargar['procesado'] = True
            

    return render(request, 'home.html', cargar)

def peticiones_view(request):
    context = {"general": True, "porFecha": False, "porError": False, "textoGeneral": "", "reset": False, "fechas": [], "verFecha": False, "fechaActiva": '', "codigos": [], "verCodigo": False, "codigoActivo": ''}
    if request.method == 'POST':
        if 'general' in request.POST:
            context['general'] = True
            context['porFecha'] = False
            context['porError'] = False
        elif 'porFecha' in request.POST:
            context['general'] = False
            context['porFecha'] = True
            context['porError'] = False
        elif 'porError' in request.POST:
            context['general'] = False
            context['porFecha'] = False
            context['porError'] = True
        elif 'reset' in request.POST:
            context['reset'] = True
        elif 'verFecha' in request.POST:
            context['verFecha'] = True

            context['general'] = False
            context['porFecha'] = True
            context['porError'] = False
        elif 'verCodigo' in request.POST:
            context['verCodigo'] = True

            context['general'] = False
            context['porFecha'] = False
            context['porError'] = True
    if context['general']:
        if not context['reset']:
            est = requests.get(url+'estadistica')
            respo = est.json()
            if respo['mensaje'] == 'exito':
                context['textoGeneral'] = respo['data']
        else:
            print('Hay reset')
            est = requests.put(url+'estadistica')
            respo = est.json()
            print(respo)
            if respo['mensaje'] == 'Exito':
                context['textoGeneral'] = respo['data']
    elif context['porFecha']:
        fechasRes = requests.get(url+'fecha')
        res = fechasRes.json()
        context['fechas'] = res['fechas']
        print(res)

        if context['verFecha']:
            context['fechaActiva'] = request.POST['fechaSelect']
            fechaCuerpo = {"fecha": request.POST['fechaSelect']}
            datosRes = requests.post(url+'fecha', json=fechaCuerpo)
            datosjson = datosRes.json()
            print(datosjson)
            plt.title("Usuarios y Mensajes en "+request.POST['fechaSelect'])
            colores = []
            for x in datosjson['usuarios']:
                color = (random.random(), random.random(), random.random(),)
                colores.append(color)
            print(colores)
            plt.bar(datosjson['usuarios'], height=datosjson['mensajes'], color=colores, width=0.6)
            plt.ylabel('Cantidad de Mensajes')
            plt.xlabel('Usuarios')
            plt.savefig('multimedia/img/usuarios.jpg')
            plt.close()

    elif context['porError']:
        codigosRes = requests.get(url+'error')
        res = codigosRes.json()
        context['codigos'] = res['codigos']

        if context['verCodigo']:
            context['codigoActivo'] = request.POST['codigoSelect']
            codigoCuerpo = {"codigo": request.POST['codigoSelect']}
            datosRes = requests.post(url+'error', json=codigoCuerpo)
            datosjson = datosRes.json()
            print(datosjson)
            plt.title("Fechas y Mensajes del error "+request.POST['codigoSelect'])
            colores = []
            
            for x in datosjson['fechas']:
                color = (random.random(), random.random(), random.random(),)
                colores.append(color)
            print(colores)
            plt.bar(datosjson['fechas'], height=datosjson['mensajes'], color=colores, width=0.6)
            plt.ylabel('Cantidad de Mensajes')
            plt.xlabel('Fechas')
            plt.savefig('multimedia/img/codigos.jpg')
            plt.close()

    return render(request, 'peticiones.html', context)

def ayuda_view(request):
    base = os.path.dirname(__file__)
    ruta = os.path.abspath(os.path.join(base, '..', '..', 'documentacion.pdf'))
    if request.method == 'POST':
        subprocess.Popen([ruta], shell=True)
    return render(request, 'ayuda.html', {})

