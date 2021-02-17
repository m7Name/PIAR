from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import win32print
import subprocess
import time
import os
import os.path

from .models import Order, Photo, Product, Client, Check_list
from django.contrib.auth import login, authenticate, logout

import numpy as np
from .forms import form0
from .forms import form1

import base64
import threading
import threading
import qrcode
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
import time
import sys
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


################################################################################
def barcode1(code):
    try:
        os.remove(f"{settings.WEB_DIR}/barcode1.png")
    except:
        pass
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(f'{code}', writer=ImageWriter())
    options = dict(compress=True, module_width=0.2, module_height=2.0, text_distance=0.4, font_size= 6, quiet_zone= 1, foreground="red")
    ean.save('static/barcode1', options )
    return


def barcode2(code):
    try:
        os.remove(f"{settings.WEB_DIR}/barcode2.png")
    except:
        pass
    EAN = barcode.get_barcode_class('ean13')
    ean = EAN(f'{code}', writer=ImageWriter())
    options = dict(compress=True, module_width=0.2, module_height=2.0, write_text=False, quiet_zone= 1, foreground="red")
    ean.save('static/barcode2', options )
    return



def qr(input_data):
    try:    
        os.remove(f"{settings.WEB_DIR}/qrcode.png")
    except:
        pass

    qr = qrcode.QRCode(
        version=1,
        box_size=3,
        border=1)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('static/qrcode.png')


def pdf_make(codex, logo,code, client_name , product_name, pcs, done_pcs, end_date,size,revision,weight):
    time.sleep(0.3)
    while  os.path.isfile(f'static/barcode2.png') and os.path.isfile(f'static/barcode1.png') and os.path.isfile(f'static/qrcode.png') != True:
        time.sleep(0.3)
    else:
        if not os.path.exists(f'static/orders/{client_name}/{product_name}/{codex}'):
                os.makedirs(f"static/orders/{client_name}/{product_name}/{codex}/PDF")
        pdf = FPDF('P', 'mm', (75, 100))
        pdf.add_page()
        pdf.set_font('Arial', 'B', 8)
        pdf.image('static/barcode_andrey.jpg', x = 0, y = -1, w= 75, h=99)
        pdf.image(f'media/{logo}', x = 1, y = 0, w= 20, h=20)
        pdf.image('static/barcode2.png', x = 2, y = 77, w= 45, h=12)
        pdf.image('static/barcode1.png', x = 2, y = 87, w= 45, h=14)
        pdf.image('static/qrcode.png', x = 55, y = 80, w= 16, h=14)
        pdf.text( 38, 6, f'{product_name} / {revision}') #itea
        #############################################################
        pdf.text( 8, 25, f'DISCRIPTION: {client_name}') #iteam
        pdf.text( 8, 29, f'PCS/CTN: {done_pcs}/{pcs}') #iteam
        pdf.text( 8, 33, f'S/N: {code}') #iteam
        pdf.text( 8, 38, f'MEASUREMENT: {size}') #iteam
        pdf.text( 8, 42, f'GROSS WEIGHT: {weight}') #iteam
        pdf.text( 8, 47, 'MADE IN: Estonia') #iteam
        pdf.text( 8, 51, f'DATE CODE: {end_date}') #iteam

        pdf.output(f'static/orders/{client_name}/{product_name}/{codex}/PDF/{done_pcs}.pdf', 'F')       
################################################################################

def dashboard_view(request):  
    user = request.user
    if user.is_authenticated:
        pass
    else:
        return redirect("accounts/login/")
    context = {}
    # try:
    try:     
            orders = Order.objects.get(workers_are_doing=True)
    except:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    photos = Photo.objects.filter(photo_order_code=orders.order_code)
    prod = Product.objects.get(product_name=orders.order_product_name)
    clien =  Client.objects.get(client_name=orders.order_client_name)
    logo = clien.client_logo_220x220 
    client_name = orders.order_client_name
    product_name = orders.order_product_name
    codex = orders.order_code    
    pcs = orders.order_pcs
    if orders.order_done_pcs == 0:
        done_pcs = orders.order_done_pcs +1
    else:
        done_pcs = orders.order_done_pcs
    code = 100000000000+ done_pcs
    code2 = 100000000000+ done_pcs
    end_date = orders.order_end_date
    youtube_manual = prod.product_youtube_manual
    size = prod.product_size
    weight = prod.product_weight
    revision = prod.product_revision
    if os.path.isfile(f'static/orders/{client_name}/{product_name}/{codex}/PDF/{done_pcs}.pdf') != True:
        t = threading.Thread(target=barcode1,args=[code])
        t2 = threading.Thread(target=barcode2,args=[code2])
        t3 = threading.Thread(target=qr,args=[youtube_manual])
        t4 = threading.Thread(target=pdf_make,args=[codex, logo,code, client_name , product_name, pcs, done_pcs, end_date,size,revision,weight])
        t.start()
        t2.start()
        t3.start()        
        t4.start()
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     return render(request, "dashboard copy.html")      

    products = Product.objects.all()
    context['orders'] = orders 
    context['prods'] = prod
    context['done_pcs']= done_pcs
    while  os.path.isfile(f'static/orders/{client_name}/{product_name}/{codex}/PDF/{done_pcs}.pdf') != True:
        time.sleep(0.3)
    else:
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
            photo.photo_pdf_name = f"{orders.order_code}-{orders.order_done_pcs}"
            photo.photo_pdf_dir = f'static/orders/{orders.order_client_name}/{orders.order_product_name}/{orders.order_code}/PDF/{orders.order_done_pcs}.pdf'
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
            os.makedirs(f"static/orders/{client_name}/{product_name}/{code}/PDF")
        filename = f'static/orders/{client_name}/{product_name}/{code}/{code}-{done_pcs}.jpg' # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
                f.write(imgdata) 

        #pdf_file  = r'C:\Users\msnam\Desktop\PIAR\piar_web\static\orders\Piar OÜ\BB60\10000000000000\PDF\32.pdf'.format(client_name, product_name, code, done_pcs)
        
        pdf_file  = r'{0}\orders\{1}\{2}\{3}\PDF\{4}.pdf'.format(settings.WEB_DIR, client_name, product_name, code, done_pcs)
        time.sleep(3)
        if settings.PRINTER_WORKS:
            acrobat = 'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe'
            name = win32print.GetDefaultPrinter()
            cmd = '"{}" /n /o /t "{}" "{}"'.format(acrobat, pdf_file, name)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)