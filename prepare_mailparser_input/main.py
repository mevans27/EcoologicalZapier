from input_data import *

import re
import urllib3
import certifi
import json
import time

table_of_items_ordered = input_data["items_ordered"]
access_token = input_data["access_token"]
is_drop_shipper = input_data["is_drop_shipper"]


# noinspection DuplicatedCode
def grab_sku_object_from_sos(http, item_sku, token):
    time.sleep(1)
    resp = http.request(
        "GET",
        "https://api.sosinventory.com/api/v2/item?start=0&maxresults=1&sku=" + item_sku,
        headers={
            'Authorization': 'Bearer ' + token,
            'Host': 'api.sosinventory.com'
        },
        retries=5
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    print("grabSkuObjectFromSos json return:")
    print(json_object)
    if json_object['count'] == 0:
        message = "SKU: " + item_sku + ", not found in SOS Inventory, please add it and re-run this Zap using the order JSON backed up in Zapier: https://tables.zapier.com/app/tables/t/01H2E4ZS8BE994ESEC8S7BMDSS. Submission link: https://form-8b1992.zapier.app/"
        print(message)
        raise TypeError(message)
    return json_object


def get_sku_table(items_ordered):
    items_sku_table = re.findall(r"(?<=SKU: ).+(?=, QTY:)", items_ordered, re.IGNORECASE)
    return items_sku_table


def get_qty_table(items_ordered):
    items_qty_table = re.findall(r"(?<=QTY: )\d+(?=,)", items_ordered, re.IGNORECASE)
    return items_qty_table


def get_price_table(items_ordered, http_object, token):
    price_table_array = []
    for line in items_ordered.splitlines():
        print("line", line)
        if re.search(r"Price: ", line):
            price = re.search(r'Price: (.*?),', line, re.IGNORECASE).group(1)
            price_table_array.append(price)
        else:
            sku = re.search(r"(?<=SKU: ).+(?=, QTY:)", line, re.IGNORECASE).group().strip()
            sku_object = grab_sku_object_from_sos(http_object, sku, token)
            sales_price = str(sku_object['data'][0]['salesPrice'])
            price_table_array.append(sales_price)

    return price_table_array


def get_vendor_table(http_object, token, items_sku_table):
    vendor_array = []
    for sku in items_sku_table:
        sku_object = grab_sku_object_from_sos(http_object, sku, token)
        is_vendor = str(sku_object['data'][0]['vendor'])
        if is_vendor == "None":
            vendor = "Ecoological"
        else:
            vendor = str(sku_object['data'][0]['vendor']['name'])
        vendor_array.append(vendor)

    return vendor_array


def get_total_discounted_price(item_is_drop_shipper, item_price_table, item_qty_table):
    item_total_price = 0
    for i in range(len(item_price_table)):
        item_total_price += float(item_price_table[i]) * int(item_qty_table[i])
    print("item_total_price:", item_total_price)
    if item_is_drop_shipper == "true":
        discount = 0.6
    else:
        discount = 1

    discounted_total_price = round(item_total_price * discount, 2)
    return discounted_total_price


# noinspection DuplicatedCode
def correct_plus_sign_skus(items_table):
    input_array = items_table.split('\n')
    final_ordered_items_table_string = ""
    for i in range(len(input_array)):
        row = input_array[i]
        print("Row:" + row)
        if "+" in row:
            qty = re.search(r'(?<=QTY: )\d+(?=,)', row, re.IGNORECASE).group().strip()
            sku1 = re.search(r'(?<=SKU: )(.*)(?=\+)', row).group().strip()
            sku2 = re.search(r'(?<=\+)(.*)(?=, QTY:)', row, re.IGNORECASE).group().strip()
            final_ordered_items_table_string += f"SKU: {sku1}, QTY: {qty},\n"
            final_ordered_items_table_string += f"SKU: {sku2}, QTY: {qty},"
        elif row is None or row == "" or row == "\n" or row == " " or row == "\t" or row == "\r":
            print("found empty row, ignoring")
            continue
        else:
            final_ordered_items_table_string += row
        if i < len(input_array) - 1:
            final_ordered_items_table_string += "\n"
    return final_ordered_items_table_string


connect_timeout = 10.0
read_timeout = 20.0
http_instance = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
)

# Find and replace ", SKU" or ",SKU" in table_of_items_ordered with ",\nSKU" ignoring case

table_of_items_ordered = re.sub(r',.?SKU', ',\nSKU', table_of_items_ordered, re.IGNORECASE)

print("table_of_items_ordered:\n", table_of_items_ordered)

table_of_items_ordered = correct_plus_sign_skus(table_of_items_ordered)
sku_table = get_sku_table(table_of_items_ordered)
price_table = get_price_table(table_of_items_ordered, http_instance, access_token)
vendor_table = get_vendor_table(http_instance, access_token, sku_table)
qty_table = get_qty_table(table_of_items_ordered)
order_total_price = get_total_discounted_price(is_drop_shipper, price_table, qty_table)

items_sku_string = ",".join(sku_table)
print("items_sku_string:\n", items_sku_string)

items_qty_string = ",".join(qty_table)
print("items_qty_string:\n", items_qty_string)

items_price_string = ",".join(price_table)
print("items_price_string:\n", items_price_string)

items_vendor_string = ",".join(vendor_table)
print("items_vendor_string:\n", items_vendor_string)

print("order_total_price:", order_total_price)

output = [{'sku_table': items_sku_string, 'qty_table': items_qty_string, 'price_table': items_price_string,
           'vendor_table': items_vendor_string, 'order_total_price': order_total_price}]
