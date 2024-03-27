from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.forms import inlineformset_factory

from distribution.forms import MessageForm, MailingSettingsForm, ClientForm
from distribution.models import Client, MailingSettings, Message, Log


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('distribution:clients_list')

    def test_func(self):
        return self.request.user.is_content_manager or self.request.user.is_superuser


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('distribution:clients_list')

    def test_func(self):
        return self.request.user.is_content_manager or self.request.user.is_superuser


class MailingSettingsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailingSettings

    def test_func(self):
        mailing_settings = self.get_object()
        return self.request.user.is_content_manager or self.request.user.is_superuser or self.request.user == mailing_settings.owner


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        user = self.request.user
        if user.is_superuser:
            context_data['all'] = MailingSettings.objects.count()
            context_data['active'] = MailingSettings.objects.filter(status=MailingSettings.STARTED).count()
            mailing_list = context_data['object_list']
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['clients_count'] = len(clients)
        else:
            mailing_list = MailingSettings.objects.filter(owner=user)
            clients = [[client.email for client in mailing.clients.all()] for mailing in mailing_list]
            context_data['all'] = mailing_list.count()
            context_data['active'] = mailing_list.filter(status=MailingSettings.STARTED).count()
            context_data['clients_count'] = len(clients)

        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('distribution:distribution_list')

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST)
        else:
            context_data['formset'] = MessageFormset()

        return context_data

    def get_success_url(self):
        return reverse('distribution:distribution_list')


class MailingSettingsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingSettings

    def test_func(self):
        mailing_settings = self.get_object()
        return self.request.user.is_content_manager or self.request.user.is_superuser or self.request.user == mailing_settings.owner

    def get_success_url(self):
        return reverse('distribution:distribution_list')


class MailingSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessageFormset = inlineformset_factory(MailingSettings, Message, extra=1, form=MessageForm)

        if self.request.method == 'POST':
            context_data['formset'] = MessageFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MessageFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('distribution:distribution_detail', args=[self.object.pk])


class LogListView(LoginRequiredMixin, ListView):
    model = Log

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        mailing_list = MailingSettings.objects.filter(owner=user).first()
        if user.is_superuser or user.is_content_manager:
            context_data['all'] = Log.objects.count()
            context_data['success'] = Log.objects.filter(
                status=True).count()
            context_data['error'] = Log.objects.filter(status=False).count()
        else:
            user_logs = Log.objects.filter(mailing_list=mailing_list)
            context_data['all'] = user_logs.count()
            context_data['success'] = user_logs.filter(
                status=True).count()
            context_data['error'] = user_logs.filter(status=False).count()
        return context_data
