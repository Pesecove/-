from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, RegisterView, WarehouseViewSet

router = DefaultRouter()
router.register(r"warehouses", WarehouseViewSet)
router.register(r"products", ProductViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]