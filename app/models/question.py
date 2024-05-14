from app import db

####
import requests
import os
import json
####

##### .env
from os.path import join, dirname
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()
#####

# モデルに関する設定
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    body = db.Column(db.String(255))
    # Userに所有されている状態
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', name='user_id__question_id_fk'))

    @classmethod
    def from_args(cls, title: str, body: str, user_id: int):
        instance = cls()
        instance.title = title
        instance.body = body
        instance.user_id = user_id
        return instance

    def find_sfdc_data():

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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

    ######################################################################################
    def find_sfdc_data_id(id: str):

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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

        #####
        id_len = len(id)
        if id_len == 18:
            api_url = instance_url + "/services/data/" + sfdc_api_ver + "/query?q=SELECT+Id%2cName%2cShippingAddress+FROM+Account+WHERE+Id='" + id + "'"

            print(api_headers)
            print(api_url)

            api_response = requests.get(api_url, headers=api_headers, timeout=60)
            if api_response.status_code != 200:
                print("sfdc api get data connect error.")

            api_response_info = json.loads(api_response.text)
            print(json.dumps(api_response_info, indent=2))
            return api_response.text

        else:
            return "指定したSalesforceレコードIDのSalesfoce取引先データはありませんでした。"

    ######################################################################################
    def find_sfdc_search_data(id: str):

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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

        #####
        id_len = len(id)
        if id_len == 18:
            api_url = instance_url + "/services/data/" + sfdc_api_ver + "/query?q=SELECT+Id%2cName%2cShippingAddress+FROM+Account+WHERE+Id='" + id + "'"

            print(api_headers)
            print(api_url)

            api_response = requests.get(api_url, headers=api_headers, timeout=60)
            if api_response.status_code != 200:
                print("sfdc api get data connect error.")

            api_response_info = json.loads(api_response.text)
            return api_response.text
        else:
            return "指定したSalesforceレコードIDのSalesfoce取引先データはありませんでした。"

    ######################################################################################
    def sfdc_data_update(id: str, name: str):

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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
            print("response.status_code")
            print(response.status_code)

        session = requests.Session()
        response_info = json.loads(response.text)
        instance_url = response_info['instance_url']
        access_token = response_info['access_token']
        print(response_info)
        print(instance_url)
        print(access_token)

        api_headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-type': 'application/json'}
        api_request_body = {
            "Name": name 
        }
        api_request_body_json_data = json.dumps(api_request_body).encode("utf-8")

        print("api_headers")
        print(api_headers)

        print("api_request_body")
        print(api_request_body)
        print(json.dumps(api_request_body))
        
        #####
        id_len = len(id)
        if id_len == 18:

            api_url = instance_url + "/services/data/" + sfdc_api_ver + "/sobjects/Account/" + id
            print(api_headers)
            print(api_url)

            api_response = requests.patch(api_url, headers=api_headers, data=api_request_body_json_data)

            if api_response.status_code != 200:
                print("sfdc api update data connect error.")
                print("api_response.status_code")
                print(api_response.status_code)

            return api_response.text
        else:
            return "指定したSalesforceレコードIDのSalesfoce取引先データはありませんでした。"

    ######################################################################################
    def sfdc_data_create(name: str, phone: str):

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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
            print("response.status_code")
            print(response.status_code)

        session = requests.Session()
        response_info = json.loads(response.text)
        instance_url = response_info['instance_url']
        access_token = response_info['access_token']
        print(response_info)
        print(instance_url)
        print(access_token)

        api_headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-type': 'application/json'}
        api_request_body = {
            "Name": name,
            "Phone": phone
        }
        api_request_body_json_data = json.dumps(api_request_body).encode("utf-8")

        print("api_headers")
        print(api_headers)

        print("api_request_body")
        print(api_request_body)
        print(json.dumps(api_request_body))
        
        #####
        name_len = len(name)
        if name_len >= 1:

            api_url = instance_url + "/services/data/" + sfdc_api_ver + "/sobjects/Account/"
            print(api_headers)
            print(api_url)

            api_response = requests.post(api_url, headers=api_headers, data=api_request_body_json_data)

            if api_response.status_code != 200:
                print("sfdc api update data connect error.")
                print("api_response.status_code")
                print(api_response.status_code)

            return api_response.text
        else:
            return "Salesfoce取引先データの作成に失敗しました。"

    ######################################################################################
    def sfdc_data_delete(id: str):

        #####
        sfdc_login_host = os.environ.get("DATABASEDOTCOM_HOST")
        sfdc_client_id = os.environ.get("DATABASEDOTCOM_CLIENT_ID")
        sfdc_client_secret = os.environ.get("DATABASEDOTCOM_CLIENT_SECRET")
        sfdc_api_username = os.environ.get("DATABASEDOTCOM_CLIENT_USERNAME")
        sfdc_api_password = os.environ.get("DATABASEDOTCOM_CLIENT_AUTHENTICATE_PASSWORD")
        sfdc_api_ver = os.environ.get("DATABASEDOTCOM_VER")

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
            print("response.status_code")
            print(response.status_code)

        session = requests.Session()
        response_info = json.loads(response.text)
        instance_url = response_info['instance_url']
        access_token = response_info['access_token']
        print(response_info)
        print(instance_url)
        print(access_token)

        api_headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-type': 'application/json'}
        api_request_body = {
            "Id": id
        }
        api_request_body_json_data = json.dumps(api_request_body).encode("utf-8")

        print("api_headers")
        print(api_headers)

        print("api_request_body")
        print(api_request_body)
        print(json.dumps(api_request_body))

        #####
        id_len = len(id)
        if id_len == 18:

            api_url = instance_url + "/services/data/" + sfdc_api_ver + "/sobjects/Account/" + id
            print(api_headers)
            print(api_url)

            api_response = requests.delete(api_url, headers=api_headers, data=api_request_body_json_data)

            if api_response.status_code != 200:
                print("sfdc api update data connect error.")
                print("api_response.status_code")
                print(api_response.status_code)

            return api_response.text
        else:
            return "Salesfoce取引先データの削除に失敗しました。指定したSalesforceレコードIDのSalesfoce取引先データはありませんでした。"
