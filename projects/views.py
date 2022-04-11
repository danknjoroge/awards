from email.mime import message
from pyexpat.errors import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostProjectForm,ProfileForm, UpdateProfile, UpdateUser
from .models import Projects, Profile
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer, ProfileSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .permissions import IsAuthenticatedOrReadOnly

# Create your views here.
def index(request):
    projects = Projects.objects.all()
    return render(request, 'index.html',{'projects':projects})

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
        return redirect(home)

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

# @login_required(login_url='/accounts/login/')
# def profile(request):
#     current_user = request.user
#     if request.POST:
#         proform = ProfileForm(request.POST, request.FILES)
#         if proform.is_valid():
#             profile = proform.save(commit=False)
#             profile.user= current_user
#             profile.save()
#         return redirect('profile')
#     else:
#         proform = ProfileForm()
#     return render(request, 'profile.html', {'proform': proform})


@login_required(login_url='/accounts/login/')
def one_image(request, image_id):
    try:
        image = Projects.objects.get(id = image_id)
    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'image.html', {'image': image})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user

    return render(request, 'profile.html')

@login_required(login_url='/accounts/login/')
def updateprofile(request):
    # current_user = request.user
    if request.method == 'POST':
        user_form= UpdateUser(request.POST, instance=request.user)
        profile_form= UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully!')

            return redirect(to='profile')
    else:
        user_form =UpdateUser(instance=request.user)
        profile_form = UpdateProfile(instance=request.user.profile)
        
    return render(request, 'profile.html',{'user_form':user_form, 'form':profile_form})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
        return redirect('profile')

    else:
        form = ProfileForm()
        profile = Profile.objects.all()
        project = Projects.objects.all()
    return render(request, 'profile.html', {'form': form, 'profile': profile, 'project': project})

def profileview(request, id):
    profile = Projects.objects.get(user=id)
    userid = request.user.id

    return render(request, 'projects.html',{"profile":profile, "userid":userid})

def delete_post(request, pk):
    post = Projects.objects.get(id=pk)
    
    if request.method == 'POST':
        try:
            post.delete()
            return redirect('home')
        except Exception:
            messages.error('Post does not exist')

    context = { 'obj':post }
    return render(request, 'delete.html', context)





class ProfileList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        profiles= Profile.objects.all()
        serializers= ProfileSerializer(profiles, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers= ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)

    # def 



class ProjectList(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        project= Projects.objects.all()
        serializers= ProjectSerializer(project, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers= ProjectSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)



class ProfileSingle(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        prof = self.get_profile(pk)
        serializers = ProfileSerializer(prof, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        prof = self.get_profile(pk)
        prof.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ProjectSingle(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get_project(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        proj = self.get_project(pk)
        serializers = ProjectSerializer(proj)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        proj = self.get_project(pk)
        serializers = ProfileSerializer(proj, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        proj = self.get_project(pk)
        proj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




