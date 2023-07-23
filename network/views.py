from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json


from .models import User, Post


def index(request):
    all_post = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {
        "allposts": all_post
    })


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allposts = Post.objects.filter(user_id=user_id).order_by('-timestamp')
    return render(request, "network/profile.html", {
        "user": user,
        "allposts": allposts
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request, user):
    if request.method == "POST":
       content = request.POST["content"]
       post = Post.objects.create(user=User.objects.get(username=user), content=content)
       post.save()
       return HttpResponseRedirect(reverse("index"))
    
def allpost(request):
    all_post = Post.objects.all().order_by('-timestamp')
    print(all_post)
    return JsonResponse([post.serialize() for post in all_post], safe=False) 

