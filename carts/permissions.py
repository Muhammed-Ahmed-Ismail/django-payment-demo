from rest_framework.permissions import BasePermission


class IsOwnerOfCartLine(BasePermission):

    def has_object_permission(self, request, view, cart_line):
        return cart_line.cart.user == request.user


class IsOwnerOfCart(BasePermission):
    def has_object_permission(self, request, view, cart):
        return cart.user == request.user

