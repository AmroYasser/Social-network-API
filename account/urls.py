from django.urls import path
from .views import RegisterView, get_user_data

urlpatterns = [
    path("register/", RegisterView.as_view(), name="sign_up"),
    path("users/<int:id>/", get_user_data, name="user_detail"),
]
