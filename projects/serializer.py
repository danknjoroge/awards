from rest_framework import serializers
from .models import Projects, User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('title', 'image', 'description', 'live_link', 'posted_by', 'date_posted' )