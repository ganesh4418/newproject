from django.urls import path, include
from .views import CustomTokenObtainPairView, LogoutView, UserSignupViewSet
from rest_framework.routers import DefaultRouter
from .views import (RequestDemoViewSet, ContactUsViewSet, HelpandSupportViewSet,
                    UserProfileList, UserProfileDetail)
from . import views


router = DefaultRouter()
router.register(r'request-demo', RequestDemoViewSet)
router.register(r'contact-us', ContactUsViewSet)
router.register(r'helpandsupport', HelpandSupportViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserSignupViewSet.as_view(), name='signup'),
    path('user-profile/', views.UserProfileList.as_view(), name='profile-list'),
    path('Update-profile-photo/<int:pk>/', views.UserProfileDetail.as_view(), name='profile-detail'),
    path('', include(router.urls)),
]
