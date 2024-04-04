from user.models import User
from django.db import models
from django.utils.timezone import now

status = (('cleared', 'cleared'), ('uncleared', 'uncleared'), ('void', 'void'))
transaction_type = (('expense', 'expense'), ('income', 'income'))

class Goal(models.Model):
    goalname = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'goal'

    def __str__(self):
        return self.goalname

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    expDateTime = models.DateField()
    category = models.CharField()
    subCategory = models.CharField()
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(choices=transaction_type, max_length=50)
    status = models.CharField(choices=status, max_length=30)
    description = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Expense'

    # def __str__(self):
    #     return self.status
    
    
typename=(('creditcard','CreditCard'),('cash','Cash'),('cheque','cheque'))

class AccountType(models.Model):
    # accounttype_id = models.IntegerField(primary_key=True)
    type_name=models.CharField(choices=typename,max_length=100)
    class Meta:
        db_table="accounttype"
    def __str__(self):
        return self.type_name
    

class CurrencyType(models.Model):
    # currencytype_id = models.IntegerField(primary_key=True)
    currency=models.CharField(max_length=100)
    class Meta:
        db_table="currencytype"
    def __str__(self):
        return self.currency
    

    
class Account(models.Model):
    # account_id = models.IntegerField(primary_key=True)
    created_at = models.DateField(null=True)
    balance=models.FloatField()
    currencytype=models.ForeignKey(CurrencyType,on_delete=models.CASCADE)
    # default
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accounttype = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    income = models.FloatField(null=True)
    day = models.DateField(null=True)
    class Meta:
        db_table="account"
    
    