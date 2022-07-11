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

# Import Section
from flask import Flask, render_template, request, url_for, redirect
import json, dnac_app, os
from dotenv import load_dotenv

# load all environment variables
load_dotenv()


# Global variables
app = Flask(__name__)

#Read data from json file
def getJson(filepath):
	with open(filepath, 'r') as f:
		json_content = json.loads(f.read())
		f.close()

	return json_content

#Write data to json file
def writeJson(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)
    f.close()


##Routes
#Instructions

#Index
@app.route('/', methods=["GET", "POST"])
def index():
    try:
        host = os.environ['DNAC_HOST']
        token = dnac_app.get_dnac_token(host, os.environ['DNAC_USER'], os.environ['DNAC_PASS'])
        switches = dnac_app.get_switches(host, token)
        templates = dnac_app.get_templates(host, token)
        
        if request.method == "POST":
            selected_switches = dict(request.form.lists())['switch']
            selected_template = request.form.get('template')
            for switch in selected_switches:
                dnac_app.apply_template(selected_template, switch, host, token)
            
        return render_template('home.html', switches=switches, templates=templates, hiddenLinks=True)
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('home.html', error=False, errormessage="", errorcode=e)
   
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8756, debug=True)