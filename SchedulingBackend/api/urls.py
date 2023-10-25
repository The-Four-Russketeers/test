from django.urls import path
from . import views #imports main function from .views in api folder

urlpatterns = [
   path('',views.LeadListCreate.as_view()) #When we type in the url: domain/api - we get transported to the api view
]
