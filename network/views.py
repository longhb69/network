from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
import json

from .models import User, Post,Follow, Like

def index(request):
    all_post = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')

    pages = paginator.get_page(page_number)
    nums = "a" * pages.paginator.num_pages

    all_likes = Like.objects.all()
    liked_post = []
    for like in all_likes:
        if like.user == request.user:
            liked_post.append(like.post)

    return render(request, "network/index.html", {
        "pages": pages,
        "nums": nums,
        "liked_post": liked_post
    })

def following(request):
    following = Follow.objects.get(user=request.user)
    all_posts = []
    for user in following.following.all():
        post = Post.objects.get(user=user)
        all_posts.append(post)

    return render(request, "network/following.html", {
        "all_posts": all_posts
    })


def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)
    current_user = User.objects.get(pk=request.user.pk)
    allposts = Post.objects.filter(user_id=user_id).order_by('-timestamp')
    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')

    pages = paginator.get_page(page_number)
    nums = "a" * pages.paginator.num_pages

    already_followed = False
    try:
        follow = Follow.objects.get(user_id=user_id)
        if current_user in follow.follower.all():
            already_followed = True

        following_count = follow.following.count()
        follower_count = follow.follower.count()
    except Follow.DoesNotExist:
        following_count = 0
        follower_count = 0

    is_not_user = True if request.user != user_profile else False
    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "pages": pages,
        "nums": nums,
        "following_count": following_count,
        "follower_count": follower_count,
        "is_not_user": is_not_user,
        "already_followed": already_followed
    })

def follow(request, user_id):
    user_follower = User.objects.get(pk=user_id)  
    user_following = User.objects.get(pk=request.user.pk) 
    follower = Follow.objects.filter(user=user_follower).first()
    following = Follow.objects.filter(user=user_following).first()

    if follower is not None:
        follower.follower.add(user_following)
        follower.save()
    else:
        follower = Follow.objects.create(user=user_follower)
        follower.follower.add(user_following)
        follower.save()
    
    if following  is not None:
        following.following.add(user_follower)
        following.save()
    else:
        following = Follow.objects.create(user=user_following)
        following.following.add(user_follower)
        following.save()

    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request, user_id):
    user_follower = User.objects.get(pk=user_id)  
    user_following = User.objects.get(pk=request.user.pk) 
    follower = Follow.objects.get(user=user_follower)
    following = Follow.objects.get(user=user_following)

    follower.follower.remove(user_following)
    following.following.remove(user_follower)
    
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id": user_id}))


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
    

def editpost(request, id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
    
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
def like(request, id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        like = Like.objects.create(user=request.user, post=post)
        data = json.loads(request.body)
        post.like = data["like"]
        post.save()
        like.save()
        return HttpResponse(status=204)
def unlike(request, id):
    if request.method == "PUT":
        try: 
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        Like.objects.get(user=request.user, post=post).delete()
        data = json.loads(request.body)
        post.like = data["like"]
        post.save()
        return HttpResponse(status=204)
        
def allpost(request):
    all_post = Post.objects.all().order_by('-timestamp')
    print(all_post)
    return JsonResponse([post.serialize() for post in all_post], safe=False) 

