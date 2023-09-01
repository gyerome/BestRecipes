from django.contrib import admin
from .models import Recipe, Category, UserSubscribes, Forum, Comment, Forum_theme
from django.db.models import F


admin.site.register(Category)
admin.site.register(UserSubscribes)
admin.site.register(Forum)
admin.site.register(Forum_theme)

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for comment in queryset:
            comment.forum.comments-=1
            comment.forum.save()

        queryset.delete()

@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for recipe in queryset:
            recipe.author.recipes_quantity-=1
            recipe.author.save()

        queryset.delete()