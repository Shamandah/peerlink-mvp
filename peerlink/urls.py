# peerlink/urls.py
from django.urls import path
from . import views

app_name = 'peerlink'

urlpatterns = [
    path('', views.home, name='home'),
    path('request/', views.request_support, name='request_support'),
    path('wait/<int:request_id>/', views.wait_for_match, name='wait_for_match'),
    path('support/<int:request_id>/', views.support_options, name='support_options'), 
    path('chat/<int:request_id>/', views.chat_session, name='chat_session'),
    
    # NEW: API endpoint for OpenAI chat bot
    path('api/ask/', views.ask_bot, name='ask_bot'),
]