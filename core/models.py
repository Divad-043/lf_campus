from django.db import models
from accounts.models import User, Visitor
from django.contrib.gis.db import models as lmodels
import uuid
# from django_google_maps import fields as map_fields


item_status = [
    ('Verified', 'Verified'),
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected')
]


class Item(models.Model):
    id=models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="owner")
    founder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="founder")
    added_by_visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True, blank=True)
    found_date = models.DateField(null=True, blank=True)
    lost_date = models.DateField(null=True, blank=True)
    lost_location_latitude = models.FloatField(null=True, blank=True)
    lost_location_longitude = models.FloatField(null=True, blank=True)
    found_location_latitude = models.FloatField(null=True, blank=True)
    found_location_longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField('ItemCategory')
    status = models.CharField(max_length=15, choices=item_status, default="Pending")
    first_image = models.ImageField(upload_to='item_images/', null=True)
    second_image = models.ImageField(upload_to='item_images/', null=True)

    def __str__(self):
        return str(self.uid)

    def get_map_html(self):
        return f'<iframe width="100%" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.openstreetmap.org/export/embed.html?bbox={self.location}&amp;layer=mapnik&amp;marker={self.location}"></iframe>'


class ItemCategory(models.Model):
    name = models.CharField(max_length=40)
    questions = models.ManyToManyField('ItemQuestion')
    image_for_display = models.ImageField(upload_to="display/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Item Categories"

    def __str__(self):
        return self.name


class ItemQuestion(models.Model):
    question = models.CharField(max_length=200)
    is_for_reclamation = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class ItemQuestionResponse(models.Model):
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE)
    question = models.ForeignKey('ItemQuestion', on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'question', 'item'], name="pk_question_response_item")
        ]


class Reclamation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    question = models.ForeignKey(ItemQuestion, on_delete=models.CASCADE)
    response = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'item', 'question'], name="pk_reclamation")
        ]


class DepositPoint(models.Model):
    name = models.CharField(max_length=50)
    # location = lmodels.PointField()
    items = models.ManyToManyField(Item, through='ItemDeposit')
    admins = models.ManyToManyField(User, through='DepositPointAdministration')
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_for_display = models.ImageField(upload_to="display/", null=True, blank=True)

    def __str__(self):
        return self.name


class DepositPointAdministration(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit_point = models.ForeignKey(DepositPoint, on_delete=models.CASCADE)


class ItemDeposit(models.Model):
    deposit_point = models.ForeignKey(DepositPoint, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deposit_point', 'item'], name="pk_deposit")
        ]

