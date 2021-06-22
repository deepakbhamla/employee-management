from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from  companyapp import views
from django.conf.urls import url

app_name = 'companyapp'
urlpatterns = [
  path('',views.company_list, name='company-list'),
  path('add-company/',views.add_company, name='add-company'),
  path('add-employee/',views.add_employee, name='add-employee'),
  path('search/',views.search_company, name='search-result'),
  path('populate/',views.populate_db, name='populate-db'),

  url(r'^update-company/(?P<id>\d+)/$',views.update_company, name='update-company'),
  url(r'^update-employee/(?P<id>\d+)/$',views.update_employee, name='update-employee'),
  url(r'^pdf-download/(?P<company_name>[\w\-\ ]+)/$',views.pdf_download, name='pdf-download'),

  url(r'^company/(?P<company>[\w\-\ ]+)/$', views.employee_list, name='employee_list'),

]
