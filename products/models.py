from django.db import models

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(max_length=140, unique=True)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["name"]
		verbose_name_plural = "Categories"

	def __str__(self) -> str:
		return self.name



class Product(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True)
	category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False)
	image = models.ImageField(upload_to="products/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["slug"]),
			models.Index(fields=["is_featured", "is_active"]),
		]

	def __str__(self) -> str:
		return self.name