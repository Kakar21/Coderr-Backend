"""
URL configuration for coderr_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users.api import views as users_views
from django.conf.urls.static import static
from apps.offers.api import views as offers_views
from apps.orders.api import views as orders_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/base-info/', include('apps.info.api.urls')),
    path('api/offers/', include('apps.offers.api.urls')),
    path('api/offerdetails/<int:pk>/', offers_views.OfferdetailsDetailView.as_view(), name='offerdetail-detail'),
    path('api/orders/', include('apps.orders.api.urls')),
    path('api/order-count/<int:business_user_id>/', orders_views.OrderCountView.as_view(), name='order-count'),
    path('api/completed-order-count/<int:business_user_id>/', orders_views.CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('api/profile/', include('apps.users.api.urls')),
    path('api/profiles/', include('apps.users.api.urls')),
    path('api/registration/', users_views.RegistrationView.as_view(), name='registration'),
    path('api/login/', users_views.LoginView.as_view(), name='login'),
    path('api/reviews/', users_views.ReviewList.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', users_views.ReviewDetail.as_view(), name='review-detail'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
