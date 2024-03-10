from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task,Interaction
from django.db.models import Sum,Count
from django.db.models.functions import TruncMonth
from django.views.decorators.csrf import csrf_exempt 
from django.http import JsonResponse
from django.db.models.functions import ExtractYear, ExtractMonth





# Create your views here.
def dashboard(request):
    return render(request, 'index.html')    

def login(request):
    if request.method == 'POST':
        # Get username and password from the submitted form
        username = request.POST['username']
        password = request.POST['password']
        # Attempt to retrieve a user with the given username from the database
        user = User.objects.get(username = username)
        # Check if the provided password matches the user's password
        if user.check_password(password):
            # If the password is correct, log the user in
            auth_login(request,user)
            messages.success(request,f'Welcome {username} You have logged in Successfully.')
            return redirect('dashboard')
        else:
            # If user does not exist, show an error message
            messages.error(request,"Invalid login credentials")
    return render(request,'login.html')

@login_required(login_url='login')
def user_logout(request):
    username = request.user.username #fetch the username
    logout(request)
    messages.success(request,f'{username} You have logged out')
    return redirect('login')


#---------------------------------------------------------------------------------------------------------------
#registor form for customer
from .forms import RegistrationForm

def registration_form(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request,'register_form.html',{'form_data':form})
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():                 # checks data's basic validation
            form.save()                     # saves data in form("RegistrationForm") after Validation. 
            messages.success(request,"You have Register Successfully...") # message to shows that action is successfully completed.
            return redirect('listCustomer')         # Sends user To Home page using url we set for homepage in urls.py[CRMProject]
        else:
            for field,errors in form.errors.items():    #builtIn feature of RegistrationForm in django
                for error in errors:
                    messages.error(request,f"{field.capitalize()} : {error}")   # gives error message of respective field.
            return render(request,'register_form.html',{'form_data':form}) # To load register form page if theres any issue creating account/s.    
    return render(request,'register_form.html',{'form_data':form})

#--------------------------------------------------------------------------------------------------------------
#after register form, details of customer list
from .models import Customer

def customerList(request):
    customers = Customer.objects.all()
    return render(request,'tables.html',{'customers':customers})



def customerDetail(request, pk):
    customer_detail = Customer.objects.get(pk=pk)
    return render(request,'register_form.html',{'customer_detail':customer_detail})

def customerDelete(request, pk):
    customer = Customer.objects.get(pk=pk)
    customer.delete()
    messages.success(request, 'Customer Information deleted successfully.')
    customer = Customer.objects.all()
    return render(request,'tables.html',{'customers':customer})

def customerUpdate(request, pk):
    customer = Customer.objects.get(pk=pk)
    customers = Customer.objects.all()
    if request.method=="POST":
        customer.username = request.POST.get('username')
        customer.email = request.POST.get('email')
        customer.phone_number = request.POST.get('phone_number')
        customer.company_name = request.POST.get('company_name')
        customer.company_notes = request.POST.get('company_notes')
        customer.save()
        messages.success(request, 'Customer Information updated successfully.')
        return redirect('listCustomer')
    return render(request,'update.html',{'customer':customer})

#-----------------------------------------------------------------------------------------------------------
#Deal Management
from .models import Deal

def deal_list(request):
    deals = Deal.objects.all()
    return render(request, 'deal_list.html', {'deals': deals})




#create new deal form
from .forms import DealForm
def create_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal created successfully.')
            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request, 'create_deal.html', {'form': form})

#Edit Deal list
def edit_deal(request, pk):
    update_deal = get_object_or_404(Deal, pk=pk)

    if request.method == "POST":
        form = DealForm(request.POST, instance=update_deal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal updated successfully.')
            return redirect('deal_list')
    else:
        form = DealForm(instance=update_deal)

    return render(request, 'edit_deal.html', {'form': form, 'update_deal': update_deal})


#Delete Deal List
def delete_deal(request, pk):
    deal_to_delete = get_object_or_404(Deal, pk=pk)

    if request.method == 'POST':
        deal_to_delete.delete()
        messages.success(request, 'Deal deleted successfully.')
        return redirect('deal_list')

    return render(request, 'delete_deal.html', {'deal_to_delete': deal_to_delete})


#---------------------------------------------------------------------------------------------------------------
#Task Management


def task_list(request):
    tasks = Task.objects.all()
    context = {
        'task':tasks,
    }
    return render(request,'task_list.html',context)
    # return render(request, 'task_list.html', {'tasks': tasks})

#create new task form
from .forms import TaskForm
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

#Edit task list
def edit_task(request, pk):
    update_task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=update_task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=update_task)

    return render(request, 'edit_task.html', {'form': form, 'update_task': update_task})

#Delete task List
def delete_task(request, pk):
    delete_to_task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        delete_to_task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')

    return render(request, 'delete_task.html', {'delete_to_task': delete_to_task})

