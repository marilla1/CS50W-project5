from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .forms import *

# Create your views here.

@login_required
def index(request):
    user = request.user
    context = {
        'user': user,
    }

    return render(request,"pos/index.html", context)


@csrf_exempt
@require_POST
def create_presentation(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'})
    
    form = PresentationForm(data)
    if form.is_valid():
        presentation = form.save()
        response_data = {
            'success': True,
            'message': 'Presentation created successfully!',
            'presentation': {
                'id': presentation.id,
                'name': presentation.name,
                'description': presentation.description,
                'status': presentation.status,
                'created_at': presentation.created_at,
                'updated_at': presentation.updated_at,
            }
        }
    else:
        response_data = {
            'success': False,
            'message': 'Form is not valid',
            'errors': form.errors,
        }
    
    return JsonResponse(response_data)

def view_presentation(request):
    presentation = Presentation.objects.all()
    context = {
        'data': presentation,
    }
    return render(request, "pos/presentation.html", context)


@csrf_exempt
@require_POST
def createcategory(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'})
    
    form = CategoryForm(data)
    if form.is_valid():
        category = form.save()
        response_data = {
            'success': True,
            'message': 'Category created successfully!',
            'category': {
                'id': category.id,
                'categoryname': category.categoryname,
                'status': category.status,
                'created_at': category.created_at,
                'updated_at': category.updated_at,
            }
        }
    else:
        response_data = {
            'success': False,
            'message': 'Form is not valid',
            'errors': form.errors,
        }
    
    return JsonResponse(response_data)

def view_categories(request):
    categories = Category.objects.all()
    return render(request, "pos/categories.html", {'data': categories})


@csrf_exempt
@require_POST
def createsize(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'})
    
    form = SizeForm(data)
    if form.is_valid():
        size = form.save()
        response_data = {
            'success': True,
            'message': 'Size created successfully!',
            'size': {  # Cambiado el nombre del campo a 'size'
                'id': size.id,
                'size': size.size,  # Cambiado el nombre del campo a 'size'
                'status': size.status,
                'created_at': size.created_at,
                'updated_at': size.updated_at,
            }
        }
    else:
        response_data = {
            'success': False,
            'message': 'Form is not valid',
            'errors': form.errors,
        }
    
    return JsonResponse(response_data)

def view_size(request):
    sizes = Size.objects.all()
    return render(request, "pos/size.html", {'data': sizes})


@csrf_exempt
@require_POST
def update_config(request):
    form = SettingsForm(request.POST, request.FILES)
    if form.is_valid():
        settings = form.save()
        response_data = {
            'success': True,
            'message': 'Settings updated successfully!',
            'settings': {
                'id': settings.id,
                'systemname': settings.systemname,
                'image_url': settings.image.url,
                'address': settings.address,
                'phone': settings.phone,
                'exchange': settings.exchange,
                'created_at': settings.created_at,
                'updated_at': settings.updated_at,
            }
        }
    else:
        response_data = {
            'success': False,
            'message': 'Form is not valid',
            'errors': form.errors,
        }

    return JsonResponse(response_data)

def config(request):
    data = Settings.objects.all()
    return render(request, "pos/config.html", {'data': data})

def product(request):
    presentation = Presentation.objects.all()
    size = Size.objects.all()
    context = {
        'presentation': presentation,
        'size': size,
    }

    return render(request,"pos/products.html", context)

def sale(request):
    return render(request,"pos/sales.html")
    