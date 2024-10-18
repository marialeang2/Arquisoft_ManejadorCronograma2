from django.shortcuts import render
from django.http import HttpResponse
from reportes.logic import logic_cronogramas, logic_pagos
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportes.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return HttpResponse("Hello world Django views")

def formulario_view(request):
    #if request.method == 'GET':
    #    id = request.GET.get("id", None)
    #    variables_dto = gl.getCursos()
    #    variables = serializers.serialize('json', variables_dto)
    #    return HttpResponse(variables, 'application/json')
    return render(request, 'pagina.html')
@csrf_exempt
def generar_lista_correos (request):
     if request.method == 'GET':
      data = request.GET
      anioCronograma = request.GET.get('anio', '2024')
      nombreCronograma = request.GET.get('nombrecronograma', 'Cronograma Matemáticas 2024')
      fecha_pago = request.GET.get('fecha_pago', '2024-01-01')
      
      cronograma = logic_cronogramas.traerCronograma(anioCronograma, nombreCronograma)
      pagos = logic_pagos.traerPagos(cronograma.id, fecha_pago)
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
         fecha = pago.fecha
         concepto = pago.nombre

         send_email(correo,responsable,fecha,concepto)

         correos.append(correo)
         pdf.drawString(100, y, f"Nombre: {responsable} Fecha: {correo} ")
         y -= 20  

         if y < 100:  
          pdf.showPage()
          pdf.setFont("Times_Roman", 12)
          y = 800

      pdf.save()
      return response

def send_email(receptor,responsable,fecha,concepto):
    subject = f"{responsable} Pago {concepto} de {fecha} "
    message = 'Su pago debe ser realizado prontamente'
    recepient = receptor
    send_mail(subject, message, EMAIL_HOST_USER, [recepient])


     
     