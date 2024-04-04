
from django import forms
from.models import Expense
from .models import Account
# from user.models import User
# class ExcludeFieldMixin:
#     """
#     Form mixin to exclude a specific field from all forms.
#     """
#     exclude_fields = ['user']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         for field_name in self.exclude_fields:
#             if field_name in self.fields:
#                 del self.fields['user']

class ExpenseCreationForm( forms.ModelForm):
    class Meta:
        model = Expense
        fields ='__all__'
        exclude = ['user']
        
        widgets = {
            'expenseDateTime': forms.DateInput(attrs={'type': 'date'}),
         }
        
    # def _init_(self, *args, user_type=None, **kwargs):
    #     super(ExpCreationForm, self)._init_(*args, **kwargs)

    #     # Disable a specific choice option for the 'user_type' field based on the condition
    #     disabled_option = 'is_user'  # Change this to the option you want to disable
    #     if user_type and 'user_type' in self.fields:
    #         choices = self.fields['user_type'].choices
    #         self.fields['user_type'].choices = [(value, label, {'disabled': value == disabled_option}) for value, label in choices]
            
class AccountCreationForm(forms.ModelForm):
    class Meta:
        model = Account
        # fields = '__all__'
        exclude = ['user']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
            'day': forms.DateInput(attrs={'type': 'date'}),
        }
