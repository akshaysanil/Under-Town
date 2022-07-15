from django.shortcuts import render
from home.models import Awesome
from store.models import BestSellers, Product,Carousel
from category.models import Category

# Create your views here.
def home (request):
    products       = Product.objects.all().filter(is_available = True)
    product_count = products.count()
    carousels = Carousel.objects.all().filter(is_available = True)


    bestsellers = BestSellers.objects.all().filter(is_best =True)
    awesomes = Awesome.objects.all().filter(is_awesome =True)
    category = Category.objects.all()

    context  = {
        'products' : products,
        'product_count' : product_count,
        'carousels' : carousels,
        'bestsellers' : bestsellers,
        'awesomes' : awesomes, 
        'category' : category,

    }

    return render (request,'home.html',context) 