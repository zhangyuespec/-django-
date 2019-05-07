from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_kefu = models.BooleanField(default=False)

    def __str__(self):
        return "用户名:"+self.username+",用户编号:{}".format(self.nid)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


class Room(models.Model):
    nid = models.AutoField(primary_key=True)
    room_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    room_discribe = models.TextField()
    status = models.CharField(max_length=255, default="空闲")

    def __str__(self):
        return "{}号{}房".format(self.nid, self.room_type)

    class Meta:
        verbose_name = "房屋信息"
        verbose_name_plural = verbose_name


class User_room(models.Model):
    """保存当前订单,订单更新的时候就会取消"""
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="User", to_field="nid")
    room = models.ForeignKey(to="Room", to_field="nid")
    create_time = models.DateTimeField(auto_now_add=True)
    use_time = models.IntegerField()

    def __str__(self):
        return self.user.username + "定{}".format(self.room.nid) + "号房间" + "{}天".format(self.use_time)

    class Meta:
        verbose_name = "当前订单"
        verbose_name_plural = verbose_name


class User_order_room(models.Model):
    """历史订单,创建订单时候一起创建,更新订单时候不更新"""
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="User", to_field="nid")
    room = models.ForeignKey(to="Room", to_field="nid")
    create_time = models.DateTimeField(auto_now_add=True)
    use_time = models.IntegerField()

    def __str__(self):
        return self.user.username + "定{}".format(self.room.nid) + "号房间" + "{}天".format(self.use_time)

    class Meta:
        verbose_name = "历史订单"
        verbose_name_plural = verbose_name




class Room_discount(models.Model):
    nid = models.AutoField(primary_key=True)
    room = models.ForeignKey(to="Room", to_field="nid")
    discount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "{}号房间打{}折".format(self.room.nid, self.discount)

    class Meta:
        verbose_name = "房间折扣"
        verbose_name_plural = verbose_name


class Money_count(models.Model):
    nid = models.AutoField(primary_key=True)
    count = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "总收益为{}".format(self.count)

    class Meta:
        verbose_name = "酒店总收益"
        verbose_name_plural = verbose_name
