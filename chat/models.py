import json

from django.db import models
from django.utils.functional import cached_property
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE
from pyhub.rag.fields.sqlite import SQLiteVectorField
from pyhub.rag.models.sqlite import SQLiteVectorDocument

from chat.llm import LLM


class TaxLawDocument(SQLiteVectorDocument):
    embedding = SQLiteVectorField(
        dimensions=3072,
        editable=False,
        embedding_model="text-embedding-3-large",
    )

    @cached_property
    def page_content_obj(self):
        return json.loads(self.page_content)


class Room(LifecycleModelMixin, models.Model):
    name = models.CharField(max_length=255)
    system_prompt = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @hook(AFTER_UPDATE, when="system_prompt", has_changed=True)
    def on_after_update(self):
        self.message_set.all().delete()

    def create_ai_message(self):
        # 현재 방의 이전 메시지들을 수집
        message_qs = self.message_set.all()
        messages = [{"role": msg.role, "content": msg.content} for msg in message_qs]

        # 세법 해석례 문서 검색이 필요할 때
        user_message = messages[-1]["content"].strip()
        if user_message.startswith("!"):
            user_message = user_message[1:]
            # RAG를 원하는 모델을 사용하여 유사 문서 검색
            doc_list = TaxLawDocument.objects.similarity_search(user_message)
            지식 = str(doc_list)
            system_prompt = self.system_prompt + "\n\n" + f"참고문서 : {지식}"
        else:
            system_prompt = self.system_prompt

        # AI 응답 생성
        llm = LLM(
            model="gpt-4o-mini",
            temperature=1,
            system_prompt=system_prompt,
            initial_messages=messages,
        )
        ai_message = llm.make_reply()

        # AI 응답을 새 메시지로 저장
        return self.message_set.create(
            role=Message.Role.ASSISTANT,
            content=ai_message,
        )

    class Meta:
        ordering = ["-pk"]


class Message(models.Model):
    class Role(models.TextChoices):
        USER = "user"
        ASSISTANT = "assistant"

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=Role.choices, default=Role.USER)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["pk"]
