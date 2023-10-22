from django.urls import path
from .views import main #imports main function from .views in api folder

urlpatterns = [
    path('',main) #If we get a blank url, call the main function frrom views
]
