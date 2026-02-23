from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import os
import json

from .models import SupportRequest
from .openai_bot import generate_ai_reply

# ---------------------------------------
# Core Logic Views
# ---------------------------------------

def home(request):
    return render(request, 'peerlink/home.html')

def request_support(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        reason = request.POST.get('reason')
        
        salt = os.environ.get('PHONE_SALT', 'peerlink-demo-salt')
        phone_hash = hashlib.sha256((phone + salt).encode()).hexdigest()
        
        support_request = SupportRequest.objects.create(
            phone_hash=phone_hash[:32],
            reason=reason
        )
        return redirect('peerlink:wait_for_match', request_id=support_request.id)
    
    return render(request, 'peerlink/request_form.html')

def wait_for_match(request, request_id):
    return redirect('peerlink:support_options', request_id=request_id)

def support_options(request, request_id):
    support_request = get_object_or_404(SupportRequest, id=request_id)
    
    resources = {
        'academic': {
            'title': 'Taking it one step at a time',
            'tips': [
                "Your worth isn't defined by your grades. You are doing your best.",
                "Try breaking tasks into tiny, manageable pieces.",
                "It's okay to step away and breathe when things feel heavy."
            ],
            'exercise': "Let's try a grounding breath: Inhale for 4, hold for 4, exhale for 6."
        },
        'lonely': {
            'title': 'A space for connection',
            'tips': [
                "It's brave to admit you're feeling lonely. Many peers feel the same.",
                "Small steps count—even a simple 'hello' to someone today.",
                "You belong here, and your presence matters."
            ],
            'exercise': "Think of one place on campus where you feel even a little bit peaceful."
        }
    }

    context = {
        'request': support_request,
        'resource': resources.get(support_request.reason, resources.get('lonely')) # Fallback to lonely
    }
    return render(request, 'peerlink/support_options.html', context)

def chat_session(request, request_id):
    support_request = get_object_or_404(SupportRequest, id=request_id)
    
    peer_greetings = {
        'academic': "Hi there. I'm a peer here at MKU. I heard things have been stressful with your studies... I'm here to listen.",
        'lonely': "Hi. I'm glad you reached out. It can feel really quiet sometimes, but you're not alone right now. How are you doing?",
        'overwhelmed': "Hey. I'm a peer mentor. It sounds like things are moving really fast lately... do you want to talk about what's on your mind?",
        'other': "Hi there. I'm an MKU peer. I'm just here to sit with you and listen. How are you feeling today?"
    }
    
    context = {
        'request': support_request,
        'peer_greeting': peer_greetings.get(support_request.reason, peer_greetings['other'])
    }
    return render(request, 'peerlink/chat.html', context)

# ---------------------------------------
# API for Soft Dialogue Response
# ---------------------------------------

@csrf_exempt
def ask_bot(request):
    """Bridge between the UI and the AI soft-persona brain."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "").strip()

            if not question:
                return JsonResponse({"error": "Empty message"}, status=400)

            # Generate the reply using your Gemini/OpenAI bot code
            answer = generate_ai_reply(question)

            return JsonResponse({"answer": answer})

        except Exception as e:
            # Check your terminal/command prompt to see this error print!
            print(f"\x1b[31m[DEBUG ERROR]\x1b[0m: {str(e)}") 
            return JsonResponse({
                "answer": "I'm so sorry, I'm having a little trouble connecting right now. Let's try again in a moment."
            })

    return JsonResponse({"error": "Invalid request method"}, status=405)