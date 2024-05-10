from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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