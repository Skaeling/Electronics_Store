from rest_framework import serializers
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
    contacts = ContactViewSerializer(read_only=True)
    products = ProductViewSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = ["id", "title", "purchase_level", "arrears", "supplier", "contacts", "products", "created_at"]


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        exclude = ['arrears']
