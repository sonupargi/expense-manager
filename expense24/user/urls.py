from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    
    path("user_register/",views.UserRegisterView.as_view(),name="user_register"),
    path("login/",views.UserLoginView.as_view(),name="login"),
    path("user_dashboard/",views.UserDashboardView.as_view(),name="user_dashboard"),
    # path("developer_dashboard/",views.DeveloperDashboardView.as_view(),name="developer_dashboard"),
   # path("logout/",views.logout_view,name="logout"),
   
    
]