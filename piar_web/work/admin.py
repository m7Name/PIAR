from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client , Product, Order, Photo


# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_info')
    search_fields = ('client_name', 'client_info')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Client, ClientAdmin)




class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_size','product_weight')
    search_fields = ('product_name', 'product_size','product_weight')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Product, ProductAdmin)



class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code','order_client_name', 'order_product_name',  'order_add_date','order_end_date', 'order_pcs', 'order_in_work')
    search_fields = ('order_client_name', 'order_product_name' , 'order_in_work')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Order, OrderAdmin)



class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_name','photo_order_code', 'photo_date')
    search_fields = ('photo_name', 'photo_order_code' , 'photo_date')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Photo, PhotoAdmin)