from email.mime import message
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostProjectForm, UpdateProfile, UpdateUser
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


@login_required(login_url='/accounts/login/')
def search(request):
    if 'projects' in request.GET and request.GET["projects"]:
        search_term = request.GET.get('projects')
        search_title = Projects.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "project": search_title})
    else:
        
        return render(request, 'search.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user



# @login_required(login_url='/accounts/login/')
# def updateProfile(request):
#     # current_user = request.user
#     if request.method == 'POST':
#         user_form= UpdateUser(request.POST, instance=request.user)
#         profile_form= UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request,'Profile updated successfully!')

#             return redirect('profile')
#     else:
#         user_form =UpdateUser(instance=request.user)
#         profile_form = UpdateProfile(instance=request.user.profile)
#         params= {
#             'user_form':user_form,
#             'profile_form':profile_form
#         }
#     return render(request, 'profile.html',params)


        













