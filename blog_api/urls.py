from django.urls import path, re_path

from .views import PostList, PostDetail, UserPostList



urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    re_path("^user/(?P<id>.+)/$", UserPostList.as_view()),
]
