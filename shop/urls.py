from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('task-status/<str:task_id>/', views.task_status, name='task_status'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create_update, name='product_create'),
    path('products/<int:pk>/edit/', views.product_create_update, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('products/bulk-delete/', views.bulk_delete_products, name='bulk_delete_products'),

]
