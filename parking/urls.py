from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('passes/', views.valid_passes, name='passes'),
    path('requests/', views.pass_requests, name='requests'),
    
    path('register/', views.tentant_signup, name='register'),
    path('register-staff/', views.register_staff, name='register_staff'),
    path('register-building/', views.register_building, name='register_building'),
    
    path('logout/', views.user_logout, name='logout'),
    path('approval-pending/', views.approval_pending, name='approval_pending'),
    
    path('staff_list/', views.staff_list, name='staff_list'),
    path('tenant_list/', views.tenant_list, name='tenant_list'),
    path('request_pass/<str:pk>/', views.request_pass, name='request_pass'),
    
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('dashboard/<str:pk>/', views.user_dashboard, name='dashboard'),
]