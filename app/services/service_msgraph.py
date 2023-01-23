from decouple import config
from fastapi.responses import JSONResponse
from msal import ConfidentialClientApplication, PublicClientApplication
import requests

class MSGraphService:
    def __init__(self):
        self.msgraph_client_id = None
        self.msgraph_client_secret = None
        self.msgraph_tenant_id = None
        self.msgraph_authority = 'https://login.microsoftonline.com/'
        self.msgraph_scope = [config("MSGRAPH_SCOPE")]
        self.msgraph_endpoint = config("MSGRAPH_ENDPOINT")

    def config(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id):
        content = {"message": True}
        response = JSONResponse(content=content)
        response.set_cookie(key='msgraph_client_id', value=msgraph_client_id)
        response.set_cookie(key='msgraph_client_secret', value=msgraph_client_secret)
        response.set_cookie(key='msgraph_tenant_id', value=msgraph_tenant_id)
        return response

    def az_connect(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id):
        app = ConfidentialClientApplication(msgraph_client_id, authority=self.msgraph_authority + msgraph_tenant_id, client_credential=msgraph_client_secret)
        token = app.acquire_token_silent(self.msgraph_scope, account=None)
        if token:
            access_token = 'Bearer ' + token['access_token']
            print('Access token was loaded from cache')
        if not token:
            token = app.acquire_token_for_client(scopes=self.msgraph_scope)
            access_token = 'Bearer ' + token['access_token']
            print('New access token was acquired from Azure AD')
        return access_token

    def bind_connect(self, msgraph_client_id, msgraph_tenant_id, username, password):
        app = PublicClientApplication(msgraph_client_id, authority=self.msgraph_authority + msgraph_tenant_id)
        token = None
        accounts = app.get_accounts()
        if accounts:
            # If so, you could then somehow display these accounts and let end user choose
            print("Pick the account you want to use to proceed:")
            for a in accounts:
                print(a["username"])
            # Assuming the end user chose this one
            chosen = accounts[0]
            # Now let's try to find a token in cache for this account
            token = app.acquire_token_silent(["User.Read"], account=chosen)
            access_token = 'Bearer ' + token['access_token']

        if not token:
            # So no suitable token exists in cache. Let's get a new one from AAD.
            token = app.acquire_token_by_username_password(username, password, scopes=["User.Read"])
            access_token = 'Bearer ' + token['access_token']
        return access_token

    def service_health(self):
        access_token = self.az_connect()
        url = f'{self.msgraph_endpoint}/admin/serviceAnnouncement/healthOverviews/Microsoft 365 suite?$expand=issues'
        headers = {
            'Authorization': access_token
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def all_users(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users'
        headers = {
            'Authorization': access_token
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def search_user(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}'
        headers = {
            'Authorization': access_token
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def license_user(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}/licenseDetails'
        headers = {
            'Authorization': access_token
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def get_skuId(self, license):
        data = {
            "Office 365 A1 Plus for faculty": "78e66a63-337a-4a9a-8959-41c6654dfb56",
            "Office 365 A1 Plus for students": "e82ae690-a2d5-4d76-8d30-7c6e01e6022e",
            "Office 365 A1 for faculty": "94763226-9b3c-4e75-a931-5c89701abe66",
            "Office 365 A1 for students": "314c4481-f395-4525-be8b-2ec4bb1e9d91"
        }
        return data[license]

    def assign_license(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username, license):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}/assignLicense'
        skuId = self.get_skuId(license)
        headers = {
            'Authorization': access_token
        }
        data = {
            "addLicenses": [
                {
                "disabledPlans": [],
                "skuId": skuId
                }
            ],
            "removeLicenses": []
        }
        try:
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(status_code=response.status_code, content={"message": response.reason})
        except Exception as e:
            return e

    def change_license(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username, old_license, new_license):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}/assignLicense'
        new_skuId = self.get_skuId(new_license)
        old_skuId = self.get_skuId(old_license)
        headers = {
            'Authorization': access_token
        }
        data = {
            "addLicenses": [
                {
                "disabledPlans": [],
                "skuId": new_skuId
                }
            ],
            "removeLicenses": [old_skuId]
        }
        try:
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(status_code=response.status_code, content={"message": response.reason})
        except Exception as e:
            return e

    def remove_license(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username, license):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}/assignLicense'
        skuId = self.get_skuId(license)
        headers = {
            'Authorization': access_token
        }
        data = {
            "addLicenses": [
                {
                "disabledPlans": [],
                "skuId": skuId
                }
            ],
            "removeLicenses": [skuId]
        }
        try:
            response = requests.post(url=url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                return JSONResponse(status_code=response.status_code, content={"message": response.reason})
        except Exception as e:
            return e

    def create_user(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, display_name, given_name, surname, job_title, mail, mobile_phone, principle_name, password):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = 'https://graph.microsoft.com/v1.0/users/'
        headers = {
            'Authorization': access_token
        }
        data = {
            "accountEnabled": True,
            "displayName": display_name,
            "givenName": given_name,
            "surname": surname,
            "jobTitle": job_title,
            "mail": mail,
            "mobilePhone": mobile_phone,
            "mailNickname": "Steve",
            "userPrincipalName": principle_name,
            "preferredLanguage": "en-US",
            "usageLocation": "US",
            "passwordProfile" : {
                "forceChangePasswordNextSignIn": False,
                "password": password
            }
        }
        response = requests.post(url=url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def update_user(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username, account_enable, display_name, given_name, surname, job_title, mobile_phone):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}'
        headers = {
            'Authorization': access_token
        }
        data = {
            "accountEnabled": account_enable,
            "displayName": display_name,
            "givenName": given_name,
            "surname": surname,
            "jobTitle": job_title,
            "mobilePhone": mobile_phone,
            "mailNickname": "Steve",
            "preferredLanguage": "en-US",
            "usageLocation": "US"
        }
        # Remove key in dictionary with None values
        filtered = {k: v for k, v in data.items() if v is not None}
        data.clear()
        data.update(filtered)
        response = requests.patch(url=url, headers=headers, json=data)

        if response.status_code == 204:
            return JSONResponse(status_code=200, content={"message": True})
        elif response.status_code == 404:
            return JSONResponse(status_code=404, content={"message": 'Not Found'})
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def delete_user(self, msgraph_client_id, msgraph_client_secret, msgraph_tenant_id, username):
        access_token = self.az_connect(msgraph_client_id, msgraph_client_secret, msgraph_tenant_id)
        url = f'{self.msgraph_endpoint}/users/{username}'
        headers = {
            'Authorization': access_token
        }
        response = requests.delete(url=url, headers=headers)

        if response.status_code == 204:
            return JSONResponse(status_code=200, content={"message": True})
        elif response.status_code == 404:
            return JSONResponse(status_code=404, content={"message": 'Not Found'})
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})

    def reset_password(self, msgraph_client_id, msgraph_tenant_id, username, old_password, new_password):
        access_token = self.bind_connect(msgraph_client_id, msgraph_tenant_id, username, old_password)
        url = f'{self.msgraph_endpoint}/users/{username}'
        headers = {
            'Authorization': access_token
        }
        data = {
            "passwordProfile" : {
                "forceChangePasswordNextSignIn": False,
                "password": new_password
            }
        }
        response = requests.patch(url=url, headers=headers, json=data)
        print(response)

        if response.status_code == 204:
            return JSONResponse(status_code=200, content={"message": True})
        elif response.status_code == 404:
            return JSONResponse(status_code=404, content={"message": 'Not Found'})
        else:
            return JSONResponse(status_code=response.status_code, content={"message": response.reason})