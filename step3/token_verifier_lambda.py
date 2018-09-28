#!/usr/bin/env python
# coding: utf-8
# aws-labs: https://github.com/awslabs/aws-support-tools/tree/master/Cognito/decode-verify-jwt
from __future__ import print_function
from google.auth.transport import requests
from google.oauth2 import id_token
import time
import os
import requests

from jose import jwk, jwt
from jose.utils import base64url_decode



#################################################
def token_verifier(keys, token):

    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        logger.error('Public key not found in jwks.json')
        return None, False

    # construct the public key
    public_key = jwk.construct(keys[key_index])

    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)

    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        logger.error('Signature verification failed')
        return None, False

    logger.info('Signature successfully verified')

    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)

    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        logger.error('Token is expired')
        return None, False
    
    
    # now we can use the claims
    logger.info(" CLAIMS: {}".format(claims))
    return claims, True

def google_token_verifier(token, google_client_id):
    try:
        # Verify and get information from id_token
        reqUrl = google_client_id + '.apps.googleusercontent.com'
        userInfo = id_token.verify_oauth2_token(
            event['authorizationToken'], 
            requests.Request(), 
            reqUrl)
        logger.info("Google Info: {}".format(userInfo))
 
        # Deny access if the account is not a Google account
        if userInfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            logger.error("Token is not valid Google Auth")
            return None, False
 
        # Get principalId and name from userInfo
        principalId = userInfo['sub']
        name = userInfo['name']
 
    except ValueError as err:
        # Deny access if the token is invalid
        logger.error("Token not valid Google OAuth: {}".format(err))

    logger.info("CLAIMS: {}".format(userInfo))
    return userInfo, True