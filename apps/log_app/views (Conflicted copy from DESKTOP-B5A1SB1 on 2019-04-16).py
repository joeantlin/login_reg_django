from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "log_app/index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            #print(request.POST)
            fn = request.POST["fname"]
            ln = request.POST["lname"]
            em = request.POST["email"]
            pw = request.POST["pass"]
            hashpw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=fn, last_name=ln, email=em, password=hashpw)
            print(newuser)
            request.session["name"] = fn
            return redirect('/success')

def success(request):
    print(User.objects.all().values())
    return render(request, "log_app/success.html")

def logout(request):
    request.session.clear()
    return redirect('/')