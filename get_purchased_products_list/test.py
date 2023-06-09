from main import *


# Note: You will likely need to change the token to the most recent. You can grab it from Zapier.


class TestLineItem:

    # Testing get_taxable

    def test_get_taxable_when_state_is_ca(self):
        state = "CA"
        expected = True
        actual = LineItem.get_taxable(state)
        assert (actual == expected)

    def test_get_taxable_when_state_is_not_ca(self):
        state = "NY"
        expected = False
        actual = LineItem.get_taxable(state)
        assert (actual == expected)

    # Testing get_final_individual_item_discount

    def test_get_final_individual_item_discount_with_discount_and_drop_shipper(self):
        item_discount = 50
        drop_shipper = 'true'
        expected = 40
        actual = LineItem.get_final_individual_item_discount(item_discount, drop_shipper)
        assert (actual == expected)

    def test_get_final_individual_item_discount_without_discount_and_drop_shipper(self):
        item_discount = 0
        drop_shipper = 'true'
        expected = 40
        actual = LineItem.get_final_individual_item_discount(item_discount, drop_shipper)
        assert (actual == expected)

    def test_get_final_individual_item_discount_with_discount_and_not_drop_shipper(self):
        item_discount = 50
        drop_shipper = 'false'
        expected = 50
        actual = LineItem.get_final_individual_item_discount(item_discount, drop_shipper)
        assert (actual == expected)

    def test_get_final_individual_item_discount_without_discount_and_not_drop_shipper(self):
        item_discount = 0
        drop_shipper = 'false'
        expected = 0
        actual = LineItem.get_final_individual_item_discount(item_discount, drop_shipper)
        assert (actual == expected)

    # Testing get_override_price

    def test_get_override_price_with_price_override(self):
        item_ordered_line = "SKU: BK0310, Qty: 1, Price: 100.00,"
        item_subtotal = 10
        final_individual_item_discount = 0
        expected = 100
        actual = LineItem.get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal)
        assert (actual == expected)

    def test_get_override_price_with_price_override_and_discount(self):
        item_ordered_line = "SKU: BK0310, Qty: 1, Price: 100.00,"
        item_subtotal = 10
        final_individual_item_discount = 40
        expected = 60
        actual = LineItem.get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal)
        assert (actual == expected)

    def test_get_override_price_with_line_item_price(self):
        item_ordered_line = "SKU: BK0310, Qty: 1,"
        item_subtotal = 10
        final_individual_item_discount = 0
        expected = 10
        actual = LineItem.get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal)
        assert (actual == expected)

    def test_get_override_price_with_line_item_price_and_discount(self):
        item_ordered_line = "SKU: BK0310, Qty: 1,"
        item_subtotal = 12.34
        final_individual_item_discount = 40
        expected = 7.40
        actual = LineItem.get_override_price(final_individual_item_discount, item_ordered_line, item_subtotal)
        assert (actual == expected)

    # Testing get_final_calculated_amount

    def test_get_final_calculated_amount_with_quantity_4(self):
        override_price = 12.34
        item_quantity = 4
        expected = 49.36
        actual = LineItem.get_final_calculated_amount(override_price, item_quantity)
        assert (actual == expected)

    def test_get_final_calculated_amount_with_quantity_1(self):
        override_price = 12.34
        item_quantity = 1
        expected = 12.34
        actual = LineItem.get_final_calculated_amount(override_price, item_quantity)
        assert (actual == expected)

    def test_get_final_calculated_amount_with_decimal_price(self):
        override_price = 12.3456
        item_quantity = 3
        expected = 37.04
        actual = LineItem.get_final_calculated_amount(override_price, item_quantity)
        assert (actual == expected)

    # Testing get_business_days

    def test_get_business_days_with_chevy_standard_sku(self):
        item_description = "Make: CHEVY     Model: SILVERADO 1500     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'BK0310'
        expected = 10
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_toyota_standard_sku(self):
        item_description = "Make: TOYOTA     Model: PRIUS     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'BK0310'
        expected = 10
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_tacoma_standard_sku(self):
        item_description = "Make:   Model: TACOMA     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'BK0310'
        expected = 10
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_aerobox_standard_sku(self):
        item_description = "Make:   Model: AEROBOX     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'BK0310'
        expected = 5
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_gapshield_standard_sku(self):
        item_description = "Make:   Model: GAPSHIELD     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'BK0310'
        expected = 3
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_toyota_nonstandard_sku_mg(self):
        item_description = "Make: CHEVY     Model: SILVERADO 1500     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'MG1234'
        expected = 56
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_toyota_nonstandard_sku_ss(self):
        item_description = "Make: CHEVY     Model: SILVERADO 1500     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'SS1234'
        expected = 56
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    def test_get_business_days_with_toyota_nonstandard_sku_ab(self):
        item_description = "Make: CHEVY     Model: SILVERADO 1500     Year:'14-'15\nLocation: FRONT BUMPER\nColor: GLOSS WHITE\nAlt1: NO sensor holes\nAlt1: WITH fog lamps\n# of Pieces: 3"
        item_sku = 'AB1234'
        expected = 56
        actual = LineItem.get_business_days(item_description, item_sku)
        assert (actual == expected)

    # Testing get_due_date
    def test_get_due_date_with_month_overlap(self):
        item_received_date = '2023-03-31'
        business_days = 10
        expected = '2023-04-10'
        actual = LineItem.get_due_date(item_received_date, business_days)
        assert (actual == expected)

    def test_get_due_date_with_month_no_overlap(self):
        item_received_date = '2023-03-11'
        business_days = 20
        expected = '2023-03-31'
        actual = LineItem.get_due_date(item_received_date, business_days)
        assert (actual == expected)

    def test_get_due_date_with_longest_days(self):
        item_received_date = '2023-03-31'
        business_days = 56
        expected = '2023-05-26'
        actual = LineItem.get_due_date(item_received_date, business_days)
        assert (actual == expected)


