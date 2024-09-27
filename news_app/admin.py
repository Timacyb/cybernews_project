from django.contrib import admin

# Register your models here.
from .models import News, Category, Contact, Comment


@admin.register(News)
class NewAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "publish_time", "status"]
    list_filter = ["status", "created_time", "publish_time"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_time"
    search_fields = ["title", "body"]
    ordering = ["status", "publish_time"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["id"]


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ["name"]
admin.site.register(Contact)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments', 'activate_comments']

    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def activate_comment(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Comment, CommentAdmin)