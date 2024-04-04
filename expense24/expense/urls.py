from django.contrib import admin
from django.urls import path, include
# Make sure the import statement is correct and points to the correct location of your views.
#from expense.views import ExpenseCreationView,  ExpenseListView, ExpenseDetailView, ExpenseUpdateView, ExpenseDeleteView, AccountCreationView, AccountListView, AccountUpdateView, AccountDetailView, AccountDeleteView, bar_chart_expense,navbar, index, home
from.views import *
from.import views
urlpatterns = [
    path('navbar/', navbar, name='navbar'),
    path('index/', index, name='index'),
    path('home/',home, name='home'),
    # Ensure the path for 'create' ends with a slash.
    path('create/', ExpenseCreationView.as_view(), name='create'),
    path('list_expense/', ExpenseListView.as_view(), name='expense_list'),
    path('list_invoice/', InvoiceListView.as_view(), name='invoice_list'),
    path('expense_detail/<int:pk>/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('update_expense/<int:pk>/', ExpenseUpdateView.as_view(), name='update_expense'),
    path('expense_delete/<int:pk>/', ExpenseDeleteView.as_view(), name='delete_expense'),
    path('manage_exp/', AccountCreationView.as_view(), name='manage_exp'),
    path('list1_expense/', AccountListView.as_view(), name='list1_expense'),
    path('update_acc/<int:pk>/', AccountUpdateView.as_view(), name='update_acc'),
    path('detail_acc/<int:pk>/', AccountDetailView.as_view(), name='detail_acc'),
    path('delete_acc/<int:pk>/', AccountDeleteView.as_view(), name='delete_acc'),
    path("chart/",bar_chart_expense, name="chart"),
    # Add other URL patterns here as needed.
]