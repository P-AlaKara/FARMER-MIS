from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmerProfile

User = get_user_model()


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ('location', 'city', 'crop', 'farm_size_acres', 'phone')


class FarmerSerializer(serializers.ModelSerializer):
    farmer_profile = FarmerProfileSerializer(required=False)
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name',
                  'date_joined', 'farmer_profile', 'password')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        profile_data = validated_data.pop('farmer_profile', {})
        password = validated_data.pop('password', None)
        validated_data['role'] = 'farmer'
        user = User.objects.create_user(password=password, **validated_data)
        FarmerProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('farmer_profile', {})
        password = validated_data.pop('password', None)

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
    farmers = FarmerSerializer(many=True)