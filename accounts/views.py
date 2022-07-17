from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile
import uuid
from django.conf import settings
from django.core.mail import send_mail

#Login User
def login1(request):

    if request.method== 'POST':
        email=request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        user_obj=User.objects.filter(username=username).first()
        profile_obj=profile_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj is None:
            messages.info(request,'User Not found')
            return redirect('login1')
        
        if not profile_obj.is_verified:
            messages.info(request,'Email not verified yet')
            u=User.objects.get(username=username)
            prof=Profile.objects.get(user=u)
            auth_token=prof.auth_tokens
            send_mail_later(email,auth_token)
            return redirect("token_sent")

        if user is not None:
            auth.login(request,user)
            messages.info(request,'Logged in Successfully')
            return redirect('home')
        else:
            messages.info(request,'Check your Credentials')
            return redirect('login1')
    else:
        return render(request,'login1.html')    

#Register
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        
       
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
                user_obj = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user_obj.save()
                auth_token=str(uuid.uuid4())
                profile_obj=Profile.objects.create(user=user_obj,auth_tokens=auth_token)
                profile_obj.save()
                send_mail_later(email,auth_token)
                return redirect('token_sent')
        else:
            messages.info(request,'passwords not matching..')    
            return redirect('register')

    else:
        return render(request,'register.html')


#Logout
def logout(request):
    auth.logout(request)
    return redirect('home')


#Token sent in gmail
def token_sent(request):
    return render(request,'tokensent.html')


#User profile verification
def verify(request , auth_tokens):
    
    profile_obj = Profile.objects.filter(auth_tokens = auth_tokens).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request, 'Your account is already verified.')
            return redirect('login1')

        else:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login1')
    else:
        return redirect('register')
    
        


#Send email
def send_mail_later(email,token):
    subject='Your account need to be verified'
    message=f'Hi, click the link to verify your account http://127.0.0.1:8000/accounts/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)

