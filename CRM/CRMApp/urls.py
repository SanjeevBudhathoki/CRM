
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('logout', views.user_logout, name='logout'),

    #registration customer form
    path('register',views.registration_form,name='register'),

    #customer list
    path('list/',views.customerList, name='listCustomer'),
    path('detail/<int:pk>/',views.customerDetail,name='customerDetail'),
    path('delete/<int:pk>/',views.customerDelete,name='delete'),
    path('update/<int:pk>/',views.customerUpdate,name='update'),

    #deal management
    path('create_deal/', views.create_deal, name='create_deal'),
    path('deal_list/', views.deal_list, name='deal_list'),
    path('edit_deal/<int:pk>/', views.edit_deal, name='edit_deal'),
    path('delete_deal/<int:pk>/', views.delete_deal, name='delete_deal'),

    #task management
    path('create_task/', views.create_task, name='create_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),

    path('customer/<int:pk>/', views.customerDetail, name='customer_detail'),

    path('interaction_delete/<int:pk>/', views.interactionDelete, name='interaction_delete'),

]

