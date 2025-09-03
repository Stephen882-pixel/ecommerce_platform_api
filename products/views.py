from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class DefaultPagination(PageNumberPagination):
	page_size_query_param = "page_size"
	max_page_size = 100


class IsAdminOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in ("GET", "HEAD", "OPTIONS"):
			return True
		return bool(request.user and request.user.is_staff)


# Products
class ProductListCreateView(generics.ListCreateAPIView):
	queryset = Product.objects.filter(is_active=True)
	serializer_class = ProductSerializer
	pagination_class = DefaultPagination
	permission_classes = [IsAdminOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ["name", "description", "category__name"]
	ordering_fields = ["created_at", "price", "name"]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [IsAdminOrReadOnly]
	lookup_field = "pk"


class ProductSearchView(generics.ListAPIView):
	serializer_class = ProductSerializer
	pagination_class = DefaultPagination

	def get_queryset(self):
		query = self.request.query_params.get("q", "").strip()
		qs = Product.objects.filter(is_active=True)
		if query:
			qs = qs.filter(
				Q(name__icontains=query)
				| Q(description__icontains=query)
				| Q(category__name__icontains=query)
			)
		return qs


class ProductFilterView(generics.ListAPIView):
	serializer_class = ProductSerializer
	pagination_class = DefaultPagination

	def get_queryset(self):
		qs = Product.objects.filter(is_active=True)
		category_id = self.request.query_params.get("category")
		min_price = self.request.query_params.get("min_price")
		max_price = self.request.query_params.get("max_price")
		is_featured = self.request.query_params.get("featured")

		if category_id:
			qs = qs.filter(category_id=category_id)
		if min_price is not None:
			qs = qs.filter(price__gte=min_price)
		if max_price is not None:
			qs = qs.filter(price__lte=max_price)
		if is_featured is not None:
			qs = qs.filter(is_featured=is_featured.lower() in ["1", "true", "yes"])
		return qs


class FeaturedProductsView(generics.ListAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.filter(is_active=True, is_featured=True)
	pagination_class = DefaultPagination


# Categories
class CategoryListCreateView(generics.ListCreateAPIView):
	queryset = Category.objects.filter(is_active=True)
	serializer_class = CategorySerializer
	permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAdminOrReadOnly]
	lookup_field = "pk"