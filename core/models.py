from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

# Create your models here.
class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creada"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre"
    )
    contact_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Persona de contacto"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Teléfono"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creado"
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Categoría"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Proveedor"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock actual"
    )
    min_stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock mínimo"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creado"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property # Indica si el stock está por debajo del mínimo
    def low_stock(self):
        return self.stock <= self.min_stock


class StockMovement(models.Model):

    ENTRY = 'IN'
    EXIT = 'OUT'

    MOVEMENT_TYPE_CHOICES = (
        (ENTRY, 'Entrada'),
        (EXIT, 'Salida'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='movements',
        verbose_name="Producto"
    )
    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPE_CHOICES,
        verbose_name="Tipo"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Cantidad"
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Motivo"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Usuario"
    )

    class Meta:
        verbose_name = "Movimiento de stock"
        verbose_name_plural = "Movimientos de stock"
        ordering = ['-created_at']
        
    
    def save(self, *args, **kwargs):
        """
        Actualiza el stock del producto al crear un movimiento.
        - ENTRY suma stock
        - EXIT resta stock (no permite stock negativo)
        """

        if not self.pk:
            if self.movement_type == self.ENTRY:
                self.product.stock += self.quantity

            elif self.movement_type == self.EXIT:
                if self.quantity > self.product.stock:
                    raise ValidationError(
                        f"No hay stock suficiente. Stock actual: {self.product.stock}"
                    )
                self.product.stock -= self.quantity

            self.product.save()

        super().save(*args, **kwargs)

        

    def __str__(self):
        # Método para mostrar una representación legible del movimiento de stock
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"