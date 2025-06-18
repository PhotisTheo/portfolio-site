# myportfolio/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="homepage"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/<slug:slug>/", views.project_detail, name="project_detail"),  # 🆕
    path("about/", views.about, name="about"),
    path("contact/", views.contact_view, name="contact"),  # <-- Fix this line
]
