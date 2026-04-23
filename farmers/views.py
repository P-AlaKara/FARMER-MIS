from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import FarmerProfile
from .serializers import FarmerSerializer, AdminDashboardSerializer
from .permissions import IsAdmin, IsFarmer
from .weather import get_weather, get_farming_insight

# Create your views here.
User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        farmers = User.objects.filter(role='farmer').select_related('farmer_profile')
        data = {
            'total_farmers': farmers.count(),
            'farmers': FarmerSerializer(farmers, many=True).data,
        }
        return Response(data)


class FarmerDashboardView(APIView):
    permission_classes = [IsFarmer]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'farmer_profile', None)
        city = profile.city if profile else ''
        crop = profile.crop if profile else ''

        weather = get_weather(city)
        insight = get_farming_insight(weather, crop)

        return Response({
            'welcome': f'Welcome, {user.get_full_name()}!',
            'weather': weather,
            'insight': insight,
        })


class FarmerListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = FarmerSerializer
    queryset = User.objects.filter(role='farmer').select_related('farmer_profile')


class FarmerDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    serializer_class = FarmerSerializer
    queryset = User.objects.filter(role='farmer').select_related('farmer_profile')