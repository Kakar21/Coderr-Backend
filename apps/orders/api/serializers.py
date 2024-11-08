from rest_framework import serializers
from ..models import Order
from apps.offers.models import Offerdetail


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset=Offerdetail.objects.all(), write_only=True
    )
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    revisions = serializers.SerializerMethodField(read_only=True)
    delivery_time_in_days = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    features = serializers.SerializerMethodField(read_only=True)
    offer_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'offer_detail_id', 'business_user', 'title', 'revisions', 
            'delivery_time_in_days', 'price', 'features', 'offer_type', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 
                            'delivery_time_in_days', 'price', 'features', 'offer_type', 
                            'status', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        return obj.business_user.id

    def get_title(self, obj):
        return obj.title

    def get_revisions(self, obj):
        return obj.revisions

    def get_delivery_time_in_days(self, obj):
        return obj.delivery_time_in_days

    def get_price(self, obj):
        return obj.price

    def get_features(self, obj):
        return obj.features

    def get_offer_type(self, obj):
        return obj.offer_type

    def create(self, validated_data):
        offer_detail = validated_data.pop('offer_detail_id')
        validated_data['offer_detail'] = offer_detail

        validated_data['customer_user'] = self.context['request'].user
        return super().create(validated_data)
