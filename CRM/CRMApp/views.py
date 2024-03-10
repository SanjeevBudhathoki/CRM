from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login ,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task,Interaction







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
    logout(request)
    messages.success(request,f'You have logged out')
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
            return redirect('deal_list')
    else:
        form = DealForm(instance=update_deal)

    return render(request, 'edit_deal.html', {'form': form, 'update_deal': update_deal})


#Delete Deal List
def delete_deal(request, pk):
    deal_to_delete = get_object_or_404(Deal, pk=pk)

    if request.method == 'POST':
        deal_to_delete.delete()
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
            return redirect('task_list')
    else:
        form = TaskForm(instance=update_task)

    return render(request, 'edit_task.html', {'form': form, 'update_task': update_task})

#Delete task List
def delete_task(request, pk):
    delete_to_task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        delete_to_task.delete()
        return redirect('task_list')

    return render(request, 'delete_task.html', {'delete_to_task': delete_to_task})


#show all progress related to task in dashboard
def dashboard(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(task_status='D').count()

    # Calculate the percentage of completed tasks
    completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,
    }

    return render(request, 'index.html', context)

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

    # if interactions.exists():
    #     latest_interaction = interactions.latest('interacted_time').interacted_time
    #     latest_interaction = timezone.localtime(latest_interaction)
    # else:
    #     latest_interaction = datetime.min

    # if request.user.is_superuser:
    #     user_group = False
    # else:
    #     user_group = request.user.groups.values_list('name', flat=True).first()

    if request.method == 'POST':
        # interacted_date_time_str = request.POST.get('datetime')
        # interacted_date_time = timezone.make_aware(datetime.strptime(interacted_date_time_str, '%Y-%m-%dT%H:%M'))
        # interacted_date_time = timezone.localtime(interacted_date_time)

        # if interacted_date_time <= latest_interaction:
        #     messages.error(request, "Interacted date and time must be greater than the latest interaction date.")
        # else:
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
