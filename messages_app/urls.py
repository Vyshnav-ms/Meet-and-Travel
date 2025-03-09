from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation-detail'),
    path('send/<str:username>/', views.send_message, name='send-message'),
]

