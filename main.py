# This is a sample Python script.

import json
import re
from datetime import timedelta, datetime

import certifi
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import urllib3


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
        self.taxCode = "null"


class LineItem:
    def __init__(self, item_description, item_quantity, drop_shipper, item_discount, item_ordered_line, state,
                 item_subtotal, item_sku, item_received_date):
        self.item = json.dumps(Item(item_description['data'][0]['fullname']).__dict__)
        self.Class = json.dumps(Class().__dict__)
        self.tax = json.dumps(Tax(self.get_taxable(state)).__dict__)
        self.description = item_description['data'][0]['description']
        self.quantity = item_quantity
        self.weightunit = "lb"
        self.volumeunit = "cbm"
        self.percentdiscount = self.get_final_individual_item_discount(0, drop_shipper)
        self.unitprice = self.get_override_price(self.percentdiscount, item_ordered_line, item_subtotal)
        self.amount = self.get_final_calculated_amount(self.unitprice, item_quantity)
        self.listPrice = item_subtotal
        self.percentdiscount = item_discount
        self.duedate = self.get_due_date(item_received_date, self.get_business_days(self.description, item_sku))

    @staticmethod
    def get_taxable(state):
        if state == "CA":
            return True
        else:
            return False

    @staticmethod
    def get_final_individual_item_discount(item_discount, drop_shipper):
        if drop_shipper == "true":
            print("\"Is drop shipper\" is: ", drop_shipper)
            final_individual_item_discount = 40
        else:
            print("\"Is drop shipper\" is: ", drop_shipper)
            final_individual_item_discount = item_discount

        return final_individual_item_discount

    @staticmethod
    def get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal):

        if re.search('Price:', item_ordered_line):
            print("Item Ordered specifies price")
            item_price = re.search(r'Price: (.*?),', item_ordered_line).group(1)
            item_qty = re.search(r'Qty: (.*?),', item_ordered_line).group(1)
            override_price = float(item_price) * float(item_qty)
        else:
            print("Item Ordered does not specify price, using item_subtotal from SOS")
            override_price = item_subtotal

        if float(final_individual_item_discount) > 0:
            print("Discount is greater than zero, discount:", final_individual_item_discount)
            override_price = round(float(override_price) * ((100 - float(final_individual_item_discount)) / 100), 2)

        return override_price

    @staticmethod
    def get_final_calculated_amount(override_price, item_quantity):
        final_calculated_amount = round(float(override_price) * float(item_quantity), 2)
        return final_calculated_amount

    @staticmethod
    def get_business_days(item_description, item_sku):
        if re.search('MG|SS|AB', item_sku):
            business_days = 56
        elif re.search('Tacoma|Toyota', item_description, re.IGNORECASE):
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
        return due_date.strftime("%Y-%m-%d")


def get_item_description(sku, token):
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
    print(json_object)

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


if __name__ == '__main__':
    access_token = "S2i9vmTc9ZRk7nBD5mdgV6gK_0baSvDVEBzK7ARbZ2yuiNleckpFyWGvp9FcpWNs0t0UEbeNbYbyDLzZsDT89UtOgvbNyJj4nxBgaeI3DZ5NzQ00vDFJJVqiC4Otqbgp4Q6HoKHOk0gWhsPC1tzwSjSt64tWrBVkDxo0vzzGhVTvMlUcWwDbDu--JDX3wGLIbchYkfbwUlyxnZtZIW-bqq1EvtN_2pTxs0Va2RS82vs0eM4c_lrMGj2e8uv2EEmhHqx2dZ9iDkh7TY6A_SgM4h9NShVNAgYf5CrZQbfcBCn8J3Ev"
    # noinspection DuplicatedCode
    order_sku = "BK0310"
    state_code = "CA"
    received_date = "2021-01-01"
    quantity = 1
    is_drop_shipper = "false"
    individual_item_discount = 0
    item_ordered = "SKU: BK0310, Qty: 1, Price: 100.00,"
    subtotal = 20
    order_item_description = get_item_description(order_sku, access_token)
    order_line_item = LineItem(order_item_description, quantity, is_drop_shipper, individual_item_discount,
                               item_ordered, state_code, subtotal, order_sku, received_date)

    # convert to JSON format

    line_item_json = convert_line_item_to_json(order_line_item)
    # print created JSON objects
    print(line_item_json)
