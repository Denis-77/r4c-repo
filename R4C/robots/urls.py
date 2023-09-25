from django.urls import path

from .views import download_excel

urlpatterns = [

    path('excel/', download_excel, name='download_excel'),
]