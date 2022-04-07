from .models import Projects
from django import forms


class PostProject(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['posted_by', 'date_posted']

        
