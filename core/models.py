from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

class Profile(TimeStampedModel):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('therapist', 'Therapist'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return self.user.username

class TherapistProfile(TimeStampedModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    certifications = models.TextField()
    specializations = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    certificate_pdf = models.FileField(upload_to='certificates/', blank=True, null=True)
    id_pdf = models.FileField(upload_to='ids/', blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} - Therapist"

class ClientProfile(TimeStampedModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    medical_history = models.TextField()
    therapy_goals = models.TextField()
    preferred_therapist_gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('No Preference', 'No Preference')])
    specific_issues = models.TextField()
    id_pdf = models.FileField(upload_to='client_ids/', blank=True, null=True)

    def __str__(self):
        return f"{self.profile.user.username} - Client"

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    therapist = models.ForeignKey(User, related_name='therapist', on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    confirmed = models.BooleanField(default=False)  # New field to indicate if the appointment is confirmed

    def __str__(self):
        return f"{self.client.username} - {self.date}"

class Goal(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    progress = models.IntegerField(default=0)  # Percentage completion

    def __str__(self):
        return f"{self.title} - {self.client.username}"

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='resources/', blank=True, null=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.subject}"

class PrivacySetting(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name='privacy_setting')
    share_appointments = models.BooleanField(default=True)
    share_goals = models.BooleanField(default=True)
    share_resources = models.BooleanField(default=True)

    def __str__(self):
        return f"Privacy settings for {self.client.username}"
