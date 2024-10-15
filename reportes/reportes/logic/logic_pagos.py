from generarreportes.models import Pago

def traerPagos(Cronograma):
    pagos = Pago.objects.filter(cronograma = Cronograma)
    return pagos