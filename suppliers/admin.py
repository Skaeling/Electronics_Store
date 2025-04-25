from django.contrib import admin
from .models import NetworkNode, Contact, Product


class ContactInline(admin.StackedInline):
    model = Contact


# class ProductInline(admin.TabularInline):
#     model = Product
#     extra = 1


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    exclude = ['created_at']
    list_display = ("__str__", 'supplier')
    list_filter = ['contacts__city']
    inlines = [ContactInline,
               # ProductInline
               ]
