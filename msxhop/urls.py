"""msxhop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from msxhop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework_jwt import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from goods.views import GoodsListViewSet, CategoryVieweSet, HotSearchsViewset, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset,AddressViewset
from trade.views import ShoppingCartViewset,OrderViewset


# router方式
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'categorys', CategoryVieweSet,  base_name='categorys')
router.register(r'hotsearchs', HotSearchsViewset,  base_name='hotsearchs')
router.register(r'codes', SmsCodeViewset,  base_name='codes')
router.register(r'users', UserViewset,  base_name='users')
router.register(r'userfavs', UserFavViewset,  base_name='userfavs')
router.register(r'messages', LeavingMessageViewset,  base_name='messages')
router.register(r'address', AddressViewset,  base_name='address')
router.register(r'shopcarts', ShoppingCartViewset,  base_name='shopcarts')
router.register(r'orders', OrderViewset,  base_name='orders')
router.register(r'banners', BannerViewset,  base_name='banners')
router.register(r'indexgoods', IndexCategoryViewset,  base_name='indexgoods')



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'docs/', include_docs_urls(title='我的文档')),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^jwt-auth/', views.obtain_jwt_token),
    url(r'^login/$', views.obtain_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'goods/$', goods_list, name='goods_list'),
    # 第三方登录
    url('', include('social_django.urls', namespace='social')),

    url(r'^', include(router.urls)),
]
