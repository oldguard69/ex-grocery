from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True, )
    name = models.CharField(max_length=512)
    description = models.TextField()
    price = models.FloatField()
    hard_description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
