from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_shipment, name='new_shipment'),
    re_path(r'^(?P<pk>\d+)/?$', views.details, name='details'),
    re_path(r'^update/(?P<pk>[0-9]+)/?$', views.update, name='update'),
    re_path(r'^delete/(?P<pk>[0-9]+)/?$', views.delete, name='delete'),
    path('gettrack/', views.gettrack, name='gettrack'),
    path('getcorporatetrack/', views.getcorporatetrack, name='getcorporatetrack'),
    re_path(r'^user/(?P<pk>[0-9]+)/?$', views.listUserShipments, name='listUserShipments'),
    path('categories/', views.sendCategories, name='sendCategories'),
    path('shiporder/', views.shipOrder, name='shipOrder'),
]
