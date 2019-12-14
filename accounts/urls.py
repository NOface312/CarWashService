from django.urls import path
from .views import (
    LoginView,
    RegisterViewClient,
    RegisterViewCompany,
    ClientDetailChangeView,
    CompanyDetailChangeView,
    ProfileClientView,
    ProfileCompanyView,
    HomeView,
    ChoiceView,
    ServiceCreateView,
    MyServiceListView,
    ServiceUpdateView,
    ServiceDeleteView,
)
from . import views

from django.conf.urls import url, include
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic import TemplateView

urlpatterns = [
    #---LOGIN_AND_REGISTER_URLS---
    url(r'^login/$', LoginView.as_view(template_name='accounts/login.html'), name='login_url'),
    url(r'^register/choice$', ChoiceView.as_view(), name='choice_url'),
    url(r'^register/client$', RegisterViewClient.as_view(), name='register_url_client'),
    url(r'^register/company$', RegisterViewCompany.as_view(), name='register_url_company'),
    url(r'^logout/$', LogoutView.as_view(), name='logout_url'),
    #---LOGIN_AND_REGISTER_URLS---

    #---INFO_VIEWS_URLS---
    url(r'^$', HomeView.as_view(), name='home_url'),
    url(r'^profile/client$', ProfileClientView.as_view(), name='profile_client_url'),
    url(r'^profile/company$', ProfileCompanyView.as_view(), name='profile_company_url'),
    #---INFO_VIEWS_URLS---

    #---ACCOINT_CHANGE_URLS---
    url('profile/change/client/$', ClientDetailChangeView.as_view(), name='service_profile_change_url'),
    url(r'^profile/change/company/$', CompanyDetailChangeView.as_view(), name='company_profile_change_url'),
    #---ACCOINT_CHANGE_URLS---

    #---SERVICE_URLS---
    url(r'^service/list/$', MyServiceListView.as_view(), name='service_list_url'),
    url(r'^service/create$', ServiceCreateView.as_view(), name='service_create_url'),
    url(r'^service/edit/(?P<service>\d+)/$', ServiceUpdateView.as_view(), name='service_edit_url'),
    url(r'^service/delete/(?P<service>\d+)/$', ServiceDeleteView.as_view(), name='service_delete_url'),
    #---SERVICE_URLS---
]
