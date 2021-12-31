from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Brand(models.Model):
    brand = models.CharField(max_length=150)
    website = models.URLField()
    logo = models.ImageField(upload_to='brands',
                             null=True,
                             blank=True,
                             default='img.png')
    description = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=50, allow_unicode=True, blank=True, editable=False)

    def __str__(self):
        return str(self.brand)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand)
        super(Brand, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:brand_detail", args=[str(self.slug)])

    class Meta:
        ordering = ['brand']


class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, blank=True, null=True)
    product_image = models.ImageField(upload_to='products',
                                      null=True,
                                      blank=True,
                                      default='img.png')
    slug = models.SlugField(unique=True, max_length=50, allow_unicode=True, blank=True, editable=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.brand)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse("products:product_detail", args=[str(self.slug)])


class Price(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6)
    check_date = models.DateTimeField(auto_now_add=True, editable=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, blank=False, null=False)

    def __str__(self):
        return f'{self.price} {self.product}'

    class Meta:
        ordering = ['-check_date']
