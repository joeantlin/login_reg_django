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
            print(request.POST)
            fn = request.POST["fname"]
            ln = request.POST["lname"]
            em = request.POST["email"]
            pw = request.POST["pass"]
            hashpw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
            newuser = User.objects.create(first_name=fn, last_name=ln, email=em, password=hashpw)
            print(newuser)
            user = User.objects.get(email=em)
            request.session["name"] = user.first_name
            request.session["id"] = user.id
            messages.success(request, 'You have succefully made an account')
            return redirect('/success')

def login(request):
    if request.method == "POST":
        errors = User.objects.log_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        else:
            em = request.POST["email"]
            pw = request.POST["pass"]
            user = User.objects.filter(email=em)
            if user == None: 
                print("failed email")
                messages.error(request, 'Incorrect Login Info') 
                return redirect("/")
            else:
                user = User.objects.get(email=em)
                if bcrypt.checkpw(pw.encode(), user.password.encode()):
                    print("password match")
                    request.session["name"] = user.first_name
                    request.session["id"] = user.id
                    messages.success(request, 'You have succefully logged in')
                    return redirect("/success")
                else:
                    print("failed password")
                    messages.error(request, 'Incorrect Login Info') 
                    return redirect("/")
        

        

def success(request):
    if "name" in request.session:
        return render(request, "log_app/success.html")
    else:
        messages.error(request, 'You must be logged in to access that information') 
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')