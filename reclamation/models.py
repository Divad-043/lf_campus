from django.db import models
from accounts.models import User
from core.models import Item, ItemQuestion


class Reclamation(models.Model):
    reclamation_status = [
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    question = models.ForeignKey(ItemQuestion, on_delete=models.CASCADE)
    response = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=reclamation_status, default="Pending")

    def __str__(self):
        return f'{self.user} - {self.item} - {self.question}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'item', 'question'], name="pk_reclamation")
        ]
