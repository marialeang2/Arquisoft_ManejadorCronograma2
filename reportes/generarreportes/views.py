from django.shortcuts import render
from django.http import HttpResponse
from reportes.logic import logic_reportes
from django.core import serializers
from generarreportes.models import Reporte, Estudiante, Pago
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def home(request):
    return HttpResponse("Hello world Django views")

def buscarReporteId(request,pk):
   
    if request.method == 'GET':
        pagos = logic_reportes.get_reporte(pk)
        
        return HttpResponse(pagos, 'aplication/json')
    

def generar_reporte(request, nombre_estudiante):
    # Buscar el estudiante por su nombre
    estudiante = get_object_or_404(Estudiante, nombre=nombre_estudiante)

    # Obtener todos los pagos relacionados a ese estudiante
    pagos = Pago.objects.filter(estudiante=estudiante)

    # Si quieres guardar un nuevo reporte con estos pagos
    reporte = Reporte.objects.create(nombre=f'Reporte de {estudiante.nombre}',tipo='Pase y salvo',ruta='hola')
    reporte.pago.set(pagos)  # Asociar los pagos al reporte

    # Preparar los datos para la respuesta JSON
    pagos_data = [{'fecha_pago': pago.fecha, 'nombre': pago.nombre} for pago in pagos]

    reporte_data = {
        'reporte': reporte.nombre,
        'estudiante': estudiante.nombre,
        'pagos': pagos_data
    }

    # Retornar el reporte como JSON
    return JsonResponse(reporte_data)