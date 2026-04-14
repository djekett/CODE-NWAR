from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio, name="portfolio"),
    path("toporahma/", views.home, name="home"),
    path("telecharger/", views.download_form, name="download_form"),
    path("telecharger/merci/<int:pk>/", views.download_success, name="download_success"),
    path("telecharger/fichier/<int:pk>/", views.download_file, name="download_file"),
    path("telecharger/contribution/<int:pk>/", views.mark_contribution, name="mark_contribution"),
]
