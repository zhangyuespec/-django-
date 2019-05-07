from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from order import forms, models
import random
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
import numpy as np
from django.db.models import F


# Create your views here.
def register(request):
    form_obj = forms.RegForm()
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        form_obj = forms.RegForm(request.POST)
        print(request.POST)
        # 帮我做校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新的用户
            print(111111)
            print(form_obj.cleaned_data)
            form_obj.cleaned_data.pop("re_password")
            print(66666666)
            # form_obj.cleaned_data.pop("csrfmiddlewaretoken")
            print(form_obj.cleaned_data)
            # print(**form_obj.cleaned_data)
            print(7777)
            try:

                models.User.objects.create_user(**form_obj.cleaned_data)

                ret["msg"] = "/index/"
            except:

                ret["msg"] = "/error/"
                print(ret["msg"])
            print(44444444)

            print(5555555555)
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            print(ret)
            print("=" * 120)
            return JsonResponse(ret)
    # 生成一个form对象
    # form_obj = forms.RegForm()
    print(222222222)
    print(form_obj.fields)
    return render(request, "register.html", {"form_obj": form_obj})


def login(request):
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(username=username, password=pwd)
            if user:
                # 用户名密码正确
                # 给用户做登录
                if user.is_kefu:
                    auth.login(request, user)
                    # ret["msg"] = "/index/"
                    ret["msg"] = "/kefu_index/"
                else:
                    auth.login(request, user)
                    ret["msg"] = "/index/"
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    return render(request, "login.html")


def check_username_exist(request):
    print(555555)
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    print(username + "11111111")
    is_exist = models.User.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册"

    return JsonResponse(ret)


def get_valid_img(request):
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 220  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


def logout(request):
    auth.logout(request)
    return redirect("/index/")


def index(request):
    room_list = models.Room.objects.all()
    room_disscount_list = models.Room_discount.objects.all()
    user_room_list = models.User_room.objects.all()
    return render(request, "index.html",
                  {"room_list": room_list, "room_discount_list": room_disscount_list, "user_room_list": user_room_list})

# from django.db.models import F
def yuding(request, user_pk, room_pk, day):
    user = user_pk
    room = room_pk
    day = day
    if models.User_room.objects.filter(room_id=room):
        return render(request,"user_oder_error.html")
    else:
        models.User_room.objects.create(user_id=user, room_id=room, use_time=day)
        models.User_order_room.objects.create(user_id=user, room_id=room, use_time=day)
        models.Room.objects.filter(pk=room).update(status="被预定")
        # room_temp = models.Room.objects.filter(pk=room)
        # money = room_temp.get('price')
        room_temp = models.Room.objects.filter(nid=room).first()
        money = room_temp.price
        day = int(day)
        try:
            discount = models.Room_discount.objects.filter(room_id=room).first()
            discount = discount.discount
            discount = int(discount)
            M = int(money) * discount * 0.1
            M = M*day
        except:
            M = money
            M = M * day
        countm = models.Money_count.objects.first()
        countm = countm.count
        countm += int(M)


        money_count = models.Money_count.objects.filter(nid=1)
        money_count.update(count=countm)
        return redirect("/index/")

def kefu_yuding(request,  room_pk, day,username):
    user = username
    room = room_pk
    day = day
    # user = models.User.objects.filter(username=user)
    # print(user.nid)
    if models.User_room.objects.filter(room_id=room):
        return render(request,"kefu_yuding_error.html")
    else:
        models.User_room.objects.create(user_id=user, room_id=room, use_time=day)
        models.User_order_room.objects.create(user_id=user,  room_id=room, use_time=day)
        models.Room.objects.filter(pk=room).update(status="被预定")
        room_temp = models.Room.objects.filter(nid=room).first()
        money = room_temp.price
        # print(room_temp.price)
        day = int(day)
        try:
            # print(1111111111111)
            discount = models.Room_discount.objects.filter(room_id=room).first()
            # print(222222222)
            discount=discount.discount
            # print(3333333333)
            discount = int(discount)
            # print(4444444444444)
            # print(money,discount)
            M = int(money)*discount*0.1
            # print(M)
            M = M*day

            # print(M)
        except:
            # print(555555)
            M = money
            M = M * day
        countm = models.Money_count.objects.first()
        countm = countm.count
        # print(countm)
        countm = countm+int(M)
        # print(countm)
        # day = int(day)
        # print(day)
        # countm = countm*day
        # print(countm)
        money_count = models.Money_count.objects.filter(nid=1)
        money_count.update(count = countm)
        return redirect("/kefu_index/")

def user_order(request, user_pk):
    user_order_room = models.User_order_room.objects.filter(user_id=user_pk)
    user_info = models.User.objects.filter(pk=user_pk)
    user_room = models.User_room.objects.filter(user_id=user_pk)
    return render(request, "home.html", {"user_order_room": user_order_room,"user_info":user_info,"user_room":user_room})

# from django.contrib.auth.models import User
def re_password(request,username):
    new = request.POST['password']
    re_new = request.POST['re_password']
    if new != re_new:
        return render(request,"repassword_error.html")
    else:
        user = models.User.objects.get(username=username)
        try:
            user.set_password(new)
            user.save()
            return redirect('/index/')
        except :
            return render(request, "repassword_error.html")

def kefu_index(request):
    room_list = models.Room.objects.all()
    room_disscount_list = models.Room_discount.objects.all()
    user_room_list = models.User_room.objects.all()
    money_count = models.Money_count.objects.filter(nid=1)
    return render(request, "kefu_index.html",
                  {"room_list": room_list, "room_discount_list": room_disscount_list, "user_room_list": user_room_list,"money_list":money_count})

    # return render(request,"kefu_index.html")

def get_kongfang(request):
    type = request.GET.get('book_name')
    room_list = models.Room.objects.filter(status="空闲",room_type__contains=type)
    room_disscount_list = models.Room_discount.objects.all()
    if request.user.is_kefu:
        return render(request, "kefu_index.html",
                      {"room_list": room_list, "room_discount_list": room_disscount_list})
    else:
        return render(request, "index.html",
                      {"room_list": room_list, "room_discount_list": room_disscount_list})

def kefu_order(request, user_pk):
    user_order_room = models.User_order_room.objects.all()
    user_info = models.User.objects.filter(pk=user_pk)
    money_count = models.Money_count.objects.filter(nid=1)
    user_room = models.User_room.objects.all()
    return render(request, "home.html", {"user_order_room": user_order_room,"user_info":user_info,"money_list":money_count,"user_room":user_room})

def kefu_tuiding(request,user_pk,room_pk):
    try:
        models.User_room.objects.filter(user_id=user_pk,room_id=room_pk).delete()
        models.Room.objects.filter(nid=room_pk).update(status="未打扫")
        return redirect('/kefu_index/')
    except:
        return render(request,"kefu_tuiding_error.html")

def change_status(request,room_pk,status):
    try:
        a = models.User_room.objects.filter(room_id=room_pk)
        if a:
            return render(request,"no_change.html")
        models.Room.objects.filter(nid=room_pk).update(status=status)
        return redirect('/kefu_index/')
    except:
        return render(request,"no.html")