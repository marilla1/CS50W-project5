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
    path('sale/', views.sale, name='sale'),
]