from django.db import models
# models.py
from django.db import models
from django.contrib.auth.models import User

class PeerSupporter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)
    trained_at = models.DateTimeField(auto_now_add=True)

class SupportRequest(models.Model):
    REASON_CHOICES = [
        ('academic', 'Academic Stress'),
        ('lonely', 'Loneliness'),
        ('overwhelmed', 'Overwhelmed'),
        ('other', 'Other'),
    ]
    phone_hash = models.CharField(max_length=64)  # hashed phone for anonymity
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    matched_peer = models.ForeignKey(PeerSupporter, null=True, blank=True, on_delete=models.SET_NULL)
    is_completed = models.BooleanField(default=False)

class ChatSession(models.Model):
    request = models.OneToOneField(SupportRequest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    student_feedback = models.CharField(max_length=10, null=True, blank=True)  # "helpful" / "not_helpful"

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # "student" or "peer"
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Auto-delete after 24h via management command or task
# Create your models here.
