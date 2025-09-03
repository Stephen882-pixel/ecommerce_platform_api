from django.urls import path
from .views import (
	ProductListCreateView,
	ProductDetailView,
	ProductSearchView,
	ProductFilterView,
	FeaturedProductsView,
	CategoryListCreateView,
	CategoryDetailView,
)


urlpatterns = [
	# Products
	path("", ProductListCreateView.as_view(), name="product-list-create"),
	path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
	path("search/", ProductSearchView.as_view(), name="product-search"),
	path("filter/", ProductFilterView.as_view(), name="product-filter"),
	path("featured/", FeaturedProductsView.as_view(), name="product-featured"),

	# Categories
	path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
	path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
]

