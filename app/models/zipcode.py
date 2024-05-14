import requests

##import xml.dom.minidom

####
import os
import json
####

##### .env
from os.path import join, dirname
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

####load_dotenv()
#####

class ZipCode():

    def find_all():

        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")
        print(sfdc_api_password)

        # Post-URL => {JSON}placeholderを利用する
        url = "https://" + sfdc_login_host + "/services/oauth2/token"
        #####

        headers = {'content-type':'application/x-www-form-urlencoded'}

        # リクエストボディを定義
        request_body = {
                      "grant_type": "password",
                      "client_id": sfdc_client_id,
                      "client_secret": sfdc_client_secret,
                      "username": sfdc_api_username,
                      "password": sfdc_api_password
            }

        response = requests.post(url, headers=headers, data=request_body)

        if response.status_code != 200:
            print("sfdc api connect error.")

        session = requests.Session()
        response_info = json.loads(response.text)
        instance_url = response_info['instance_url']
        access_token = response_info['access_token']
        print(response_info)
        print(instance_url)
        print(access_token)

        api_headers = {'Authorization': 'Bearer {}'.format(access_token)}

        api_url = instance_url + "/services/data/" + sfdc_api_ver + "/query?q=SELECT+Id%2cName%2cShippingAddress+FROM+Account+LIMIT+5"

        print(api_headers)
        print(api_url)

        api_response = requests.get(api_url, headers=api_headers, timeout=60)
        if api_response.status_code != 200:
            print("sfdc api get data connect error.")

        api_response_info = json.loads(api_response.text)
        print(json.dumps(api_response_info, indent=2))
        return api_response.text
