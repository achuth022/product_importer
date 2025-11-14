from django.shortcuts import render,redirect, get_object_or_404
import csv 
from .models import Product
from django.shortcuts import render
import os
from django.conf import settings
from .tasks import import_products_task
from django.http import JsonResponse
from celery.result import AsyncResult
from product_importer.celery import app  # celery instance
from .forms import ProductForm
from django.contrib import messages
from .webhook import send_product_webhook

# shop/views.py
def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Please upload a valid CSV file.'})

        # Save CSV temporarily
        file_path = os.path.join(settings.BASE_DIR, 'temp', csv_file.name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb+') as f:
            for chunk in csv_file.chunks():
                f.write(chunk)

        # Trigger Celery task
        task = import_products_task.delay(file_path)

        # Return task_id for frontend
        return JsonResponse({'task_id': task.id})

    return render(request, 'shop/upload.html')


  #return the current progress of task
def task_status(request, task_id):
    task = AsyncResult(task_id, app=app)
    if task.state == 'PENDING':
        response = {'state': task.state, 'percent': 0}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'percent': task.info.get('percent', 0)}
    else:
        response = {'state': task.state, 'percent': 100, 'error': str(task.info)}
    return JsonResponse(response)

  #view product
def product_list(request):
    products = Product.objects.all()

    # Filtering
    sku_query = request.GET.get('sku', '')
    name_query = request.GET.get('name', '')
    status_query = request.GET.get('status', '')

    if sku_query:
        products = products.filter(sku__icontains=sku_query)
    if name_query:
        products = products.filter(name__icontains=name_query)
    if status_query:
        if status_query.lower() == 'active':
            products = products.filter(active=True)
        elif status_query.lower() == 'inactive':
            products = products.filter(active=False)

    context = {
        'products': products,
        'sku_query': sku_query,
        'name_query': name_query,
        'status_query': status_query,
    }
    return render(request, 'shop/product_list.html', context)

    #create
def product_create_update(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
        action = "Update"
    else:
        product = None
        action = "Create"

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            
            send_product_webhook(product, event_type="created")

            messages.success(request, f"Product {action.lower()}d successfully!")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', {'form': form, 'action': action})

  #edit produc
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('product_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_edit.html', {'form': form, 'product': product})

  #delete product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('product_list')

   #bulk delete
def bulk_delete_products(request):
    if request.method == 'POST':
        Product.objects.all().delete()
        messages.success(request, "All products deleted successfully!")
    return redirect('product_list')

def home(request):
    return render(request, 'shop/home.html')
