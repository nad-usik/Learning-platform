from django import forms
from .models import ChatMessages


class ChatMessageForm(forms.ModelForm):

    body = forms.CharField(label="", widget=forms.Textarea(attrs={'style': 'width: 100%; box-sizing: border-box; border: none; padding: 10px', 'rows': 2, 'placeholder': "Напишите сообщение..."}))

    class Meta:
        model = ChatMessages
        fields =['body', ]
