from main import *


def test_convert():
    string = 'EK4001'
    li = convert(string)
    assert li == ['EK4001']
    string = 'EK4001,BK0310'
    li = convert(string)
    assert li == ['EK4001', 'BK0310']


def test_merge():
    list1 = ['a', 'b', 'c']
    list2 = [1, 2, 3]
    list3 = [4, 5, 6]
    list4 = [7, 8, 9]
    merged_item_list = merge(list1, list2, list3, list4)
    assert (merged_item_list == (('a', 1, 4, 7), ('b', 2, 5, 8), ('c', 3, 6, 9)))


def test_grab_sku_object_from_sos():
    json_object = grab_sku_object_from_sos('EK4001', access_token)
    assert (json_object['data'][0]['sku'] == 'EK4001')


def test_grab_vendor_object_from_sos():
    json_object = grab_vendor_object_from_sos('test_vendor', access_token)
    assert (json_object['count'] == 0)
    json_object = grab_vendor_object_from_sos('Trim Illusion', access_token)
    assert (json_object['data'][0]['email'] == 'e.cook@trimillusion.com')


def test_create_new_vendor():
    item_vendor = 'Test Vendor'
    json_object = create_new_vendor(item_vendor)
    assert (json_object['message'] == 'There is already a vendor with that name.')


def test_create_new_item():
    item_vendor = 'Test Vendor'
    item_sku = 'Test SKU'
    item_sales_price = '1.00'
    json_object = create_new_item(item_vendor, item_sku, item_sales_price)
    assert (json_object['message'] == 'There is already another item with that name.')


def test_check_if_item_already_exists():
    json_object = {'count': 1, 'data': [{'sku': 'Test SKU', 'name': 'Test SKU', 'description': 'Test SKU', 'type': 'Inventory Item', 'item_sales_price': '1.00', 'item_vendor': {'name': 'Test Vendor'}, 'incomeAccount': {'name': 'Inventory Asset'}}]}
    item_sku = 'Test SKU'
    item_sku_already_exists = check_if_item_already_exists(json_object, item_sku)
    assert (item_sku_already_exists is True)
    json_object = {'count': 0, 'data': []}
    item_sku = 'SKU_1'
    item_sku_already_exists = check_if_item_already_exists(json_object, item_sku)
    assert (item_sku_already_exists is False)


def test_check_if_vendor_already_exists():
    json_object = {'count': 1, 'data': [{'name': 'Test Vendor', 'id': '5f6e4e0f-a9d3-4e2e-a9e8-d9d5e5d9d5e5'}]}
    item_vendor = 'Test Vendor'
    item_vendor_already_exists, vendor_from_item = check_if_vendor_already_exists(json_object, item_vendor)
    assert (item_vendor_already_exists is True)
    assert (vendor_from_item == 'Test Vendor')
    json_object = {'count': 0, 'data': []}
    item_vendor = 'Test'
    item_vendor_already_exists, vendor_from_item = check_if_vendor_already_exists(json_object, item_vendor)
    assert (item_vendor_already_exists is False)
    assert (vendor_from_item == '')


def test_get_tables_of_items_ordered():
    test_merged_item_list = (('EF0212', '1', 'Ecoological', '10'), ('EF0412', '2', 'Ecoological', '20'), ('DF3012', '3', 'Tufskinz', '30'), ('DF3012', '4', 'Trim Illusion', '40'))
    print(test_merged_item_list)
    items_ordered, drop_shipper_items_ordered, test_vendor_set = get_tables_of_items_ordered(test_merged_item_list)
    assert (items_ordered == 'SKU: EF0212, Qty: 1, Price: 10,\nSKU: EF0412, Qty: 2, Price: 20,\nSKU: DF3012, Qty: 3, Price: 30,\nSKU: DF3012, Qty: 4, Price: 40,')
    assert (drop_shipper_items_ordered == 'Vendor:Tufskinz, SKU: DF3012, Qty: 3, Price: 30;Vendor:Trim Illusion, SKU: DF3012, Qty: 4, Price: 40;')


def test_get_payment_gateway_names():
    assert (get_payment_gateway_names('authorize_net') == 'AUTH.NET')
    assert (get_payment_gateway_names('paypal') == 'paypal')
    assert (get_payment_gateway_names('stripe') == 'Due on receipt')
