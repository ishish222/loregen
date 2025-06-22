import boto3
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

ENVIRONMENT = os.environ['ENVIRONMENT']


def get_secret(secret_arn):
    secrets_client = boto3.client('secretsmanager')
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return response['SecretString']
