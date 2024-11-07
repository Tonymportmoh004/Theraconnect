from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import UserForm, ProfileForm, ClientProfileForm, TherapistProfileForm, GoalForm, ResourceForm, MessageForm, PrivacySettingForm, FeedbackForm, AppointmentForm
from .tokens import account_activation_token
from datetime import datetime
from django.utils import timezone
from .models import Appointment, Goal, Resource, Message, PrivacySetting, Feedback

def send_verification_email(user, request):
    mail_subject = 'Activate your account.'
    message = render_to_string('core/acc_active_email.html', {
        'user': user,
        'domain': request.META['HTTP_HOST'],
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    send_mail(mail_subject, message, 'happytheraconnect@gmail.com', [to_email])

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        client_form = ClientProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = 'client'  # Automatically set the role to 'client'
            profile.save()
            client_profile = client_form.save(commit=False)
            client_profile.profile = profile
            client_profile.save()
            send_verification_email(user, request)
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            print(user_form.errors)
            print(profile_form.errors)
            print(client_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        client_form = ClientProfileForm()
    return render(request, 'core/register.html', {'user_form': user_form, 'profile_form': profile_form, 'client_form': client_form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid!')

def register_role(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if 'therapist' in request.POST:
            therapist_form = TherapistProfileForm(request.POST, request.FILES)
            if therapist_form.is_valid():
                therapist_profile = therapist_form.save(commit=False)
                therapist_profile.profile = user.profile
                therapist_profile.save()
                login(request, user)
                return redirect('profile')  # Redirect after successful therapist registration
        elif 'client' in request.POST:
            client_form = ClientProfileForm(request.POST, request.FILES)
            if client_form.is_valid():
                client_profile = client_form.save(commit=False)
                client_profile.profile = user.profile
                client_profile.save()
                login(request, user)
                return redirect('profile')  # Redirect after successful client registration
    else:
        therapist_form = TherapistProfileForm()
        client_form = ClientProfileForm()

    return render(request, 'core/register_role.html', {
        'therapist_form': therapist_form,
        'client_form': client_form
    })

def register_therapist(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        therapist_form = TherapistProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid() and therapist_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = 'therapist'  # Automatically set the role to 'therapist'
            profile.save()
            therapist_profile = therapist_form.save(commit=False)
            therapist_profile.profile = profile
            therapist_profile.save()
            send_verification_email(user, request)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        therapist_form = TherapistProfileForm()
    return render(request, 'core/register_therapist.html', {'user_form': user_form, 'profile_form': profile_form, 'therapist_form': therapist_form})

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def client_dashboard(request):
    # Fetching upcoming and past appointments
    upcoming_appointments = Appointment.objects.filter(client=request.user, date__gte=timezone.now()).order_by('date')
    past_appointments = Appointment.objects.filter(client=request.user, date__lt=timezone.now()).order_by('-date')

    # Fetching the therapist associated with the client
    therapist = request.user.appointments.first().therapist if request.user.appointments.exists() else None

    # Fetching the goals associated with the client
    goals = Goal.objects.filter(client=request.user).order_by('-start_date')

    # Fetching all resources
    resources = Resource.objects.all()

    # Fetching sent and received messages
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')

    # Fetching or creating privacy settings for the client
    privacy_setting, created = PrivacySetting.objects.get_or_create(client=request.user)

    # Fetching feedback
    feedbacks = Feedback.objects.filter(client=request.user).order_by('-timestamp')

    # Handling form submissions
    if request.method == 'POST':
        if 'goal_form' in request.POST:
            goal_form = GoalForm(request.POST)
            if goal_form.is_valid():
                new_goal = goal_form.save(commit=False)
                new_goal.client = request.user
                new_goal.save()
                return redirect('client_dashboard')
        elif 'resource_form' in request.POST:
            resource_form = ResourceForm(request.POST, request.FILES)
            if resource_form.is_valid():
                resource_form.save()
                return redirect('client_dashboard')
        elif 'message_form' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.sender = request.user
                new_message.save()
                return redirect('client_dashboard')
        elif 'privacy_form' in request.POST:
            privacy_form = PrivacySettingForm(request.POST, instance=privacy_setting)
            if privacy_form.is_valid():
                privacy_form.save()
                return redirect('client_dashboard')
        elif 'feedback_form' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                new_feedback = feedback_form.save(commit=False)
                new_feedback.client = request.user
                new_feedback.save()
                return redirect('client_dashboard')
    else:
        goal_form = GoalForm()
        resource_form = ResourceForm()
        message_form = MessageForm()
        privacy_form = PrivacySettingForm(instance=privacy_setting)
        feedback_form = FeedbackForm()

    # Rendering the client dashboard template
    return render(request, 'core/client_dashboard.html', {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'therapist': therapist,
        'goals': goals,
        'resources': resources,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'privacy_setting': privacy_setting,
        'feedbacks': feedbacks,
        'goal_form': goal_form,
        'resource_form': resource_form,
        'message_form': message_form,
        'privacy_form': privacy_form,
        'feedback_form': feedback_form
    })

@login_required
def therapist_dashboard(request):
    # Fetching upcoming and past appointments
    upcoming_appointments = Appointment.objects.filter(therapist=request.user, date__gte=timezone.now()).order_by('date')
    past_appointments = Appointment.objects.filter(therapist=request.user, date__lt=timezone.now()).order_by('-date')

    # Fetching the therapist profile
    therapist_profile = request.user.therapistprofile

    # Fetching the goals of clients associated with the therapist
    client_goals = Goal.objects.filter(client__appointments__therapist=request.user).order_by('-start_date')

    # Fetching all resources
    resources = Resource.objects.all()

    # Fetching sent and received messages
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')

    # Fetching or creating privacy settings for the therapist
    privacy_setting, created = PrivacySetting.objects.get_or_create(client=request.user)

    # Fetching feedback from clients
    feedbacks = Feedback.objects.filter(client__appointments__therapist=request.user).order_by('-timestamp')

    # Handling form submissions
    if request.method == 'POST':
        if 'resource_form' in request.POST:
            resource_form = ResourceForm(request.POST, request.FILES)
            if resource_form.is_valid():
                resource_form.save()
                return redirect('therapist_dashboard')
        elif 'message_form' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.sender = request.user
                new_message.save()
                return redirect('therapist_dashboard')
        elif 'privacy_form' in request.POST:
            privacy_form = PrivacySettingForm(request.POST, instance=privacy_setting)
            if privacy_form.is_valid():
                privacy_form.save()
                return redirect('therapist_dashboard')
    else:
        resource_form = ResourceForm()
        message_form = MessageForm()
        privacy_form = PrivacySettingForm(instance=privacy_setting)

    # Rendering the therapist dashboard template
    return render(request, 'core/therapist_dashboard.html', {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'therapist_profile': therapist_profile,
        'client_goals': client_goals,
        'resources': resources,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'privacy_setting': privacy_setting,
        'feedbacks': feedbacks,
        'resource_form': resource_form,
        'message_form': message_form,
        'privacy_form': privacy_form
    })

@login_required
def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.save()
            return redirect('client_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'core/schedule_appointment.html', {'form': form})

@login_required
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, therapist=request.user)
    if request.method == 'POST':
        appointment.confirmed = True
        appointment.save()
        return redirect('therapist_dashboard')

    return render(request, 'core/confirm_appointment.html', {'appointment': appointment})
