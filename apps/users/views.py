from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from .models import VerifyCode

from utils.yunpian import YunPian
from random import choice
import string

User = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 使用username和mobile验证用户名
            user = User.objects.get(Q(username=username) | Q(mobile=username))  # 使用get,是希望只查询到一个用户
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        '''生成4位数字的验证码'''
        seeds = string.digits
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)   # 调用SmsSerializer,验证前端提交的数据
        serializer.is_valid(raise_exception=True)   # 验证不通过,返回400错误码
        mobile = serializer.validated_data['mobile']   # 获取'mobile'的值
        return Response({
            'mobile': mobile,
        }, status=status.HTTP_201_CREATED)

    '''
        # 调用接口发送验证码
        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile,
            }, status=status.HTTP_201_CREATED)
    '''


class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    用户
    '''
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    # 动态设置serializer
    def get_serializer_class(self):
        if self.action == 'retrieve':   # 获取详细信息时需要权限
            return UserDetailSerializer
        elif self.action == "create":   # 新建,不需要权限
            return UserRegSerializer
        return UserDetailSerializer

    # 动态设置权限
    def get_permissions(self):
        if self.action == 'retrieve':   # 获取,删除时需要权限
            return [permissions.IsAuthenticated()]
        elif self.action == "create":   # 新建,不需要权限
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        # 生成jwt token
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()





