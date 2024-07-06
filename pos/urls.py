from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("presentation/", views.view_presentation, name="presentation"),
    path('create_presentation/', views.create_presentation, name='create_presentation'),
    path('categories/', views.view_categories, name='categories' ),
    path('createcategory/', views.createcategory, name='create_category'),
    path('sizes/', views.view_size, name='size'),
    path('createsize/', views.createsize, name='createsize'),
    path('config/', views.config, name='config'),
    path('update_config/', views.update_config, name='update_config'),
    path('product/', views.product, name='product'),
    path("product_detail/<int:id>", views.productDescription, name="productDescription"),
    path('sale/', views.sale, name='sale'),
    path('printInvoiceSale/<int:id>', views.printInvoiceSale, name='printInvoiceSale'),
    path('api/', views.api, name='api'),
    path('users/', views.create_user, name='users'),
]