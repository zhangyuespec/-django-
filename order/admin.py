from django.contrib import admin

# Register your models here.
from order import models

admin.site.register(models.Room)
admin.site.register(models.User)
admin.site.register(models.Money_count)
admin.site.register(models.Room_discount)
# admin.site.register(models.Room_status)
admin.site.register(models.User_order_room)
admin.site.register(models.User_room)