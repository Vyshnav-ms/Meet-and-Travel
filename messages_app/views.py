from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Message, Conversation
from .forms import MessageForm

@login_required
def inbox(request):
    # Get all conversations for the current user
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Count unread messages
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()
    
    context = {
        'conversations': conversations,
        'unread_count': unread_count
    }
    return render(request, 'messages_app/inbox.html', context)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Get the other participant
    other_user = conversation.participants.exclude(id=request.user.id).first()
    
    # Get all messages in this conversation
    conversation_messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # Mark messages as read
    unread_messages = conversation_messages.filter(receiver=request.user, is_read=False)
    for msg in unread_messages:
        msg.is_read = True
        msg.save()
    
    # Handle new message form
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = other_user
            new_message.save()
            
            # Update conversation timestamp
            conversation.save()  # This will update the auto_now field
            
            messages.success(request, 'Message sent successfully!')
            return redirect('conversation-detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conversation,
        'other_user': other_user,
        'messages_list': conversation_messages,
        'form': form
    }
    return render(request, 'messages_app/conversation_detail.html', context)

@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)
    
    # Don't allow sending messages to yourself
    if receiver == request.user:
        messages.error(request, "You can't send messages to yourself.")
        return redirect('home')
    
    # Check if a conversation already exists
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=receiver).first()
    
    # If no conversation exists, create one
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, receiver)
    
    # Handle the message form
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = receiver
            new_message.save()
            
            # Update conversation timestamp
            conversation.save()
            
            messages.success(request, f'Message sent to {receiver.username}!')
            return redirect('conversation-detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    context = {
        'form': form,
        'receiver': receiver
    }
    return render(request, 'messages_app/send_message.html', context)

