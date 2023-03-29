from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmi(admin.ModelAdmin):
    list_display = ['owner', 'founder', 'found_date', 'lost_date']


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'question', 'response']


@admin.register(DepositPoint)
class DepositPointAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']


@admin.register(ItemQuestion)
class ItemQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_for_reclamation']


@admin.register(DepositPointAdministration)
class DepositPointAdminAdmin(admin.ModelAdmin):
    list_display = ['admin', 'deposit_point']


@admin.register(ItemDeposit)
class ItemDepositAdmin(admin.ModelAdmin):
    list_display = ['deposit_point', 'item', 'added_by', 'date_added']