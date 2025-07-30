# myreceiptutils/formatter.py

from datetime import datetime

def format_transaction_date(date_obj):
    return date_obj.strftime("%b %d %Y")  # Ex: "Jul 16 2025"

def generate_transaction_code(prefix="TXN"):
    now = datetime.now()
    return f"{prefix}{now.strftime('%Y%m%d%H%M%S')}"
