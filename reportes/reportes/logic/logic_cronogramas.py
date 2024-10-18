from generarreportes.models import Cronograma

def traerCronograma(anio,nombre):
    cronograma = Cronograma.objects.get(nombre=nombre)
    return cronograma
    