from django.db import models
from .user import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)
    status = models.IntegerField()