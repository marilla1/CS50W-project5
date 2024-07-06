from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .forms import *
from django.db import transaction
from django.contrib.auth.models import User

# Create your views here.

@login_required
def index(request):
    user = request.user
    context = {
        'user': user,
    }

    return render(request,"pos/index.html", context)

def test(request):
    return render(request, "pos/test.html")


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
    if request.method == 'POST':
        producto = request.POST.get('producto')
        presentation_id = request.POST.get('presentation')
        size_id = request.POST.get('size')
        description = request.POST.get('description')

        try:
            presentation = Presentation.objects.get(id=presentation_id)
            size = Size.objects.get(id=size_id)

            new_product = Product.objects.create(
                productname=producto,
                presentation=presentation,
                size=size,
                description=description,
            )

            return redirect('product')  

        except Presentation.DoesNotExist:
            pass
        except Size.DoesNotExist:
            pass

    presentation = Presentation.objects.all()
    size = Size.objects.all()
    products = Product.objects.all()
    context = {
        'presentation': presentation,
        'size': size,
        'products': products,
    }
    return render(request, 'pos/products.html', context)

def productDescription(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'GET':
        dato = Product.objects.get(id=id) 
        details = ProductDetail.objects.all()
        context = {
            'dato': dato,
            'detail': details,
        }
        return render(request, "pos/productDetail.html", context)
    else:
        price = request.POST.get('price')
        product_detail = ProductDetail(product=product, price=price)
        product_detail.save()
        return redirect('productDescription', id=product.id)
    
    # return HttpResponse(status=405)

def printInvoiceProduct(request, id):
    product = get_object_or_404(Product, id=id)
    product_details = ProductDetail.objects.filter(product=product)
    context = {
        'product': product,
        'product_details': product_details,
    }
    return render(request, "pos/invoiceP.html", context)


@login_required
def sale(request):
    if request.method == 'POST':
        customer_name = request.POST.get('Customer')
        discount = request.POST.get('discount')
        money_r = request.POST.get('money_r')
        money_change = request.POST.get('money_change')

        user = request.user if request.user.is_authenticated else None

        if user is None:
            return HttpResponse("User is not authenticated.")

        with transaction.atomic():
            sale_instance = Sale(
                customer_name=customer_name,
                discount=discount,
                money_r=money_r,
                money_change=money_change,
                user=user  
            )
            sale_instance.save() 

            quantity = request.POST.get('quantity')
            product_id = request.POST.get('product')

            if product_id and quantity:
                product = Product.objects.get(id=product_id)  

                sale_detail_instance = Sale_detail(
                    quantity=quantity,
                    product=product, 
                    sale=sale_instance,
                    user=user  
                )
                sale_detail_instance.save()

        return redirect('sale')  
    else:
        product = Product.objects.all()
        sale = Sale.objects.all()
        product_details = ProductDetail.objects.select_related('product').all()
        product_data = []
        for detail in product_details:
            product_data.append({
            'id': detail.product.id,
            'productname': detail.product.productname,
            'size': detail.product.size.size,  
            'price': detail.price,
            })
        context = {
            'product': product,
            'sale': sale,
            'product_data': product_data,
        }
        return render(request, "pos/sales.html", context)

    

def printInvoiceSale(request, id):
    sale = get_object_or_404(Sale, id=id)
    
    sale_details = Sale_detail.objects.filter(sale=sale)
    
    total = sum(detail.quantity * ProductDetail.objects.get(product=detail.product).price for detail in sale_details)
    
    context = {
        'sale': sale,
        'sale_details': sale_details,
        'total': total,
        'money_received': sale.money_r,
        'money_change': sale.money_change,
    }
    
    return render(request, "pos/invoiceP.html", context)

def api(request, id=None):
    if id is not None:
        sale = get_object_or_404(Sale, id=id)
        sale_details = Sale_detail.objects.filter(sale=sale)
        total = sum(detail.quantity * ProductDetail.objects.get(product=detail.product).price for detail in sale_details)
        
        sale_data = {
            'sale_id': sale.id,
            'customer_name': sale.customer_name,
            'discount': sale.discount,
            'money_received': sale.money_r,
            'money_change': sale.money_change,
            'total': total,
            'sale_details': [
                {
                    'product_id': detail.product.id,
                    'product_name': detail.product.productname,
                    'quantity': detail.quantity,
                    'price_per_unit': ProductDetail.objects.get(product=detail.product).price,
                    'subtotal': detail.quantity * ProductDetail.objects.get(product=detail.product).price
                }
                for detail in sale_details
            ]
        }
        
        return JsonResponse(sale_data)
    else:
        sales = Sale.objects.all()
        sales_list = []
        for sale in sales:
            sale_details = Sale_detail.objects.filter(sale=sale)
            total = sum(detail.quantity * ProductDetail.objects.get(product=detail.product).price for detail in sale_details)
            sale_data = {
                'sale_id': sale.id,
                'customer_name': sale.customer_name,
                'discount': sale.discount,
                'money_received': sale.money_r,
                'money_change': sale.money_change,
                'total': total,
                'sale_details': [
                    {
                        'product_id': detail.product.id,
                        'product_name': detail.product.productname,
                        'quantity': detail.quantity,
                        'price_per_unit': ProductDetail.objects.get(product=detail.product).price,
                        'subtotal': detail.quantity * ProductDetail.objects.get(product=detail.product).price
                    }
                    for detail in sale_details
                ]
            }
            sales_list.append(sale_data)
        
        return JsonResponse({'sales': sales_list})
    
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')  
    else:
        form = UserCreationForm()

    users = User.objects.all()  

    return render(request, 'pos/user.html', {'form': form, 'users': users})