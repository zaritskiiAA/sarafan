from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

from .utils import set_cookie
from sarafan.core.backend import JWTifier
from sarafan.constants import JWTAuthSettings


def register_view(request):

    if request.user.is_authenticated:
        return redirect('products-list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return redirect('products-list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                username=username, password=password,
            ) or request.user

            if user.is_authenticated:
                jwtifier = JWTifier(user)
                access, refresh = jwtifier.create_refresh()
                response = redirect('products-list')
                set_cookie(
                    response,
                    JWTAuthSettings.JWT_ACCESS_HEADER.value,
                    f'Bearer {access}',
                )
                set_cookie(
                    response,
                    f"Refresh{JWTAuthSettings.JWT_ACCESS_HEADER.value}",
                    f'{refresh}',
                    path=JWTAuthSettings.JWT_REFRESH_PATH.value,
                )
                return response
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):

    response = redirect('login')

    if request.user.is_authenticated:

        if JWTAuthSettings.JWT_LOGOUT_ACCESS.value:
            set_cookie(response, JWTAuthSettings.JWT_ACCESS_HEADER.value, "")

        set_cookie(
            response,
            f"Refresh{JWTAuthSettings.JWT_ACCESS_HEADER.value}",
            "",
            path=JWTAuthSettings.JWT_REFRESH_PATH.value,
        )
        return response

    return response


def refresh_view(request):

    try:
        token_str = request.COOKIES.get(
            f"Refresh{JWTAuthSettings.JWT_ACCESS_HEADER.value}"
        )

        token = JWTifier.token_from_str(token_str)
        assert token is not None
        assert token["user"].is_active

        jwtifier = JWTifier(token["user"])
        assert jwtifier.validate_token(token_str, "refresh")
        access = jwtifier.create_access()

        response = redirect('products-list')
        set_cookie(
            response, JWTAuthSettings.JWT_ACCESS_HEADER.value, f"Bearer {access}"
        )
        return response
    except (AssertionError, ValueError):
        return redirect('login')
