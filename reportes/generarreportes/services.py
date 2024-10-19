from reportes.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def send_email(receptor,responsable,fecha,concepto):
    subject = f"{responsable} Pago {concepto} de {fecha} "
    message = 'Su pago debe ser realizado prontamente'
    recepient = receptor
    send_mail(subject, message, EMAIL_HOST_USER, [recepient])