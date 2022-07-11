""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import requests, json, time

def get_templates(host, token):
    headers = {
              'content-type': "application/json",
              'x-auth-token': token
          }

    url = "https://{}/dna/intent/api/v1/template-programmer/template".format(host)
    resp = requests.get(url, headers=headers, verify=False)

    return resp.json()

def get_switches(host, token):
    headers = {
              'content-type': "application/json",
              'x-auth-token': token
          }

    url = "https://{}/dna/intent/api/v1/network-device".format(host)
    resp = requests.get(url, headers=headers, verify=False)

    result = []
    for device in resp.json()['response']:
        if device['family'] == "Switches and Hubs":
            result += [device]
    
    return result

def apply_template(template_id, device_id, host, token):
    headers = {
              'content-type': "application/json",
              'x-auth-token': token
          }

    url = "https://{}/dna/intent/api/v2/template-programmer/template?id={}".format(host, template_id)
    resp = requests.get(url, headers=headers, verify=False)
    
    body = {
        "forcePushTemplate": True,
        "targetInfo": [
            {
                "id": get_ip(device_id, host, token),
                "params": {},
                "type": "MANAGED_DEVICE_IP",
            }
        ],
        "templateId": template_id  
    }

    url = "https://{}/dna/intent/api/v2/template-programmer/template/deploy".format(host)
    resp = requests.post(url, headers=headers, data=json.dumps(body), verify=False)
    print('task result: ' + json.dumps(resp.json()))

    task_id = resp.json()['response']['url']
    url = "https://{}{}".format(host, task_id)
    resp = requests.get(url, headers=headers, data=json.dumps(body), verify=False)
    print(resp.json())
    count = 3
    while count > 0:
        time.sleep(5)
        resp = requests.get(url, headers=headers, data=json.dumps(body), verify=False)
        print(resp.json())
        count -= 1

def get_ip(device, host, token):
    headers = {
              'content-type': "application/json",
              'x-auth-token': token
          }

    url = "https://{}/dna/intent/api/v1/network-device/{}".format(host, device)
    resp = requests.get(url, headers=headers, verify=False)

    return resp.json()['response']['managementIpAddress']

# Get DNAC API token
def get_dnac_token(host, username, password):
    headers = {
              'content-type': "application/json",
              'x-auth-token': ""
          }

    url = "https://{}/api/system/v1/auth/token".format(host)
    response = requests.request("POST", url, auth=requests.auth.HTTPBasicAuth(username, password),
                                headers=headers, verify=False)
    return response.json()["Token"]