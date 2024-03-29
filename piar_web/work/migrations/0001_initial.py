# Generated by Django 3.0.5 on 2021-02-17 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_order_code', models.CharField(max_length=500, unique=True)),
                ('check_photo_name', models.CharField(max_length=100)),
                ('check_photo_date', models.DateField(auto_now_add=True)),
                ('check_validation', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Checking of picking',
                'verbose_name_plural': 'Checking of picking',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, unique=True)),
                ('client_info', models.CharField(max_length=100)),
                ('client_logo_220x220', models.ImageField(upload_to='logo')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Client',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_name', models.CharField(max_length=500, unique=True)),
                ('photo_order_code', models.CharField(max_length=500)),
                ('photo_code', models.CharField(max_length=500)),
                ('photo_dir', models.CharField(max_length=500)),
                ('photo_pdf_name', models.CharField(blank=True, max_length=500)),
                ('photo_pdf_dir', models.CharField(blank=True, max_length=500)),
                ('photo_date', models.DateField(auto_now_add=True)),
                ('photo_time', models.TimeField(auto_now=True)),
                ('photo_check_list', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photo',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500, unique=True)),
                ('product_size', models.CharField(max_length=100)),
                ('product_weight', models.CharField(max_length=100)),
                ('product_revision', models.CharField(max_length=500)),
                ('product_youtube_manual', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(max_length=100)),
                ('order_pcs', models.IntegerField(blank=True, null=True)),
                ('order_done_pcs', models.IntegerField(default=0)),
                ('order_palet', models.CharField(blank=True, choices=[('EPAL', 'EPAL'), ('Castom', 'Castom'), ('Other', 'Other')], max_length=50, null=True)),
                ('order_add_date', models.DateField(auto_now_add=True)),
                ('order_end_date', models.DateField()),
                ('order_in_work', models.BooleanField(default=False)),
                ('workers_are_doing', models.BooleanField(default=False)),
                ('order_description', models.TextField(blank=True, max_length=5200)),
                ('order_client_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.Client')),
                ('order_product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.Product')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Order',
            },
        ),
    ]
