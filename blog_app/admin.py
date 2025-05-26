# blog_app/admin.py
from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    # For tags, Taggit provides its own field in the admin, so no explicit field needed here.
    # It automatically creates a nice widget for adding/selecting tags.

@admin.register(Comment) # Register the new Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['disable_comments', 'enable_comments'] # Custom actions for moderation

    def disable_comments(self, request, queryset):
        queryset.update(active=False)
    disable_comments.short_description = "Disable selected comments"

    def enable_comments(self, request, queryset):
        queryset.update(active=True)
    enable_comments.short_description = "Enable selected comments"