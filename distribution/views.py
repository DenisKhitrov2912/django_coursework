from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from pytils.translit import slugify

from .models import Clients, Message, DistributionParams, TrySending

from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView


class ClientsCreateView(CreateView):
    model = Clients
    fields = (
        'email', 'name', 'surname', 'patronymic', 'comment',)
    success_url = reverse_lazy('distribution:clients')


class ClientsDetailView(DetailView):
    model = Clients


class ClientsListView(ListView):
    model = Clients
    template_name = 'distribution/clients_list.html'


class ClientsUpdateView(UpdateView):
    model = Clients
    fields = (
        'email', 'name', 'surname', 'patronymic', 'comment',)
    success_url = reverse_lazy('distribution:clients')


class ClientsDeleteView(DeleteView):
    model = Clients
    success_url = reverse_lazy('distribution:clients')


class MessageCreateView(CreateView):
    model = Message
    fields = (
        'theme', 'message',)
    success_url = reverse_lazy('distribution:messages')


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message
    template_name = 'distribution/message_list.html'


class MessageUpdateView(UpdateView):
    model = Message
    fields = (
        'theme', 'message',)
    success_url = reverse_lazy('distribution:messages')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('distribution:messages')


class DistParamsCreateView(CreateView):
    model = DistributionParams
    fields = (
        'date', 'date_end', 'time', 'time_end', 'period',)
    success_url = reverse_lazy('distribution:clients_list')


class DistParamsDetailView(DetailView):
    model = DistributionParams


class DistParamsListView(ListView):
    model = DistributionParams
    template_name = 'distribution/clients_list.html'


class DistParamsUpdateView(UpdateView):
    model = DistributionParams
    fields = (
        'period',)
    success_url = reverse_lazy('distribution:clients_list')


class DistParamsDeleteView(DeleteView):
    model = DistributionParams
    success_url = reverse_lazy('distribution:client_create')


class TrySendingDetailView(DetailView):
    model = TrySending


class TrySendingListView(ListView):
    model = TrySending
    template_name = 'distribution/clients_list.html'


class TrySendingDeleteView(DeleteView):
    model = TrySending
    success_url = reverse_lazy('distribution:clients_list')
