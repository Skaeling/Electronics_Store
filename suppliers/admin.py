from django.contrib import admin
from .models import NetworkNode, Contact, Product

from django.utils.html import format_html


def clear_debt(modeladmin, request, queryset):
    """Обнуляет значение поля debt выбранных объектов сети"""
    queryset.update(debt=0.00)
    modeladmin.message_user(request, 'Задолженность выбранных объектов сети погашена')


clear_debt.short_description = 'Обнулить задолженность перед поставщиками'


class ContactInline(admin.StackedInline):
    model = Contact


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    readonly_fields = ('supplier_link',)

    exclude = ['created_at']
    list_display = ("__str__", 'purchase_level', 'supplier_link', 'debt')
    list_filter = ['contacts__country', 'contacts__city']
    inlines = [ContactInline]
    actions = [clear_debt]

    def supplier_link(self, obj):
        """Формирует ссылку на страницу поставщика в одноименном поле, если его нет возвращает текстовую строку"""
        if obj.supplier:
            return format_html('<a href="/admin/suppliers/networknode/{}/change/">{}</a>', obj.supplier.id,
                               obj.supplier.title)
        return "Нет"

    supplier_link.short_description = 'Поставщик'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Исключает возможность выбора объектов сети 2-го уровня в качестве поставщиков оборудования
        при создании или обновлении объекта"""
        if db_field.name == "supplier":
            if 'admin' in request.path and 'change' in request.path:
                object_id = request.resolver_match.kwargs.get('object_id')
                if object_id:
                    kwargs["queryset"] = NetworkNode.objects.exclude(id=object_id).exclude(purchase_level=2)
            else:
                kwargs["queryset"] = NetworkNode.objects.exclude(purchase_level=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'model', 'distributors', 'release_date']
