# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='username', max_length=30, unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'})),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=254, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_kefu', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Money_count',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('count', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '酒店总收益',
                'verbose_name_plural': '酒店总收益',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('room_discribe', models.TextField()),
                ('status', models.CharField(max_length=255, default='空闲')),
            ],
            options={
                'verbose_name': '房屋信息',
                'verbose_name_plural': '房屋信息',
            },
        ),
        migrations.CreateModel(
            name='Room_discount',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('discount', models.DecimalField(max_digits=8, decimal_places=2)),
                ('room', models.ForeignKey(to='order.Room')),
            ],
            options={
                'verbose_name': '房间折扣',
                'verbose_name_plural': '房间折扣',
            },
        ),
        migrations.CreateModel(
            name='User_order_room',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('use_time', models.IntegerField()),
                ('room', models.ForeignKey(to='order.Room')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '历史订单',
                'verbose_name_plural': '历史订单',
            },
        ),
        migrations.CreateModel(
            name='User_room',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('use_time', models.IntegerField()),
                ('room', models.ForeignKey(to='order.Room')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '当前订单',
                'verbose_name_plural': '当前订单',
            },
        ),
    ]
