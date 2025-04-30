from django.urls import path
from . import views


# чтобы ссылаться на маршруты вот так: blog:post_list
# для избежания конфликта имен между различными приложениями
app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>",
         views.post_detail,
         name="post_detail"),
]
