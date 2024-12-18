from django.db import models
import uuid
from .Chat import Chat

class ROLE_TYPE(models.TextChoices):
    USER = 'user'
    ASSISTANT = 'assistant'

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, name='id')
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role_type = models.CharField(max_length=10, choices=ROLE_TYPE.choices, blank=False, null=False)
    msg = models.TextField(blank=False, null=True)
    context = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'messages'

    def json(self):
        return {
            "role": self.role_type,
            "content": f'{self.context}\n{self.msg}' if self.context else self.msg 
        }