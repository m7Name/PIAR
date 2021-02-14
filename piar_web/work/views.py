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
import PIL
import numpy as np
from .forms import form0
from .forms import form1
import re
import base64
import threading

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
    try: 
        orders = Order.objects.get(workers_are_doing=True)
        photos = Photo.objects.filter(photo_order_code=orders.order_code)
        all_photo = len(photos)
        context['allphoto'] = all_photo
    except:   
        return render(request, "gallery.html", context)

    
    context['photo'] = photos
    
    context['orders'] = orders    
    return render(request, "gallery.html", context)

def photo_search(request):
    if request.method == 'POST':       
        tim = request.POST.get("q")   
        try:     
            orders = Order.objects.get(workers_are_doing=True)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        xx = len(orders)
        context = {}
        if xx != 0:
            orders = Photo.objects.filter(photo_code=tim)
            context['photo'] = orders
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, "gallery.html", context)

def  check_list_validation(request):
    if request.method == 'POST':       
        tim = request.POST.get("check")
        try:     
            orders = Order.objects.get(workers_are_doing=True)
        except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        try:        
            checks = Photo.objects.filter(photo_order_code=orders.order_code).get(photo_code=tim)
            checks.photo_check_list= True
            checks.save()
        except:
            checks = {}
        context = {}
        context['check'] = checks 
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def photo_search(request):
#     if request.method == 'POST':       
#         tim = request.POST.get("q")
#         context = {}
#         orders2 = Photo.objects.filter(photo_code=tim)
#         print(orders2)
#         context['photo'] = orders2
#     return render(request, "gallery.html", context)


def unmark_all(request):
    try:     
        orders = Order.objects.get(workers_are_doing=True)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    checks = Photo.objects.filter(photo_order_code=orders.order_code, photo_check_list= True )   
    for checks in checks:
        checks.photo_check_list= False
        checks.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def check_view(request):  
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    try: 
        orders = Order.objects.get(workers_are_doing=True)
        photos = Photo.objects.filter(photo_order_code=orders.order_code).order_by('-id')
        
        context['photo'] = photos
        context['order'] = orders
        context['cheked'] = len(photos.filter(photo_check_list=True))
        context['need_to_check'] = len(photos)        
        x = len(photos.filter(photo_check_list=True)) *100
        y = int(x / len(photos) )
    except:
        y=0
    context['procent'] = y
    return render(request, "check.html", context)



def inventory_sell_marked(request):
    if request.method == 'POST':       
        tim = request.POST.get("im")
        orders = Order.objects.get(workers_are_doing=True)
        imgdata = base64.b64decode(tim)

        if orders.order_done_pcs == orders.order_pcs:
            return HttpResponseRedirect('/dashboard/')
        else:
            photo = Photo()
            orders.order_done_pcs = orders.order_done_pcs+1
            photo.photo_name = f"{orders.order_code}-{orders.order_done_pcs}"
            photo.photo_order_code = orders.order_code
            photo.photo_code=orders.order_done_pcs
            photo.photo_dir = f'static/orders/{orders.order_client_name}/{orders.order_product_name}/{orders.order_code}/{orders.order_code}-{orders.order_done_pcs}.jpg'
            photo_pdf_name = 0
            photo_pdf_dir = 0
            photo.save()                         
            orders.save()

            client_name= orders.order_client_name
            product_name= orders.order_product_name
            code= orders.order_code
            done_pcs= orders.order_done_pcs
            t = threading.Thread(target=doCrawl,args=[client_name, product_name,code, done_pcs, imgdata ])
            t.start()
                   
           
        return HttpResponseRedirect('/dashboard/')


def doCrawl(client_name, product_name,code, done_pcs,imgdata ):        
        if not os.path.exists(f'static/orders/{client_name}/{product_name}/{code}'):
            os.makedirs(f"static/orders/{client_name}/{product_name}/{code}")
        filename = f'static/orders/{client_name}/{product_name}/{code}/{code}-{done_pcs}.jpg' # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
                f.write(imgdata) 