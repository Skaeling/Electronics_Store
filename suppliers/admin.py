from django.contrib import admin
from .models import NetworkNode, Contact, Product

from django.utils.html import format_html


def clear_arrears(modeladmin, request, queryset):
    queryset.update(arrears=0.00)
    modeladmin.message_user(request, 'Задолженность выбранных объектов сети погашена')


clear_arrears.short_description = 'Обнулить задолженность перед поставщиками выбранных объектов сети'


class ContactInline(admin.StackedInline):
    model = Contact


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    exclude = ['created_at']
    list_display = ("__str__", 'supplier_link', 'arrears')
    list_filter = ['contacts__city']
    inlines = [ContactInline]
    actions = [clear_arrears]

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="/admin/suppliers/networknode/{}/change/">{}</a>', obj.supplier.id,
                               obj.supplier.title)
        return "Нет поставщика"

    supplier_link.short_description = 'Поставщик'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'model', 'distributors', 'release_date']
