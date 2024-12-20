from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.user_type == 'User' :
                login(request,user)
                messages.success(request,"Logined Successfully")
                return redirect('dashboard')
            elif user.user_type == 'Admin':
                login(request,user)
                messages.success(request,"Logined Successfully")
                return redirect('dashboard')
            else:
                messages.error(request,"You don't have access this page")
        else:
            messages.error(request,"Incorrect Username and Password!!")
    return render(request,'registration/signin.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully Registered")
            return redirect('signin')
        else:
            # If the form is invalid, iterate over errors and display them
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    context = {
        "form":UserRegistrationForm()
    }
    return render(request,'registration/signup.html',context)



@login_required
def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request,"Logout Succesfully")
    return redirect('signin')