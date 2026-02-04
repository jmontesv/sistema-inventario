from django import forms
from .models import Supplier, Product, StockMovement
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address', 'is_active']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'sku',
            'category',
            'supplier',
            'min_stock',
            'price',
            'is_active'
        ]


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reason']
        widgets = {
            'movement_type': forms.HiddenInput()
        }
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")
        movement_type = cleaned_data.get("movement_type")
    
        if movement_type == StockMovement.EXIT and quantity:
            if quantity > product.stock:
                raise ValidationError(
                    f"Stock insuficiente. Disponible: {product.stock}"
                )

        return cleaned_data
    

class ProductImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Archivo CSV",
        help_text="Sube un CSV con columnas: name, sku, category, supplier, price, stock"
    )

# Registro de usuario personalizado
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Correo electrónico válido")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")



