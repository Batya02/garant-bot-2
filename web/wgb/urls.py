from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("users", users, name="users"),
    path("more-info/<int:user_id>", more_info_user),
    path("login/", login),
    path("profile/<int:user_id>", user_profile, name="user_profile"),
    path("profile/<int:user_id>/shops", shops, name="shops"),
    path("profile/<int:user_id>/sales", sales, name="sales"),
    path("logout", logout)
]

handler404 = pageNotFound