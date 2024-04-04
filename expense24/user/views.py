# from django.utils.encoding import force_text, force_str
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView , LoginView
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.views.generic import ListView
from expense.models import Expense
from .models import User
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import logout
from django.conf import settings


# Your existing views...

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/user_register.html'
    success_url = '/user/login/'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'is_user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        subject = "Welcome to Mysite"
        message = "Hello Guys! Now you can create and manage your expense. Thank you for joining us."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [form.instance.email]  # Access email from form instance
        send_mail(subject, message, email_from, recipient_list)
        return response

# @method_decorator(login_required, name='dispatch')
class UserLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        return '/user/user_dashboard/'  # Redirect to dashboard after login

    def logout_view(request):
        logout(request)
        return redirect('/user/login/')
    
# def forgot_password(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             user = User.objects.filter(email=email).first()
#             if user:
#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 reset_link = request.build_absolute_uri('/reset-password/{}/{}'.format(uid, token))

#                 send_mail(
#                     'Password Reset Request',
#                     f'Click the following link to reset your password: {reset_link}',
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False,
#                 )
#                 return render(request, 'password_reset_email_sent.html')
#     else:
#         form = PasswordResetForm()
#     return render(request, 'forgot_password.html', {'form': form})


# def reset_password(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             password = request.POST['password']
#             user.set_password(password)
#             user.save()
            
#             # Log the user in after password reset
#             user = authenticate(request, username=user.username, password=password)
#             if user is not None:
#                 login(request, user)
                
#             return redirect('password_reset_success')
#         else:
#             return render(request, 'reset_password.html')
#     else:
#         return HttpResponse('Password reset link is invalid.')
    
    
# def password_reset_success(request):
#     return render(request, 'password_reset_success.html')
    



# @method_decorator(login_required, name='dispatch')
class UserDashboardView(ListView):
    template_name = 'user/user_dashboard.html'
    context_object_name = 'user_dashboard'

    def get(self, request, *args, **kwargs):
        user = request.user
        expense1 = Expense.objects.filter(user=user).values()
        expense = Expense.objects.filter(user=user).values('id', 'amount', 'transaction_type', 'description', 'expDateTime', 'status')

        sort_by = self.request.GET.get('sort_by', 'amount')
        direction = self.request.GET.get('direction', 'asc')

        if direction == 'asc':
            expense = expense.order_by(sort_by)
        elif direction == 'desc':
            expense = expense.order_by(f'-{sort_by}')

        return render(request, 'user/user_dashboard.html', {'expenses': expense, 'expense1': expense1})
    
    def get(self, request, *args, **kwargs):
        # def safe(request): 
        
        if request.user.is_authenticated:
            # expenses = Expense.objects.filter(payee__user=request.user).all()
            # expense = Expense.objects.all().values()
            expenses = Expense.objects.filter(user=request.user).all()
            try:
             user_income = sum(list(expenses.filter( transaction_type="income").values_list('amount', flat=True)))
            except: 
             user_income = 0
            
            try:
             user_expenses = sum(list(expenses.filter( transaction_type="expense").values_list('amount', flat=True)))
            except:
             user_expenses = 0
            
            try:
             safe_amount = user_income - (user_expenses*10/100)
            except: 
             safe_amount = 0
            
            
            #char logic here...
            
            labels = []
            data = []
            print("funcion called...")
            # Query for expenses
            queryset = Expense.objects.filter(user=request.user).order_by('-amount')[:10]
            print("queryset ",queryset)

    # Populate labels and data from queryset
        for expense in queryset:
            labels.append(expense.category)
            data.append(expense.amount)
        
        #print("*"*80)
        print("user_income", user_income)
        print("user_expenses", user_expenses)
        return render(request, 'user/user_dashboard.html', 
            {
        "expenses": expenses,
        "user_income": user_income, 
        "user_expenses": user_expenses, 
        "safe_amount": user_income-user_expenses,
        "data":data,
        "labels":labels
            
            
        })
       
    

    # def safe(request): 
    #     if request.user.is_authenticated:
    #         # expenses = Expense.objects.filter(payee__user=request.user).all()
    #         # expense = Expense.objects.all().values()
    #         expenses = Expense.objects.filter(user=request.user).all()
    #         try:
    #          user_income = sum(list(expenses.filter( transaction_type="income").values_list('amount', flat=True)))
    #         except: 
    #          user_income = 0
            
    #         try:
    #          user_expenses = sum(list(expenses.filter( transaction_type="expense").values_list('amount', flat=True)))
    #         except:
    #          user_expenses = 0
            
    #         try:
    #          safe_amount = user_income - (user_expenses*10/100)
    #         except: 
    #          safe_amount = 0
            
        
    #     #print("*"*80)
    #         print("user_income", user_income)
    #         print("user_expenses", user_expenses)
    #         return render(request, 'user/safe.html', 
    #             {
    #         "expenses": expenses,
    #         "user_income": user_income, 
    #         "user_expenses": user_expenses, 
    #         "safe_amount": user_income-user_expenses
            
            
    #            })
    #     else:
    #         return redirect('user_dashboard')
    

