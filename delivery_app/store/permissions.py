from rest_framework import permissions
from .models import Store


#только владелец гана озгорто алат башкалар только окуйт
class CheckCreateStore(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'владелец':
            return True
        return False

#ар бир владелец озунун магазининдегини гана озгорто алат
class CheckOwnerStore(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner

# если бироонун магазини мага(владелецке) вопще ачылбасын десек
#class CheckOwnerStore(permissions.BasePermission):
    #def has_object_permission(self, request, view, obj):
        #return request.user == obj.owner


class CheckCourier(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.courier.role == 'доставлен'


#client
class CheckOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 'владелец':
            return False
        return True


class CheckOrderUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.order_client:
            return True
        return False


class CheckCRUD(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.user_role == 'владелец'


class CheckReview(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

