from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,AnonymousUser 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import UrlShortener
import string
import random



# Create your views here.


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html")


@login_required(login_url="/login/")
def logout_view(request):
    user = request.user
    logout(request)
    return HttpResponseRedirect("/login/")



def generate_short_url():
    characters = string.digits + string.ascii_letters
    short_url = "".join(random.choice(characters) for i in range(6))
    return short_url



def creat_short_url(request):
    
    original_url = request.GET.get("url")
    print(original_url,22222222222)
    short_url = generate_short_url()
    short_url_inst = UrlShortener.objects.create(long_url=original_url, short_url=short_url)
    short_url_inst.save()
    return HttpResponse(short_url)
    

@login_required(login_url="/login/")
def shorten_url(request):
    return render(request, "shorten_url.html")

@login_required(login_url="/login/")
def short_url_detail(request, short_url):
    short_url_obj = UrlShortener.objects.get(short_url=short_url)
    return render(request, "short_url_detail.html", {"short_url_obj": short_url_obj})



def short_url_redirect(request, short_url):
    try:
        short_url_obj = get_object_or_404(UrlShortener, short_url=short_url)
        short_url_obj.count += 1
        short_url_obj.save()
        return HttpResponseRedirect(f'{short_url_obj.long_url}')
    except:
        return HttpResponse("Invalid URL")