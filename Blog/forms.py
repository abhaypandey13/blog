from django import forms
from . import models

class loginForm(forms.ModelForm):
    class Meta:
        model = models.user
        fields= ('username', 'password')


class signUpForm(forms.ModelForm):
    class Meta:
        model = models.user
        fields = ('firstname', 'lastname', 'email','username','dob','my_photo','password')
    # firstname = forms.CharField()
    # lastname = forms.CharField()
    # email = forms.EmailField()
    # username = forms.CharField()
    # dob = forms.DateField()
    # my_photo = forms.ImageField()
    # password = forms. CharField()
    #'firstname', 'lastname', 'email','username','dob','my_photo','password')


class createBlog(forms.ModelForm):
    class Meta:
        model= models.blog
        fields =('title','content','blog_photo')

class blogcomment(forms.ModelForm):
    class Meta:
        model = models.comment
        fields = ('comment',)
