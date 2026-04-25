from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import FarmerProfile

User = get_user_model()


class FarmerProfileSerializer(serializers.ModelSerializer):
    city           = serializers.CharField(max_length=100)
    crop           = serializers.CharField(max_length=100)
    phone          = serializers.CharField(max_length=20)
    location       = serializers.CharField(max_length=100, required=False, allow_blank=True)
    farm_size_acres = serializers.DecimalField(
        max_digits=8, decimal_places=2, required=False, allow_null=True
    )

    class Meta:
        model  = FarmerProfile
        fields = ('location', 'city', 'crop', 'farm_size_acres', 'phone')


class FarmerSerializer(serializers.ModelSerializer):
    farmer_profile = FarmerProfileSerializer(required=True)
    full_name      = serializers.SerializerMethodField()
    password       = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model  = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'date_joined', 'farmer_profile', 'password',
        )
        extra_kwargs = {
            'email':      {'required': True},
            'first_name': {'required': True},
            'last_name':  {'required': True},
        }

    def get_full_name(self, obj):
        return obj.get_full_name()

    def validate(self, attrs):
        # Password is required only on create (no instance yet)
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password is required.'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('farmer_profile')
        password     = validated_data.pop('password')
        validated_data['role'] = 'farmer'
        user = User.objects.create_user(password=password, **validated_data)
        FarmerProfile.objects.update_or_create(user=user, defaults=profile_data)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('farmer_profile', {})
        password     = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        profile, _ = FarmerProfile.objects.get_or_create(user=instance)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance


class AdminDashboardSerializer(serializers.Serializer):
    total_farmers = serializers.IntegerField()
    farmers       = FarmerSerializer(many=True)