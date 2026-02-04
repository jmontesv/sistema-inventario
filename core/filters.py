import django_filters
from .models import Product, Category, Supplier, StockMovement
from django.db import models
from django import forms

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Nombre'
    )
    sku = django_filters.CharFilter(
        field_name='sku',
        lookup_expr='icontains',
        label='SKU'
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Categoría'
    )
    supplier = django_filters.ModelChoiceFilter(
        queryset=Supplier.objects.all(),
        label='Proveedor'
    )
    low_stock = django_filters.BooleanFilter(
        method='filter_low_stock',
        label='Stock bajo'
    )

    class Meta:
        model = Product
        fields = []  # dejamos vacío porque definimos los filtros arriba

    def filter_low_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__lte=models.F('min_stock'))
        return queryset

# Filtro para movimientos de stock
class StockMovementFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name="created_at", 
        lookup_expr='gte', 
        label='Desde', 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-2 py-1'})
    )
    end_date = django_filters.DateFilter(
        field_name="created_at", 
        lookup_expr='lte', 
        label='Hasta', 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-2 py-1'})
    )
    
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'start_date', 'end_date']