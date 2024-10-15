from generarreportes.models import Cronograma

def traerCronograma(anio,nombre):
    cronograma = Cronograma.objects.filter(nombre=nombre,anio=anio)
    return cronograma
    