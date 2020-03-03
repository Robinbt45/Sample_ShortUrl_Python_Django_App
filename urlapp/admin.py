from django.contrib import admin
from .models import *

# Register your models here.
class URLAdmin(admin.ModelAdmin):
    model = MyUrls
    list_display = ['url', 'tinyurl']

admin.site.register(MyUrls, URLAdmin)
