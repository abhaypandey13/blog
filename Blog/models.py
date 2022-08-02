from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(('email is must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, **kwargs):
        user= self._create_user(is_staff=False, is_superuser=False,**kwargs)
        user.set_password(password)
        user.save()
        return user

    # def create_admin(self, **kwargs):
    #     return self._create_user(is_staff=True, is_superuser=False, **kwargs)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True,
                                 **extra_fields)
        user.is_active = True
        user.save()
        return user


class user(AbstractUser):
    firstname = models.CharField(max_length=50,null=True)
    lastname = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=250, unique=True, primary_key=True)
    dob = models.DateField(null=True)
    my_photo = models.ImageField(upload_to='my_photos', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    blog_photo = models.ImageField(upload_to='blog_photo', blank=True)
    blogger = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class comment(models.Model):
    comment = models.CharField(max_length=255)
    blog = models.ForeignKey(blog, on_delete=models.CASCADE)
