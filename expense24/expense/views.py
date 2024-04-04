from django.shortcuts import render
# from django.http import JsonResponse
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from .models import *
from django.views.generic import ListView,DetailView
from django.views.generic import DeleteView,UpdateView
from django.utils.dateformat import DateFormat
from django.http import HttpResponseRedirect

# from .forms import PDFUploadForm
# import PyPDF2



# from django.conf import settings
# from django.core.mail import send_mail
# from django.http import HttpResponse


# Create your views here.
# 1.navbar
def navbar(request):
    return render(request,'expense/navbar.html')

def index(request):
    return render(request,'expense/index.html')

def home(request):
    return render(request,'expense/home.html')




class ExpenseCreationView(CreateView):
    form_class =ExpenseCreationForm
    model = Expense
    template_name = 'expense/create.html'
    success_url = '/expense/list_expense/'

    def get_context_data(self,**kwargs):
        email = self.request.POST.get('email')
        print(email)
        kwargs['user_type'] = 'is_user'
        
        return super().get_context_data(**kwargs)
    


    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        print("email id ----",self.request.user.email)
        subject = "Welcome to Mysite"
        message = "We are pleased to inform you that your recent income/expense has been added successfully to your Expense Manager App. Your records are now available for you to access and review at any time with our Expense Manager App, you can easily keep track of your income and expenses, set budgets, and monitor your spending habits. By doing so, you can better manage your finances, avoid overspending, and achieve your financial goals."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]        
        send_mail(subject, message, email_from, recipient_list)
        print(recipient_list)   
        return response
    
    
   
    
   


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expense/list_expense.html'
    context_object_name = 'list_expense'
    
    # def get_queryset(self):
    #     return super().get_queryset()  

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        # list_exp1=Expense.objects.filter(user=user).values()
        list_expense = Expense.objects.filter(user=user).values("id",'user', 'category','subCategory','amount','expDateTime','transaction_type','status','description','goal__goalname')
        print(list_expense)
        return render(request,'expense/list_expense.html',{'list_expense':list_expense})
    




class ExpenseUpdateView(UpdateView):
    model = Expense
    form_class = ExpenseCreationForm
    template_name = 'expense/create.html'
    success_url = '/expense/list_expense/'

   

    
class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expense/expense_detail.html'
    context_object_name = 'expense_detail'
    success_url = '/expense/expense_detail/'
    
             
    
    def get(self, request ,*args, **kwargs):
       print("called.....")
       user = request.user
       print(user)
       labels=[]
       data =[]
       category = Expense.objects.all().values_list('category',flat=True)
    # category = Expense.objects.filter(user=user).values_list('category__categoryname',flat=True)
    
       amount = Expense.objects.all().values_list('amount',flat=True)
    # amount = Expense.objects.filter(user=user).values_list('amount',flat=True)
       for i in category:
            labels.append(i)
       for i in amount:
            data.append(i)
       expense = Expense.objects.get(id=self.kwargs['pk'])
       print("expense....",expense)
       expense_data = {
        "id": expense.id,
        "user": expense.user,
        "category": expense.category,
        "subCategory": expense.subCategory,
        "amount": expense.amount,
        "expDateTime": expense.expDateTime,
        "transaction_type": expense.transaction_type,
        "status": expense.status,
        "description": expense.description,
        "goal__goalname": expense.goal.goalname if expense.goal else None
    }
       print(expense)
       
    #    return render(request, self.template_name, {'exp_detail': self.get_object(),'expense':expense,'labels':self.labels,'data':self.data})
       return render(request, self.template_name, {'expense_detail': expense_data,'expense':expense,'labels':labels,'data':data})
      
     
    

    
class ExpenseDeleteView(DeleteView):
    model = Expense
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    success_url = '/expense/list_expense/'
    
    
class AccountCreationView(CreateView):
    model = Account
    form_class = AccountCreationForm
    template_name = 'expense/manage_exp.html'
    success_url = '/expense/list1_expense/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class AccountListView(ListView):
    model = Account
    template_name = 'expense/list1_expense.html'
    context_object_name = 'list1_expense'
    
    def get_queryset(self):
        return super().get_queryset()
    


class AccountUpdateView(UpdateView):
    model = Account
    form_class = AccountCreationForm
    template_name = 'expense/manage_exp.html'
    success_url = '/expense/list1_expense/'


