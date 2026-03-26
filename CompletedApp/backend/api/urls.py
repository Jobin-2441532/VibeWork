from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    JobListView,
    ApplicationListView,
    ApplicationDetailView,
    DashboardStatsView,
    ProfileDetailView,
    ReviewListCreateView,
    NotificationListView,
    NotificationUpdateView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Advanced Features
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/me/', ProfileDetailView.as_view(), name='profile-me'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationUpdateView.as_view(), name='notification-update'),
]
