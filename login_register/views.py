from django.contrib import auth
from django.contrib.auth.models import User
from .forms import SignUpForm,LoginForm,ChangePasswordForm
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template.context_processors import csrf
from django.shortcuts import redirect, render
from urlapp.views import getdataAcToCateogry
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email =request.POST['email']
            password =request.POST['password']
            User.objects.create_user(username=username, password=password,email=email)
            return HttpResponseRedirect('/account/signup_sucess')
    else:
        form = SignUpForm()
    args={}
    args['form']=form
    args.update(csrf(request))
    return render(request,'profile/signup.html',args)

def signup_sucess(request):
    return HttpResponseRedirect('/account/login')


def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect('/home/')
                
    else:
        form = LoginForm()   
    args={}
    args.update(csrf(request))
    args['form']=form
    return render(request,'profile/login.html',args)


@login_required(login_url='/account/login/')
def changePassword(request):
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword=request.POST['new_password']
            user=request.user
            user.set_password(newpassword)
            user.save()
            args={}
            return render(request,'urltemp/home.html',args)
    else:                    
        form = ChangePasswordForm()
    args={}
    args.update(csrf(request))
    args['form']=form
    return render(request,'profile/changePassword.html',args)

@login_required(login_url='/account/login/')  
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/account/login/')

@login_required(login_url='/account/login/')   
def goToHome(request):
    args={}
    args['data']=getdataAcToCateogry(request)
    return render(request,'urltemp/home.html',args)

