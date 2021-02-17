from django.db import models, transaction
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator
PALET = (
    ('EPAL', 'EPAL'),
    ('Castom', 'Castom'),
    ('Other', 'Other'),
)
class Client(models.Model):
    client_name = models.CharField(max_length=100, unique=True)
    client_info = models.CharField(max_length=100)
    client_logo_220x220 =models.ImageField(upload_to='logo')
    REQUIRED_FIELDS = ['client_name']
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Client"

    def __str__(self):
        return self.client_name

class Product(models.Model):
    product_name = models.CharField(max_length=500, unique=True)
    product_size = models.CharField(max_length=100)
    product_weight = models.CharField(max_length=100)
    product_revision = models.CharField(max_length=500)
    product_youtube_manual = models.CharField(max_length=500)
    REQUIRED_FIELDS = ['product_name']
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Product"

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
    order_product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=100)
    order_pcs = models.IntegerField(null=True, blank=True)
    order_done_pcs = models.IntegerField(default=0)
    order_palet = models.CharField(max_length=50, choices=PALET, null=True, blank=True)   
    order_add_date = models.DateField(auto_now_add=True)
    order_end_date = models.DateField()
    order_in_work = models.BooleanField(default=False)
    workers_are_doing = models.BooleanField(default=False)
    order_description = models.TextField(max_length=5200, blank=True)
    REQUIRED_FIELDS = ['order_code']
    def save(self, *args, **kwargs):
        if not self.workers_are_doing:
            return super(Order, self).save(*args, **kwargs)
        with transaction.atomic():
            Order.objects.filter(
                workers_are_doing=True).update(workers_are_doing=False)
            return super(Order, self).save(*args, **kwargs)


    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Order"



class Photo(models.Model):
    photo_name = models.CharField(max_length=500, unique=True)
    photo_order_code = models.CharField(max_length=500)
    photo_code = models.CharField(max_length=500)
    photo_dir = models.CharField(max_length=500)
    photo_pdf_name = models.CharField(max_length=500, blank=True)
    photo_pdf_dir = models.CharField(max_length=500, blank=True)
    photo_date = models.DateField(auto_now_add=True)
    photo_time = models.TimeField(auto_now=True)
    photo_check_list = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['photo_name']
    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photo"

    def __str__(self):
        return self.photo_name



class Check_list(models.Model):
    check_order_code = models.CharField(max_length=500, unique=True)
    check_photo_name = models.CharField(max_length=100)
    check_photo_date = models.DateField(auto_now_add=True)
    check_validation = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['check_order_code']
    class Meta:
        verbose_name = "Checking of picking"
        verbose_name_plural = "Checking of picking"

    def __str__(self):
        return self.check_order_code