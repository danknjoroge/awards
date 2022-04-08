from dataclasses import field
from rest_framework import serializers
from .models import Projects, Profile

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('title', 'image', 'description', 'live_link', 'posted_by', 'date_posted')


        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'contact' )




