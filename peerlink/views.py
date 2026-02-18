from django.shortcuts import render
# peerlink/views.py
import hashlib
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import SupportRequest

def home(request):
    """Landing page: 'Need to talk?'"""
    return render(request, 'peerlink/home.html')

def request_support(request):
    """Step 1: Student enters phone and selects reason"""
    if request.method == 'POST':
        phone = request.POST.get('phone')
        reason = request.POST.get('reason')
        
        # Simple anonymization: hash phone (never store raw number)
        salt = os.environ.get('PHONE_SALT', 'peerlink-demo-salt')
        phone_hash = hashlib.sha256((phone + salt).encode()).hexdigest()
        
        # Create support request
        support_request = SupportRequest.objects.create(
            phone_hash=phone_hash[:32],  # SQLite has 64-char limit? Keep it safe.
            reason=reason
        )
        return redirect('peerlink:wait_for_match', request_id=support_request.id)
    
    return render(request, 'peerlink/request_form.html')

def wait_for_match(request, request_id):
    """Step 2: Wait screen (in real app: poll for match)"""
    support_request = get_object_or_404(SupportRequest, id=request_id)
   # For MVP demo: skip waiting, go straight to options
    return redirect('peerlink:support_options', request_id=request_id)
# peerlink/views.py (add at the bottom)
def support_options(request, request_id):
    """Show support options (only text enabled for MVP)"""
    support_request = get_object_or_404(SupportRequest, id=request_id)
    # peerlink/views.py
def support_options(request, request_id):
    support_request = get_object_or_404(SupportRequest, id=request_id)
    
    # Define resources by reason
    resources = {
        'academic': {
            'title': 'You’re Not Alone in This',
            'tips': [
                "Break big tasks into 25-minute chunks (Pomodoro technique).",
                "It’s okay to ask your lecturer for an extension—most will say yes.",
                "Your worth isn’t your grades. You’re learning, not failing."
            ],
            'exercise': "Try this: Close your eyes. Breathe in for 4 sec, hold for 4, out for 6. Repeat 3x."
        },
        'lonely': {
            'title': 'Connection Starts With You',
            'tips': [
                "Send a voice note to someone you miss—even if it’s been weeks.",
                "Join one campus club this week. Just show up once.",
                "Loneliness lies. It tells you no one cares—but people do."
            ],
            'exercise': "Write down 3 people you could reach out to today. Pick one."
        },
        'overwhelmed': {
            'title': 'Pause. Breathe. Prioritize.',
            'tips': [
                "Write everything down—then circle the ONE thing that must happen today.",
                "Say this: ‘I don’t have to solve everything right now.’",
                "Step outside for 2 minutes. Feel the sun or wind on your skin."
            ],
            'exercise': "Ground yourself: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste."
        },
        'other': {
            'title': 'Take a Gentle Breath',
            'tips': [
                "It’s okay not to have words for what you’re feeling.",
                "Be as kind to yourself as you would be to a friend.",
                "This moment will pass—even if it doesn’t feel like it now."
            ],
            'exercise': "Place a hand on your heart. Feel its warmth. You’re still here. That’s courage."
        }
    }

    context = {
        'request': support_request,
        'resource': resources.get(support_request.reason, resources['other'])
    }
    return render(request, 'peerlink/support_options.html', context)
# peerlink/views.py
def chat_session(request, request_id):
    support_request = get_object_or_404(SupportRequest, id=request_id)
    
    # Map reason to friendly intro
    peer_greetings = {
        'academic': "Hi there! I'm a trained MKU peer. I saw you mentioned academic stress — how are your studies going?",
        'lonely': "Hi there! I'm a trained MKU peer. I noticed you're feeling lonely — would you like to talk about what’s on your mind?",
        'overwhelmed': "Hi there! I'm a trained MKU peer. You mentioned feeling overwhelmed — what’s weighing on you right now?",
        'other': "Hi there! I'm a trained MKU peer. How are you feeling today?"
    }
    
    context = {
        'request': support_request,
        'peer_greeting': peer_greetings.get(support_request.reason, peer_greetings['other'])
    }
    return render(request, 'peerlink/chat.html', context)