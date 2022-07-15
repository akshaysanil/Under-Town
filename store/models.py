
from itertools import product
from tabnanny import verbose
from django.db import models
from category.models import MainCategory,SubCategory,Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Product(models.Model):
    product_name  = models.CharField(max_length=100 , unique=True)
    product_slug  = models.SlugField(max_length=100 , unique=True)
    description   = models.TextField()
    price         = models.IntegerField()
    product_image = models.ImageField(upload_to='products')
    is_available  = models.BooleanField(default=True)
    stock         = models.IntegerField()
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    brand         = models.CharField(max_length=100 ,blank=True)
    main_category = models.ForeignKey(MainCategory,on_delete=models.CASCADE,null=True,blank=True)
    category      = models.ForeignKey(Category,on_delete=models.CASCADE,null=True, blank=True)
    sub_category  = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)

    def get_url(self):
        return reverse ('product_detail',args=[self.main_category.slug , self.category.slug , self.sub_category.slug , self.product_slug])

    def __str__(self):
        return self.product_name 


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active= True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size' ,is_active= True)


variation_category_choices = (('color','color'),('size','size'))


class Variation(models.Model):
    product            = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100 , choices=variation_category_choices)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)
    created_date       = models.DateTimeField(auto_now=True)

    objects = VariationManager() 

    def __str__(self):
        return self.variation_value


class Carousel(models.Model):
    category    = models.ForeignKey(Category,on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    banner_image       = models.ImageField(upload_to='products')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BestSellers(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_best = models.BooleanField(default=False)

    def __unicode__(self):
        return self.product 



class ReviewRating(models.Model):
     product = models.ForeignKey(Product,on_delete=models.CASCADE)
     user = models.ForeignKey(Account,on_delete=models.CASCADE)
     subject = models.CharField(max_length=100, blank=True)
     review = models.TextField()
     rating = models.FloatField()
     ip = models.CharField(max_length=20, blank=True)
     status = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
         return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'products',max_length = 225)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery' 







