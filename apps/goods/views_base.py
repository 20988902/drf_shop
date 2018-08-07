#!/usr/bin/env python
#coding: utf-8
__author__ = 'lixl'
__date__ = '2018/7/24 0:08'

from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from goods.models import Goods
import json

class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]

        # 方式一
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        # return JsonResponse(json_list, safe=False)
        # return HttpResponse(json.dumps(json_list), content_type='application/json')

        # 方式二
        from django.core import serializers
        json_data = serializers.serialize('json', goods)
        return HttpResponse(json_data, content_type='application/json')