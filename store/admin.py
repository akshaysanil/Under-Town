from django.contrib import admin
from .models import BestSellers, Product, ProductGallery, ReviewRating,Variation,Carousel


# Register your models here.

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra: 1



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug' : ('product_name',)}
    list_display        = ('product_name','brand','price','stock','main_category','sub_category','modified_date','is_available')
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display  = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter   = ('product','variation_category','variation_value') 


class BestSelersAdmin(admin.ModelAdmin):
    list_display  = ('product','is_best')
    list_editable = ('is_best',)





admin.site.register(Variation,VariationAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Carousel)
admin.site.register(BestSellers,BestSelersAdmin)

admin.site.register(ReviewRating)
admin.site.register(ProductGallery)

