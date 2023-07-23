from input_data import *
import json
import time
import urllib3
import certifi

for key in input_data:
    if input_data[key] is None or input_data[key] == '\"\"':
        input_data[key] = ""
    input_data[key] = input_data[key].strip('\"')

access_token = input_data["access_token"]
customer_name = input_data["customer_name"]

connect_timeout = 10.0
read_timeout = 20.0
http_object = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=connect_timeout, read=read_timeout)
)


def create_new_customer(new_customer_name, request_access_token, http):
    time.sleep(1)
    encoded_body = json.dumps(new_customer_name)
    resp = http.request(
        "POST",
        "https://api.sosinventory.com/api/v2/customer/",
        headers={
            'Authorization': 'Bearer ' + request_access_token,
            'Host': 'api.sosinventory.com'
        },
        body=encoded_body
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    return json_object


def get_customer_id(checking_customer_name, request_access_token, http):
    time.sleep(1)
    resp = http.request(
        "GET",
        "https://api.sosinventory.com/api/v2/customer?start=0&maxresults=200&name=" + checking_customer_name,
        headers={
            'Authorization': 'Bearer ' + request_access_token,
            'Host': 'api.sosinventory.com'
        }
    )
    json_object = json.loads(resp.data.decode("utf-8"))
    return json_object


customer = get_customer_id(customer_name, access_token, http_object)
print(customer)
if customer["totalCount"] == 0:
    print("Customer does not exist, creating new customer_name_item")
    customer_name_body = {
        "name": customer_name
    }
    create_new_customer_return = create_new_customer(customer_name_body, access_token, http_object)
    print(create_new_customer_return)
    if create_new_customer_return["status"] != "ok":
        print("Error creating customer_name_item")
        raise Exception("Error creating customer_name_item")
    customer_id = create_new_customer_return["data"]["id"]
    print("Customer created successfully")
    print("Customer ID: " + str(customer_id))
else:
    customer_id = customer["data"][0]["id"]
    print("Customer already exists, customer_name_item ID: " + str(customer_id))

output = [{'customer_id': customer_id}]
