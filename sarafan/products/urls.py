from django.urls import path

from .views import (
    CategoriesListView,
    ProductListView,
    ShopingCartDetailView,
    ShopingCartDeleteView,
    ChangeShopingCartItems,
)


urlpatterns = [
    path('', ProductListView.as_view(), name='products-list'),
    path('category/', CategoriesListView.as_view(), name='category-list'),
    path(
        'cart/<int:user_id>/',
        ShopingCartDetailView.as_view(),
        name='user-cart',
    ),
    path(
        'cart/<int:user_id>/change/',
        ChangeShopingCartItems.as_view(),
        name='user-cart-change',
    ),
    path(
        'cart/<int:user_id>/delete/',
        ShopingCartDeleteView.as_view(),
        name='user-cart-delete',
    ),
]
