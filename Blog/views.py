from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .forms import loginForm, signUpForm, createBlog, blogcomment
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from . import models

def login(request):
    login_form = loginForm()

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            auth_login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,'login.html',{'login_form':login_form,'message':'Please check the username and password'})

    else:
        return render(request,'login.html',{'login_form':login_form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def signup(request):
    # print(request.method)
    signup_form = signUpForm()
    if request.method =='POST':
        #print(request.POST)
        signup_form = signUpForm(request.POST)
        #print(signup_form)
        # signup_form.firstname = request.POST['firstname']
        # signup_form.lastname = request.POST['lastname']
        # signup_form.email = request.POST['email']
        # signup_form.username = request.POST['username']
        # signup_form.dob = request.POST['dob']
        # signup_form.my_photo = request.POST.get('my_photo',False)
        # signup_form.password = request.POST['password']

        if signup_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
        else:
            print(signup_form.errors)
    else:
        #print('hello1')
        signup_form = signUpForm()
    #print('hello2')
    return render(request, 'signup.html',{'signup_form':signup_form})

class create_blog(LoginRequiredMixin,CreateView):
    def get(self, request):
        context = {'form':createBlog(),'title':'create'}
        return render(request, 'create.html',context)

    def post(self, request):
        form = createBlog(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.blogger = request.user
            blog.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'create.html',{'form':form})
    # login_url = '/login/'
    # redirect_field_name = 'index.html'
    # template_name = 'create.html'
    #
    # form_class = createBlog
    #
    # model = models.blog

class index(ListView, LoginRequiredMixin):
    def get(self, request):
        #print(request.user)
        blogs= models.blog.objects.filter(blogger= request.user).values('id','title','content','created_at','blog_photo')
        #print(list(blogs))
        return render(request, 'index.html',{'title':'index','blogs':list(blogs)})

    def post(self, request):
        #print(request.POST)
        return user_logout(request)

class delete(LoginRequiredMixin, DetailView):
    def get(self, request, id):
        blog = models.blog.objects.filter(id=id)
        blog.delete()
        return HttpResponseRedirect(reverse('index'))


class blog(ListView, LoginRequiredMixin, CreateView):
    def get(self, request, id):
        #print(request.user)
        blog= models.blog.objects.get(id=id)
        #blog=list(blog)[0]
        #print(blog)
        comments = models.comment.objects.filter(blog=id).values('comment')

        #print(comments)
        '''
        new_list=[]
        print(list(comments))
        for comment in list(comments):
            new_dict={}
            blogg= models.blog.objects.filter(id=comment.get('blog_id')).values()
            blogg=list(blogg)[0]
            print(blogg)
            bloger = models.user.objects.filter(email=blogg['blogger_id']).values('username')
            print(bloger)
            bloger = list(bloger)[0]
            new_dict['comment']=comment['comment']
            new_dict['comment_user'] = bloger['username']
            new_list.append(new_dict)
        print(new_list)
        '''
        context = {'form':blogcomment(),'title':'blog','blog':blog,'comments':comments}
        return render(request, 'blog.html',{'title':'blog','blog':blog,'comments':comments,'form':blogcomment()})

    def post(self, request, id):
        #print(request.POST)
        if 'logout' in request.POST:
            return user_logout(request)
        else:
            form = blogcomment(request.POST)
            blog = models.blog.objects.get(id=id)
            #print(blog)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.save()
                return HttpResponseRedirect(reverse('blogview', kwargs={'id':id}))
            return render(request, 'blog.html',{'form':form})

class sr(ListView, LoginRequiredMixin):
    def get(self, request, string):
        print(request )
        blogs= models.blog.objects.filter(title__contains=string).values('id','title','content','created_at')
        print(blogs)
        return render(request,'search-page.html',{'data':list(blogs),'title':'Search Results'})
