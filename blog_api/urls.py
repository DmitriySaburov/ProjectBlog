from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .views import PostList, PostDetail, UserPostList



urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    re_path("^user/(?P<id>.+)/$", UserPostList.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
