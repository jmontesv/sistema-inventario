from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin  
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .models import Category, Supplier, Product, StockMovement
from django.db.models import Count
from .forms import SupplierForm, ProductForm, StockMovementForm, ProductImportForm
from django.shortcuts import render, redirect
from .filters import ProductFilter, StockMovementFilter
from django.db import models
from django.db.models import Sum, F
import csv
from django.contrib import messages
from django.http import StreamingHttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group



# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Número de productos, categorías y proveedores
        context["total_products"] = Product.objects.count()
        context["total_categories"] = Category.objects.count()
        context["total_suppliers"] = Supplier.objects.count()
        
        # Número de productos con stock bajo
        context["low_stock_count"] = Product.objects.filter(stock__lte=models.F('min_stock')).count()
        
        # Conteo de productos por categoría
        categories = Product.objects.values_list('category__name', flat=True)
        context['category_labels'] = list(set(categories))
        context['category_counts'] = [Product.objects.filter(category__name=c).count() for c in context['category_labels']]

        # Suma total de entradas y salidas
        total_entries = StockMovement.objects.filter(movement_type=StockMovement.ENTRY)\
                        .aggregate(total=Sum('quantity'))['total'] or 0
        total_exits = StockMovement.objects.filter(movement_type=StockMovement.EXIT)\
                        .aggregate(total=Sum('quantity'))['total'] or 0

        context['entries_total'] = total_entries
        context['exits_total'] = total_exits

        # Valor total del inventario: stock * precio por producto
        valor_inventario = Product.objects.aggregate(
            total=Sum(F('stock') * F('price'))
        )['total'] or 0

        context['valor_inventario'] = valor_inventario
        
        return context


# Listar todas las categorías
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return (
            Category.objects
            .annotate(product_count=Count('products'))
            .order_by('name')
        )

# Crear nueva categoría
class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    template_name = 'categories/category_form.html'
    fields = ['name', 'description', 'is_active']
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.add_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('category_list')
        context["title"] = "Nueva categoría"
        return context
    
    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Editar categoría existente
class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'categories/category_form.html'
    fields = ['name', 'description', 'is_active']
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.change_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('category_list')
        context["title"] = "Editar categoría"
        return context
    
    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Eliminar categoría
class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.delete_category'

    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Listar todos los proveedores
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/supplier_list.html'
    context_object_name = 'suppliers'

    # Perosnalizar el queryset para incluir el conteo de productos
    def get_queryset(self):
        return (
            Supplier.objects
            .annotate(product_count=Count('products'))
            .order_by('name')
        )
    
# Crear proveedores
class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.add_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('supplier_list')
        context["title"] = "Nuevo proveedor"
        return context

    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Editar proveedores
class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplier_form.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.change_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('supplier_list')
        context["title"] = "Editar proveedor"
        return context
    
    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)
    

# Eliminar proveedores
class SupplierDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/supplier_confirm_delete.html'
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.delete_supplier'   

    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Lista de productos
class ProductListView(LoginRequiredMixin,FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        querydict = self.request.GET.copy()
        querydict.pop('page', None)

        context['querystring'] = querydict.urlencode()
        return context


# Crear productos
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('product_list')
        context["title"] = "Nuevo producto"
        return context
    
    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Editar productos
class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.change_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('product_list')
        context["title"] = "Editar producto"
        return context
    
    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)

# Eliminar productos
class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'

    def handle_no_permission(self):
        # Redirige a login si no está logueado
        if not self.request.user.is_authenticated:
            return redirect('login')  

        # Cargar un template custom si está logueado pero sin permisos
        return render(self.request, '403_custom.html', status=403)


# Listar movimientos de stock
class MovementListView(LoginRequiredMixin, FilterView, ListView):
    model = StockMovement
    filterset_class = StockMovementFilter
    template_name = 'movements/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        querydict = self.request.GET.copy()
        querydict.pop('page', None)

        context['querystring'] = querydict.urlencode()
        return context


