from rest_framework import permissions

class IsSupplier(permissions.BasePermission):
    """Доступ только для Поставщиков"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'supplier'

class IsConsumer(permissions.BasePermission):
    """Доступ только для Потребителей"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'consumer'