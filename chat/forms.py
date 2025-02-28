from django import forms
from .models import Message, Room


# 새 채팅방 생성 및 수정 페이지에서
# 입력 HTML 폼 생성 및 유효성 검사를 담당
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "system_prompt"]


# 채팅 메시지 입력/수정 폼을 생성하고 유효성 검사를 담당
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["content"]
