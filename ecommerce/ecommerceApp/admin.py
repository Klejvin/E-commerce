from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductVariant)
admin.site.register(Order)
