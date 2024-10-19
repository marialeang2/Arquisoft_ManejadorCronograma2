from generarreportes.models import Cronograma, Pago
from datetime import timedelta
from django.utils import timezone

def traerCronograma(anio,nombre):
    cronograma = Cronograma.objects.get(nombre=nombre)
    return cronograma

def cronogramaPagos( ):
    hoy = timezone.now().date()
    fecha_limite = hoy + timedelta(days=2)
    pagos_proximos = Pago.objects.filter(fecha__range=[hoy, fecha_limite]).all()
    return pagos_proximos