import sys
import time
import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist

# Import models
from fetch_data.models import Key

from fetch_data.models import Piscine
from fetch_data.models import User, Project, Cursus
from fetch_data.models import ClusterLocation
from fetch_data.models import CursusProject
# End Import models

# Load environment variables from .env file
# load_dotenv(".env")
# API_URL = os.getenv("API_URL")
# auth_server_url = os.getenv("AUTH_SERVER")
API_URL = "https://api.intra.42.fr/v2"
auth_server_url='https://api.intra.42.fr/v2/oauth/token'

tokens = []  # Initialize an empty list to store the tokens

def updateTokenInfo(save, uid, secret):
    time_now = time.time()
    token_req_payload = {'grant_type': 'client_credentials'}
    response = requests.post(
        auth_server_url,
        data = token_req_payload, verify = True, allow_redirects = False,
        auth = (uid, secret)
    )
    res_json = response.json()
    save.token = res_json["access_token"]
    save.valid_until = int(res_json["expires_in"]) + int(time_now)
    dt_object = datetime.utcfromtimestamp(int(res_json["secret_valid_until"]))
    save.expire_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    save.save()


def printTokenInfo(info):
    time_now = int(time.time())
    print(f"name:        {info.name}")
    print(f"uid:         {info.uid}")
    print(f"secret:      {info.secret}")
    print(f"token:       {info.token}")
    print(f"valid_until: {info.valid_until}")
    print(f"valid_for:   {int(info.valid_until) - time_now}")
    print(f"expire_date: {info.expire_date}")

def checkExpirationDate(expire_date):
    # Parse the given datetime string into a datetime object
    given_time = datetime.strptime(expire_date, "%Y-%m-%d %H:%M:%S")
    # Get the current time
    current_time = datetime.now()
    # Check if the current time is later than the given time
    return current_time > given_time

def needToUpdate(token_obj):
    actual_time = int(time.time())
    print(f"-------------------")
    if not token_obj.token or not token_obj.valid_until or not token_obj.expire_date:
        print(f"update [{token_obj.name}]: missing info")
        return True
    if int(token_obj.valid_until) <= actual_time:
        print(f"update [{token_obj.name}]: token expired")
        return True
    if checkExpirationDate(token_obj.expire_date) == True:
        print(f"update [{token_obj.name}]: secret expired")
        return True
    return False

def initializeTokens():
    """Populates the tokens list with all Key objects."""
    global tokens
    tokens = list(Key.objects.all())

def chooseToken():
    """Returns the next token in the sequence, wrapping around to the first token after the last."""
    global tokens
    if not tokens:
        initializeTokens()  # Ensure tokens are initialized if they haven't been yet
    
    if tokens:
        chosen_token = tokens.pop(0)  # Remove and return the first token
        tokens.append(chosen_token) # Add the removed token to the end
        if chosen_token.name == '1_LOGIN':
            chosen_token = tokens.pop(0)  # Remove and return the first token
            tokens.append(chosen_token) # Add the removed token to the end
        if needToUpdate(chosen_token):
            updateTokenInfo(chosen_token, chosen_token.uid, chosen_token.secret)
            printTokenInfo(chosen_token)
        return chosen_token
    else:
        raise Exception("No tokens available")

def makeRequest(petition, add_params):
    try:
        token_obj = chooseToken()
        params = {
            "grant_type": "client_credentials",
            "access_token": token_obj.token,
        }
        params.update(add_params)
        
        # Make the GET request
        response = requests.get(petition, params)
        
        # Check for common HTTP errors
        if response.status_code == 400:
            print("Error 400: The request is malformed.")
        elif response.status_code == 401:
            print("Error 401: Unauthorized.")
        elif response.status_code == 403:
            print("Error 403: Forbidden.")
        elif response.status_code == 404:
            print("Error 404: Page or resource is not found.")
        elif response.status_code == 422:
            print("Error 422: Unprocessable entity.")
        elif response.status_code == 500:
            print("Error 500: We have a problem with our server. Please try again later.")
        elif "connection refused" in response.text.lower():
            print("Connection refused: Most likely cause is not using HTTPS.")

        # Proceed if the response was successful (200 OK)
        if response.status_code == 200:
            data = json.loads(response.text)
            time.sleep(0.51)
            return data
        else:
            raise Exception(f"Failed to retrieve data: {response.status_code}")
    except Exception as e:
        print(f"HTTP request: {petition} failed, retry in 10 secondini")
        time.sleep(10)
        return (makeRequest(petition, add_params))

