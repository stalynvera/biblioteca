from django.shortcuts import render
from django.http import JsonResponse
from .models import libros

def lista_libros(request):
    # Obtener todos los libros y serializarlos en formato JSON
    libros_queryset = libros.objects.all().values()  # Obtiene todos los libros
    return JsonResponse(list(libros_queryset), safe=False)  # Devuelve los datos en formato JSON
