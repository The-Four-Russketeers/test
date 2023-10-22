from django.shortcuts import render
from django.http import HttpResponse

# This will house all our endpoints 

def main(request):
    return HttpResponse("<h1>Wilson was here and is actively working on this</h1>")