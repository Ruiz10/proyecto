from django.urls import path
from .views import (
    ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    MesaListView, MesaDetailView, MesaCreateView, MesaUpdateView, MesaDeleteView,
    ReservaListView, ReservaDetailView, ReservaCreateView, ReservaUpdateView, ReservaDeleteView
)
#CLIENTES URLS
urlpatterns = [
    path('cliente/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),
    path('cliente/create/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/<int:pk>/update/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/<int:pk>/delete/', ClienteDeleteView.as_view(), name='cliente_delete'),
#MESA URLS
    path('mesa/', MesaListView.as_view(), name='mesa_list'),
    path('mesa/<int:pk>/', MesaDetailView.as_view(), name='mesa_detail'),
    path('mesa/create/', MesaCreateView.as_view(), name='mesa_create'),
    path('mesa/<int:pk>/update/', MesaUpdateView.as_view(), name='mesa_update'),
    path('mesa/<int:pk>/delete/', MesaDeleteView.as_view(), name='mesa_delete'),
#RESERVA URLS
    path('reserva/', ReservaListView.as_view(), name='reserva_list'),
    path('reserva/<int:pk>/', ReservaDetailView.as_view(), name='reserva_detail'),
    path('reserva/create/', ReservaCreateView.as_view(), name='reserva_create'),
    path('reserva/<int:pk>/update/', ReservaUpdateView.as_view(), name='reserva_update'),
    path('reserva/<int:pk>/delete/', ReservaDeleteView.as_view(), name='reserva_delete'),
]
