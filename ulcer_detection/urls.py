from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    # Root → general user login page
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),

    # General user app (login, dashboard, logout)
    path("", include("sensor_app.urls")),

    # Admin interface
    path("admin/", admin.site.urls),
]

