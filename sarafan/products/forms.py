from typing import Any

from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from .models import CartItem


class CartModelFormSet(BaseModelFormSet):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.cart = kwargs.pop('cart')
        super().__init__(*args, **kwargs)

    def add_fields(self, form: Any, index: Any) -> Any:
        super().add_fields(form, index)
        form.fields['cart'].initial = self.cart
        form.fields['cart'].widget = forms.HiddenInput()


ShopingCartModelFormSet = modelformset_factory(
    CartItem,
    fields=['product', 'quantity', 'cart'],
    can_delete=True,
    extra=1,
    formset=CartModelFormSet,
)
