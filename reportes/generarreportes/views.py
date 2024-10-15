from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from reportes.logic import logic_reportes
from django.core import serializers
from generarreportes.models import Reporte, Estudiante, Pago
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from reportes.logic import logic_cronogramas, logic_pagos
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def home(request):
    return HttpResponse("Hello world Django views")

#def formulario_view(request):
    #if request.method == 'GET':
    #    id = request.GET.get("id", None)
    #    variables_dto = gl.getCursos()
    #    variables = serializers.serialize('json', variables_dto)
    #    return HttpResponse(variables, 'application/json')
    #return render(request, 'consulta.html')

def generar_lista_correos (anioCronograma, nombreCronograma):
     cronograma = logic_cronogramas.traerCronograma(anioCronograma, nombreCronograma)
     pagos = logic_pagos.traerPagos(cronograma)
     correos = []
     
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'inline; filename="estado_de_cuenta.pdf"'
     
     pdf = canvas.Canvas(response, pagesize=A4)
     pdf.setTitle("Correos Recuperados")
     pdf.setFont("Times-Bold", 16)
     pdf.drawString(100, 800, "Correos Recuperados")
     
     pdf.setFont("Times-Bold", 14)
     pdf.drawString(100, 780, "Correos:")
     pdf.setFont("Times-Roman", 10)
     y = 760
     for pago in pagos:
         correo = pago.responsableF.correo
         responsable = pago.responsableF.nombre
         correos.append(correo)
         pdf.drawString(100, y, f"Nombre: {responsable} Fecha: {correo} ")
         y -= 20  

         if y < 100:  
          pdf.showPage()
          pdf.setFont("Times_Roman", 12)
          y = 800

     pdf.save()
     return correos, response


     
     