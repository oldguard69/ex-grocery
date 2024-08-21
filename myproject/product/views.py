from common.models import Product
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView

from product.serializers import ListProductSerializer, RetrieveUpdateProductSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("product_id",)
    ordering = ("product_id",)


class ProductGetUpdate(RetrieveAPIView, UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = RetrieveUpdateProductSerializer
