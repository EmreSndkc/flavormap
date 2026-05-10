from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('restoranlar/', views.restaurant_list, name='restaurant_list'),
    path('restoranlar/yeni/', views.restaurant_create, name='restaurant_create'),
    path('restoranlar/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('restoranlar/<int:pk>/favori/', views.toggle_favorite, name='toggle_favorite'),
    path('restoranlar/<int:pk>/duzenle/', views.restaurant_update, name='restaurant_update'),
    path('restoranlar/<int:pk>/sil/', views.restaurant_delete, name='restaurant_delete'),
    
    # Review URLs
    path('yorumlar/<int:pk>/duzenle/', views.review_update, name='review_update'),
    path('yorumlar/<int:pk>/sil/', views.review_delete, name='review_delete'),
    
    path('hakkinda/', views.about, name='about'),
    path('iletisim/', views.contact, name='contact'),
    path('profil/', views.profile, name='profile'),
    
    # Auth URLs
    path('giris/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),
    path('kayit/', views.register, name='register'),
]
