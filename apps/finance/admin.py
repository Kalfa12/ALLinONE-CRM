from django.contrib import admin

from .models import Expense, Revenue

admin.site.register(Expense)
admin.site.register(Revenue)
