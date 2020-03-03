from django.forms import ModelForm
from .models import MyUrls

class UrlForm(ModelForm):
     class Meta:
         model = MyUrls
         fields = ['url']