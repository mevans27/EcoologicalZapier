from main import *

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def test_grab_sku_object_from_sos():
    json_object = grab_sku_object_from_sos(http, 'T-DF101', access_token)
    expected = 'T-DF101'
    actual = json_object['data'][0]['sku']
    assert (actual == expected)


def test_get_sku_table():
    test_table_of_items_ordered = 'SKU: T-DF101, QTY: 1, TURN5,\nSKU: EK4001, QTY: 1, TURN5,\nSKU: 3GT-VENT-BLACK, QTY: 1, TURN5,'
    expected = ['T-DF101', 'EK4001', '3GT-VENT-BLACK']
    actual = get_sku_table(test_table_of_items_ordered)
    assert (actual == expected)


def test_get_qty_table():
    test_table_of_items_ordered = 'SKU: T-DF101, QTY: 1, TURN5,\nSKU: EK4001, QTY: 1, TURN5,\nSKU: 3GT-VENT-BLACK, QTY: 1, TURN5,'
    expected = ['1', '1', '1']
    actual = get_qty_table(test_table_of_items_ordered)
    assert (actual == expected)


def test_get_vendor_table():
    http_object = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    test_items_sku_table = ['T-DF101', 'EK4001', '3GT-VENT-BLACK']
    vendor_array = get_vendor_table(http_object, access_token, test_items_sku_table)
    assert (vendor_array == ['Ecoological', 'Ecoological', 'MESO Customs'])


def test_get_price_table():
    test_table_of_items_ordered = 'SKU: FD0101, QTY: 1, Price: 167.97, TURN5,\nSKU: DD1001, QTY: 1, Price: 83.97, TURN5,\nSKU: DD1001, QTY: 1, TURN5,'
    http_object = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    test_price_table = get_price_table(test_table_of_items_ordered, http_object, access_token)
    expected_price_table = ['167.97', '83.97', '139.95']
    assert (test_price_table == expected_price_table)


def test_get_total_discounted_price_drop_shipper():
    test_is_drop_shipper = "true"
    test_item_price_table = ['10', '20', '30']
    test_item_qty_table = ['1', '2', '3']
    expected = 84
    actual = get_total_discounted_price(test_is_drop_shipper, test_item_price_table, test_item_qty_table)
    assert (actual == expected)


def test_get_total_discounted_price_not_drop_shipper():
    test_is_drop_shipper = "false"
    test_item_price_table = ['10', '20', '30']
    test_item_qty_table = ['1', '2', '3']
    expected = 140.0
    actual = get_total_discounted_price(test_is_drop_shipper, test_item_price_table, test_item_qty_table)
    assert (actual == expected)