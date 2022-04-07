import datetime
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic = models.ImageField(default='default.jpg', upload_to='images/')

#     def __str__(self):
#         return f'{self.user.username} Profile'

class Projects(models.Model):
    title = models.CharField(max_length=122)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    description = models.TextField()
    live_link = models.URLField(max_length=222, default='url')
    posted_by = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE )
    date_posted = models.DateTimeField(auto_now_add=True)

    def save_project(self):
        self.save()


