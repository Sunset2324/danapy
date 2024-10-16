# -*- coding: utf-8 -*-
import os, sys
import requests

path = os.path.join(os.path.dirname(__file__),'../model')
sys.path.insert(0, path)

from models.auth import Auth
from models import etc
from models import error

class DanaClient:
    BASE_URL = 'https://api.dana.id/'

    def __init__(self, app_id=None, device_id=None, token=None, debug=False):
        self.session = requests.session()
        self.session.headers = {
            'app-id': app_id,
            'device-id': device_id,
        }
        self.app_id = app_id
        self.device_id = device_id
        self.token = token
        self.debug = debug
        self.logged_in = False

    # Utility method to make HTTP requests
    def req(self, method, url, *args, **kwargs):
        full_url = self.BASE_URL + url
        try:
            response = getattr(self.session, method)(full_url, *args, **kwargs)
            response.raise_for_status()
            if self.debug:
                print(response.text)
            return response
        except requests.HTTPError as err:
            raise Exception(f"HTTP error: {err}")
        except requests.RequestException as e:
            raise Exception(f"Request error: {e}")
    
    # Check if the user is logged in
    def need_logged_in(f):
        def wrap_kargs(*args, **kwargs):
            self = args[0]
            if self.logged_in:
                return f(*args, **kwargs)
            else:
                raise Exception('You need to log in to perform this action.')
        return wrap_kargs
    
    # Login method
    def login(self, username, password):
        response = self.req('post', 'login', json={'username': username, 'password': password})
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            self.logged_in = True
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            print("Login successful.")
        else:
            raise Exception("Login failed.")
    
    # Logout method
    def logout(self):
        if not self.logged_in:
            print("Already logged out.")
            return
        response = self.req('get', 'logout')
        if response.status_code == 200:
            self.logged_in = False
            print("Logout successful.")
        else:
            raise Exception("Logout failed.")

    # Method to check account mutation (history of transactions)
    @need_logged_in
    def cek_mutasi(self):
        response = self.req('get', 'cek_mutasi')
        return response.json()
    
    # Method to transfer balance to another account
    @need_logged_in
    def transfer(self, tujuan, jumlah):
        data = {'tujuan': tujuan, 'jumlah': jumlah}
        response = self.req('post', 'transfer', json=data)
        if response.status_code == 200:
            print("Transfer successful.")
        else:
            raise Exception("Transfer failed.")
        return response.json()
    
    # Method to save transfer receipt for auditing
    @need_logged_in
    def simpan_bukti_transfer(self, transfer_data):
        response = self.req('post', 'simpan_bukti_transfer', json=transfer_data)
        if response.status_code == 200:
            print("Receipt saved.")
        else:
            raise Exception("Failed to save receipt.")
        return response.json()

# Example of usage
if __name__ == '__main__':
    client = DanaClient(app_id="your-app-id", device_id="your-device-id", debug=True)

    # Login
    try:
        client.login('your-username', 'your-password')
        
        # Cek mutasi rekening
        mutasi = client.cek_mutasi()
        print("Account mutation:", mutasi)
        
        # Transfer dana
        transfer_result = client.transfer('target-phone-number', 50000)
        print("Transfer Result:", transfer_result)
        
        # Simpan bukti transfer
        receipt = client.simpan_bukti_transfer(transfer_result)
        print("Receipt:", receipt)
        
        # Logout
        client.logout()

    except Exception as e:
        print(f"Error: {e}")
