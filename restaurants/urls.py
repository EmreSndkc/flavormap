from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restoranlar/', views.restaurant_list, name='restaurant_list'),
    path('restoranlar/yeni/', views.restaurant_create, name='restaurant_create'),
    path('restoranlar/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('hakkinda/', views.about, name='about'),
    path('iletisim/', views.contact, name='contact'),
    
    # Auth URLs
    path('giris/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),
    path('kayit/', views.register, name='register'),
]
