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

#from .forms import MakeOrder
from accounts.models import (
    User,
    Company,
    Service,
    Client,
)
from .models import Order
from .forms import OrderCreatingForm
from accounts.mydecorator import account_type_required


#---ORDER_LIST_VIEWS---
@method_decorator(account_type_required(account_type = Client), name='dispatch')
class ClientOrdersListView(TemplateView):
    template_name = 'order_app/order_client_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "My orders"
        orders = Order.objects.all().filter(user=self.request.user)


        context = {
            'page_name': page_name,
            'user': user,
            'orders' : orders,
        }
        return context


@method_decorator(account_type_required(account_type = Company), name='dispatch')
class CompanyOrdersListView(TemplateView):
    template_name = 'order_app/order_company_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "Orders Control"
        try:
            orders = Order.objects.all().filter(company=Company.objects.get(user = self.request.user))
        except:
            orders = []


        context = {
            'page_name': page_name,
            'user': user,
            'orders' : orders,
        }
        return context
#---ORDER_LIST_VIEWS---


#---ORDERS_VIEWS---
@method_decorator(account_type_required(account_type = Client), name='dispatch')
class ChoiceCompanyView(TemplateView):
    template_name = 'order_app/make_order_company_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "Choice Company"
        companys = Company.objects.all()


        context = {
            'page_name': page_name,
            'user': user,
            'companys' : companys,
        }
        return context


@method_decorator(account_type_required(account_type = Client), name='dispatch')
class ChoiceServiceView(TemplateView):
    template_name = 'order_app/make_order_service_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        page_name = "Choice Company"
        services = Service.objects.all()
        company = Company.objects.get(id = self.kwargs['company'])


        context = {
            'page_name': page_name,
            'user': user,
            'services': services,
            'company' : company,
        }
        return context


@method_decorator(account_type_required(account_type = Client), name='dispatch')
class MakeOrderView(CreateView):
    form_class = OrderCreatingForm
    success_url = '/profile/'
    template_name = 'order_app/make_order.html'

    def get_form_kwargs(self):
        kwargs = super(MakeOrderView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(MakeOrderView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        page_name = "Order Confirm"
        context['user'] = self.request.user
        context['page_name'] = page_name
        return context


    def form_valid(self, form):
        order = form.save(commit=False)

        order.user = self.request.user
        order.service = Service.objects.get(id = self.kwargs['service'])
        order.company = Company.objects.get(id = self.kwargs['company'])

        order.save()

        return redirect(reverse_lazy('client_orders_url'))
#---ORDERS_VIEWS---


#---ORDERS_CLIENT_EDIT_VIEWS---
@method_decorator(account_type_required(account_type = Client), name='dispatch')
class OrderClientUpdateView(UpdateView):
    form_class = OrderCreatingForm
    model = Order
    success_url = '/profile/'
    template_name = 'order_app/order_client_edit.html'
    pk_url_kwarg = 'order'

    def get_form_kwargs(self):
        kwargs = super(OrderClientUpdateView, self).get_form_kwargs()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs['order'])
        if self.request.user != order.user:
            return redirect('')
        return super(OrderClientUpdateView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(OrderClientUpdateView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        print("asdsad")
        context['user'] = user
        context['page_name'] = "Edit Order"
        return context


@method_decorator(account_type_required(account_type = Client), name='dispatch')
class OrderClientDeleteView(DeleteView):
    form_class = OrderCreatingForm
    model = Order
    success_url = '/profile/'
    template_name = 'order_app/order_client_delete.html'
    pk_url_kwarg = 'order'

    def get_form_kwargs(self):
        kwargs = super(OrderClientDeleteView, self).get_form_kwargs()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs['order'])
        if self.request.user != order.user:
            return redirect('')
        return super(OrderClientDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(OrderClientDeleteView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user'] = user
        context['page_name'] = "Delete Order"
        return context

#---ORDERS_CLIENT_EDIT_VIEWS---



#---ORDERS_COMPANY_EDIT_VIEWS---
@method_decorator(account_type_required(account_type = Company), name='dispatch')
class OrderCompanyUpdateView(UpdateView):
    form_class = OrderCreatingForm
    model = Order
    success_url = '/profile/'
    template_name = 'order_app/order_company_edit.html'
    pk_url_kwarg = 'order'

    def get_form_kwargs(self):
        kwargs = super(OrderCompanyUpdateView, self).get_form_kwargs()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs['order'])
        if self.request.user.company != order.user.company:
            return redirect('')
        return super(OrderCompanyUpdateView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(OrderCompanyUpdateView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        print("asdsad")
        context['user'] = user
        context['page_name'] = "Edit Order"
        return context


@method_decorator(account_type_required(account_type = Company), name='dispatch')
class OrderCompanyDeleteView(DeleteView):
    form_class = OrderCreatingForm
    model = Order
    success_url = '/profile/'
    template_name = 'order_app/order_company_delete.html'
    pk_url_kwarg = 'order'

    def get_form_kwargs(self):
        kwargs = super(OrderCompanyDeleteView, self).get_form_kwargs()
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        order = Order.objects.get(id = self.kwargs['order'])
        if self.request.user.company != order.user.company:
            return redirect('')
        return super(OrderCompanyDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(OrderCompanyDeleteView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        context['user'] = user
        context['page_name'] = "Delete Order"
        return context
#---ORDERS_CLIENT_EDIT_VIEWS---
