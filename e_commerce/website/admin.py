from django.contrib import admin
from website.models import Product,AuthUser
from website.models import Review
# Register your models here.
admin.site.register(Product)
admin.site.register(AuthUser)
admin.site.register(Review)