# Crear entrada de stock para un producto específico
class MovementCreateEntryView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'movements/movement_form.html'

    def get_initial(self):
        return {
            'product': Product.objects.get(pk=self.kwargs['pk']),
            'movement_type': StockMovement.ENTRY
        }

    def form_valid(self, form):
        # Asignar producto, tipo y usuario
        form.instance.product = Product.objects.get(pk=self.kwargs['pk'])
        form.instance.movement_type = StockMovement.ENTRY
        form.instance.user = self.request.user

        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('product_list')
        context['title'] = 'Nuevo movimiento de entrada'
        return context

    def get_success_url(self):
        return reverse_lazy('product_list')

# Crear salida de stock para un producto específico
class MovementCreateExitView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'movements/movement_form.html'

    def get_initial(self):
        return {
            'product': Product.objects.get(pk=self.kwargs['pk']),
            'movement_type': StockMovement.EXIT
        }

    def form_valid(self, form):
        # Asignar producto, tipo y usuario
        form.instance.product = Product.objects.get(pk=self.kwargs['pk'])
        form.instance.movement_type = StockMovement.EXIT
        form.instance.user = self.request.user

        response = super().form_valid(form)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('product_list')
        context['title'] = 'Nuevo movimiento de salida'
        return context

    def get_success_url(self):
        return reverse_lazy('product_list')

# Importar productos desde CSV
@login_required
@permission_required('products.add_product', raise_exception=True)
def import_products(request):
    if request.method == "POST":
        form = ProductImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            added_count = 0
            errors = []

            for i, row in enumerate(reader, start=2):  # start=2 para contar encabezado
                try:
                    # Obtenemos o creamos categoría y proveedor
                    category, _ = Category.objects.get_or_create(name=row['category'])
                    supplier, _ = Supplier.objects.get_or_create(name=row['supplier'])

                    # Creamos o actualizamos producto
                    product, created = Product.objects.update_or_create(
                        sku=row['sku'],
                        defaults={
                            'name': row['name'],
                            'category': category,
                            'supplier': supplier,
                            'price': float(row['price']),
                            'stock': int(row['stock'])
                        }
                    )
                    added_count += 1

                except Exception as e:
                    errors.append(f"Fila {i}: {e}")

            messages.success(request, f"{added_count} productos importados correctamente.")
            if errors:
                messages.error(request, f"Errores:\n" + "\n".join(errors))

            return redirect('product_list')
    else:
        form = ProductImportForm()

    return render(request, 'products/import_products.html', {'form': form})

# Exportar productos a CSV
def export_products(request):
    # Aplicamos los mismos filtros que en la lista
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    queryset = product_filter.qs

    def rows():
        yield ['Nombre', 'SKU', 'Categoría', 'Proveedor', 'Stock', 'Precio']

        for p in queryset.select_related('category', 'supplier'):
            yield [
                p.name,
                p.sku,
                p.category.name if p.category else '',
                p.supplier.name if p.supplier else '',
                p.stock,
                p.price,
            ]

    response = StreamingHttpResponse(
        (','.join(map(str, row)) + '\n' for row in rows()),
        content_type="text/csv"
    )
    response['Content-Disposition'] = 'attachment; filename=productos.csv'
    return response

# Exportar movimientos de stock a CSV
def export_movements(request):
    movement_filter = StockMovementFilter(
        request.GET,
        queryset=StockMovement.objects.select_related(
            'product', 'product__category', 'created_by'
        )
    )

    queryset = movement_filter.qs.order_by('-created_at')

    def rows():
        yield [
            'Fecha',
            'Producto',
            'Categoría',
            'Tipo',
            'Cantidad',
            'Usuario'
        ]

        for m in queryset:
            yield [
                m.created_at.strftime('%Y-%m-%d %H:%M'),
                m.product.name,
                m.product.category.name if m.product.category else '',
                'Entrada' if m.movement_type == m.ENTRY else 'Salida',
                m.quantity,
                m.created_by.username if m.created_by else '',
            ]

    response = StreamingHttpResponse(
        (','.join(map(str, row)) + '\n' for row in rows()),
        content_type='text/csv'
    )
    response['Content-Disposition'] = 'attachment; filename=movimientos_stock.csv'

    return response

# Registro de usuario personalizado
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            empleado_group = Group.objects.get(name='Empleado')
            user.groups.add(empleado_group)

            messages.success(request, f"Usuario {user.username} registrado correctamente.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})