from input_data import input_data

for key in input_data:
    if input_data[key] is None or input_data[key] == '\"\"':
        input_data[key] = ""
    input_data[key] = ''.join(i for i in input_data[key] if i not in '"')

received_at = input_data["received_at"]
date = input_data["date"]
time = input_data["time"]
purchase_order = input_data["purchase_order"]
discount = input_data["discount"]
notes = input_data["notes"]
table_of_items_ordered = input_data["table_of_items_ordered"]
billing_customer_name = input_data["billing_customer_name"]
billing_address_line1 = input_data["billing_address_line1"]
billing_address_line2 = input_data["billing_address_line2"]
billing_address_city = input_data["billing_address_city"]
billing_address_state_or_province = input_data["billing_address_state_or_province"]
billing_address_postal_code = input_data["billing_address_postal_code"]
billing_address_country = input_data["billing_address_country"]
billing_address_email_address = input_data["billing_address_email_address"]
billing_address_phone = input_data["billing_address_phone"]
shipping_customer_name = input_data["shipping_customer_name"]
shipping_address_line1 = input_data["shipping_address_line1"]
shipping_address_line2 = input_data["shipping_address_line2"]
shipping_address_city = input_data["shipping_address_city"]
shipping_address_state_or_province = input_data["shipping_address_state_or_province"]
shipping_address_postal_code = input_data["shipping_address_postal_code"]
shipping_address_country = input_data["shipping_address_country"]
shipping_address_email_address = input_data["shipping_address_email_address"]
shipping_address_phone = input_data["shipping_address_phone"]
tax = input_data["tax"]
shipping_amount = input_data["shipping_amount"]

print(billing_address_line2)

output = [
    {'received_at': received_at, 'date': date, 'time': time, 'purchase_order': purchase_order, 'discount': discount,
     'notes': notes, 'table_of_items_ordered': table_of_items_ordered, 'billing_customer_name': billing_customer_name,
     'billing_address_line1': billing_address_line1, 'billing_address_line2': billing_address_line2,
     'billing_address_city': billing_address_city,
     'billing_address_state_or_province': billing_address_state_or_province,
     'billing_address_postal_code': billing_address_postal_code, 'billing_address_country': billing_address_country,
     'billing_address_email_address': billing_address_email_address, 'billing_address_phone': billing_address_phone,
     'shipping_customer_name': shipping_customer_name, 'shipping_address_line1': shipping_address_line1,
     'shipping_address_line2': shipping_address_line2, 'shipping_address_city': shipping_address_city,
     'shipping_address_state_or_province': shipping_address_state_or_province,
     'shipping_address_postal_code': shipping_address_postal_code, 'shipping_address_country': shipping_address_country,
     'shipping_address_email_address': shipping_address_email_address,
     'shipping_address_phone': shipping_address_phone, 'tax': tax, 'shipping_amount': shipping_amount}]
