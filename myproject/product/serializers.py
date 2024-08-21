from common.models import Product
from rest_framework.serializers import ModelSerializer


class ListProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("product_id", "name", "price", "description")


class RetrieveUpdateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("product_id", "name", "price", "description", "created_at", "updated_at")
