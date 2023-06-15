from main import *


def test_clean_purchased_products_list_multiple_line_items():
    test_purchased_products_list_multiple_line_items = '{"lineNumber": 1, "item": {"name": "MESO Customs:CLIMATE-KNOBS-DZ-BLACK"}, "class": {"id": 1, "name": "Ecoological"}, "job": null, "workcenter": null, "tax": {"taxable": true, "taxCode": null}, "linkedTransaction": null, "description": "Climate Control Rings // DUAL ZONE // BLACK", "quantity": 1, "weight": 0.0, "volume": 0.0, "weightunit": "lb", "volumeunit": "cbm", "percentdiscount": 0, "unitprice": 30.0, "amount": 30.0, "altAmount": 0.0, "picked": 0.0, "shipped": 0.0, "returned": 0.0, "cost": null, "margin": null, "listPrice": "60.00", "duedate": "2023-06-22T00:00:00", "uom": null, "bin": null, "lot": null, "serials": null},{"lineNumber": 2, "item": {"name": "3GT-VENT-BLACK"}, "class": {"id": 1, "name": "Ecoological"}, "job": null, "workcenter": null, "tax": {"taxable": true, "taxCode": null}, "linkedTransaction": null, "description": "3GT-VENT-BLACK", "quantity": 1, "weight": 0.0, "volume": 0.0, "weightunit": "lb", "volumeunit": "cbm", "percentdiscount": 0, "unitprice": 30.0, "amount": 30.0, "altAmount": 0.0, "picked": 0.0, "shipped": 0.0, "returned": 0.0, "cost": null, "margin": null, "listPrice": "60.00", "duedate": "2023-06-22T00:00:00", "uom": null, "bin": null, "lot": null, "serials": null}'
    expected = [{'lineNumber': 1, 'item': {'name': 'MESO Customs:CLIMATE-KNOBS-DZ-BLACK'}, 'class': {'id': 1, 'name': 'Ecoological'}, 'job': None, 'workcenter': None, 'tax': {'taxable': True, 'taxCode': None}, 'linkedTransaction': None, 'description': 'Climate Control Rings // DUAL ZONE // BLACK', 'quantity': 1, 'weight': 0.0, 'volume': 0.0, 'weightunit': 'lb', 'volumeunit': 'cbm', 'percentdiscount': 0, 'unitprice': 30.0, 'amount': 30.0, 'altAmount': 0.0, 'picked': 0.0, 'shipped': 0.0, 'returned': 0.0, 'cost': None, 'margin': None, 'listPrice': '60.00', 'duedate': '2023-06-22T00:00:00', 'uom': None, 'bin': None, 'lot': None, 'serials': None}, {'lineNumber': 2, 'item': {'name': '3GT-VENT-BLACK'}, 'class': {'id': 1, 'name': 'Ecoological'}, 'job': None, 'workcenter': None, 'tax': {'taxable': True, 'taxCode': None}, 'linkedTransaction': None, 'description': '3GT-VENT-BLACK', 'quantity': 1, 'weight': 0.0, 'volume': 0.0, 'weightunit': 'lb', 'volumeunit': 'cbm', 'percentdiscount': 0, 'unitprice': 30.0, 'amount': 30.0, 'altAmount': 0.0, 'picked': 0.0, 'shipped': 0.0, 'returned': 0.0, 'cost': None, 'margin': None, 'listPrice': '60.00', 'duedate': '2023-06-22T00:00:00', 'uom': None, 'bin': None, 'lot': None, 'serials': None}]
    print("expected: ", expected)
    actual = clean_purchased_products_list(test_purchased_products_list_multiple_line_items)
    print("actual: ", actual)
    assert (actual == expected)


def test_clean_purchased_products_list_single_line_item():
    test_purchased_products_list_single_line_item = '{"lineNumber": 1, "item": {"name": "BumperShellz:EK4001"}, "class": {"id": 1, "name": "Ecoological"}, "job": null, "workcenter": null, "tax": {"taxable": false, "taxCode": null}, "linkedTransaction": null, "description": "Make: CHEVY Model: SILVERADO 1500 Year: \'19-\'23 Location: REAR BUMPER Color: GLOSS BLACK Alt1: WITH Sensor Holes Alt2: DUAL EXHAUST # of Pieces: 3", "quantity": 1, "weight": 0.0, "volume": 0.0, "weightunit": "lb", "volumeunit": "cbm", "percentdiscount": 0, "unitprice": 204.95, "amount": 204.95, "altAmount": 0.0, "picked": 0.0, "shipped": 0.0, "returned": 0.0, "cost": null, "margin": null, "listPrice": "30.0", "duedate": "2023-05-21T00:00:00", "uom": null, "bin": null, "lot": null, "serials": null}'
    expected = [{'lineNumber': 1, 'item': {'name': 'BumperShellz:EK4001'}, 'class': {'id': 1, 'name': 'Ecoological'}, 'job': None, 'workcenter': None, 'tax': {'taxable': False, 'taxCode': None}, 'linkedTransaction': None, 'description': 'Make: CHEVY Model: SILVERADO 1500 Year: 19-23 Location: REAR BUMPER Color: GLOSS BLACK Alt1: WITH Sensor Holes Alt2: DUAL EXHAUST # of Pieces: 3', 'quantity': 1, 'weight': 0.0, 'volume': 0.0, 'weightunit': 'lb', 'volumeunit': 'cbm', 'percentdiscount': 0, 'unitprice': 204.95, 'amount': 204.95, 'altAmount': 0.0, 'picked': 0.0, 'shipped': 0.0, 'returned': 0.0, 'cost': None, 'margin': None, 'listPrice': '30.0', 'duedate': '2023-05-21T00:00:00', 'uom': None, 'bin': None, 'lot': None, 'serials': None}]
    print("expected: ", expected)
    actual = clean_purchased_products_list(test_purchased_products_list_single_line_item)
    print('actual:', actual)
    assert (actual == expected)



