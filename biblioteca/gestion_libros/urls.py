from django.urls import path
from .views import lista_libros

urlpatterns = [
    path('api/libros/', lista_libros, name='lista_libros'),
]
