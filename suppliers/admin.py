from django.contrib import admin
from .models import NetworkNode, Contact


def clear_arrears(modeladmin, request, queryset):
    queryset.update(arrears=0.00)
    modeladmin.message_user(request, 'Задолженность выбранных объектов сети погашена')


clear_arrears.short_description = 'Обнулить задолженность перед поставщиками выбранных объектов сети'


class ContactInline(admin.StackedInline):
    model = Contact


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    exclude = ['created_at']
    list_display = ("__str__", 'supplier', 'arrears')
    list_filter = ['contacts__city']
    inlines = [ContactInline]
    actions = [clear_arrears]