#---------------------------------------------------------------------------------------------------------------
#show all progress related in dashboard
def dashboard(request):
    #Count of Tasks Done
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(task_status='D').count()
    completion_percentage = int((completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0)

    #Count of Open Task
    tasks = Task.objects.all()
    open_task_count = tasks.filter(task_status='O').count()


    #Amount Count of Deal won
    total_deal = Deal.objects.count()
    completed_deal = Deal.objects.filter(deal_status='W').count()
    total_amount_won = Deal.objects.filter(deal_status='W').aggregate(Sum('deal_amount'))['deal_amount__sum'] or 0

    #Amount Count of Deal lost
    lost_deal = Deal.objects.filter(deal_status='L').count()
    aggregate_result = Deal.objects.filter(deal_status='L').aggregate(Sum('deal_amount'))
    total_amount_lost = aggregate_result.get('deal_amount__sum', 0) or 0

    #Count of Deal Open
    deals = Deal.objects.all()
    total_open = deals.filter(deal_status='O').aggregate(Sum('deal_amount'))['deal_amount__sum'] or 0
    open_deal_count = deals.filter(deal_status='O').count()

    #Count of Deal Won and Loss in Chart 
    deals = Deal.objects.all()
    won_deal_count = deals.filter(deal_status='Won').count()
    lost_deal_count = deals.filter(deal_status='Lost').count()

    #Aggregate customer counts per month
    attendance_data = (
        Customer.objects.annotate(month=TruncMonth('arrived_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    ) 
    attendance_data_list = list(attendance_data)
    print(attendance_data_list)
    context = {
        #Count of Tasks Done
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,

        #Count of Open Task
        'tasks': tasks,
        'open_task_count': open_task_count,

        #Amount Count of Deal won
        'total_deal': total_deal,
        'completed_deal': completed_deal,
        'total_amount_won': total_amount_won,

        #Amount Count of Deal lost
        'lost_deal': lost_deal,
        'total_amount_lost': total_amount_lost,

        #Count of Deal Open
        'deals': deals,
        'total_open': total_open,
        'open_deal_count': open_deal_count,

        #Count of Deal Won and Loss in Chart 
        'won_deal_count': won_deal_count,
        'lost_deal_count': lost_deal_count,

        #chart for attendance
        'attendance_data': attendance_data_list,

    }

    
    return render(request, 'index.html', context)

def get_filter_options(request):
    grouped_customer = Customer.objects.annotate(year=ExtractYear("arrived_date")).values("year").order_by("-year").distinct()
    options = [customer["year"] for customer in grouped_customer]

    return JsonResponse({
        "options": options,
    })

@csrf_exempt
def customer_attendance(request, year):
    # attendance_data = (
    #     Customer.objects.annotate(month=TruncMonth('arrived_date'))
    #     .values('month')
    #     .annotate(count=Count('id'))
    #     .order_by('month')
    # )
    # attendance_data_list = list(attendance_data)
    # return render(request,'attendee.html', {'attendance_data': attendance_data_list})
    # return JsonResponse({'attendance_list':attendance_data_list})
    customers = Customer.objects.filter(arrived_date__year=year)
    attendance_data = customers.annotate(month = ExtractMonth('arrived_date')).values('month')\
    .annotate(count=Count('id')).order_by('month')
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    attende_dict = dict()
    for month in months:
        attende_dict[month] = 0

    for group in attendance_data:
        attende_dict[months[group['month']-1]] = group['count']

    return JsonResponse({
        'title': f"attende in months",
        'data':{
            'labels':list(attende_dict.keys()),
            'datasets':[{
                'label':'attende',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor':'rgba(75, 192, 192, 0.2)',
                'data':list(attende_dict.values()),
                'borderWidth':1
            }]
        }
    })



#---------------------------------------------------------------------------------------------------------------
#Interaction History
from django.utils import timezone
from datetime import datetime, time


@login_required(login_url='login')
def customerDetail(request, pk):
    customer_detail = get_object_or_404(Customer, pk=pk)
    interactions = Interaction.objects.filter(interacted_customer=customer_detail.id)
    status_option = Interaction._meta.get_field('interacted_mode').choices
    status_option_list = [choices[1] for choices in status_option]

    context = {
        'customer_detail': customer_detail,
        'interactions': interactions,
        'status_option_list':status_option_list

    }

    if request.method == 'POST':
            post = Interaction()
            post.interacted_mode = request.POST.get('interacted_mode')
            post.interacted_time = request.POST.get('datetime')
            post.interaction_notes = request.POST.get('notes')
            post.interacted_customer = customer_detail
            post.intrAddedByUser = request.user.username
            post.save()
    
    return render(request, 'customer_detail.html', context)


def interactionDelete(request, pk):
    interaction_delete = Interaction.objects.get(pk=pk)
    customerid = interaction_delete.interacted_customer.pk
    interaction_delete.delete()
    return redirect('customer_detail',customerid)

#------------------------------------------------------------------------------------------------------------------
#Profile Details of user information
@login_required
def user_info(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'user_info.html', context)








