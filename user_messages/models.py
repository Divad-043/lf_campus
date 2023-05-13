from django.db import models
from accounts.models import User

# Create your models here.
class UserMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)