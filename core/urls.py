from django.urls import path
from .views import home, register, register_role, activate, dashboard, register_therapist, client_dashboard, therapist_dashboard, schedule_appointment, confirm_appointment

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('register/therapist/', register_therapist, name='register_therapist'),
    path('register/role/<int:user_id>/', register_role, name='register_role'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('client_dashboard/', client_dashboard, name='client_dashboard'),
    path('therapist_dashboard/', therapist_dashboard, name='therapist_dashboard'),
    path('schedule_appointment/', schedule_appointment, name='schedule_appointment'),
    path('confirm_appointment/<int:appointment_id>/', confirm_appointment, name='confirm_appointment'),
]
