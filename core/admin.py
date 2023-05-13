from django.contrib import admin
from .models import *
# from django_google_maps import widgets as map_widgets
# from django_google_maps import fields as map_fields


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['owner', 'founder', 'found_date', 'lost_date', 'lost_location_latitude', 'lost_location_longitude', 'found_location_longitude',  'found_location_latitude']
    # formfield_overrides = {
    #     map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    # }


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'question', 'response']


@admin.register(DepositPoint)
class DepositPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'longitude', 'latitude']


@admin.register(ItemQuestion)
class ItemQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_for_reclamation']


@admin.register(DepositPointAdministration)
class DepositPointAdminAdmin(admin.ModelAdmin):
    list_display = ['admin', 'deposit_point']


@admin.register(ItemDeposit)
class ItemDepositAdmin(admin.ModelAdmin):
    list_display = ['deposit_point', 'item', 'added_by', 'date_added']


@admin.register(ItemQuestionResponse)
class ItemQuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['item', 'question', 'answer']