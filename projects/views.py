from django.shortcuts import render
from .models import Projects

# Create your views here.
def index(request):
    projects = Projects.objects.all()
    return render(request, 'index.html', {"projects": projects})