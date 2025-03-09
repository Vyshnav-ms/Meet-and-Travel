from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Write your message here...',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Message
        fields = ['content']

