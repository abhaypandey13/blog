from django.test import Client, TestCase
from django.urls import reverse

class Test_activity1(TestCase):
    def setUp(self):
        csrf_client = Client(enforce_csrf_checks=True)
        self.c= Client()


    def testcase1_signup(self):
        response = self.c.get(reverse('signup'))
        assert b'username' in response.content,"username field doesn't exist in signup page"
        assert b'email' in response.content,"email field doesn't exist in signup page"

    def testcase5_login_success(self):
        fir = self.c.post('/signup/',{'username':'hokage7','firstname':'naruto','lastname':'uzumaki','email':'narutohinata@leaf.com',
                                        'password':'#Hokage7','confirm':'#Hokage7','dob':'1999-01-01'},follow=True)
        first= self.c.post('/signup/',{'username':'sharingan7','firstname':'sasuke','lastname':'hinata','email':'sasuke@leaf.com',
                                        'password':'#luchiha','confirm':'#luchiha','dob':'2020-01-01'}, follow=True)
        log = self.c.post('/login/',{'username':'sharingan7','password':'#luchiha','login':'login'})
        log = self.c.get('/index/')
        assert b'index' in log.content

    def testcase6_create_blog(self):
        fir = self.c.post('/signup/',{'username':'hokage7','firstname':'naruto','lastname':'uzumaki','email':'narutohinata@leaf.com',
                                        'password':'#Hokage7','confirm':'#Hokage7','dob':'1999-01-01'},follow=True)
        first= self.c.post('/signup/',{'username':'sharingan7','firstname':'sasuke','lastname':'hinata','email':'sasuke@leaf.com',
                                        'password':'#luchiha','confirm':'#luchiha','dob':'2020-01-01'}, follow=True)
        log = self.c.post('/login/',{'username':'sharingan7','password':'#luchiha','login':'login'})

        cr = self.c.post('/create/',{'title':'django website','content':'testcase_blog successfully created','create_blog':'create_blog'}, follow=True)
        
        assert b'django website' in cr.content, "blog not created and it's not displayed in index"
        assert b'testcase' in cr.content

    def testcase7_blog_page(self):
        fir = self.c.post('/signup/',{'username':'hokage7','firstname':'naruto','lastname':'uzumaki','email':'narutohinata@leaf.com',
                                        'password':'#Hokage7','confirm':'#Hokage7','dob':'1999-01-01'},follow=True)
        first= self.c.post('/signup/',{'username':'sharingan7','firstname':'sasuke','lastname':'hinata','email':'sasuke@leaf.com',
                                        'password':'#luchiha','confirm':'#luchiha','dob':'2020-01-01'}, follow=True)
        log = self.c.post('/login/',{'username':'sharingan7','password':'#luchiha','login':'login'})

        cr = self.c.post('/create/',{'title':'django website','content':'testcase_blog successfully created','create blog':'create blog'}, follow=True)
        cr = self.c.get('/index/')
        cr = self.c.get('/index/blog/1/')

        assert b'django website' in cr.content, "full view of the blog doesn't show up on '/index/blog/1/'"
        assert b'testcase_blog successfully created' in cr.content, "full view of the blog doesn't show up on '/index/blog/1/'"
