from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import NetworkNode, Contact, Product


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
    supplier = serializers.StringRelatedField()
    contacts = ContactViewSerializer(required=False)
    products = ProductViewSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = ["id", "title", "purchase_level", "debt", "supplier", "contacts", "products", "created_at"]

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', None)
        network_node = NetworkNode.objects.create(**validated_data)
        if contacts_data:
            Contact.objects.create(network_node=network_node, **contacts_data)
        return network_node

    def update(self, instance, validated_data):
        if 'debt' in validated_data:
            raise ValidationError({"debt": "Обновление поля 'debt' запрещено."})
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        contacts_data = validated_data.get('contacts')

        if contacts_data:
            contact_instance, created = Contact.objects.update_or_create(
                network_node=instance,
                defaults=contacts_data
            )

        return instance
