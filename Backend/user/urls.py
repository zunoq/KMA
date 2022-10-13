from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from user.views import (
    UserView,
    UserByIdView,
    SelfInfoView,
    ChangePasswordView,
    SendOTPView,
    ResetPasswordView,
    StaffRequestView,
    StaffRequestByIdView,
    StaffCreateRequestView,
    StaffDeleteRequest,
    StaffUpdateRequestView,
)


urlpatterns = [
    path("token/auth", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    path("users", UserView.as_view()),
    path("users/<uuid:user_id>", UserByIdView.as_view()),
    path("self/info", SelfInfoView.as_view()),
    path("self/password", ChangePasswordView.as_view()),
    path("otp/reset", SendOTPView.as_view()),
    path("password/reset", ResetPasswordView.as_view()),
    path("staff/requests", StaffRequestView.as_view()),
    path("staff/requests/<uuid:request_id>", StaffRequestByIdView.as_view()),
    path('staff/requests/create', StaffCreateRequestView.as_view()),
    path('staff/requests/delete/<uuid:customer_id>', StaffDeleteRequest.as_view()),
    path('staff/requests/update/<uuid:customer_id>', StaffUpdateRequestView.as_view()),
]
