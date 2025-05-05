from django.contrib import admin
from django.utils.html import format_html
from rest_framework import exceptions

from .models import Contact, NetworkNode, Product
from .validators import SupplierLevelValidator, validate_debt


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
        """Исключает возможность выбора объектов сети 2-го уровня и текущего объекта в качестве
        поставщиков оборудования при создании или обновлении объекта"""
        if db_field.name == "supplier":
            if 'admin' in request.path and 'change' in request.path:
                object_id = request.resolver_match.kwargs.get('object_id')
                if object_id:
                    kwargs["queryset"] = NetworkNode.objects.exclude(id=object_id).exclude(purchase_level=2)
            else:
                kwargs["queryset"] = NetworkNode.objects.exclude(purchase_level=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """Исключает возможность создания второго объекта с purchase_level == 0"""
        admin_level_choices = [
            (1, 'Контрагент'),
            (2, 'Покупатель'),
        ]
        if db_field.name == 'purchase_level':
            is_admin_change = 'admin' in request.path and 'change' in request.path
            manufactory_exists = NetworkNode.objects.filter(purchase_level=0).exists()

            if is_admin_change:
                object_id = request.resolver_match.kwargs.get('object_id')
                if manufactory_exists:
                    manufactory = NetworkNode.objects.get(purchase_level=0)
                    if int(object_id) == manufactory.pk:
                        kwargs['choices'] = NetworkNode.LEVELS_CHOICES
                    else:
                        kwargs['choices'] = admin_level_choices
                else:
                    kwargs['choices'] = NetworkNode.LEVELS_CHOICES
            else:
                kwargs['choices'] = admin_level_choices if manufactory_exists else NetworkNode.LEVELS_CHOICES

        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Расширяет проверку данных с помощью кастомных валидаторов при сохранении формы"""
        attrs = {
            'purchase_level': form.cleaned_data.get('purchase_level'),
            'debt': form.cleaned_data.get('debt', 0.00),
            'supplier': form.cleaned_data.get('supplier'),
        }

        try:
            SupplierLevelValidator()(attrs)
            validate_debt(attrs)
        except exceptions.ValidationError as e:
            error_messages = []
            if isinstance(e.detail, list):
                for message in e.detail:
                    error_messages.append(str(message))
            else:
                error_messages.append(str(e.detail))
            error_message = ', '.join(error_messages)
            self.message_user(request, error_message, level='error')
            return

        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'model', 'distributors', 'release_date']
