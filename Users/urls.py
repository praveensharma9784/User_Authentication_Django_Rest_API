from django.urls import path
from Users.views import UserRegistrationView,UserLoginView,UserChangePasswordView
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'register'),
    path('login/', UserLoginView.as_view(), name= 'login'),
    path('profile/', UserLoginView.as_view(), name= 'profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name= 'changepassword'),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]