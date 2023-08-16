from django.contrib import admin
from django.urls import path
from senti_gram import views

urlpatterns = [
    
    path('', views.index, name='senti')
]