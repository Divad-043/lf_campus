import uuid
from django.db import models
from accounts.models import User
from core.models import ItemCategory

# Create your models here.

class ItemIdentifierType(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

class ItemIdentifier(models.Model):
    id=models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    identifier_type = models.ForeignKey(ItemIdentifierType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField()
