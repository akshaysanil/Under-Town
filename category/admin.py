from django.contrib import admin
from .models import MainCategory,Category,SubCategory

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('main_category_name',)}
    list_display        = ('main_category_name','slug',)
admin.site.register(MainCategory,CategoryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name',)}
    list_display        = ('category_name','slug','main_category',)
admin.site.register(Category,CategoryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('sub_category_name',)}
    list_display        = ('sub_category_name','slug','category',)

admin.site.register(SubCategory,CategoryAdmin)




