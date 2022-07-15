from django import forms
from .models import Awesome
from store.models import Carousel,BestSellers



class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['category','title','banner_image','is_available']


