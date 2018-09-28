#!/usr/bin/env python
# coding: utf-8

"""
=====
NOTES
=====

- https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
- https://github.com/awslabs/aws-apigateway-lambda-authorizer-blueprints
- https://aws.amazon.com/blogs/compute/introducing-custom-authorizers-in-amazon-api-gateway/
"""
from __future__ import print_function

import re
import os
import string
import time
import pprint
import json
import logging
import logging.handlers
import urllib
import ConfigParser
from token_verifier_lambda import token_verifier

handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE", "./test-lambda.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)
 


def lambda_handler(event, context):
    """
    https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model-handler-types.html
    :param event:
    :param context: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """
    logger.info("event: {}".format(event))
    logger.info("context: {}".format(context))
    project_name = event.get('project_name')
    application = event.get('application')
    job_name = "api_gateway_authorizer_v1_{app}".format(app=application)
    logger.info("JOB: {} - {}".format(project_name, job_name))
    print("Client token: " + event['authorizationToken'])
    print("Method ARN: " + event['methodArn'])

    # Call Token verifier func
    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(event['region'], event['userpool_id'])
    response = urllib.urlopen(keys_url)
    keys = json.loads(response.read())['keys']
    token = event["authorizationToken"]
    claims, res = token_verifier(keys, token)

    # # Use this instead with google_auth keys
    # claims, res = token_verifier_lambda.google_token_verifier(token, event['app_client_id'])
    if res is False:
        logger.error("Unauthorized user!")
        logger.error("User Pool not authorized to access API Gateway. See logs for job success or failure status.")
        return generatePolicy(None, None, 'Deny', event['methodArn'])

    principalId = claims["sub"]
    logger.info("Principal Id: {}".format(principalId))
    authResponse = generatePolicy(principalId, claims['username'], 'Allow', event['methodArn'])

    logger.info("Policy: {}".format(authResponse))
    logger.info("User Pool authorized to access API Gateway. See logs for job success or failure status.")
    return authResponse


def generatePolicy(principalId, name, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
 
        authResponse['policyDocument'] = policyDocument
 
        if name is not None:
            context = {
                'name': name
            }
            authResponse['context'] = context
 
    return authResponse


#################################################
if __name__ == "__main__":
    from collections import namedtuple
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    region = config.get('aws', 'AWS_DEFAULT_REGION')
    id_token = config.get('cognito', 'ID_TOKEN')
    userpool_id = config.get('cognito', 'USERPOOL_ID')
    app_client_id = config.get('cognito', 'APP_CLIENT_ID')
    arn = config.get('cognito', 'METHOD_ARN')
    region = config.get('aws', 'AWS_DEFAULT_REGION')
    
    
    event = {
        "project_name": "ares",
        "application": "API Gateway Authorizer",
        "worker_function_name": "",
        "region": region,
        "userpool_id": userpool_id,
        "authorizationToken": id_token,
        "app_client_id": app_client_id,
        "methodArn": arn,
    }

    nt = namedtuple('test', 'function_name value')
    context = nt("function_name", "ares")
    
    job_status = lambda_handler(event=event, context=context)