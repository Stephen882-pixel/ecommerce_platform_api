from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "slug", "is_active", "created_at")
	list_filter = ("is_active",)
	search_fields = ("name", "slug")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"name",
		"slug",
		"category",
		"price",
		"stock",
		"is_active",
		"is_featured",
		"created_at",
	)
	list_filter = ("is_active", "is_featured", "category")
	search_fields = ("name", "slug", "description")
	prepopulated_fields = {"slug": ("name",)}
	autocomplete_fields = ("category",)

