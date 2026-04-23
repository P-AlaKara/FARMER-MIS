from django.urls import path
from .views import (
    AdminDashboardView,
    FarmerDashboardView,
    FarmerListCreateView,
    FarmerDetailView,
)

urlpatterns = [
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/farmer/', FarmerDashboardView.as_view(), name='farmer-dashboard'),
    path('', FarmerListCreateView.as_view(), name='farmer-list-create'),
    path('<int:pk>/', FarmerDetailView.as_view(), name='farmer-detail'),
]