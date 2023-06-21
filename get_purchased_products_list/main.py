from input_data import *

import json
import re
from datetime import timedelta, datetime
import os

import certifi
import urllib3

access_token = input_data['access_token']
state_code = input_data['state_code']
received_date = input_data['received_date']
is_drop_shipper = input_data['is_drop_shipper']
subtotal = input_data['subtotal']
table_of_items_ordered = input_data['items_ordered']
table_of_items_ordered = os.linesep.join([s for s in table_of_items_ordered.splitlines() if s])


class Class:
    def __init__(self):
        self.id = 1
        self.name = "Ecoological"


class Item:
    def __init__(self, fullname):
        self.name = fullname


class Tax:
    def __init__(self, taxable):
        self.taxable = taxable
        self.taxCode = None


class LineItem:
    def __init__(self, item_description, item_quantity, drop_shipper, item_ordered_line, state,
                 item_subtotal, item_received_date, item_counter):
        self.lineNumber = item_counter
        self.item = json.dumps(Item(item_description['data'][0]['fullname']).__dict__)
        self.Class = json.dumps(Class().__dict__)
        self.job = None
        self.workcenter = None
        self.tax = json.dumps(Tax(self.get_taxable(state)).__dict__)
        self.linkedTransaction = None
        self.description = item_description['data'][0]['description']
        self.quantity = item_quantity
        self.weight = 0.00
        self.volume = 0.00
        self.weightunit = "lb"
        self.volumeunit = "cbm"
        self.percentdiscount = self.get_final_individual_item_discount(0, drop_shipper)
        self.unitprice = self.get_override_price(self.percentdiscount, item_ordered_line, item_subtotal)
        self.amount = self.get_final_calculated_amount(self.unitprice, item_quantity)
        self.altAmount = 0.00
        self.picked = 0.00
        self.shipped = 0.00
        self.returned = 0.00
        self.cost = None
        self.margin = None
        self.listPrice = self.unitprice
        self.duedate = self.get_due_date(item_received_date, self.get_business_days(self.description))
        self.uom = None
        self.bin = None
        self.lot = None
        self.serials = None

    @staticmethod
    def get_taxable(state):
        if state == "CA":
            return True
        else:
            return False

    @staticmethod
    def get_final_individual_item_discount(item_discount, drop_shipper):
        if drop_shipper == "true":
            final_individual_item_discount = 40
        else:
            final_individual_item_discount = item_discount

        return final_individual_item_discount

    @staticmethod
    def get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal):

        if re.search('Price:', item_ordered_line):
            item_price = re.search(r'Price: (.*?),', item_ordered_line, re.IGNORECASE).group(1)
            item_qty = re.search(r'(?<=QTY: )\d+(?=,)', item_ordered_line, re.IGNORECASE).group().strip()
            override_price = float(item_price) * float(item_qty)
        else:
            override_price = item_subtotal

        if float(final_individual_item_discount) > 0:
            override_price = round(float(override_price) * ((100 - float(final_individual_item_discount)) / 100), 2)

        return override_price

    @staticmethod
    def get_final_calculated_amount(override_price, item_quantity):
        final_calculated_amount = round(float(override_price) * float(item_quantity), 2)
        return final_calculated_amount

    @staticmethod
    def get_business_days(item_description):
        if re.search('Tacoma|Toyota', item_description, re.IGNORECASE):
            business_days = 10
        elif re.search('Aerobox', item_description, re.IGNORECASE):
            business_days = 5
        elif re.search('Gapshield', item_description, re.IGNORECASE):
            business_days = 3
        else:
            business_days = 10
        return business_days

    @staticmethod
    def get_due_date(item_received_date, business_days):
        formatted_received_date: datetime = datetime.strptime(item_received_date, "%Y-%m-%d")
        due_date = formatted_received_date + timedelta(days=business_days)
        return due_date.strftime("%Y-%m-%d") + "T00:00:00"


def get_item_description(sku, token):
    print("sku:" + sku)
    connect_timeout = 10.0
    read_timeout = 20.0
    http = urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=certifi.where(),
        timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
    )

    resp = http.request(
        "GET",
        "https://api.sosinventory.com/api/v2/item?start=0&maxresults=1&sku=" + sku,
        headers={
            'Authorization': 'Bearer ' + token,
            'Host': 'api.sosinventory.com'
        },
        retries=5
    )

    json_object = json.loads(resp.data.decode("utf-8"))

    if json_object['count'] == 0:
        message = "SKU: " + sku + ", not found in SOS Inventory, please add it and re-run this Zap using the order JSON backed up in Zapier: https://tables.zapier.com/app/tables/t/01H2E4ZS8BE994ESEC8S7BMDSS. Submission link: https://form-8b1992.zapier.app/"
        print(message)
        raise TypeError(message)
    return json_object


def convert_line_item_to_json(line_item):
    json_string = json.dumps(line_item.__dict__)

    # remove extra quotes from json string surrounding brackets
    json_string = json_string.replace('"{', '{').replace('}"', '}')

    # replace escaped quotes with actual quotes, and remove newline special characters
    json_string = json_string.replace('\\"', '"').replace('\\n', ' ')

    # replace Class with class
    json_string = json_string.replace("Class", "class")

    return json_string


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


items = correct_plus_sign_skus(table_of_items_ordered)

purchased_products_list = []
items_array = items.split('\n')
counter = 1
for item_ordered in items_array:
    order_quantity = int(re.search(r'(?<=QTY: )\d+(?=,)', item_ordered, re.IGNORECASE).group().strip())
    order_sku = re.search(r'(?<=SKU: )(.*?)(?=,)', item_ordered, re.IGNORECASE).group().strip()
    order_item_description = get_item_description(order_sku, access_token)
    print(order_item_description)
    order_line_item = LineItem(order_item_description, order_quantity, is_drop_shipper,
                               item_ordered, state_code, subtotal, received_date, counter)
    line_item_json = convert_line_item_to_json(order_line_item)
    purchased_products_list.append(line_item_json)
    counter += 1

print("Purchased_products_list:")
print(purchased_products_list)

output = [{'purchased_products_list': purchased_products_list}]
