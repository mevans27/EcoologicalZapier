from input_data import *

total_price = input_data['total_price']
subtotal_price = input_data['subtotal_price']
total_discounts = input_data['total_discounts']
state = input_data['state']
total_tax = input_data['total_tax']


def get_taxable(code_state):
    if code_state == "CA":
        return True
    else:
        return False


def get_calculated_total(price, discounts):
    total = round(float(price) - float(discounts), 2)
    return total


def get_tax_percent(tax, is_taxable, subtotal, discounts):
    if is_taxable:
        final_tax_percent = round(tax / (subtotal - discounts) * 100, 2)
    else:
        final_tax_percent = round(tax / subtotal * 100, 2)

    return final_tax_percent


def get_formatted_discount_text(discounts):
    if discounts > 0:
        formatted = -discounts
    else:
        formatted = discounts
    return formatted


taxable = get_taxable(state)
calculated_total = float(total_price) - float(total_discounts)
tax_percent = get_tax_percent(float(total_tax), taxable, float(subtotal_price), float(total_discounts))
formatted_discount_text = get_formatted_discount_text(float(total_discounts))

output = [{'taxable': taxable, 'calculated_total': calculated_total, 'tax_percent': tax_percent, 'formatted_discount_text': formatted_discount_text}]
