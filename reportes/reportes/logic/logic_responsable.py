from generarreportes.models import Responsablef

def traerPagos():
    pagos = Pago.objects.filter(cronograma = Cronograma)
    return pagos