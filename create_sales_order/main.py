from input_data import *

import urllib3
import certifi
import json
import time
import ast


def create_new_sales_order(api_body, request_access_token):
    time.sleep(1)
    encoded_body = json.dumps(api_body)
    resp = http.request(
        "POST",
        "https://api.sosinventory.com/api/v2/salesorder/",
        headers={
            'Authorization': 'Bearer ' + request_access_token,
            'Host': 'api.sosinventory.com'
        },
        body=encoded_body
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    return json_object


def clean_purchased_products_list(item_purchased_products_list):
    item_purchased_products_list = "[" +item_purchased_products_list + "]"
    item_purchased_products_list = json.loads(item_purchased_products_list)
    return item_purchased_products_list

def get_drop_shipper_variables(is_drop_shipper, is_billing_information_specified, input_data, customer_default_address_name, customer_default_address_phone, email, customer_default_address_line1, customer_default_address_line2, customer_default_address_city, customer_default_address_province_code, customer_default_address_zip, customer_default_address_country_code):
    if is_drop_shipper == "true":
        billing_customer_default_address_name = input_data['billing_customer_default_address_name']
        billing_customer_default_address_phone = input_data['billing_customer_default_address_phone']
        billing_email = input_data['billing_email']
        billing_customer_default_address_line1 = input_data['billing_customer_default_address_line1']
        billing_customer_default_address_line2 = input_data['billing_customer_default_address_line2']
        if billing_customer_default_address_line2 == "null" or billing_customer_default_address_line2 == "" or billing_customer_default_address_line2 == '\"\"':
            billing_customer_default_address_line2 = None
        billing_customer_default_address_city = input_data['billing_customer_default_address_city']
        billing_customer_default_address_province_code = input_data['billing_customer_default_address_province_code']
        billing_customer_default_address_zip = input_data['billing_customer_default_address_zip']
        billing_customer_default_address_country_code = input_data['billing_customer_default_address_country_code']
        email = billing_email  # For dropshippers, the Shipping email comes from the dropshipper not the end customer
    else:
        if is_billing_information_specified == "true":
            billing_customer_default_address_name = input_data['billing_customer_default_address_name']
            billing_customer_default_address_phone = input_data['billing_customer_default_address_phone']
            billing_email = input_data['billing_email']
            billing_customer_default_address_line1 = input_data['billing_customer_default_address_line1']
            billing_customer_default_address_line2 = input_data['billing_customer_default_address_line2']
            if billing_customer_default_address_line2 == "null" or billing_customer_default_address_line2 == "" or billing_customer_default_address_line2 == '\"\"':
                billing_customer_default_address_line2 = None
            billing_customer_default_address_city = input_data['billing_customer_default_address_city']
            billing_customer_default_address_province_code = input_data[
                'billing_customer_default_address_province_code']
            billing_customer_default_address_zip = input_data['billing_customer_default_address_zip']
            billing_customer_default_address_country_code = input_data['billing_customer_default_address_country_code']
        else:
            billing_customer_default_address_name = customer_default_address_name
            billing_customer_default_address_phone = customer_default_address_phone
            billing_email = email
            billing_customer_default_address_line1 = customer_default_address_line1
            billing_customer_default_address_line2 = customer_default_address_line2
            billing_customer_default_address_city = customer_default_address_city
            billing_customer_default_address_province_code = customer_default_address_province_code
            billing_customer_default_address_zip = customer_default_address_zip
            billing_customer_default_address_country_code = customer_default_address_country_code

    return billing_customer_default_address_name, billing_customer_default_address_phone, billing_email, billing_customer_default_address_line1, billing_customer_default_address_line2, billing_customer_default_address_city, billing_customer_default_address_province_code, billing_customer_default_address_zip, billing_customer_default_address_country_code, email


access_token = input_data["access_token"]
updated_at = input_data["updated_at"]
name = input_data['name']
customer_default_address_name = input_data['customer_default_address_name']
subtotal_price = input_data['subtotal_price']
formatted_discount_text = -abs(float(input_data['formatted_discount_text']))
tax_percent = input_data['tax_percent']
taxable = input_data['taxable']
calculated_total = input_data['calculated_total']
payment_names = input_data['payment_names']
customer_default_address_province_code = input_data['customer_default_address_province_code']
customer_default_address_phone = input_data['customer_default_address_phone']
email = input_data['email']
customer_default_address_line1 = input_data['customer_default_address_line1']
customer_default_address_line2 = input_data['customer_default_address_line2']
if customer_default_address_line2 == "null" or customer_default_address_line2 == "" or customer_default_address_line2 == '\"\"':
    print("customer_default_address_line2 is null or empty")
    customer_default_address_line2 = None
customer_default_address_city = input_data['customer_default_address_city']
customer_default_address_zip = input_data['customer_default_address_zip']
customer_default_address_country_code = input_data['customer_default_address_country_code']
total_shipping_price_set_shop_money_amount = input_data['total_shipping_price_set_shop_money_amount']
purchased_products_list = clean_purchased_products_list(input_data['purchased_products_list'])
is_drop_shipper = input_data['is_drop_shipper']
is_billing_information_specified = input_data['is_billing_information_specified']

billing_customer_default_address_name, billing_customer_default_address_phone, billing_email, billing_customer_default_address_line1, billing_customer_default_address_line2, billing_customer_default_address_city, billing_customer_default_address_province_code, billing_customer_default_address_zip, billing_customer_default_address_country_code, email = get_drop_shipper_variables(is_drop_shipper, is_billing_information_specified, input_data, customer_default_address_name, customer_default_address_phone, email, customer_default_address_line1, customer_default_address_line2, customer_default_address_city, customer_default_address_province_code, customer_default_address_zip, customer_default_address_country_code)




connect_timeout = 10.0
read_timeout = 20.0
http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
)

