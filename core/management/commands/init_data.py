from django.core.management.base import BaseCommand
from core.models import Category, Supplier, Product

class Command(BaseCommand):
    help = 'Carga datos iniciales de ejemplo'

    def handle(self, *args, **options):
        
        # ========================
        # CATEGORÍAS
        # ========================
        self.stdout.write('Creando categorías...')
        categorias_data = [
            {
                'name': 'Electrónica',
                'description': 'Dispositivos electrónicos y accesorios'
            },
            {
                'name': 'Oficina',
                'description': 'Material y suministros de oficina'
            },
            {
                'name': 'Herramientas',
                'description': 'Herramientas manuales y eléctricas'
            },
            {
                'name': 'Informática',
                'description': 'Componentes y accesorios informáticos'
            },
            {
                'name': 'Mobiliario',
                'description': 'Muebles y equipamiento'
            },
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categorias[cat_data['name']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Categoría "{cat.name}" creada'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Categoría "{cat.name}" ya existe'))

        # ========================
        # PROVEEDORES
        # ========================
        self.stdout.write('\nCreando proveedores...')
        proveedores_data = [
            {
                'name': 'TechSupply S.L.',
                'contact_name': 'Carlos Martínez',
                'email': 'info@techsupply.es',
                'phone': '+34 910 123 456',
                'address': 'Calle Mayor 15, Madrid'
            },
            {
                'name': 'Oficina Total',
                'contact_name': 'Ana García',
                'email': 'ventas@oficinatotal.es',
                'phone': '+34 915 234 567',
                'address': 'Av. Diagonal 200, Barcelona'
            },
            {
                'name': 'Herramientas Pro',
                'contact_name': 'Miguel Ruiz',
                'email': 'contacto@herramientaspro.es',
                'phone': '+34 963 345 678',
                'address': 'Polígono Industrial Norte, Valencia'
            },
            {
                'name': 'InfoComponents',
                'contact_name': 'Laura Sánchez',
                'email': 'info@infocomponents.es',
                'phone': '+34 954 456 789',
                'address': 'Calle Sierpes 42, Sevilla'
            },
        ]
        
        proveedores = {}
        for prov_data in proveedores_data:
            prov, created = Supplier.objects.get_or_create(
                name=prov_data['name'],
                defaults={
                    'contact_name': prov_data['contact_name'],
                    'email': prov_data['email'],
                    'phone': prov_data['phone'],
                    'address': prov_data['address']
                }
            )
            proveedores[prov_data['name']] = prov
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Proveedor "{prov.name}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Proveedor "{prov.name}" ya existe'))

        # ========================
        # PRODUCTOS
        # ========================
        self.stdout.write('\nCreando productos...')
        productos_data = [
            # Electrónica
            {
                'name': 'Monitor LED 24"',
                'sku': 'MON-LED-24',
                'category': 'Electrónica',
                'supplier': 'TechSupply S.L.',
                'stock': 15,
                'min_stock': 5,
                'price': 189.99
            },
            {
                'name': 'Teclado Mecánico RGB',
                'sku': 'TEC-MEC-RGB',
                'category': 'Electrónica',
                'supplier': 'TechSupply S.L.',
                'stock': 30,
                'min_stock': 10,
                'price': 79.99
            },
            {
                'name': 'Ratón Inalámbrico',
                'sku': 'RAT-INAL-001',
                'category': 'Electrónica',
                'supplier': 'TechSupply S.L.',
                'stock': 45,
                'min_stock': 15,
                'price': 24.99
            },
            
            # Oficina
            {
                'name': 'Papel A4 (500 hojas)',
                'sku': 'PAP-A4-500',
                'category': 'Oficina',
                'supplier': 'Oficina Total',
                'stock': 200,
                'min_stock': 50,
                'price': 4.99
            },
            {
                'name': 'Bolígrafos Azul (Caja 50 uds)',
                'sku': 'BOL-AZ-50',
                'category': 'Oficina',
                'supplier': 'Oficina Total',
                'stock': 25,
                'min_stock': 10,
                'price': 12.50
            },
            {
                'name': 'Carpetas Archivador',
                'sku': 'CAR-ARC-001',
                'category': 'Oficina',
                'supplier': 'Oficina Total',
                'stock': 60,
                'min_stock': 20,
                'price': 2.99
            },
            
            # Herramientas
            {
                'name': 'Taladro Eléctrico 500W',
                'sku': 'TAL-ELEC-500',
                'category': 'Herramientas',
                'supplier': 'Herramientas Pro',
                'stock': 8,
                'min_stock': 3,
                'price': 89.99
            },
            {
                'name': 'Set Destornilladores (12 piezas)',
                'sku': 'SET-DEST-12',
                'category': 'Herramientas',
                'supplier': 'Herramientas Pro',
                'stock': 20,
                'min_stock': 5,
                'price': 34.99
            },
            {
                'name': 'Caja Herramientas Metálica',
                'sku': 'CAJ-HER-MET',
                'category': 'Herramientas',
                'supplier': 'Herramientas Pro',
                'stock': 12,
                'min_stock': 4,
                'price': 45.00
            },
            
            # Informática
            {
                'name': 'Disco Duro SSD 500GB',
                'sku': 'SSD-500GB-001',
                'category': 'Informática',
                'supplier': 'InfoComponents',
                'stock': 25,
                'min_stock': 10,
                'price': 59.99
            },
            {
                'name': 'Memoria RAM DDR4 8GB',
                'sku': 'RAM-DDR4-8GB',
                'category': 'Informática',
                'supplier': 'InfoComponents',
                'stock': 40,
                'min_stock': 15,
                'price': 39.99
            },
            {
                'name': 'Cable HDMI 2m',
                'sku': 'CAB-HDMI-2M',
                'category': 'Informática',
                'supplier': 'InfoComponents',
                'stock': 100,
                'min_stock': 30,
                'price': 9.99
            },
            
            # Mobiliario
            {
                'name': 'Silla Oficina Ergonómica',
                'sku': 'SIL-OFI-ERG',
                'category': 'Mobiliario',
                'supplier': 'Oficina Total',
                'stock': 5,
                'min_stock': 2,
                'price': 159.99
            },
            {
                'name': 'Escritorio 120x60cm',
                'sku': 'ESC-120-60',
                'category': 'Mobiliario',
                'supplier': 'Oficina Total',
                'stock': 3,
                'min_stock': 1,
                'price': 249.99
            },
            {
                'name': 'Lámpara LED Escritorio',
                'sku': 'LAM-LED-ESC',
                'category': 'Mobiliario',
                'supplier': 'TechSupply S.L.',
                'stock': 18,
                'min_stock': 5,
                'price': 29.99
            },
        ]
        
        for prod_data in productos_data:
            producto, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults={
                    'name': prod_data['name'],
                    'category': categorias[prod_data['category']],
                    'supplier': proveedores[prod_data['supplier']],
                    'stock': prod_data['stock'],
                    'min_stock': prod_data['min_stock'],
                    'price': prod_data['price']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✅ Producto "{producto.name}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Producto "{producto.name}" ya existe'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Datos iniciales cargados correctamente'))
        self.stdout.write(f'📊 Total: {Category.objects.count()} categorías, {Supplier.objects.count()} proveedores, {Product.objects.count()} productos')