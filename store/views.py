

from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import CartItem
from cart.views import _cart_id
from category.models import MainCategory, SubCategory,Category
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product,BestSellers, ProductGallery, ReviewRating
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def store(
    request,
    main_category_slug = None,
    category_slug=None,
    sub_category_slug=None
    ):

    main_categories  = None
    categories       = None
    sub_categories   = None
    products         = None
    
    
    if main_category_slug != None:
        main_categories = get_object_or_404(MainCategory, slug = main_category_slug)
        products        = Product.objects.filter(main_category = main_categories ,is_available= True)

        #main_category pagination
        paginator = Paginator(products,9)
        page = request.GET.get('page')
        paged_proucts   = paginator.get_page(page)
        product_count   = products.count()



        if category_slug != None:
            categories    = get_object_or_404(Category,slug = category_slug)
            products      = Product.objects.filter(category = categories , is_available = True)
             
            #category pagination
            paginator = Paginator(products,9)
            page = request.GET.get('page')
            paged_proucts = paginator.get_page(page)
            product_count =products.count()

            if sub_category_slug != None:
                sub_categories = get_object_or_404(SubCategory,slug = sub_category_slug)
                products       = Product.objects.filter(sub_category = sub_categories , is_available = True)

                #sub category pagination
                paginator = Paginator(products,9)
                page = request.GET.get('page')
                paged_proucts = paginator.get_page('page')
                product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

        #store pagination
        paginator = Paginator(products,9)
        page = request.GET.get('page')
        paged_proucts = paginator.get_page(page)

        product_count = products.count()

    bestsellers = BestSellers.objects.all().filter(is_best =True)

    main_categories = MainCategory.objects.all()
    categories = Category.objects.all()


    context  = {
        'products': paged_proucts,
        'product_count' : product_count,
        'bestsellers' : bestsellers,
        'main':main_categories,
    }
    return render (request,'store/store.html',context)


def product_detail(
    request,
    main_category_slug,
    category_slug,
    sub_category_slug,
    product_slug
    ):
    try:
        single_product = Product.objects.get(
            main_category__slug = main_category_slug , 
            category__slug      = category_slug , 
            sub_category__slug  = sub_category_slug , 
            product_slug        = product_slug
            )
        in_cart = CartItem.objects.filter(
            cart__cart_id = _cart_id(request),
            product       = single_product
        ).exists
    except Exception as e:
        raise e

    product_gallery = ProductGallery.objects.filter(product = single_product)


    bestsellers = BestSellers.objects.all().filter(is_best =True)
    
    context = {
        'single_product' : single_product,
        'in_cart' : in_cart,
        'bestsellers' : bestsellers,
        'product_gallery' : product_gallery,
        

    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains = keyword) | Q(product_name__icontains = keyword) | Q(brand__icontains = keyword)
                )
            paginator = Paginator(products,9)
            page = request.GET.get('page')
            paged_proucts = paginator.get_page(page)

            product_count = products.count()
        else:
            products = Product.objects.all()
            paginator = Paginator(products,9)
            page = request.GET.get('page')
            paged_proucts = paginator.get_page(page)

            product_count = products.count()
        context = {
            'products':paged_proucts,
            'product_count' : product_count,
        }
        
        return render(request,'store/store.html',context)
    return redirect('store')

def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request,'Thank you... Your Review has been updated !')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request,'Thank you... Your review has been updated..')
                return redirect (url)



            
