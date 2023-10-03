from django.db import models
from core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    company = models.ForeignKey('user.Company', related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(unique=True)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(Category, related_name='products')
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name