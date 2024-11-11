from django.contrib import admin
from .models import Category, Product, BlogPost


# Настройка для модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Настройка для модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'is_published', 'views_count']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']


admin.site.register(BlogPost, BlogPostAdmin)
