from django.db import models

# Create your models here.
class Users(models.Model):
    class Meta:
        db_table = 'users'

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=512,unique=True)
    email = models.CharField(max_length=512, unique=True)
    twitter = models.CharField(max_length=512, null=True, unique=True)
    telegram = models.CharField(max_length=512, null=True, unique=True)
    bio = models.TextField(null=True, blank=True)
    wallet = models.CharField(max_length=512, null=True, unique=True)
    dnft = models.IntegerField(default=0,null=True)
    dp = models.IntegerField(default=0,null=True)
    password = models.CharField(max_length=512)
    photo = models.CharField(max_length=512, null=True, blank=True)
    role = models.IntegerField(default= 0,null=True)
    disabled=models.BooleanField(default=False)

    created_at = models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,auto_now=True)
