from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer, AddressSerializer
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    list:
        获取用户收藏功能
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)   # 未登录，抛401错误
    # serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'   # 搜索字段

    # 获取当前用户的queryset
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    # 动态serializer
    def get_serializer_class(self):
        if self.action == 'list':   # 获取信息时需要权限
            return UserFavDetailSerializer
        elif self.action == "create":   # 新建,不需要权限
            return UserFavSerializer
        return UserFavSerializer

    # 增加收藏数
    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


class LeavingMessageViewset(mixins.ListModelMixin, mixins.DestroyModelMixin,
                            mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除用户留言
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)



