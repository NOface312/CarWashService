from django.urls import path
from .views import (
    ClientOrdersListView,
    ChoiceCompanyView,
    ChoiceServiceView,
    MakeOrderView,
    CompanyOrdersListView,
    OrderClientUpdateView,
    OrderClientDeleteView,
    OrderCompanyUpdateView,
    OrderCompanyDeleteView,
)
from . import views

from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^order/client/list/$', ClientOrdersListView.as_view(), name='client_orders_url'),
    url(r'^order/company/list/$', CompanyOrdersListView.as_view(), name='company_orders_url'),
    url(r'^company/choice/$', ChoiceCompanyView.as_view(), name='company_choice_url'),
    url(r'^(?P<company>\d+)/service/choice/$', ChoiceServiceView.as_view(), name='service_choice_url'),
    url(r'^(?P<company>\d+)/(?P<service>\d+)/service/choice/$', MakeOrderView.as_view(), name='make_order_url'),
    url(r'^order/client/delete/(?P<order>\d+)/$', OrderClientDeleteView.as_view(), name='order_client_delete_url'),
    url(r'^order/client/edit/(?P<order>\d+)/$', OrderClientUpdateView.as_view(), name='order_client_edit_url'),
    url(r'^order/client/delete/(?P<order>\d+)/$', OrderCompanyDeleteView.as_view(), name='order_company_delete_url'),
    url(r'^order/client/edit/(?P<order>\d+)/$', OrderCompanyUpdateView.as_view(), name='order_company_edit_url'),
]
