from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="sensor_app/landing.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("scans/", views.scan_list, name="scan_list"),
    path("scans/new/", views.scan_create, name="scan_create"),
    path("scans/<int:pk>/", views.scan_detail, name="scan_detail"),
]

