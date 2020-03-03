from django.db import models
from django.contrib.auth.models import User


class MyUrls(models.Model):
    user=models.ForeignKey(User,blank = True, null = True,  on_delete=models.CASCADE)
    url=models.URLField(max_length=500,verbose_name='ENTER URL')
    tinyurl=models.URLField(max_length=500)
    cateogry=models.CharField(max_length=30,default="newsarticles")

    def __str__(self):
        return self.tinyurl
