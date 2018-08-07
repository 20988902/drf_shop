from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    自定义权限，只有所有者能编辑
    '''

    def has_object_permission(self, request, view, obj):
        # 允许的提交方法
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj是model对象
        return obj.user == request.user




