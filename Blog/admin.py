from django.contrib import admin
from Blog.models import user, blog, comment

admin.site.register(user)
admin.site.register(blog)
admin.site.register(comment)
