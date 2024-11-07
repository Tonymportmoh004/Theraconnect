from django import forms
from django.contrib.auth.models import User
from .models import Profile, TherapistProfile, ClientProfile, Goal, Resource, Message, PrivacySetting, Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class TherapistProfileForm(forms.ModelForm):
    class Meta:
        model = TherapistProfile
        fields = ['license_number', 'certifications', 'specializations', 'years_of_experience', 'certificate_pdf', 'id_pdf']

    def __init__(self, *args, **kwargs):
        super(TherapistProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['age', 'gender', 'medical_history', 'therapy_goals', 'preferred_therapist_gender', 'specific_issues', 'id_pdf']

    def __init__(self, *args, **kwargs):
        super(ClientProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'start_date', 'end_date', 'progress']

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Set Goal'))

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'link', 'file']

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Resource'))

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Message'))

class PrivacySettingForm(forms.ModelForm):
    class Meta:
        model = PrivacySetting
        fields = ['share_appointments', 'share_goals', 'share_resources']

    def __init__(self, *args, **kwargs):
        super(PrivacySettingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Settings'))

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_text', 'rating']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit Feedback'))

class AppointmentForm(forms.ModelForm): class Meta: model = Appointment fields = ['therapist', 'date', 'notes'] def __init__(self, *args, **kwargs): super(AppointmentForm, self).__init__(*args, **kwargs) self.helper = FormHelper() self.helper.form_method = 'post' self.helper.add_input(Submit('submit', 'Schedule Appointment'))
