from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav, UserLeavingMessage, UserAddress
from goods.serializers import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods', 'id')

class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())   # 将用户设置为当前登陆用户
    class Meta:
        model = UserFav
        #  设置联合唯一，也可以在数据库设置联合唯一
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),   # 联合唯一的字段
                message="已收藏",   # 出错时返回的信息
            )
        ]

        fields = ('user', 'goods', 'id')


class LeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())   # 将用户设置为当前登陆用户
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserLeavingMessage
        fields = ('id','user','message_type','subject','message','file','add_time')


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 将用户设置为当前登陆用户

    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name','signer_mobile')

