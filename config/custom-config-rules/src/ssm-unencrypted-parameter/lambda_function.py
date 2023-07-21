# Custom Config Rule

import boto3
import json

# Lambda Handler
# SSM describe_parameters has max 50 results, so we need to paginate the results.


def lambda_handler(event, context):
    client = boto3.client('ssm')
    p = client.get_paginator('describe_parameters')
    paginator = p.paginate().build_full_result()

    evaluations = []
    orderingtime = json.loads(event['invokingEvent'])[
        'notificationCreationTime']

    # Evaluate Each Parameter, any type but SecureString will be non-compliant
    for page in paginator['Parameters']:
        if page['Type'] == 'SecureString':
            evaluations.append(
                {
                    'ComplianceResourceType': 'AWS::SSM::Parameter',
                    'ComplianceResourceId': page['Name'],
                    'ComplianceType': 'COMPLIANT',
                    'OrderingTimestamp': orderingtime
                }
            )
        else:
            evaluations.append(
                {
                    'ComplianceResourceType': 'AWS::SSM::Parameter',
                    'ComplianceResourceId': page['Name'],
                    'ComplianceType': 'NON_COMPLIANT',
                    'OrderingTimestamp': orderingtime
                }
            )

    result_token=event['resultToken']
    config=boto3.client('config')
    response=config.put_evaluations(
        Evaluations = evaluations,
        ResultToken = result_token,
        TestMode = False
    )
