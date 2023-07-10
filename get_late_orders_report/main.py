from input_data import *

import csv
import urllib.request
from datetime import datetime
import re

url = input_data['url']

response = urllib.request.urlopen(url)
lines = [line.decode('utf-8') for line in response.readlines()]
input_csv_lines = csv.reader(lines)
other_customers_dict = {}
turn5_dict = {}


def get_word_doc(turn5_string_item, other_customers_string_item, turn5_late, other_late, total_late, total_orders):
    word_doc_string = """
Key Performance Indicators:
    Total Open Orders & Items:  """ + str(total_orders) + """
    Total late orders:  """ + str(total_late) + """

LATE ORDER REPORT:
---------------------------------------------------------
TURN5 - Late: """ + str(turn5_late) + """
""" + turn5_string_item + """
---------------------------------------------------------

---------------------------------------------------------
All other customers - Late:  """ + str(other_late) + """
""" + other_customers_string_item + """
---------------------------------------------------------
"""
    return word_doc_string


class Turn5Sale:
    def __init__(self, sales_order_number_item, total_amount_due, quantity_item, due_date_item, cancel_by_date):
        self.sales_order_number = sales_order_number_item
        self.amount_due = total_amount_due
        self.quantity = quantity_item
        self.due_date = due_date_item
        self.cancel_by = cancel_by_date


class OtherCustomerSale:
    def __init__(self, sales_order_number_item, customer_name_item, quantity_item, due_date_item, customer_notes_items):
        self.order_number = sales_order_number_item
        self.customer_name = customer_name_item
        self.quantity = quantity_item
        self.sku_array = []
        self.due_date = due_date_item
        self.notes = customer_notes_items

    @staticmethod
    def add_to_sku_array(self, sku_item):
        self.sku_array.append(sku_item)


today_date_time = datetime.today().strftime('%m/%d/%Y')
today_file_name = datetime.today().strftime('%Y/%m/%Y-%m-%d-')
today = datetime.strptime(today_date_time, '%m/%d/%Y')
all_items_counter = 0
total_late_counter = 0
turn5_late_counter = 0
other_late_counter = 0
for row in input_csv_lines:
    if row[0].isdigit() and row[4] != '':
        order_number = row[0]
        sales_order_number = row[1]
        cancel_by = row[5]
        customer_name = row[2]
        sku = row[3].replace('BumperShellz:', '')
        due_date = datetime.strptime(row[4], '%m/%d/%Y')
        due_date_str = datetime.strftime(due_date, '%m/%d/%Y')
        total_amount = float(row[6].replace('$', '').replace(' ', '').replace(',', '').replace('C', ''))
        quantity = int(row[7])
        customer_notes = re.findall(r'(?<=\[{)(.+?)(?=}])', row[8])
        all_items_counter += quantity

        if due_date < today:
            total_late_counter += quantity
            if customer_name == 'Turn 5':
                turn5_late_counter += quantity
                if turn5_dict.get(order_number) is None:
                    turn5_dict[order_number] = Turn5Sale(sales_order_number, total_amount, quantity, due_date_str, cancel_by)
                else:
                    turn5_dict[order_number].amount_due += total_amount
                    turn5_dict[order_number].quantity += quantity

            else:
                other_late_counter += quantity
                if other_customers_dict.get(order_number) is None:
                    other_customers_dict[order_number] = OtherCustomerSale(sales_order_number, customer_name, quantity, due_date_str,
                                                                           customer_notes)
                else:
                    other_customers_dict[order_number].quantity += quantity

                other_customers_dict[order_number].add_to_sku_array(other_customers_dict[order_number], sku)

    else:
        continue

turn5_string = "sos order number ~ amount due ~ quantity ~ due date ~ cancel by date\n"
for key, value in turn5_dict.items():
    turn5_string += str(key) + " ~ " + str(round(value.amount_due, 2)) + " ~ " + str(value.quantity) + " ~ " + str(value.due_date) + " ~ " + str(
        value.cancel_by)
    if key != list(turn5_dict.keys())[-1]:
        turn5_string += "\n"


other_customers_string = "sos order number ~ customer name ~ quantity ~ sku array ~ due date ~ notes\n"
for key, value in other_customers_dict.items():
    other_customers_string += str(key) + " ~ " + str(value.customer_name) + " ~ " + str(value.quantity) + " ~ " + ', '.join(value.sku_array) + " ~ " + str(
        value.due_date) + " ~ " + '. '.join(value.notes)
    if key != list(other_customers_dict.keys())[-1]:
        other_customers_string += "\n"


word_doc = get_word_doc(turn5_string, other_customers_string, turn5_late_counter, other_late_counter, total_late_counter, all_items_counter)

print(word_doc)
output = [{'word_doc': word_doc, 'today_date_time': today_date_time, 'late_turn_5_order_count': turn5_late_counter,
           'late_other_customer_order_count': other_late_counter,
           'total_late_count': total_late_counter,
           'total_orders_count': all_items_counter, 'today_file_name': today_file_name}]
