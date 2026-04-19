from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to = "product/%Y/%m/%d")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    # publishers = models.ManyToManyField(Publisher)
    #, null=True, blank=True