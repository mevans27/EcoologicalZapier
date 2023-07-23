from main import *


def test_get_customer_id_returns_customer_id_when_customer_exists():
    """Test get_customer_id returns test_customer_id when customer exists"""
    test_customer_name = 'Test Hello World'
    test_customer_id = 5144
    result = get_customer_id(test_customer_name, access_token, http_object)
    assert (result['totalCount'] == 1)
    assert (result['data'][0]['id'] == test_customer_id)