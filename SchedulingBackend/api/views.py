from django.shortcuts import render
from .models import UserInfo
from rest_framework import generics # imports templates and stuff for generic api user interface
from .serializers import LeadSerializer


# This will house all our endpoints 

class LeadListCreate(generics.ListCreateAPIView): #ListCreateAPIView is a generic template for an API
    queryset = UserInfo.objects.all()
    serializer_class = LeadSerializer
