from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist

# create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist



def add_wishlist(request,product_id):
    product = Product.objects.get(id= product_id)  
    try:    
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))

    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(wishlist_id = _wishlist_id(request))
    wishlist.save()

    is_wishlist_item_exists = WishlistItem.objects.filter(product = product, wishlist = wishlist).exists()
    if is_wishlist_item_exists:
        wishlist_item = WishlistItem.objects.filter(product=product,wishlist=wishlist)
        pass
    else:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist = wishlist,
        )
       
    return redirect ('wishlist')

def remove_wishlist_item(request,product_id,wishlist_item_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product,id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist,id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')


def wishlist(request,wishlist_items=None):
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active = True)

    except ObjectDoesNotExist:
        pass        
    context = {
        'wishlist_items':wishlist_items,
    }
    return render (request,('store/wishlist.html'),context)
