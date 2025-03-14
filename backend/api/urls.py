from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('signup-otp/', SignupOTPView.as_view(), name='signup-otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('approve-signup/', ApproveSignupView.as_view(), name='approve-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('form/', FormView.as_view(), name='form'),
    path('form/<int:pk>/', FormView.as_view(), name='form-detail'),
    path('app_no/', Sno.as_view(), name='app-no'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)