from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import NetworkNode, Contact, Product
from .validators import SupplierLevelValidator, validate_debt


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ContactViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['id', 'network_node']


class ProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["distributors"]


class NetworkNodeSerializer(serializers.ModelSerializer):
    purchase_level = serializers.ChoiceField(choices=NetworkNode.LEVELS_CHOICES, validators=[
        UniqueValidator(queryset=NetworkNode.objects.filter(purchase_level=0),
                        message="Не может быть более одного поставщика с purchase_level=0")])
    contacts = ContactViewSerializer(required=False)
    supplier = serializers.PrimaryKeyRelatedField(queryset=NetworkNode.objects.all(), required=False, allow_null=True)
    products = ProductViewSerializer(many=True, read_only=True)
    debt = serializers.DecimalField(max_digits=15, decimal_places=2, allow_null=True, default=0.00)

    def validate(self, attrs):
        data = {}
        if self.instance:
            data.update({
                'purchase_level': self.instance.purchase_level,
                'supplier': self.instance.supplier,
            })
        data.update(attrs)

        SupplierLevelValidator()(data)
        validate_debt(data)
        return super().validate(attrs)

    def create(self, validated_data):
        """Позволяет одновременно с созданием объекта сети создать и его контакты"""
        contacts_data = validated_data.pop('contacts', None)
        network_node = NetworkNode.objects.create(**validated_data)
        if contacts_data:
            Contact.objects.create(network_node=network_node, **contacts_data)
        return network_node

    def update(self, instance, validated_data):
        """Запрещает обновление поля debt и позволяет одновременное обновление или добавление контактов"""
        if 'debt' in validated_data:
            raise ValidationError({"debt": "Обновление поля 'debt' запрещено."})

        for attr, value in validated_data.items():
            if attr != 'contacts':
                setattr(instance, attr, value)
        instance.save()

        contacts_data = validated_data.get('contacts')
        if contacts_data:
            contact_instance, created = Contact.objects.update_or_create(
                network_node=instance,
                defaults=contacts_data
            )
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.supplier:
            representation['supplier'] = instance.supplier.title
        else:
            representation['supplier'] = "Нет"
        return representation

    class Meta:
        model = NetworkNode
        fields = ["id", "title", "purchase_level", "debt", "supplier", "contacts", "products", "created_at"]
