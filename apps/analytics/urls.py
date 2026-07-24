from django.urls import path
from apps.analytics.views import DashboardOverviewView, RevenueAnalyticsView

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='analytics_overview'),
    path('revenue/', RevenueAnalyticsView.as_view(), name='analytics_revenue'),
]
