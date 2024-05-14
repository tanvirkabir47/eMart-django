from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from datetime import timedelta, datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlencode, urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

# Create your views here.

def signup_view(request):
    
    error_messages = None
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if User.objects.filter(email=email).exists():
            error_messages = 'Email already exists'
            return render(request, 'signup.html', {'error_messages': error_messages})
        
        if password == password2:
            user = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name, 
                email=email,
                username=email,
                password=password
            )
            user.save()
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'User created successfully!')
                return redirect('home')
            else:
                error_messages = 'User Not Found'
            
        else:
            error_messages = 'Passwords do not match'
            
    
    return render(request, 'signup.html', {'error_messages': error_messages} )


def login_view(request):
    
    error_messages = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
         error_messages =  'User Not Found'
    
    return render(request, 'login.html', {'error_messages': error_messages})


def logout_views(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')



def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error_messages= None

    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a unique token for password reset
            current_site = get_current_site(request)
            mail_subject = 'Password Reset'

            messsage = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'time': urlsafe_base64_encode(force_bytes(timezone.now() + timedelta(hours=2))),
            })

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(mail_subject, messsage, email_from, recipient_list, fail_silently=False)
            messages.success(request, 'Password reset link has been sent to your email.')
        else:
            error_messages = 'User with this email does not exist.'
   
    return render(request, 'forgot_password.html', {'error_messages': error_messages})


def resetpassword_validate(request, uidb64, token, time64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        decoded_time = urlsafe_base64_decode(time64).decode('utf-8')
        expiration_time = datetime.fromisoformat(decoded_time)
    except:
        user = None
        expiration_time = None
        uid = None

    if user is not None and default_token_generator.check_token(user,token) and expiration_time and expiration_time > timezone.now():
        request.session['cid'] = uid
        messages.success(request, "please reset your password here")
        return redirect('reset_password')
    else:
        messages.warning(request, "Link expired!!!")
        return redirect('login')


def reset_password(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.session.get('cid'):
        if request.method == "POST":
            password = request.POST.get("create_password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                cid = request.session.get('cid')
                user = User.objects.get(pk=cid)
                new_pass = make_password(confirm_password)
                user.password = new_pass
                user.save()
                del request.session['cid']
                messages.success(request, "Reset password successfully!!!")
                return redirect('login')
            else:
                error_messages = "Password doesn't match!!!"
                return render(request, 'reset_password.html', {'error_messages': error_messages})
        else:
            return render(request, 'reset_password.html')
    else:
        messages.warning(request, "Link Expired!!!")
        return redirect('login')