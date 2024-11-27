from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class RoomMember (models.Model): 
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)


    def __str__(self):
        return self.name
    
class User (models.Model): 
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
class Post(models.Model):
    sender = models.CharField(max_length=250, null=True)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.body[0:50]
    
class Notifications (models.Model): 
    sender = models.CharField(max_length=250)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return self.body[0:50]

class Notify (models.Model): 
    sender = models.CharField(max_length=250)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self): 
        return self.body