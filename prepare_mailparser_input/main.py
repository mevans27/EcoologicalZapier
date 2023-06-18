from input_data import *
import re
import urllib3
import certifi
import json
import time

table_of_items_ordered = input_data["items_ordered"]
access_token = input_data["access_token"]


# noinspection DuplicatedCode
def grab_sku_object_from_sos(http, item_sku, token):
    time.sleep(1)
    resp = http.request(
        "GET",
        "https://api.sosinventory.com/api/v2/item?start=0&maxresults=1&query=" + item_sku,
        headers={
            'Authorization': 'Bearer ' + token,
            'Host': 'api.sosinventory.com'
        },
        retries=5
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    print("grabSkuObjectFromSos json return:")
    print(json_object)
    return json_object


def get_sku_table(items_ordered):
    items_sku_table = re.findall(r"(?<=SKU: ).+(?=, QTY:)", items_ordered)
    return items_sku_table


def get_qty_table(items_ordered):
    items_qty_table = re.findall(r"(?<=QTY: )\d+(?=,)", items_ordered)
    return items_qty_table


def get_price_and_vendor_tables(http_object, token, items_sku_table):
    price_table_array = []
    vendor_array = []
    for sku in items_sku_table:
        sku_object = grab_sku_object_from_sos(http_object, sku, token)
        sales_price = str(sku_object['data'][0]['salesPrice'])
        price_table_array.append(sales_price)
        is_vendor = str(sku_object['data'][0]['vendor'])
        if is_vendor == "None":
            vendor = "Ecoological"
        else:
            vendor = str(sku_object['data'][0]['vendor']['name'])
        vendor_array.append(vendor)

    return price_table_array, vendor_array


def get_total_discounted_price(item_price_table, item_qty_table):
    item_total_price = 0
    for i in range(len(item_price_table)):
        item_total_price += float(item_price_table[i]) * int(item_qty_table[i])
    print("item_total_price:", item_total_price)
    discounted_total_price = round(item_total_price * 0.6, 2)
    return discounted_total_price


connect_timeout = 10.0
read_timeout = 20.0
http_instance = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
)

sku_table = get_sku_table(table_of_items_ordered)
price_table, vendor_table = get_price_and_vendor_tables(http_instance, access_token, sku_table)
qty_table = get_qty_table(table_of_items_ordered)
order_total_price = get_total_discounted_price(price_table, qty_table)

items_sku_string = "\n".join(sku_table)
print("items_sku_string:\n", items_sku_string)

items_qty_string = "\n".join(qty_table)
print("items_qty_string:\n", items_qty_string)

items_price_string = "\n".join(price_table)
print("items_price_string:\n", items_price_string)

items_vendor_string = "\n".join(vendor_table)
print("items_vendor_string:\n", items_vendor_string)

print("order_total_price:", order_total_price)

output = [{'sku_table': items_sku_string, 'qty_table': items_qty_string, 'price_table': items_price_string, 'vendor_table': items_vendor_string, 'order_total_price': order_total_price}]
