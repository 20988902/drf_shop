#!/usr/bin/env python
#coding: utf-8
__author__ = 'lixl'
__date__ = '2018/7/24 21:22'

from rest_framework import serializers

from .models import Goods, GoodsCategory, HotSearchWords, GoodsImage, Banner, GoodsCategoryBrand, IndexAd
from django.db.models import Q

# 自关联 嵌套
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields  = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    '''直接使用model,不用单个添加字段'''
    category = CategorySerializer()   # 序列化嵌套，获取外键字段category的值
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'  #  __all__ 使用所有字段

    # 保存数据，会将映射的字段放到validated_data
    def create(self, validated_data):
        return Goods.objects.create(**validated_data)


class HotWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotSearchWords
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True)
        return goods_serializer.data

    ad_goods = serializers.SerializerMethodField()
    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False).data
        return goods_json

    class Meta:
        model = GoodsCategory
        fields = '__all__'




