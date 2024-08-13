from django.contrib import admin

from .models import (
    ProductCategory, ProductSubCategory,
    Product, ShopingCart, CartItem,
)


class ProductCategoryAdmin(admin.ModelAdmin):

    pass


class ProductSubCategoryAdmin(admin.ModelAdmin):

    pass


class ProductAdmin(admin.ModelAdmin):

    readonly_fields = ('mid_image', 'small_image')


class ShopingCartAdmin(admin.ModelAdmin):

    pass


class CartItemAdmin(admin.ModelAdmin):

    pass


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductSubCategory, ProductSubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShopingCart, ShopingCartAdmin)
admin.site.register(CartItem, CartItemAdmin)
