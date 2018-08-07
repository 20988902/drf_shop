from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, IndexCategorySerializer
from .models import Goods, GoodsCategory,HotSearchWords, Banner
from .filters import GoodsFilter
from rest_framework import filters


class GoodsResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 33



class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all().order_by('id')  # 查询所有记录,必须赋值给queryset
    serializer_class = GoodsSerializer  # 必须叫serializer_class
    # authentication_classes = (TokenAuthentication,)    # 需要认证时配置
    pagination_class = GoodsResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)   # 过滤器
    filterset_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    # 增加点击数
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryVieweSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet,):
    '''
    list:
         商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True)
    serializer_class = IndexCategorySerializer




