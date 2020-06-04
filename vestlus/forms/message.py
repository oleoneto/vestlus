from django import forms
from ..models import Message, PrivateMessage, GroupMessage


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = '__all__'


class GroupMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ('content',)
