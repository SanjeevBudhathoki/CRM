from django import forms
from .models import Customer
from .models import Task


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username','email','phone_number','company_name','company_notes','arrived_date']

    
    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'})
    )
    email = forms.EmailField(
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'})
    )
    phone_number = forms.CharField(
        required=True,
        max_length=10,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone_Number','pattern':'\d*','min':10})
    )

    company_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Company_Name'})
    )

    company_notes = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control'})
    )

    arrived_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'],
        widget=forms.DateInput(attrs={'type':'date'}),
    )

    


#Deal Management
from .models import Deal

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['deal_title', 'deal_status', 'expected_close_date', 'deal_amount', 'deal_withCustomer']

        widgets = {
            'expected_close_date': forms.DateInput(attrs={'type': 'date'}),
        }

#Task Management


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title','task_status','task_description','task_duedate','task_relatedtodeal']

        widgets = {
            'task_duedate': forms.DateInput(attrs={'type': 'date'}),
        }

