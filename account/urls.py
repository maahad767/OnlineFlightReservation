from django.urls import path
from . import views

urlpatterns = [
    path('determiner', views.dashboard, name='dashboard'),
    path('dashboard', views.UserDashboardView.as_view(), name='user-dashboard'),
    path('admin/dashboard', views.AdminDashboardView.as_view(),
         name='admin-dashboard'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.logoutView, name='logout'),
]
