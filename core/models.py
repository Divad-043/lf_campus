import uuid
from django.db import models
from django.urls import reverse
from accounts.models import User, Visitor

item_status = [
    ('Verified', 'Verified'),
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected')
]


class Item(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="owner")
    founder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="founder")
    added_by_visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, null=True, blank=True)
    confirmed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    deposit_point = models.ForeignKey('DepositPoint', on_delete=models.CASCADE, null=True, blank=True)
    found_date = models.DateField(null=True, blank=True)
    lost_date = models.DateField(null=True, blank=True)
    lost_location_latitude = models.FloatField(null=True, blank=True)
    lost_location_longitude = models.FloatField(null=True, blank=True)
    found_location_latitude = models.FloatField(null=True, blank=True)
    found_location_longitude = models.FloatField(null=True, blank=True)
    found_location_name = models.CharField(max_length=50, null=True, blank=True)
    lost_location_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=15, choices=item_status, default="Pending")
    first_image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    second_image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_map_html(self):
        return f'<iframe width="100%" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" ' \
               f'src="https://www.openstreetmap.org/export/embed.htm' \
               f'l?bbox={self.found_location_longitude, self.found_location_latitude}&amp;layer=mapnik&amp;'\
               f'marker={self.found_location_longitude, self.found_location_latitude}"></iframe>'

    def get_popup_information(self):
        value = {
            'type': 'Feature',
            'properties': {
                'description':
                    '<img height="40px" width="100%" src="' + str(self.first_image.url) + '"></img>'
                    f'<h5><strong>Name : {self.itemquestionresponse_set.filter(item=self).first().answer}</strong></h5>'
                    '<p><a href="' + self.get_absolute_url() + '" style="color:"blue"; target="_blank" title="Opens in '
                    'a new window">Show Detail</a>  '
                    '</p>',
                'iconSize': [18, 18],
                'message': 'test',
                'title': self.itemquestionresponse_set.filter(item=self).first().answer,
                'image': self.category.icon_for_map.url,
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [self.found_location_longitude, self.found_location_latitude]
            }
        }
        return value

    def get_absolute_url(self):
        return reverse("core:item_detail", kwargs={"pk": self.pk})


class ItemCategory(models.Model):
    name = models.CharField(max_length=40)
    questions = models.ManyToManyField('ItemQuestion')
    image_for_display = models.ImageField(upload_to="display/", null=True, blank=True)
    icon_for_map = models.ImageField(upload_to='icons_map/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Item Categories"

    def __str__(self):
        return self.name


class ItemQuestionTag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ItemQuestion(models.Model):
    question = models.CharField(max_length=200)
    is_for_reclamation = models.BooleanField(default=False)
    tag = models.ForeignKey(ItemQuestionTag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question


class ItemQuestionResponse(models.Model):
    category = models.ForeignKey('ItemCategory', on_delete=models.CASCADE)
    question = models.ForeignKey('ItemQuestion', on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.answer}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'question', 'item'], name="pk_question_response_item")
        ]


class DepositPoint(models.Model):
    name = models.CharField(max_length=50)
    items = models.ManyToManyField(Item, through='ItemDeposit')
    admins = models.ManyToManyField(User, through='DepositPointAdministration')
    phone = models.CharField(max_length=9, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    open_hour = models.TimeField(null=True, blank=True)
    close_hour = models.TimeField(null=True, blank=True)
    image_for_display = models.ImageField(upload_to="display/", null=True, blank=True)
    associate_university = models.ForeignKey('University', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class DepositPointAdministration(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit_point = models.ForeignKey(DepositPoint, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now=True)


class ItemDeposit(models.Model):
    deposit_point = models.ForeignKey(DepositPoint, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deposit_point', 'item'], name="pk_deposit")
        ]


class University(models.Model):
    name = models.CharField(max_length=200)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    image = models.ImageField(upload_to='universities/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_total_number_of_items(self):
        return Item.objects.filter(depositpoint__associate_university=self).count()

    class Meta:
        verbose_name_plural = 'Universities'
