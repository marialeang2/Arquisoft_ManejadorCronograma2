from django.shortcuts import render
from django.http import HttpResponse
from reportes.logic import logic_reportes
from django.core import serializers


def home(request):
    return HttpResponse("Hello world Django views")

def buscarReporteId(request,pk):
    if request.method == 'GET':
        reporte = logic_reportes.get_reporte(pk)
        #reporte_dto = serializers.serialize('json',reporte)
        return HttpResponse(reporte, 'aplication/json')