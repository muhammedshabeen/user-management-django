from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import re

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logined Successfully")
            return redirect('dashboard')
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
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Profile edited successfully")
            return redirect('profile')
        else:
            # If the form is invalid, iterate over errors and display them
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    context = {
        "form":ProfileEditForm(instance=user)
    }
    return render(request,'profile.html',context)

@login_required
def signout(request):
    logout(request)
    messages.success(request,"Logout Succesfully")
    return redirect('signin')

@login_required
def user_lists(request):
    user_objs= CustomUser.objects.filter().exclude(is_superuser=True).order_by('-id')
    context = {
        "user_objs":user_objs,
    }
    return render(request,"user_view.html",context)



@login_required
def change_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("profile")

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("profile")
        
        if not any(char.isupper() for char in password1):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect("profile")

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
            messages.error(request, "Password must contain at least one special character (!, @, #, $, etc.).")
            return redirect("profile")

        # Set the new password
        request.user.password = make_password(password1)
        request.user.save()

        messages.success(request, "Your password has been updated successfully.")
        return redirect("profile")
    else:
        messages.error(request,"Method not allowed")
        return redirect("profile")
        