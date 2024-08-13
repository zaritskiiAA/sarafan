from typing import Any

from django.shortcuts import render, redirect
from django.http import (
    HttpRequest, HttpResponse,
    HttpResponseRedirect, HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views.generic import DetailView, DeleteView, View
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import ProductCategory, Product, ShopingCart
from .forms import ShopingCartModelFormSet
from sarafan.constants import NumericalValues


class CategoriesListView(ListView):
    """Выводит список категорий и связанных подкатегорий."""

    model = ProductCategory
    template_name = 'products/category.html'
    paginate_by = NumericalValues.PAGINATION_CATEGORY_VALUE


class ProductListView(ListView):
    """Выводит список продуктов."""

    model = Product
    template_name = 'products/product.html'
    paginate_by = NumericalValues.PAGINATION_PRODUCT_VALUE

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.select_related(
            'sub_category', 'sub_category__category',
        ).all()


class ShopingCartDetailView(LoginRequiredMixin, DetailView):
    """Выводит корзину пользователя."""

    model = ShopingCart
    pk_url_kwarg = 'user_id'
    template_name = 'products/shoping_cart.html'

    def dispatch(
            self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:

        if request.user.id != self.kwargs.get(self.pk_url_kwarg):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        return get_object_or_404(
            ShopingCart, user=self.kwargs.get(self.pk_url_kwarg),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        context['url_kwarg'] = self.kwargs.get(self.pk_url_kwarg)
        cart_items = context['object'].items.select_related('product').all()
        context['cart_items'] = cart_items
        context['total_values'] = cart_items.aggregate(
            total_price=Sum(F('product__price') * F('quantity')),
            total_quantity=Sum(F('quantity')),
        )
        return context


class ShopingCartDeleteView(LoginRequiredMixin, DeleteView):
    """Очищаем корзину пользователя."""

    model = ShopingCart
    template_name = 'products/shoping_cart_confirm_delete.html'
    pk_url_kwarg = 'user_id'

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:

        if request.user.id != self.kwargs.get(self.pk_url_kwarg):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        return get_object_or_404(
            ShopingCart, user=self.kwargs.get(self.pk_url_kwarg),
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['url_kwarg'] = self.kwargs.get(self.pk_url_kwarg)
        return context

    def form_valid(self, form):

        success_url = self.get_success_url()
        cart_item = self.object.items.all()
        if cart_item:
            cart_item.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):

        return reverse_lazy(
            'user-cart', kwargs={
                self.pk_url_kwarg: self.kwargs.get(self.pk_url_kwarg),
            }
        )


class ChangeShopingCartItems(LoginRequiredMixin, View):

    """Добавляет, изменяет количество или удаляет продукты из корзины."""

    model = ShopingCart
    template_name = 'products/change_shoping_cart_items.html'
    pk_url_kwarg = 'user_id'

    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:

        if request.user.id != self.kwargs.get(self.pk_url_kwarg):
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        return get_object_or_404(ShopingCart, user=self.request.user)

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:

        formset = ShopingCartModelFormSet(cart=self.get_object())
        return render(
            request,
            'products/change_shoping_cart_items.html',
            {'formset': formset},
        )

    def post(self, request: HttpRequest, *args, **kwargs: Any) -> HttpResponse:

        formset = ShopingCartModelFormSet(request.POST, cart=self.get_object())
        if formset.is_valid():
            formset.save()
            return redirect('user-cart', user_id=request.user.id)
        formset = ShopingCartModelFormSet(cart=self.get_object())
        return render(
            request,
            'products/change_shoping_cart_items.html',
            {'formset': formset},
        )