def create_body(name, updated_at, payment_names, is_drop_shipper, total_shipping_price_set_shop_money_amount,
                purchased_products_list, taxable, tax_percent, calculated_total, formatted_discount_text,  subtotal_price,
                customer_default_address_name, billing_customer_default_address_name,
                customer_default_address_phone, billing_customer_default_address_phone,
                email, billing_email,
                customer_default_address_line1, billing_customer_default_address_line1,
                customer_default_address_line2, billing_customer_default_address_line2,
                customer_default_address_city, billing_customer_default_address_city,
                customer_default_address_province_code, billing_customer_default_address_province_code,
                customer_default_address_zip, billing_customer_default_address_zip,
                customer_default_address_country_code, billing_customer_default_address_country_code):
    body = {
        "starred": 0,
        "syncToken": 0,
        "number": "auto",
        "date": updated_at,
        "customer": {
            "name": billing_customer_default_address_name
        },
        "location": {
            "id": 1,
            "name": ""
        },
        "billing": {
            "company": None,
            "contact": billing_customer_default_address_name,
            "phone": billing_customer_default_address_phone,
            "email": billing_email,
            "addressName": "",
            "addressType": "",
            "address": {
                "line1": billing_customer_default_address_line1,
                "line2": billing_customer_default_address_line2,
                "line3": None,
                "line4": None,
                "line5": None,
                "city": billing_customer_default_address_city,
                "stateProvince": billing_customer_default_address_province_code,
                "postalCode": billing_customer_default_address_zip,
                "country": billing_customer_default_address_country_code
            }
        },
        "shipping": {
            "company": None,
            "contact": customer_default_address_name,
            "phone": customer_default_address_phone,
            "email": email,
            "addressName": "",
            "addressType": "",
            "address": {
                "line1": customer_default_address_line1,
                "line2": customer_default_address_line2,
                "line3": None,
                "line4": None,
                "line5": None,
                "city": customer_default_address_city,
                "stateProvince": customer_default_address_province_code,
                "postalCode": customer_default_address_zip,
                "country": customer_default_address_country_code
            }
        },
        "terms": {
            "name": payment_names
        },
        "salesRep": None,
        "channel": None,
        "department": None,
        "priority": None,
        "assignedToUser": None,
        "orderStage": {
            "id": 1,
            "name": "Processing"
        },
        "currency": {
            "id": 42,
            "name": "USD"
        },
        "serial": None,
        "linkedTransaction": None,
        "linkedInvoices": [

        ],
        "linkedShipments": [
        ],
        "exchangeRate": 1.0,
        "customerMessage": None,
        "statusMessage": None,
        "comment": "Porcupine: " + customer_default_address_name + ", PO#: " + name,
        "customerNotes": "",
        "customFields": [
            {
                "id": 14,
                "name": "In Stock Date",
                "value": None,
                "dataType": "Text"
            },
            {
                "id": 12,
                "name": "Manufacturing Date",
                "value": None,
                "dataType": "Date"
            },
            {
                "id": 13,
                "name": "SO Printed",
                "value": False,
                "dataType": "Boolean"
            }
        ],
        "customerPO": name,
        "depositPercent": 0.00000,
        "depositAmount": 0.00000,
        "subTotal": subtotal_price,
        "discountPercent": 0.00000,
        "discountAmount": formatted_discount_text,
        "taxPercent": tax_percent,
        "taxAmount": 0.00,
        "shippingAmount": total_shipping_price_set_shop_money_amount,
        "total": calculated_total,
        "discountTaxable": taxable,
        "shippingTaxable": False,
        "dropShip": False,
        "closed": False,
        "archived": False,
        "summaryOnly": False,
        "hasSignature": False,
        "keys": None,
        "values": None,
        "lines": purchased_products_list
    }
    return body


body = create_body(name, updated_at, payment_names, is_drop_shipper, total_shipping_price_set_shop_money_amount,
                purchased_products_list, taxable, tax_percent, calculated_total, formatted_discount_text,  subtotal_price,
                customer_default_address_name, billing_customer_default_address_name,
                customer_default_address_phone, billing_customer_default_address_phone,
                email, billing_email,
                customer_default_address_line1, billing_customer_default_address_line1,
                customer_default_address_line2, billing_customer_default_address_line2,
                customer_default_address_city, billing_customer_default_address_city,
                customer_default_address_province_code, billing_customer_default_address_province_code,
                customer_default_address_zip, billing_customer_default_address_zip,
                customer_default_address_country_code, billing_customer_default_address_country_code)
print("body:", body)
create_sales_order_json = create_new_sales_order(body,access_token)
output = [{'create_sales_order_json': create_sales_order_json}]
