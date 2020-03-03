from django.contrib.auth.models import User
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import redirect, render
from django.conf import settings
from .forms import UrlForm
import random
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings


# for genrtaing the Random Array for captial letter
largeCharList=list()
for i in range(65,91):
    largeCharList.append(chr(i))

# for genrtaing the Random Array for small letter
smallCharList=list()
for i in range(97,123):
     smallCharList.append(chr(i))

# for genrtaing the Random Array for number
numberList=list()     
for i in range(48,58):
     numberList.append(chr(i))


def TinyUrlGenerate(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
                murl=request.POST['url'].strip()               
                user=request.user
                urlobj=MyUrls.objects.filter(url=murl)
                if len(urlobj) > 0:
                    tinyurl=urlobj[0].tinyurl
                    if user.is_authenticated:
                        newurlobj=MyUrls.objects.all().filter(url=murl,user=user)
                        if len(newurlobj)==0:
                            MyUrls.objects.create(user=user,url=murl,tinyurl=tinyurl).save()
                            
                else:
                    fc=largeCharList[random.randint(0,25)]
                    sc=smallCharList[random.randint(0,25)]
                    nc=numberList[random.randint(0,9)]
                    try:
                        indexno=MyUrls.objects.all()[len(MyUrls.objects.all())-1].id
                    except:
                        indexno=1
                    tinyurl=settings.SITE_NAME+sc+fc+nc+str(indexno+1)
                    if user.is_authenticated:
                        MyUrls.objects.create(user=user,url=murl,tinyurl=tinyurl).save()
                    else:                  
                        MyUrls.objects.create(url=murl,tinyurl=tinyurl).save()
                
                form = UrlForm()
                args={}
                args['form']=form
                args['murl']=murl
                args['tinyurl']=tinyurl
                if user.is_authenticated:
                    cateogry=MyUrls.objects.filter(user=user,url=murl,tinyurl=tinyurl)[0].cateogry
                    args['cateogry']=cateogry
                    args['optionlist']=['foodtravel','shopping','newsarticles','educational','socialnetwork','others']
                args.update(csrf(request)) 
                return render(request,'urltemp/tinyurl.html',args)
    else:
        form = UrlForm()
    args={}
    args['form']=form
    args.update(csrf(request))
    return render(request,'urltemp/tinyurl.html',args)




def redirectToOrginalUrl(request,token):
    surl = settings.SITE_NAME+request.get_full_path().strip("/")
    urlobj=MyUrls.objects.filter(tinyurl=surl)
    if len(urlobj)>0:
        urlobj=urlobj[0]
        actulurl=urlobj.url
        return redirect(actulurl)
    else:
        return render(request,'urltemp/nourl.html')


@login_required(login_url='/account/login/')   
def getMyAllUrls(request):
    user=request.user
    urlobj=MyUrls.objects.filter(user=user)[::-1]
    paginator = Paginator(urlobj,6)
    pageno = request.GET.get('page')
    try:
        urlobj = paginator.page(pageno)
    except PageNotAnInteger:
        urlobj = paginator.page(1)
    except EmptyPage:
        urlobj = paginator.page(paginator.num_pages)

    args={}
    args['urls']=urlobj
    return render(request, 'urltemp/allUrl.html',args)

@login_required(login_url='/account/login/')
def updateCateogry(request):
     if request.method == 'POST':
         user=request.user
         murl=request.POST['url']
         mtinyurl=request.POST['tinyurl']
         cateogry=request.POST['cateogry']
         urlobj=MyUrls.objects.filter(user=user,url=murl,tinyurl=mtinyurl).update(cateogry=cateogry)
     return HttpResponseRedirect('/home/')


@login_required(login_url='/account/login/')
def getdataAcToCateogry(request):
    countobj={}
    user=request.user
    countobj.update({'foodtravel':MyUrls.objects.filter(user=user,cateogry='foodtravel').count()})
    countobj.update({'shopping':MyUrls.objects.filter(user=user,cateogry='shopping').count()})
    countobj.update({'newsarticles':MyUrls.objects.filter(user=user,cateogry='newsarticles').count()})
    countobj.update({'educational':MyUrls.objects.filter(user=user,cateogry='educational').count()})
    countobj.update({'socialnetwork':MyUrls.objects.filter(user=user,cateogry='socialnetwork').count()})
    countobj.update({'others':MyUrls.objects.filter(user=user,cateogry='others').count()})
    for key in countobj:
        countobj[key]=determineSize(countobj[key])
    return countobj 



def determineSize(value):
    fontSize=0
    if value < 1:
        fontSize=10
    elif value < 5:
        fontSize=30
    elif value < 10:
        fontSize=40
    elif value < 30:
        fontSize=50
    elif value < 50:
        fontSize=60
    elif value < 100:
        fontSize=70
    elif value < 200:
         fontSize=80
    elif value < 300:
        fontSize=90
    elif value < 400:
        fontSize=90
    else:
        fontSize=100
    return fontSize
    

@login_required(login_url='/account/login/')    
def getMyAllcategoryUrls(request):
    user=request.user
    category = request.GET.get('category')
    urlobj=MyUrls.objects.filter(user=user,cateogry=category)[::-1]
    paginator = Paginator(urlobj,6)
    pageno = request.GET.get('page')
    try:
        urlobj = paginator.page(pageno)
    except PageNotAnInteger:
        urlobj = paginator.page(1)
    except EmptyPage:
        urlobj = paginator.page(paginator.num_pages)

    args={}
    args['urls']=urlobj
    args['category']=category
    return render(request, 'urltemp/categoryurl.html',args)
    


