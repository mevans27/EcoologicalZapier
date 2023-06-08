import re
from datetime import datetime
from typing import Iterable, Any, Tuple
import urllib3
import certifi
import json
import time
from input_data import *

connect_timeout = 10.0
read_timeout = 20.0


def signal_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
    iterable = iter(it)
    ret_var = next(iterable)
    for val in iterable:
        yield False, ret_var
        ret_var = val
    yield True, ret_var


def convert(string):
    li = list(string.split(","))
    return li


def merge(list1, list2, list3, list4):
    merged_item_list = tuple(zip(list1, list2, list3, list4))
    return merged_item_list


def grab_sku_object_from_sos(item_sku, token):
    time.sleep(1)
    print("token: " + token)
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


def grab_vendor_object_from_sos(item_vendor, token):
    time.sleep(1)
    print("token: " + token)
    resp = http.request(
        "GET",
        "https://api.sosinventory.com/api/v2/vendor?start=0&maxresults=1&query="
        + item_vendor,
        headers={
            'Authorization': 'Bearer ' + token,
            'Host': 'api.sosinventory.com'
        },
        retries=5
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    print("grabVendorObjectFromSos json return:")
    print(json_object)
    return json_object


def create_new_vendor(item_vendor):
    time.sleep(1)
    encoded_body = json.dumps({"name": item_vendor})
    resp = http.request(
        "POST",
        "https://api.sosinventory.com/api/v2/vendor/",
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Host': 'api.sosinventory.com'
        },
        body=encoded_body
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    print("createNewVendor json return:")
    print(json_object)
    return json_object


def create_new_item(item_vendor, item_sku, item_sales_price):
    time.sleep(1)
    encoded_body = json.dumps({
        "name": item_sku,
        "item_sku": item_sku,
        "description": item_sku,
        "type": "Inventory Item",
        "item_sales_price": item_sales_price,
        "item_vendor": {
            "name": item_vendor
        },
        "incomeAccount": {
            "name": "Inventory Asset"
        }
    })
    resp = http.request(
        "POST",
        "https://api.sosinventory.com/api/v2/item/",
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Host': 'api.sosinventory.com'
        },
        body=encoded_body
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    print("createNewItem json return:")
    print(json_object)
    return json_object


def check_if_item_already_exists(json_object, item_sku):
    count = json_object['count']
    print("item_sku:" + item_sku)
    if count > 0:
        print("count is greater than 0")
        sku_from_item = json_object['data'][0]['sku']
        print("item_sku from item: " + sku_from_item)
        print("item_sku: " + item_sku)
        if sku_from_item == item_sku:
            item_sku_already_exists = True
            print("Item Match Found:" + sku_from_item + " and " + item_sku)
        else:
            item_sku_already_exists = False
            print("Item Match Not Found for item_sku:" + item_sku)
    else:
        item_sku_already_exists = False
        print("No Item Matches Found")
    return item_sku_already_exists


def check_if_vendor_already_exists(json_object, item_vendor):
    count = json_object['count']
    print("item_vendor:" + item_vendor)
    if count > 0:
        print("count is greater than 0")
        vendor_from_item = json_object['data'][0]['name']
        print(vendor_from_item)
        if item_vendor in vendor_from_item:
            item_vendor_already_exists = True
            print("Vendor Match Found:" + vendor_from_item + " and " + item_vendor)
        else:
            item_vendor_already_exists = False
            print("Vendor Match Not Found for item_vendor:" + item_vendor)
    else:
        item_vendor_already_exists = False
        vendor_from_item = ""
        print("No item_vendor Matches Found")
    return item_vendor_already_exists, vendor_from_item


def get_tables_of_items_ordered(merged_item_list):
    items_ordered = ""
    drop_shipper_items_ordered = ""
    item_vendor_set = set([])
    for is_last_element, x in signal_last(merged_item_list):
        sku = x[0]
        qty = x[1]
        vendor = x[2]
        sales_price = x[3]
        print("Current Vendor: " + vendor)
        if vendor != "Ecoological":
            print("Sku:", sku)
            sku_object = grab_sku_object_from_sos(sku, access_token)
            sku_already_exists = check_if_item_already_exists(sku_object, sku)
            drop_shipper_items_ordered = drop_shipper_items_ordered + "Vendor:" + vendor + ", SKU: " + sku + ", Qty: " + qty + ", Price: " + sales_price + ";"
            item_vendor_set.add(vendor)
            if not sku_already_exists:
                print("item_sku doesn't already exist")
                vendor_object = grab_vendor_object_from_sos(vendor, access_token)
                vendor_already_exists, vendor_return = check_if_vendor_already_exists(vendor_object, vendor)
                if not vendor_already_exists:
                    vendor_creation_object = create_new_vendor(vendor)
                    print(vendor_creation_object)
                item_creation_object = create_new_item(vendor_return, sku, sales_price)
                print(item_creation_object)
        items_ordered = items_ordered + "SKU: " + sku + ", Qty: " + qty + ", Price: " + sales_price + ","
        if not is_last_element:
            items_ordered = items_ordered + "\n"
    return items_ordered, drop_shipper_items_ordered, item_vendor_set


def get_payment_gateway_names(payment_names):
    if payment_names == "authorize_net":
        payment_names = "AUTH.NET"
    elif payment_names == "paypal":
        payment_names = "paypal"
    else:
        payment_names = "Due on receipt"
    return payment_names


http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
)
payment_gateway_names = payment_gateway_names.replace('+', '')
sku_line_items_list = convert(sku_line_items)
print("sku_line_items_list:", sku_line_items_list)
qty_line_items_list = convert(qty_line_items)
print("qty_line_items_list:", qty_line_items_list)
vendor_line_items_list = convert(vendor_line_items)
print("vendor_line_items_list:", vendor_line_items_list)
price_line_items_list = convert(price_line_items)
print("price_line_items_list:", price_line_items_list)
merged_list = merge(sku_line_items_list, qty_line_items_list, vendor_line_items_list, price_line_items_list)

table_of_items_ordered, drop_shipper_table_of_items_ordered, vendor_set = get_tables_of_items_ordered(merged_list)
vendor_set_string = '; '.join(str(e) for e in vendor_set)

# Converting the datetime into date and time variables
date_time_regex = re.search(r"\d{4}-\d{2}-\d{0,2}T\d{2}:\d{2}:\d{2}", date_time_str)
print("datetime regex:", date_time_regex.group())
date_time_obj = datetime.strptime(date_time_regex.group(), '%Y-%m-%dT%H:%M:%S')
date = str(date_time_obj.date())
date_time = str(date_time_obj.time())

# Convert authorize_net to authorize.net
payment_gateway_names = get_payment_gateway_names(payment_gateway_names)

output = [{'date': date, 'time': date_time, 'table_of_items_ordered': table_of_items_ordered,
           'drop_shipper_table_of_items_ordered': drop_shipper_table_of_items_ordered,
           'payment_names': payment_gateway_names, 'vendor_set_string': vendor_set_string}]
