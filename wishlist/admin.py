from django.contrib import admin
from .models import Wishlist,WishlistItem

# Register your models here.

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id','date_added')

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('product','wishlist','is_active')


admin.site.register(Wishlist)
admin.site.register(WishlistItem)