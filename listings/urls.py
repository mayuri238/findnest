from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.property_search, name='property_search'),
    path('contact/', views.contact, name='contact'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add_property, name='add_property'),
]
