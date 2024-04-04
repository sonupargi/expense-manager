from django.contrib import admin 
from .models import Expense,Goal, AccountType,CurrencyType,Account

# Register your models here.

admin.site.register(Expense)
admin.site.register(Goal)
admin.site.register(AccountType)
admin.site.register(CurrencyType)
admin.site.register(Account)