def test_get_item_description_1():
    sku = 'BK0310'
    item_description = get_item_description(sku, access_token)
    expected = 'BumperShellz:BK0310'
    actual = item_description['data'][0]['fullname']
    assert (actual == expected)


def test_get_item_description_2():
    sku = '3GT-VENT-BLACK'
    item_description = get_item_description(sku, access_token)
    expected = '3GT-VENT-BLACK'
    actual = item_description['data'][0]['fullname']
    assert (actual == expected)


def test_correct_plus_sign_skus():
    test_ordered_items_table = "SKU: BK0310, QTY: 1, Price: 123,\nSKU: BK0310+BK3010, QTY: 2,\nSKU: BK0310, QTY: 1,\nSKU: BK3010, QTY: 1,"
    test_items = correct_plus_sign_skus(test_ordered_items_table)
    assert (test_items == "SKU: BK0310, QTY: 1, Price: 123,\nSKU: BK0310, QTY: 2,\nSKU: BK3010, QTY: 2,\nSKU: BK0310, QTY: 1,\nSKU: BK3010, QTY: 1,")


def test_convert_line_item_to_json():
    # noinspection DuplicatedCode
    line_order_sku = "BK0310"
    line_state_code = "CA"
    line_received_date = "2021-01-01"
    line_quantity = 1
    line_is_drop_shipper = "false"
    line_item_ordered = "SKU: BK0310, Qty: 1, Price: 100.00,"
    line_subtotal = 20
    item_description = get_item_description(line_order_sku, access_token)
    line_item = LineItem(item_description, line_quantity, line_is_drop_shipper,
                         line_item_ordered, line_state_code, line_subtotal, line_order_sku, line_received_date)
    line_item_json_converted = convert_line_item_to_json(line_item)

    json_test = json.loads(line_item_json_converted)
    assert (json_test['class']['name'] == "Ecoological")
    assert (json_test['amount'] == 100.00)
    assert (json_test[
                'description'] == "Make: CHEVY     Model: SILVERADO 1500     Year:'14-'15 Location: FRONT BUMPER Color: GLOSS WHITE Alt1: NO sensor holes Alt1: WITH fog lamps # of Pieces: 3")
    assert (json_test['duedate'] == "2021-01-11")
    assert (json_test['item']['name'] == "BumperShellz:BK0310")
    assert (json_test['listPrice'] == 20.00)
    assert (json_test['percentdiscount'] == 0.00)
    assert (json_test['quantity'] == 1)
    assert (json_test['tax']['taxable'] is True)
    assert (json_test['tax']['taxCode'] is None)
    assert (json_test['unitprice'] == 100.00)