def safe(request):
            if request.user.is_authenticated:
            # expenses = Expense.objects.filter(payee__user=request.user).all()
            # expense = Expense.objects.all().values()
             expenses = Expense.objects.filter(user=request.user).all()
            try:
             user_income = sum(list(expenses.filter( transaction_type="income").values_list('amount', flat=True)))
            except: 
             user_income = 0
            
            try:
             user_expenses = sum(list(expenses.filter( transaction_type="expense").values_list('amount', flat=True)))
            except:
             user_expenses = 0
            
            try:
             safe_amount = user_income - (user_expenses*10/100)
            except: 
             safe_amount = 0
        
            print("user_income", user_income)
            print("user_expenses", user_expenses)
            return render(request, 'user/safe.html', 
                {
            "expenses": expenses,
            "user_income": user_income, 
            "user_expenses": user_expenses, 
            "safe_amount": user_income-user_expenses
            
            
               })
    
# def chart(request):
#     if request.user.is_authenticated:
#         expenses = Expense.objects.filter(user=request.user).all()
#         try:
#             user_income = sum(list(expenses.filter(transaction_type="income").values_list('amount', flat=True)))
#         except: 
#             user_income = 0
            
#         try:
#             user_expenses = sum(list(expenses.filter( transaction_type="expense").values_list('amount', flat=True)))
#         except:
#             user_expenses = 0
            
#         try:
#             # safe_amount = user_income - (user_income * 10 / 100)
#             safe_amount = user_income - (user_expenses*10/100)
#             safe_amount = int(safe_amount)
#         except: 
#             safe_amount = 0
        
#         chart_data = [user_income, safe_amount - user_expenses, user_expenses]
#         return render(request,'user/chart.html', {"chart_data": chart_data,  "expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": user_income-user_expenses})
#     return render(request,'user/chart.html', {"chart_data": [0, 0, 0],})

# def chart1(request):
#     if request.user.is_authenticated:
#         expenses = Expense.objects.filter(user=request.user).all()
#         try:
#             user_income = sum(list(expenses.filter(transaction_type="income").values_list('amount', flat=True)))
#         except: 
#             user_income = 0
            
#         try:
#             user_expenses = sum(list(expenses.filter( transaction_type="expense").values_list('amount', flat=True)))
#         except:
#             user_expenses = 0
            
#         try:
#             # safe_amount = user_income - (user_income * 10 / 100)
#             safe_amount = user_income - (user_expenses*10/100)
#             safe_amount = int(safe_amount)
#         except: 
#             safe_amount = 0
        
#         chart_data = [user_income, safe_amount - user_expenses, user_expenses]
#         return render(request,'user/chart.html', {"chart_data": chart_data,  "expenses": expenses, "user_income": user_income, "user_expenses": user_expenses, "safe_amount": user_income-user_expenses})
#     return render(request,'user/chart.html', {"chart_data": [0, 0, 0],})

def bar_chart_expense(request):
    context = {}
    expenses = Expense.objects.filter(user=request.user)
    labels = [expense.category for expense in expenses]
    data = [expense.amount for expense in expenses]
    print(labels)
    # context['labels'] = labels
    # context['data'] = data
    
    return render(request, 'user/user_dashboard.html', {
        "data": data,
        "labels": labels
    })