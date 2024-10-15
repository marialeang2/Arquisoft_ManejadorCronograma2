from generarreportes.models import Pago

def traerPagos(Cronograma, fecha):
    pagos = Pago.objects.filter(cronograma = Cronograma, fecha = fecha)
    return pagos