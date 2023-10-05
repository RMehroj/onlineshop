from django.db import models
from core.models import BaseModel
import datetime 

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Categories'

    @staticmethod
    def get_all_categories(): 
        return Category.objects.all() 

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    company = models.ForeignKey('user.Company', related_name='products', blank=True, null=True, on_delete=models.SET_NULL)
    website = models.URLField(unique=True)
    slug = models.SlugField(unique=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='products')
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return str(self.name) + ": $" + str(self.price)
    
    @staticmethod
    def get_product_by_id(ids): 
        return Product.objects.filter(pk__in=ids) 
  
    @staticmethod
    def get_all_product(): 
        return Product.objects.all() 
  
    @staticmethod
    def get_all_product_by_categories(categories_pk): 
        if categories_pk: 
            return Product.objects.filter(categories=categories_pk) 
        else: 
            return Product.get_all_product() 

  
class Order(BaseModel): 
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE) 
    user = models.ForeignKey('user.User', 
                                 on_delete=models.CASCADE) 
    quantity = models.IntegerField(default=1) 
    price = models.IntegerField() 
    address = models.CharField(max_length=50, default='', blank=True) 
    phone = models.CharField(max_length=50, default='', blank=True) 
    date = models.DateField(default=datetime.datetime.today) 
    status = models.BooleanField(default=False) 
  
    def placeOrder(self): 
        self.save() 
  
    @staticmethod
    def get_orders_by_company(company_pk): 
        return Order.objects.filter(company=company_pk).order_by('-date')
    
