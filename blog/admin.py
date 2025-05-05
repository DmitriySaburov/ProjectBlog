from django.contrib import admin
<<<<<<< HEAD
from .models import Post, Comment
=======

from .models import Post, Comment

>>>>>>> 42b16e22dd2834e5ac39e56518cc4e3ed3a747f5


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

<<<<<<< HEAD
=======

>>>>>>> 42b16e22dd2834e5ac39e56518cc4e3ed3a747f5
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
