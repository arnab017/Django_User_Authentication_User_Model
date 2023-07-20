from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.

def User_Registration(request):
    
    UFO = User_Form(label_suffix="")
    PFO = Profile_Form(label_suffix="")
    d = {'UFO': UFO, 'PFO': PFO}
    
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