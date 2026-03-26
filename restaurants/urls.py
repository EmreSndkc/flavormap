from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restoranlar/', views.restaurant_list, name='restaurant_list'),
    path('restoranlar/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('hakkinda/', views.about, name='about'),
    path('iletisim/', views.contact, name='contact'),
]
