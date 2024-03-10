from typing import Any
from django.db import models
from django.contrib.auth.models import User




# Create your models here.



class Customer(models.Model):
    username = models.CharField(max_length= 150,unique=True)
    email = models.CharField(max_length= 150,unique = True)
    phone_number = models.CharField(max_length= 150)
    company_name = models.CharField(max_length=150)
    company_notes = models.TextField()
    arrived_date = models.DateField()

    class Meta:
        db_table = 'Customer'

    def __str__(self):
        return self.username
    


class Deal(models.Model):
    status = (("O","Open"),("W","Won"),("L","Lost"))
    deal_title = models.CharField(max_length=100)
    deal_status = models.CharField(max_length=30, choices=status)
    expected_close_date = models.DateField()
    deal_amount = models.IntegerField()
    deal_withCustomer = models.ForeignKey(Customer,on_delete=models.CASCADE)

    class Meta:
        db_table ='Deal'

    def __str__(self):
        return self.deal_title
    
class Task(models.Model):
    status = (("O","Open"),("D","Done"))
    task_title = models.CharField(max_length=100)
    task_status = models.CharField(max_length=30, choices=status)
    task_description = models.TextField()
    task_duedate = models.DateField()
    task_relatedtodeal = models.ForeignKey(Deal,on_delete=models.CASCADE)

  
    class Meta:
        db_table = 'Task'

    def __str__(self):
        return self.task_title

class Interaction(models.Model):
    interaction_option = (('E','Email'), ('C', 'Call'), ('M','Meeting'))
    interacted_mode = models.CharField(max_length=30, choices=interaction_option)
    interacted_time = models.DateTimeField()
    interaction_notes = models.TextField()
    interacted_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        db_table = "Interaction"
    
    def __str__(self):
        return self.interacted_mode
    






