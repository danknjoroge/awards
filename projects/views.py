from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostProjectForm
from .models import Projects

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/accounts/login/')
def home(request):
    projects = Projects.objects.all()
    return render(request, 'home.html', {"projects": projects})



@login_required(login_url='/accounts/login/')
def newProject(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = current_user
            post.save()
        return redirect(index)

    else:
        form = PostProjectForm()
    return render(request, 'postproject.html', {'form': form})

def search(request):
    pass



















