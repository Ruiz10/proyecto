
# Create your views here.

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Cliente, Mesa, Reserva
from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponseRedirect

#Vista Home del proyecto
def redirect_to_api(request):
    return HttpResponseRedirect(('/api/cliente/'))

# vistas para Cliente
class ClienteListView(ListView):
    model = Cliente
    template_name = 'Cliente/list.html' # Url de referencia
    context_object_name = 'clientes'

class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'Cliente/detail.html' # Url de referencia
    context_object_name = 'cliente'

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'Cliente/create.html' # Formulario que se debe llenar
    fields = ['nombre', 'email', 'telefono'] # Al crear se devuelve a cliente_list
    success_url = reverse_lazy('cliente_list')

class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'Cliente/update.html' # Formulario que se debe actualizar
    fields = ['nombre', 'email', 'telefono']
    success_url = reverse_lazy('cliente_list')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'Cliente/delete.html'
    success_url = reverse_lazy('cliente_list')

# Vistas basadas en clases para Mesa

class MesaListView(ListView):
    model = Mesa
    template_name = 'Mesa/list.html'
    context_object_name = 'mesas'

class MesaDetailView(DetailView):
    model = Mesa
    template_name = 'Mesa/detail.html'
    context_object_name = 'mesa'

class MesaCreateView(CreateView):
    model = Mesa
    template_name = 'Mesa/create.html'
    fields = ['numero_mesa', 'capacidad']
    success_url = reverse_lazy('mesa_list')

    def form_invalid(self, form):
        print("Errores en el formulario:", form.errors)
        return super().form_invalid(form)

class MesaUpdateView(UpdateView):
    model = Mesa
    template_name = 'Mesa/update.html'
    fields = ['numero_mesa', 'capacidad']  # Formulario que rellenar
    success_url = reverse_lazy('mesa_list')

class MesaDeleteView(DeleteView):
    model = Mesa
    template_name = 'Mesa/delete.html'
    success_url = reverse_lazy('mesa_list')

# Vistas basadas en clases para Reserva


class ReservaListView(ListView):
    model = Reserva
    template_name = 'Reserva/list.html'
    context_object_name = 'reservas'

class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'Reserva/detail.html'
    context_object_name = 'reserva'

class ReservaUpdateView(UpdateView):
    def get(self, request, pk):
        # Obtener la reserva por su ID (pk)
        reserva = get_object_or_404(Reserva, pk=pk)
        clientes = Cliente.objects.all()
        mesas = Mesa.objects.all()

        return render(request, 'Reserva/update.html', {
            'reserva': reserva,
            'clientes': clientes,
            'mesas': mesas,
        })

    def post(self, request, pk):
        # Obtener la reserva por su ID (pk)
        reserva = get_object_or_404(Reserva, pk=pk)
        clientes = Cliente.objects.all()
        mesas = Mesa.objects.all()

        # Obtener datos enviados por el formulario
        cliente_id = request.POST.get('cliente')
        mesa_id = request.POST.get('mesa')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Validar datos
        if not cliente_id or not mesa_id or not fecha or not hora:
            return render(request, 'Reserva/update.html', {
                'reserva': reserva,
                'clientes': clientes,
                'mesas': mesas,
                'error': "Todos los campos son obligatorios.",
            })

        # Actualizar los datos de la reserva
        reserva.cliente_id = cliente_id  # Asignar ID del cliente
        reserva.mesa_id = mesa_id  # Asignar ID de la mesa
        reserva.fecha = fecha
        reserva.hora = hora
        reserva.save()

        # Redirigir a la lista de reservas
        return redirect('reserva_list')


class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = 'Reserva/delete.html'
    success_url = reverse_lazy('reserva_list')

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'mesa', 'fecha', 'hora']

    # Añadir los detalles adicionales del cliente en el formulario
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),  # Traer todos los Clientes
        label="Cliente",
        widget=forms.Select(
            attrs={'class': 'form-control'}  # Seleccionar Cliente
        )
    )

    # Personalizar mejor los campos
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lógica para mostrar email y teléfono
        for field in self.fields['cliente'].queryset:
            self.fields['cliente'].queryset = self.fields['cliente'].queryset.annotate(
                full_name=field.nombre + ' (' + field.email + ' - ' + field.telefono + ')'
            )

class ReservaCreateView(View):
    def get(self, request):
        # Obtener todos los clientes y mesas
        clientes = Cliente.objects.all()
        mesas = Mesa.objects.all()
        return render(request, 'Reserva/create.html', {
            'clientes': clientes,
            'mesas': mesas,
        })

    def post(self, request):
        # Obtener todos los clientes y mesas de nuevo
        clientes = Cliente.objects.all()
        mesas = Mesa.objects.all()

        # Capturar datos del formulario
        cliente_id = request.POST.get('cliente')
        mesa_id = request.POST.get('mesa')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Validar campos vacíos
        if not cliente_id or not mesa_id or not fecha or not hora:
            return render(request, 'Reserva/create.html', {
                'clientes': clientes,
                'mesas': mesas,
                'error': "Todos los campos son obligatorios.",
                'fecha': fecha,
                'hora': hora,
                'cliente_seleccionado': cliente_id,
                'mesa_seleccionada': mesa_id,
            })

        # Validar fecha (no en el pasado)
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha < datetime.now().date():
                raise ValueError("La fecha no puede ser en el pasado.")
        except ValueError as e:
            return render(request, 'Reserva/create.html', {
                'clientes': clientes,
                'mesas': mesas,
                'error': str(e),
                'fecha': fecha,
                'hora': hora,
                'cliente_seleccionado': cliente_id,
                'mesa_seleccionada': mesa_id,
            })

        # Validar hora
        try:
            hora = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            return render(request, 'Reserva/create.html', {
                'clientes': clientes,
                'mesas': mesas,
                'error': "Hora no válida.",
                'fecha': fecha,
                'hora': hora,
                'cliente_seleccionado': cliente_id,
                'mesa_seleccionada': mesa_id,
            })

        # Obtener cliente y mesa por ID
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            mesa = Mesa.objects.get(id=mesa_id)
        except Cliente.DoesNotExist:
            return render(request, 'Reserva/create.html', {
                'clientes': clientes,
                'mesas': mesas,
                'error': "Cliente no encontrado.",
                'fecha': fecha,
                'hora': hora,
                'cliente_seleccionado': cliente_id,
                'mesa_seleccionada': mesa_id,
            })
        except Mesa.DoesNotExist:
            return render(request, 'Reserva/create.html', {
                'clientes': clientes,
                'mesas': mesas,
                'error': "Mesa no encontrada.",
                'fecha': fecha,
                'hora': hora,
                'cliente_seleccionado': cliente_id,
                'mesa_seleccionada': mesa_id,
            })

        # Crear la reserva
        reserva = Reserva(cliente=cliente, mesa=mesa, fecha=fecha, hora=hora)
        reserva.save()

        # Redirigir al listado
        return redirect('reserva_list')