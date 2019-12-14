from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import (
    CreateView,
    FormView,
    TemplateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import (
    LoginForm,
    RegisterForm,
    UserDetailChangeForm,
    ClientCreationMultiForm,
    CompanyCreationMultiForm,
    CompanyForm,
    ClientEditMultiForm,
    CompanyEditMultiForm,
    CreateServiceForm
)
from .models import (
    User,
    Client,
    Company,
    Service
)
from .mydecorator import account_type_required


def test_redirect(request):
    return redirect(reverse_lazy('home_url'))

#---LOGIN_AND_REGISTER_VIEWS---
class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'


class ChoiceView(TemplateView):
    template_name = 'accounts/choice.html'

    def get_context_data(self, **kwargs):
        page_name = "Choice Page"

        context = {
            'page_name': page_name,
        }
        return context


class RegisterViewClient(CreateView):
    form_class = ClientCreationMultiForm
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        user = form['user'].save()
        client = form['client'].save()

        user.type = 'Client'
        client.user = user

        user.save()
        client.save()

        return redirect(reverse_lazy('login_url'))


class RegisterViewCompany(CreateView):
    form_class = CompanyCreationMultiForm
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        user = form['user'].save()
        company = form['company'].save()
        user.type = 'Company'
        company.user = user
        user.save()
        company.save()
        return redirect(reverse_lazy('login_url'))
#---LOGIN_AND_REGISTER_VIEWS---


#---INFO_VIEWS---
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "Home page"

        context = {
            'page_name': page_name,
            'user': user,
        }
        return context


@method_decorator(account_type_required(account_type = Client), name='dispatch')
class ProfileClientView(TemplateView):
    template_name = 'accounts/profile_client.html'

    def get_context_data(self, **kwargs):
        page_name = "Profile page"

        context = {
            'page_name': page_name,
            'user': self.request.user,
            'client': Client.objects.get(user=self.request.user)
        }

        return context


@method_decorator(account_type_required(account_type = Company), name='dispatch')
class ProfileCompanyView(TemplateView):
    template_name = 'accounts/profile_company.html'

    def get_context_data(self, **kwargs):
        page_name = "Profile page"

        context = {
            'page_name': page_name,
            'user': self.request.user,
            'company': Company.objects.get(user=self.request.user)
        }

        return context
#---INFO_VIEWS---


#---ACCOINT_CHANGE_VIEWS---
@method_decorator(account_type_required(account_type = Client), name='dispatch')
class ClientDetailChangeView(UpdateView):
    model = User
    form_class = ClientEditMultiForm
    success_url = reverse_lazy('profile_client_url')
    template_name = 'accounts/profile_change_client.html'

    def get_form_kwargs(self):
        kwargs = super(ClientDetailChangeView, self).get_form_kwargs()
        return kwargs

    def get_object(self):
        return {
            'user': self.request.user,
            'client': Client.objects.get(user=self.request.user),
        }

    def forms_valid(self, forms):
        profile = forms['profile_form'].save(commit=False)
        profile.user = forms['user'].save(commit=False)
        profile.client = forms['client'].save(commit=False)
        profile.save()
        return super(ClientDetailChangeView, self).forms_valid(forms)

    def get_context_data(self, *args, **kwargs):
        context = super(ClientDetailChangeView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user'] = user
        context['page_name'] = "Change Account"
        return context


@method_decorator(account_type_required(account_type = Company), name='dispatch')
class CompanyDetailChangeView(UpdateView):
    model = User
    form_class = CompanyEditMultiForm
    success_url = reverse_lazy('profile_company_url')
    template_name = 'accounts/profile_change_company.html'

    def get_form_kwargs(self):
        kwargs = super(CompanyDetailChangeView, self).get_form_kwargs()
        return kwargs

    def get_object(self):
        return {
            'user': self.request.user,
            'company': Company.objects.get(user=self.request.user),
        }

    def forms_valid(self, forms):
        profile = forms['profile_form'].save(commit=False)
        profile.user = forms['user'].save(commit=False)
        profile.company = forms['company'].save(commit=False)
        profile.save()
        return super(CompanyDetailChangeView, self).forms_valid(forms)

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyDetailChangeView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user'] = user
        context['page_name'] = "Change Account"
        return context
#---ACCOINT_CHANGE_VIEWS---


#---SERVICE_VIEWS---
@method_decorator(account_type_required(account_type = Company), name='dispatch')
class ServiceCreateView(CreateView):
    form_class = CreateServiceForm
    success_url = '/profile/'
    template_name = 'accounts/create_service.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceCreateView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user'] = user
        context['page_name'] = "Create Service"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = Company.objects.get(user=self.request.user)
        return super(ServiceCreateView, self).form_valid(form)


@method_decorator(account_type_required(account_type = Company), name='dispatch')
class MyServiceListView(TemplateView):
    template_name = 'accounts/service_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "Service List"
        services = Service.objects.all().filter(user=self.request.user)
        print(services)
        """if str(services) == "<QuerySet []>":
            Service.objects.create_example_service(user=self.request.user, company = Company.objects.get(user=self.request.user))
        services = Service.objects.all().filter(user=self.request.user)"""
        context = {
            'page_name': page_name,
            'user': user,
            'services' : services,
        }
        return context

@method_decorator(account_type_required(account_type = Company), name='dispatch')
class ServiceUpdateView(UpdateView):
    form_class = CreateServiceForm
    model = Service
    success_url = '/profile/'
    template_name = 'accounts/edit_service.html'
    pk_url_kwarg = 'service'

    def dispatch(self, request, *args, **kwargs):
        service = Service.objects.get(id = self.kwargs['service'])
        if self.request.user != service.user:
            return redirect('')
        return super(ServiceDeleteView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        services = Service.objects.all().filter(user=self.request.user)
        if str(services) != "<QuerySet []>":
            print("asdsad")
            context['user'] = user
            context['page_name'] = "Edit Service"
            return context
        else:
            return None


@method_decorator(login_required, name='dispatch')
class ServiceDeleteView(DeleteView):
    form_class = CreateServiceForm
    model = Service
    success_url = '/profile/'
    template_name = 'accounts/delete_service.html'
    pk_url_kwarg = 'service'

    def get_form_kwargs(self):
        kwargs = super(ServiceDeleteView, self).get_form_kwargs()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        service = Service.objects.get(id = self.kwargs['service'])
        if self.request.user != service.user:
            return redirect('')
        return super(ServiceDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ServiceDeleteView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        services = Service.objects.all().filter(user=self.request.user)
        context['user'] = user
        context['page_name'] = "Delete Service"
        return context
#---SERVICE_VIEWS---
