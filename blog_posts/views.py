from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout as user_logged_out
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .constants import url
import requests
from .models import BlogPost, Comment
import json

# Create your views here.

def home(request):
    data = requests.get(url)
    for i in data.json()['articles']:
        title = i['title']
        subtitle = i['description']
        date = i['publishedAt']
        body = i['content']
        image_url = i['urlToImage']
        post_url = i['url']
        api_author_name = i['author']

        existed_post = BlogPost.objects.filter(title=title)

        if not existed_post.exists():
            post = BlogPost(title=title, subtitle=subtitle,
                            date=date, body=body, image_url=image_url,
                            api_author_name=api_author_name, post_url=post_url)
            post.save()
    all_posts = BlogPost.objects.all()
    context = []
    for post in all_posts:
        post_dict = {
            'title': post.title,
            'subtitle': post.subtitle,
            'author': post.api_author_name,
            'id': post.id,
            'date': post.date,
            'image_url': post.image_url,
            'body': post.body,
        }
        context.append(post_dict)
    return render(request, 'index.html', {'context': context})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "User logged in successfully.")
            return redirect('home')   
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        retypped_password = request.POST['password_retype']

        emai_exists = User.objects.filter(email=email)
        username_exists = User.objects.filter(username=username)
        if emai_exists.exists() or username_exists.exists():
            messages.error(request, "email or username already taken, try different email or username.")
            return redirect('register')

        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email address.')
            return redirect('register')

        # Validate password (example: minimum length of 8 characters)
        if len(password) < 8:
            messages.error(request, 'Password should be at least 8 characters long.')
            return redirect('register')
        
        # password validation 2nd step
        if password == retypped_password:
            # Apply salting and hashing to the password
            hashed_password = make_password(password)
            print(hashed_password)
            user = User(username=username, email=email, password=hashed_password)
            user.save()
            messages.success(request, "User registered successfully.")
            return redirect('login')
        else:
            messages.error(request, "Password didnot match, please try again with correct credentials.")
            return redirect('register')

    return render(request, 'register.html')


def logout(request):
    user_logged_out(request)
    messages.success(request, 'User logged out successfully.')
    return redirect('home')


def show_post(request, id):
    post = BlogPost.objects.get(id=id)
    data = {
        'id': id,
        'title': post.title,
        'subtitle': post.subtitle,
        'date': post.date,
        'body': post.body,
        'image_url': post.image_url,
        'author': post.api_author_name,
        'post_url':post.post_url,
    }
    return render(request, 'post.html', context=data)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def make_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        image_url = request.POST['img_url']
        body = request.POST['body']
        author = request.user.username
        new_post = BlogPost(title=title, subtitle=subtitle,
                            image_url=image_url, body=body, api_author_name=author)
        new_post.save()
        messages.success(request, "New post created.")
        return redirect('home')
    return render(request, 'make-post.html')


def edit_post(request, id):
    post = BlogPost.objects.get(id=id)
    data = {
        'id': id,
        'title': post.title,
        'subtitle': post.subtitle,
        'date': post.date,
        'body': post.body,
        'image_url': post.image_url,
        'author': post.api_author_name,
        'post_url':post.post_url,
    }
    if request.method == 'POST':
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        image_url = request.POST['img_url']
        body = request.POST['body']
        post.title = title
        post.subtitle = subtitle
        post.image_url = image_url
        post.body = body
        post.save()
        messages.success(request, "Post edited.")
        return redirect('show_post', id)

    return render(request, 'edit_post.html', data)



def delete_post(request, id):
    post = BlogPost.objects.get(id=id)
    post.delete()
    messages.success(request, "Post Deleted.")
    return redirect('home')

