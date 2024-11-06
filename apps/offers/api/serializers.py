from rest_framework import serializers 
from apps.offers.models import Offer, OfferDetail
from apps.users.api.serializers import ProfileSerializer
from django.urls import reverse

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]

    def validate_features(self, value):
        if not value or len(value) < 1:
            raise serializers.ValidationError("At least one feature is required.")
        return value


class OfferSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    user_details = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 
            'updated_at', 'details', 'min_price', 'min_delivery_time', 
            'user_details'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        user_details = representation.get('user_details')
        if user_details:
            filtered_user_details = {
                'first_name': user_details.get('first_name'),
                'last_name': user_details.get('last_name'),
                'username': user_details.get('username'),
            }
            representation['user_details'] = filtered_user_details
        
        return representation
    

    def get_details(self, obj):
        request = self.context.get('request')
        return [
            {
                "id": detail.id,
                "url": reverse('offerdetail-detail', kwargs={'pk': detail.id})
            }
            for detail in obj.details.all()
        ]

    def validate(self, data):
        details = self.initial_data.get('details')
        
        if len(details) != 3:
            raise serializers.ValidationError("Exactly three offer details are required.")
        
        offer_types = {'basic', 'standard', 'premium'}
        provided_types = {detail['offer_type'] for detail in details}
        
        if provided_types != offer_types:
            raise serializers.ValidationError(
                "Each offer must contain exactly one 'basic', 'standard', and 'premium' detail."
            )
        
        return data
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
