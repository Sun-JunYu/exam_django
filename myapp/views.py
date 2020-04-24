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