from generarreportes.models import Reporte
def get_reporte(rep_pk):
    reporte = Reporte.objects.get(pk = rep_pk)
    return reporte 