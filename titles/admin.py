from django.contrib import admin

from .models import Title, Genre, Category, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk", "name", "year", "rating", "description", "genre", "category"
    )
    search_fields = ("name",)
    empty_value_display = "-empty-"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-empty-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-empty-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "author", "text", "pub_date", "score")
    search_fields = ("text",)
    empty_value_display = "-empty-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "author", "text", "pub_date")
    search_fields = ("text",)
    empty_value_display = "-empty-"
