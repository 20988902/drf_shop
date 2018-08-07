import time
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import mixins
from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer, ShopCarDetailSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewset(viewsets.ModelViewSet):
    '''
    购物车功能
    list:
        获取购物车详情
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    # queryset = ShoppingCart.objects.all()
    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == "list":
            return ShopCarDetailSerializer
        else:
            return ShopCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    # 增加购物车数量
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 删除购物车数量
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    # 修改购物车数量
    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()   # 保存购物车里的商品到OrderGoods表
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order







