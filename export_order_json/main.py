from input_data import *
import json

name = input_data['name']
customer_default_address_name = input_data['customer_default_address_name']
total_price = input_data['total_price']
subtotal_price = input_data['subtotal_price']
total_discounts = input_data['total_discounts']
total_tax = input_data['total_tax']
updated_at = input_data['updated_at']
line_items_sku = input_data['line_items_sku']
line_items_quantity = input_data['line_items_quantity']
line_items_vendor = input_data['line_items_vendor']
line_items_price = input_data['line_items_price']
payment_gateway_names = input_data['payment_gateway_names']
customer_default_address_province_code = input_data['customer_default_address_province_code']
customer_default_address_phone = input_data['customer_default_address_phone']
email = input_data['email']
customer_default_address_address1 = input_data['customer_default_address_address1']
customer_default_address_address2 = input_data['customer_default_address_address2']
customer_default_address_city = input_data['customer_default_address_city']
customer_default_address_zip = input_data['customer_default_address_zip']
customer_default_address_country_code = input_data['customer_default_address_country_code']
total_shipping_price_set_shop_money_amount = input_data['total_shipping_price_set_shop_money_amount']

json_object = {
  "name": name,
  "customer_default_address_name": customer_default_address_name,
  "total_price": total_price,
  "subtotal_price": subtotal_price,
  "total_discounts": total_discounts,
  "total_tax": total_tax,
  "updated_at": updated_at,
  "line_items_sku": line_items_sku,
  "line_items_quantity": line_items_quantity,
  "line_items_vendor": line_items_vendor,
  "line_items_price": line_items_price,
  "payment_gateway_names": payment_gateway_names,
  "customer_default_address_province_code": customer_default_address_province_code,
  "customer_default_address_phone": customer_default_address_phone,
  "email": email,
  "customer_default_address_address1": customer_default_address_address1,
  "customer_default_address_address2": customer_default_address_address2,
  "customer_default_address_city": customer_default_address_city,
  "customer_default_address_zip": customer_default_address_zip,
  "customer_default_address_country_code": customer_default_address_country_code,
  "total_shipping_price_set_shop_money_amount": total_shipping_price_set_shop_money_amount
}
json_data = json.dumps(json_object)
print(json_data)
output = [{'order_json_export': json_data}]
