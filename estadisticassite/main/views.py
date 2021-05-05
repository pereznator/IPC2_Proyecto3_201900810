from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import requests
from lxml import etree
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET
from main.afd import Automata

url = 'http://127.0.0.1:5000/'

def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def home_view(request):
    cargar = {"cargado": False, "archivo": '', "error": False, "procesado": False}
    if request.method == 'POST':
        archivo = request.FILES['doc']
        if os.path.splitext(archivo.name)[1] == '.xml':
            cargar['archivo'] = archivo
            eventos = {"eventos": []}
            fs = FileSystemStorage()
            name = fs.save(archivo.name, archivo)
            aut = Automata(name)
            cuerpo = {"eventos": aut.eventos}
            print(cuerpo)
            respuesta = requests.post(url+'estadistica', json=cuerpo)
            print(respuesta.json())
            cargar['cargado'] = True
            mensaje = respuesta.json()
            if mensaje['mensaje'] == 'Exito':
                cargar['procesado'] = True
        else:
            cargar['error'] = True

    return render(request, 'home.html', cargar)

def peticiones_view(request):
    context = {"general": True, "porFecha": False, "porError": False}
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
    if context['general']:
        est = requests.get(url+'estadistica')
    return render(request, 'peticiones.html', context)

def ayuda_view(request):
    return render(request, 'ayuda.html', {})

