from django.test import TestCase
from urlapp.models import MyUrls

class MyUrlsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        MyUrls.objects.create(
            user=None, 
            url='www.google.com/?name=howtocode&city=namewcity',
            tinyurl='http://127.0.0.1:8000/abc1'
        )

    def test_first_name_label(self):
        myurl = MyUrls.objects.get(tinyurl='http://127.0.0.1:8000/abc1')
        self.assertEquals(myurl.url,'www.google.com/?name=howtocode&city=namewcity')