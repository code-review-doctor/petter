import uuid as uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Deal(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=5000)
    link = models.URLField()
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False)
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    historical_price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=True, default=0)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valid_till = models.DateTimeField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def price_percentage(self):
        return self.current_price / self.historical_price * 100 if self.historical_price > 0 else 0

    def get_absolute_url(self):
        return reverse("deals:detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Comment(models.Model):
    author: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.first_name if self.author.first_name else self.author.username
