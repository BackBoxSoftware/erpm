#!/usr/bin/python
# -*- coding: utf-8 -*-
#  This script demonstrates:
#  1. Authenticating to the Lieberman ERPM PAM / EPV API
#  3. Requesting & returning a password key by account & target ID
#

import ssl
import json
import urllib2

# API User account details
username = 'app1'  # sys.argv[1]
password = 'Password1!'  # sys.argv[2]


def get_password():
    # Create a fake SSL context to ignore the certificate error
    # Don 't EVER do this in production, this is for local sandbox testing
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # specify connection details
    erpm_host = 'https://13.65.145.0'  # ERPM Web Service
    checkout_comment = 'Checking out a password'  # A comment to use when checking out the key
    target_name = 'dfw-vpd-pamapp1'

    # specify the needed endpoint URIs
    # Endpoint to get the API token
    token_endpoint = '/ERPMWebService/json/V2/AuthService.svc/DoLogin2'

    # Endpoint for checking out a password
    stored_account_co_endpoint = '/ERPMWebService/JSON/V2/AuthService.svc/AccountStoreOps_StoredCredential_CheckOut'

    # Get the API authentication token
    auth_token_request = urllib2.Request(erpm_host + token_endpoint)
    auth_token_request.add_header('Content-Type', 'application/json')
    auth_token_response = urllib2.urlopen(auth_token_request, context=ctx, data=json.dumps({'LoginType': 1,
                                                                                            'Password': password,
                                                                                            'Username': username}))

    api_auth_token = json.loads(auth_token_response.read())['OperationMessage']

    # Format the PW checkout message
    sp_checkout_message = json.dumps({"AuthenticationToken": api_auth_token,
                                      "AccountIdentificationInfo": {"AccountName": "ACME\\testapp",
                                                                    "AccountStore": {"CustomTypeName": "",
                                                                                     "TargetName": target_name,
                                                                                     "Type": 1}, "PasswordList": ""},
                                      "Comment": checkout_comment})

    sp_checkout_request = urllib2.Request(erpm_host + stored_account_co_endpoint)
    sp_checkout_request.add_header('Content-Type', 'application/json')
    sp_checkout_response = urllib2.urlopen(sp_checkout_request, context=ctx, data=sp_checkout_message)

    stored_password = json.loads(sp_checkout_response.read())['Password']

    # Return the account list
    return stored_password


def main():
    stored_password = get_password()
    print stored_password


main()
