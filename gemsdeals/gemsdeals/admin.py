from django.contrib import admin
from .models import Customer, Gem, Deal, Menu

# Register your models here.
admin.site.register(Customer)
admin.site.register(Gem)
admin.site.register(Deal)
admin.site.register(Menu)