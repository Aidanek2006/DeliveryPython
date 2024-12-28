from django.urls import path, include
from .views import *
from rest_framework import routers, urls


router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet, basename='user-list')
router.register(r'cart', CartViewSet, basename='cart-list')
router.register(r'cart_item', CartItemViewSet, basename='cart_items')
router.register(r'order', OrderViewSet, basename='order-list')
router.register(r'courier', CourierViewSet, basename='courier-list')
router.register(r'store_review', StoreReviewViewSet, basename='store_reviews')
router.register(r'courier_review', CourierReviewViewSet, basename='courier_reviews')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('store/', StoreListApiView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailApiView.as_view(), name='store_detail'),
    path('store/create/', StoreCreateApiView.as_view(), name='store_create'),
    path('store/edit/<int:pk>/', StoreUpdateDeleteApiView.as_view(), name='store_edit'),

]