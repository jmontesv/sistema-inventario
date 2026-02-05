from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Product, Category, Supplier, StockMovement

class Command(BaseCommand):
    help = 'Inicializa grupos y permisos'

    def handle(self, *args, **options):
        # Crear grupos
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Grupo "Admin" creado'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Grupo "Admin" ya existe'))
            
        employee_group, created = Group.objects.get_or_create(name='Empleado')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Grupo "Empleado" creado'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Grupo "Empleado" ya existe'))

        # ---------------------------
        # Permisos para Admin (todos)
        # ---------------------------
        models_admin = [Product, Category, Supplier, StockMovement]
        for model in models_admin:
            content_type = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=content_type)
            for perm in perms:
                admin_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('✅ Permisos de Admin asignados'))

        # ---------------------------
        # Permisos para Empleado
        # ---------------------------
        perms_employee = []

        # Productos, Categorías, Proveedores → solo view
        for model in [Product, Category, Supplier]:
            ct = ContentType.objects.get_for_model(model)
            view_perm = Permission.objects.get(
                codename=f'view_{model._meta.model_name}', 
                content_type=ct
            )
            perms_employee.append(view_perm)

        # Movimientos → view y add
        ct_mov = ContentType.objects.get_for_model(StockMovement)
        perms_employee.append(
            Permission.objects.get(codename='view_stockmovement', content_type=ct_mov)
        )
        perms_employee.append(
            Permission.objects.get(codename='add_stockmovement', content_type=ct_mov)
        )

        # Asignar permisos al grupo Empleado
        for perm in perms_employee:
            employee_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('✅ Permisos de Empleado asignados'))
        self.stdout.write(self.style.SUCCESS('🎉 Grupos y permisos configurados correctamente'))