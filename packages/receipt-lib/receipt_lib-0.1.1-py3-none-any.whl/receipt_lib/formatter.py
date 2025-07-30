from datetime import datetime

def format_transaction_date(date_obj):
    return date_obj.strftime("%b %d %Y")

def generate_transaction_code(prefix="TXN"):
    now = datetime.now()
    return f"{prefix}{now.strftime('%Y%m%d%H%M%S')}"

def get_formatted_current_date():
    return format_transaction_date(datetime.now())
