from django.db import models
from accounts.models import User


class UserMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    content = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    is_send = models.BooleanField(default=True)
    is_read = models.BooleanField(default=False)


# model Discussion that represents a discussion between two users with messages
class Discussion(models.Model):
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    messages = models.ManyToManyField(UserMessage, blank=True)
