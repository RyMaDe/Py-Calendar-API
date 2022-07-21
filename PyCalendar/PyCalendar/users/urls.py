from django.urls import path
from .views import (
    CustomUserCreate,
    CustomUserCreateSite,
    LoginUserSite,
    LogoutUserSite,
    UpdateUserDetails,
    UpdateUserPassword,
    )

app_name = "users"

urlpatterns = [
    path('api/register/', CustomUserCreate.as_view(), name="Create_user"),
    path('register/', CustomUserCreateSite.as_view(), name="Create_user_site"),
    path('login/', LoginUserSite.as_view(), name="Login_user"),
    path('logout/', LogoutUserSite.as_view(), name="Logout_user"),
    path('update/', UpdateUserDetails.as_view(), name="Update_user"),
    path('update/password/', UpdateUserPassword.as_view(), name="Update_password_user"),
]
