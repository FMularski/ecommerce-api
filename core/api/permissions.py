from rest_framework import permissions

from core.models import Role


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.CUSTOMER


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.SELLER
