from rest_framework import serializers 
from apps.offers.models import Offer, Offerdetail
from apps.users.api.serializers import ProfileSerializer
from django.urls import reverse

class OfferdetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for offer details.

    Handles serialization and validation of the Offerdetail model.
    Ensures data conforms to expected structure and constraints.
    """
    class Meta:
        model = Offerdetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]

    def validate_revisions(self, value):
        """
        Ensure revisions are not less than -1.
        """
        if value < -1:
            raise serializers.ValidationError("Revisions cannot be less than 0.")
        return value
    
    def validate_features(self, value):
        """
        Ensure at least one feature is provided.
        """
        if not value or len(value) < 1:
            raise serializers.ValidationError("At least one feature is required.")
        return value


class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer for offers.

    Manages serialization and validation of the Offer model.
    Includes nested serialization for offer details and user profile.
    """
    details = OfferdetailsSerializer(many=True, required=True, write_only=True)
    user_details = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 
            'updated_at', 'details', 'min_price', 'min_delivery_time', 
            'user_details'
        ]
        read_only_fields = [
            'user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time'
        ]

    def to_representation(self, instance):
        """
        Customize representation of the Offer instance.
        Includes URLs for details.
        """
        representation = super().to_representation(instance)
        
        details_representation = [
            {
                "id": detail.id,
                "url": reverse('offerdetail-detail', kwargs={'pk': detail.id})
            }
            for detail in instance.details.all()
        ]

        user_details = representation.get('user_details')
        if user_details:
            filtered_user_details = {
                'first_name': user_details.get('first_name'),
                'last_name': user_details.get('last_name'),
                'username': user_details.get('username'),
            }

        representation['details'] = details_representation
        representation['user_details'] = filtered_user_details

        return representation

    def validate(self, data):
        """
        Validate Offer data.
        Ensure exactly three offer details are provided.
        """
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
        """
        Create a new Offer instance.
        Includes related Offerdetail instances.
        """
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        
        for detail_data in details_data:
            Offerdetail.objects.create(offer=offer, **detail_data)

        offer.update_min_values()
        
        return offer


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed offers.

    Provides a detailed view of the Offer model.
    Includes nested serialization for offer details and user profile.
    """
    details = OfferdetailsSerializer(many=True, required=False)
    user_details = ProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 
            'updated_at', 'details', 'min_price', 'min_delivery_time', 
            'user_details'
        ]
        read_only_fields = [
            'user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time'
        ]

    def to_representation(self, instance):
        """
        Customize representation of the Offer instance.
        Focus on user details.
        """
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
    
    def update(self, instance, validated_data):
        """
        Update an existing Offer instance.
        Includes related Offerdetail instances.
        """
        details_data = validated_data.pop('details', None)
        instance = super().update(instance, validated_data)
        
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                if offer_type:
                    detail_instance = instance.details.filter(offer_type=offer_type).first()
                    
                    if detail_instance:
                        for attr, value in detail_data.items():
                            setattr(detail_instance, attr, value)
                        detail_instance.save()
                    else:
                        Offerdetail.objects.create(offer=instance, **detail_data)
        
        instance.update_min_values()

        return instance