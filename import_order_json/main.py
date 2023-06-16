from input_data import *

from urllib.request import urlopen
import json

url = input_data["url"]

with urlopen(url) as file:
    content = file.read().decode()

print("content before replace", content)

content = content.replace('\\\"', "")

print("content after replace", content)

json_object = json.loads(content)

name = json_object["name"]
customer_default_address_name = json_object["customer_default_address_name"]
total_price = json_object["total_price"]
subtotal_price = json_object["subtotal_price"]
total_discounts = json_object["total_discounts"]
total_tax = json_object["total_tax"]
updated_at = json_object["updated_at"]
line_items_sku = json_object["line_items_sku"]
line_items_quantity = json_object["line_items_quantity"]
line_items_vendor = json_object["line_items_vendor"]
line_items_price = json_object["line_items_price"]
payment_gateway_names = json_object["payment_gateway_names"]
customer_default_address_province_code = json_object["customer_default_address_province_code"]
customer_default_address_phone = json_object["customer_default_address_phone"]
email = json_object["email"]
customer_default_address_address1 = json_object["customer_default_address_address1"]
customer_default_address_address2 = json_object["customer_default_address_address2"]
customer_default_address_city = json_object["customer_default_address_city"]
customer_default_address_zip = json_object["customer_default_address_zip"]
customer_default_address_country_code = json_object["customer_default_address_country_code"]
total_shipping_price_set_shop_money_amount = json_object["total_shipping_price_set_shop_money_amount"]

output = [{'name': name, 'customer_default_address_name': customer_default_address_name, 'total_price': total_price, 'subtotal_price': subtotal_price, 'total_discounts': total_discounts, 'total_tax': total_tax, 'updated_at': updated_at, 'line_items_sku': line_items_sku, 'line_items_quantity': line_items_quantity, 'line_items_vendor': line_items_vendor, 'line_items_price': line_items_price, 'payment_gateway_names': payment_gateway_names, 'customer_default_address_province_code': customer_default_address_province_code, 'customer_default_address_phone': customer_default_address_phone, 'email': email, 'customer_default_address_address1': customer_default_address_address1, 'customer_default_address_address2': customer_default_address_address2, 'customer_default_address_city': customer_default_address_city, 'customer_default_address_zip': customer_default_address_zip, 'customer_default_address_country_code': customer_default_address_country_code, 'total_shipping_price_set_shop_money_amount': total_shipping_price_set_shop_money_amount}]
