#!/usr/bin/env python
#coding: utf-8
__author__ = 'lixl'
__date__ = '2018/7/30 22:12'
from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer

class ShopCarDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, )
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    #add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    nums = serializers.IntegerField(required=True, min_value=1,
                                    error_messages={
                                        'min_value':'商品数量不能小于1',
                                        'required': '请选择购买数量',
                                    }, label='数量')
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user   # 获取request,获取当前用户
        nums = validated_data['nums']
        goods = validated_data['goods']    #goods是外键，获取的是对象

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:    # 存在，数量+1
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:   # 不存在，创建数据
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    # 重写update
    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance

class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)
    class Meta:
        model = OrderGoods
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        # 生成订单号
        from random import Random
        import time
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                       userid=self.context['request'].user.id,
                                                       ranstr=random_ins.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'




