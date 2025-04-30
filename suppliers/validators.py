from rest_framework import serializers


class SupplierLevelValidator:
    """Проверяет соблюдение правил иерархии сети при создании или обновлении объекта,
    в случае нарушения выбрасывает ошибку."""
    def __call__(self, attrs):
        purchase_level = attrs.get('purchase_level')
        supplier = attrs.get('supplier')

        if supplier is not None:
            expected_supplier_level = purchase_level - 1 if purchase_level > 0 else None

            if expected_supplier_level is not None and supplier.purchase_level != expected_supplier_level:
                raise serializers.ValidationError(
                    f"Для уровня {purchase_level} необходимо выбрать поставщика с уровнем "
                    f"{expected_supplier_level}. Либо изменить ваш текущий уровень.")

            elif purchase_level == 0:
                raise serializers.ValidationError("У производителя не может быть поставщика")


def validate_debt(attrs):
    purchase_level = attrs.get('purchase_level')
    debt = attrs.get('debt', 0.00)
    if purchase_level == 0 and debt > 0.00:
        raise serializers.ValidationError("У производителя не может быть долга по закупке")
