
import requests
import json

def send_product_webhook(product, event_type="created"):
    """
    Sends product data to a webhook URL
    """
    webhook_url = "https://webhook.site/d8525845-46df-4b12-88f0-ad30ca1a2e7f"  # replace with your webhook URL
    payload = {
        "event": event_type,
        "product": {
            "sku": product.sku,
            "name": product.name,
            "description": product.description,
            "price":  float(product.price),
            "active": product.active,
        }
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Webhook sent successfully: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook: {e}")
