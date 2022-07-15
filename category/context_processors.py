from .models import MainCategory,Category,SubCategory

def menu_links(request):
    links = MainCategory.objects.all()
    return dict(links = links)

def cat_menu_links(request):
    cat_links = Category.objects.all()
    return dict(cat_links = cat_links)

def sub_cat_menu_links(request):
    sub_cat_links = SubCategory.objects.all()
    return dict(sub_cat_links=sub_cat_links)


   