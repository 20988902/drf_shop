#!/usr/bin/env python
#coding: utf-8
__author__ = 'lixl'
__date__ = '2018/7/26 22:02'

import re
from datetime import datetime, timedelta
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from msxhop.settings import REGEX_MOBILE
from .models import VerifyCode


User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        '''
        验证手机号码
        :param data: mobile
        :return:
        '''
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('用户号码非法')

        # 验证手机号码发送频率
        one_minute_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minute_ago, mobile=mobile).count():
            raise serializers.ValidationError('距离上一次发送未超过60秒')

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情序列化类
    '''
    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday','email','mobile')


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True,min_length=4, max_length=4,
                                 label='验证码',
                                 error_messages= {   # 定义错误显示的内容
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误',
                                 },
                                 help_text='验证码')   # 添加model里没有定义的字段
    # 验证唯一性
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已存在')]
                                     )
    password = serializers.CharField(write_only=True, label='密码', style={'input_type': 'password'})

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')   # 用户前端传过来的值都会放在initial_data
        if verify_records:
            last_record = verify_records[0]
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minute_ago < last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    # 对所有字段的处理
    def validate(self, attrs):   # attrs是验证后,返回的所有字段的dict
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'password', 'code', 'mobile')














