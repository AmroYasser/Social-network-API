from django.urls import path
from .views import PostViewSet, LikeViewSet

post_list = PostViewSet.as_view({"get": "list", "post": "create"})

post_detail = PostViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

post_like = LikeViewSet.as_view({"post": "create"})

urlpatterns = [
    path("", post_list, name="post_list"),
    path("<int:pk>/", post_detail, name="post_detail"),
    path("like_unlike/", post_like, name="post_like"),
]
