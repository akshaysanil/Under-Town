from django.urls import reverse
from django.db import models

# Create your models here.

class MainCategory(models.Model):
    main_category_name = models.CharField(max_length=100,unique=True)
    slug               = models.SlugField(max_length=100,unique=True)
    description        = models.TextField(blank=True)
    image              = models.ImageField(upload_to='photos/category' , blank=True)

    class Meta:
        verbose_name       = 'Maincategory'
        verbose_name_plural= 'Maincategories'

    def get_url(self):
        return reverse('products_by_main_category',args=[self.slug])

    def __str__(self):
        return self.main_category_name

    def get_category(self):
        return self.category_set.all()



class Category(models.Model):
    main_category      = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    category_name      = models.CharField(max_length=100,unique=True)
    slug               = models.SlugField(max_length=100,unique=True)
    description        = models.TextField(blank=True)
    image              = models.ImageField(upload_to='photos/category' , blank=True)

    class Meta:
        verbose_name       = 'Category'
        verbose_name_plural= 'Categories'

    def get_url(self):
        return reverse('products_by_category',args=[self.main_category.slug,self.slug])


    def __str__(self):
        return self.main_category.main_category_name +'--'+ self.category_name

    def get_main_category(self):
        return self.main_category_set.all()



class SubCategory(models.Model):
    category          = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100,unique=True)
    slug              = models.SlugField(max_length=100,unique=True)
    description       = models.TextField(blank=True)
    image             = models.ImageField(upload_to='photos/category' , blank=True)
    

    class Meta:
        verbose_name       = 'Subategory'
        verbose_name_plural= 'Subcategories'

    def get_url(self):
        return reverse('products_by_sub_category',args=[self.category.main_category.slug,self.category.slug,self.slug])

    def __str__(self):
        return self.category.main_category.main_category_name +'--' + self.category.category_name +'--' + self.sub_category_name


    



