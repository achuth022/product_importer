
from celery import shared_task
import csv
from .models import Product

@shared_task(bind=True)
def import_products_task(self, file_path):
    """
    Celery task to import products from a CSV file in the background.
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        total_rows = len(rows)

        for index, row in enumerate(rows, start=1):
            sku = row.get('SKU')
            name = row.get('Name')
            description = row.get('Description', '')
            price = row.get('Price', 0)

                                              # Ensure price is float
            try:
                price = float(price)
            except (TypeError, ValueError):
                price = 0

                                                # Update or create product
            Product.objects.update_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': description,
                    'price': price,
                }
            )

                                                  # Update task progress
            self.update_state(
                state='PROGRESS',
                meta={
                    'current': index,
                    'total': total_rows,
                    'percent': int(index / total_rows * 100)
                }
            )

    return {'current': total_rows, 'total': total_rows, 'percent': 100, 'status': 'Task completed!'}
