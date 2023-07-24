from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def User_Registration(request):
    #creating form objects
    UFO = User_Form(label_suffix="")
    PFO = Profile_Form(label_suffix="")
    d = {'UFO': UFO, 'PFO': PFO}
    
    #getting the data
    if request.method=='POST' and request.FILES:
        UFD = User_Form(request.POST)
        PFO = Profile_Form(request.POST,request.FILES)
        
        if UFD.is_valid() and PFO.is_valid():
            # encrypting the password
            NSUFD = UFD.save(commit=False)
            saved_password = UFD.cleaned_data["password"]
            NSUFD.set_password(saved_password)
            NSUFD.save()
            # assigining value to username
            NSPFO = PFO.save(commit=False)
            NSPFO.username = NSUFD
            NSPFO.save()
            #sending mail to user 
            send_mail('Registration',
                      'Registration Successfully Done',
                      'aarnab017@gmail.com',
                      [NSUFD.email],
                      fail_silently=False)
            
            return HttpResponse('<script>alert("Sign Up Successful")</script>')
        else:
            return HttpResponse('<script>alert("Invalid Data")</script>')
              
    return render(request, 'User_Registration.html',d)


def home_page(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home_page.html',d)
    
    return render(request, 'home_page.html')

def user_login(request):
    if request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']
        
        #authneication
        AUO = authenticate(username=un, password=pw)
        if AUO:
            
            #activate user checking and login request
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=un
                return HttpResponseRedirect(reverse('home_page'))
            else:
                return HttpResponse('<script>alert("Not a Active User")</script>')
        else:
            return HttpResponse('<script>alert("Invalid Details")</script>')
                
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def display_details(request):
    username = request.session.get('username')
    UO = User.objects.get(username=username)
    PO = Profile.objects.get(username=UO)
    d = {'UO':UO, 'PO':PO}
    return render(request, 'display_details.html',d)

@login_required
def change_password(request):
    if request.method == 'POST':
        pw = request.POST.get('pw')
        un = request.session.get('username')
        UO = User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('<script>alert("Password change Successful")</script>')
    return render(request, 'change_password.html')

def reset_password(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        rpw = request.POST.get('rpw')
        LUO = User.objects.filter(username=un)
        if LUO:
            if pw==rpw:
                UO = LUO[0]
                UO.set_password(pw)
                UO.save()
                return HttpResponse('<script>alert("Password Reset Successful")</script>')
            else:
                return HttpResponse('<script>alert("Password Mis-Match")</script>')
        else:
            return HttpResponse('<script>alert("Invalid username")</script>')
            
    return render(request, 'reset_password.html')