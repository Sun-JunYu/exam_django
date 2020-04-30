import datetime
import os

import cv2
from PIL import ImageDraw, ImageFont, Image
from django.shortcuts import render,redirect
#导包
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
#导入类视图
from django.views import View

import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView


# 导入数据库
from django_test.settings import UPLOAD_ROOT
from myapp.models import User

# Create your views here.
# 登录接口
class Login(APIView):

    def get(self,request):

        # 接收参数
        username = request.GET.get('username',None)
        password = request.GET.get('password',None)

        # 查询数据
        user = User.objects.filter(username=username,password=password).first()

        if user:
            return Response({
                'code' : 200,
                'message':'登录成功',
                'uid' : user.id,
                'username':user.username
            })
        else:
            return Response({
                'code':403,
                'message':'您的用户名或密码错误，请重新输入'
            })
        

# 注册接口
class Register(APIView):

    def get(self,request):

        # 接收参数
        username = request.GET.get('username',None)
        password = request.GET.get('password',None)

        # 排重操作
        user = User.objects.filter(username=username).first()

        if user:
            return Response({'code':403,'message':'该用户名已存在'})

        # 入库
        user = User(username = username,password = password)

        # 保存结果
        user.save()

        return Response({'code':200,'message':'恭喜注册成功'})

# 图片加水印压缩
def pic_logo(imgname):
    # 打开图片重新读图操作，为下面加水印做准备
    img = Image.open('./static/upload/' + imgname)
    # 定义字体            指定字体或按照宽高的百分比显示字体大小
    font = ImageFont.truetype(font='C:\\Windows\\Fonts\\msjhbd.ttc', size=20)
    # 生成画笔
    draw = ImageDraw.Draw(img)
    # 绘制     坐标  名字     颜色 字体
    draw.text((1150, 900), 'django2.0.4', fill=(76, 234, 124, 180), font=font)
    # 保存路径存储图片
    img.save('./static/upload/' + imgname)
    print(imgname)
    #压缩图片
    img = cv2.imread('./static/upload/'+imgname)
    #压缩 png压缩等级 0-9
    cv2.imwrite('./static/upload/'+imgname,img,[cv2.IMWRITE_PNG_COMPRESSION,50])

# 上传图片接口
class Upload(APIView):
    # post没有文件限制，get有，所以用post
    def post(self, request):
        # 接收参数
        myfile = request.FILES.get('file')
        id = request.POST.get('uid')
        # 修改上传图片名 引入时间戳
        now_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        myfile.name = id + now_time + '.png'
        # 建立文件流对象 open里定义图片路径  '' 加时间戳或字符串放置覆盖
        f = open(os.path.join(UPLOAD_ROOT, '', myfile.name), 'wb')
        # 写入
        for chunk in myfile.chunks():
            f.write(chunk)
        f.close()
        # 调用上面所创建好的压缩水印的参数
        pic_logo(myfile.name)
        # 查询
        user = User.objects.filter(id=int(id)).first()

        user.img = myfile.name
        user.save()
        # 返回文件名
        return Response({'filename': myfile.name, 'message': '图片上传成功'})