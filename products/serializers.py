from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = [
			"id",
			"name",
			"slug",
			"description",
			"is_active",
			"created_at",
			"updated_at",
		]
		read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)
	category_id = serializers.PrimaryKeyRelatedField(
		queryset=Category.objects.all(), source="category", write_only=True
	)

	class Meta:
		model = Product
		fields = [
			"id",
			"name",
			"slug",
			"description",
			"price",
			"stock",
			"is_active",
			"is_featured",
			"image",
			"category",
			"category_id",
			"created_at",
			"updated_at",
		]
		read_only_fields = ["id", "created_at", "updated_at", "category"]
