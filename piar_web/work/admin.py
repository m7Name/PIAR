from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client , Product, Order, Photo
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

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
    fieldsets = (
        (None, {
            'fields': ('order_client_name', 'order_product_name', 'order_code', 'order_pcs','order_palet','order_end_date','order_description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('order_done_pcs','order_in_work', 'workers_are_doing', ),
        }),
    )

admin.site.register(Order, OrderAdmin)



class PhotoAdmin(admin.ModelAdmin):
    def Photo_image(self, obj):
        return mark_safe('<a href="/{0}"><img src="/{0}" style="width: 60px; height:45px;" /></a>'. format(obj.photo_dir))
    Photo_image.short_description = 'View'
    Photo_image.allow_tags = True
    list_display = ('photo_name','photo_order_code', 'photo_date', 'photo_time')
    search_fields = ('photo_name', 'photo_order_code' , 'photo_date')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {
            'fields': ('photo_name', 'photo_order_code','photo_code')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('photo_dir','photo_pdf_name', 'photo_pdf_dir','photo_check_list' ),
        }),
    )

admin.site.register(Photo, PhotoAdmin)