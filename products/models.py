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