class AccountDetailView(DetailView):
    model = Account
    template_name = 'expense/detail_acc.html'
    context_object_name = 'detail_acc'
    success_url = '/expense/detail_acc/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = []
        data = []

        # Query for expenses related to the authenticated user
        queryset = Expense.objects.filter(user=self.request.user).order_by('-amount')[:10]
        print("queryset",queryset)

        # Populate labels and data from queryset
        for expense in queryset:
            labels.append(expense.category)
            data.append(expense.amount)

        # Create context dictionary
        context.update({
            'labels': labels,
            'data': data,
        })

        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        labels = []
        data = []

        # Query for accounts related to the authenticated user
        queryset = Account.objects.filter(user=self.request.user).order_by('-day')[:10]
        print("query set:", queryset)

        # Populate labels and data from queryset
        for account in queryset:
            if account.day:
                labels.append(DateFormat(account.day).format('Y-m-d'))
            else:
                labels.append('Unknown Date')
            data.append(account.income)

        # Create context dictionary
        context.update({
            'labels': labels,
            'data': data,
        })

        return context

class AccountDeleteView(DeleteView):
    model = Account
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    success_url = '/expense/list1_expense/'
    
    # Import your Expense model here


def bar_chart_account(request):
    # Initialize empty lists for labels and data
    labels = []
    data = []

    # Query for expenses
    queryset = Account.objects.filter(user=request.user).order_by('-day')[:10]
    print("q.....",queryset)

    # Populate labels and data from queryset
    for account in queryset:
        labels.append(DateFormat(account.day).format('Y-m-d'))
        data.append(account.income)

    # Create context dictionary
    context = {
        'labels': labels,
        'data': data,
    }

    # Render the template with the context data
    return render(request, 'expense/detail_acc.html', context)

    
def bar_chart_expense(request):
    # Initialize empty lists for labels and data
    labels = []
    data = []
    print("funcion called...")
    # Query for expenses
    queryset = Expense.objects.filter(user=request.user).order_by('-amount')[:10]

    # Populate labels and data from queryset
    for expense in queryset:
        labels.append(expense.category)
        data.append(expense.amount)

    # Create context dictionary
    context = {
        'labels': labels,
        'data': data,
    }

    # Render both chart.html and user_dashboard.html with the same context
    # render(request, 'user/user_dashboard.html', context)
    return render(request, 'expense/chart.html', context)

class ReceiptListView(ListView):
    model = Expense
    template_name = 'expense/receipt.html'
    context_object_name = 'receipt'
    
    
    
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        # list_exp1=Expense.objects.filter(user=user).values()
        receipt = Expense.objects.filter(user=user).values("id",'user', 'category','subCategory','amount','expDateTime','transaction_type','status','description','goal__goalname')
        print(receipt)
        return render(request,'expense/receipt.html',{'receipt':receipt})
    
class InvoiceListView(ListView):
    model = Expense
    template_name = 'expense/list_invoice.html'
    context_object_name = 'list_invoice'
    
    # def get_queryset(self):
    #     return super().get_queryset()  

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        # list_exp1=Expense.objects.filter(user=user).values()
        list_expense = Expense.objects.filter(user=user).values("id",'user', 'category','subCategory','amount','expDateTime','transaction_type','status','description','goal__goalname')
        print(list_expense)
        return render(request,'expense/list_invoice.html',{'list_invoice':list_expense})
    
# def convert_pdf(request):
#     if request.method == 'POST':
#         form = PDFUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             pdf_file = request.FILES['pdf_file']
#             text_content = ''
#             try:
#                 with pdf_file.open() as f:
#                     pdf_reader = PyPDF2.PdfFileReader(f)
#                     for page_num in range(pdf_reader.numPages):
#                         page = pdf_reader.getPage(page_num)
#                         text_content += page.extractText()
#             except Exception as e:
#                 error_message = str(e)
#                 return render(request, 'error.html', {'error_message': error_message})
#             return render(request, 'converted.html', {'text_content': text_content})
#     else:
#         form = PDFUploadForm()
#     return render(request, 'upload.html', {'form': form})


# def get_context_data(self, **kwargs):
#         bar_chart = self.request.POST.get('bar_chart')
#         print(bar_chart)
#         kwargs['user_type'] = 'is_user'
#         return render().get_context_data(**kwargs)


# def user_specific_chart(request):
#     # Assuming you have a model called Expense with a field called amount
#     # Fetch data for the chart specific to the logged-in user
#     user_expenses = Expense.objects.filter(user=request.user)
#     labels = []
#     data = []
#     for expense in user_expenses:
#         labels.append(expense.category)  # Example: Use category as labels
#         data.append(expense.amount)      # Example: Use amount as data points

#     return render(request, 'exp/user_chart.html', {'labels': labels, 'data': data})