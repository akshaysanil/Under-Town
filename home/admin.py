from django.contrib import admin

from home.models import Awesome

# Register your models here.
class AwesomeAdmin(admin.ModelAdmin):
    list_display  = ('product','is_awesome')
    list_editable = ('is_awesome',)


admin.site.register(Awesome,AwesomeAdmin)
