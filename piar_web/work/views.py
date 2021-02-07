from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import json
import urllib
import os
import glob
from .models import Order, Photo, Product, Client, Check_list
from django.contrib.auth import login, authenticate, logout

def home_screen_view(request):    
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    orders = Order.objects.all()
    context['orders'] = orders  
    return render(request, "home.html", context)

def dashboard_view(request):  
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    try:
        orders = Order.objects.get(workers_are_doing=True)
    except:
        return render(request, "dashboard copy.html")      

    products = Product.objects.all()
    context['orders'] = orders  
    return render(request, "dashboard.html", context)
    
def working_pick_order(request, working_order):   
    order = Order.objects.get(order_code=working_order)
    if  order.workers_are_doing == True:    
        order.workers_are_doing = False
    else :
        order.workers_are_doing = True
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def photo_view(request):  
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    photos = Photo.objects.all()
    context['photo'] = photos  
    return render(request, "gallery.html", context)



def check_view(request):  
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    checks = Check_list.objects.all()
    context['check'] = checks 
    return render(request, "check.html", context)