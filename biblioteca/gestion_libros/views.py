from django.shortcuts import render
from django.http import JsonResponse
from .models import libros  # Asegúrate de usar la ruta correcta para el modelo

def lista_libros(request):
    libros_queryset = libros.objects.all().values()
    return JsonResponse(list(libros_queryset), safe=False)
 