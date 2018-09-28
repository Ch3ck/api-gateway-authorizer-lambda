# api-gateway-authorizer-lambda
Secure your APIs with AWS Lambda authorizer functions


## Description
Experiments with AWS API Gateway containing scripts for verifying jwt tokens, λ authorizer function and basic λ function to return an api response

## Build
```
λ git clone https://github.com/Ch3ck/api-gateway-authorizer-lambda.git
λ cd api-gateway-authorizer-lambda
λ pip3 install awscli --upgrade --user
λ pip install -r requirements.txt
λ pip install . #install current lambda function locally
```

## Setup your AWS credentials
```
λ cd config
λ vim cred.ini # add required credentials
```

## Deploy
```
λ sh deploy.sh  #λ deployed!
```
The instructions for creating and/or updating the λ function on AWS is in the deploy.sh script. Feel free to comment out parts which are no longer necessary.

## Contributing
If you encounter a bug problems, I'll like to hear about it. Also, pull requests are welcomed