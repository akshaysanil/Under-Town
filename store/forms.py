from dataclasses import field, fields
from pyexpat import model
from django import forms
from .models import Carousel, Product, ReviewRating, Variation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','description','price','product_image','is_available','stock','brand','main_category','category','sub_category']

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)

        self.fields['product_name'].widget.attrs['placeholder']='Enter Product name'
        self.fields['product_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['product_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Product discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3

        self.fields['price'].widget.attrs['placeholder']='Enter Product Price'
        self.fields['price'].widget.attrs['class']='form-control form-control-user'
        self.fields['price'].widget.attrs['type']='text'

        self.fields['stock'].widget.attrs['placeholder']='Enter Product Stock'
        self.fields['stock'].widget.attrs['class']='form-control form-control-user'
        self.fields['stock'].widget.attrs['type']='text'

        self.fields['brand'].widget.attrs['placeholder']='Enter Product Brand'
        self.fields['brand'].widget.attrs['class']='form-control form-control-user'
        self.fields['brand'].widget.attrs['type']='text'

        self.fields['main_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['category'].widget.attrs['class']='form-control form-control-user'

        self.fields['sub_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['product_image'].widget.attrs['placeholder']='Add images'
        self.fields['product_image'].widget.attrs['class']='form-control'
        self.fields['product_image'].widget.attrs['type']='file'


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product','variation_category','variation_value','is_active']
        



class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']


