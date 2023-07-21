import json
import boto3

def lambda_handler(event, context):
    # Create clients
    config_client = boto3.client('config')
    workdocs_client = boto3.client('workdocs')
    ds_client = boto3.client('ds')
    
    rule_parameters = {}
    if 'ruleParameters' in event:
        rule_parameters = json.loads(event['ruleParameters'])

    domains = rule_parameters['WorkDocsDomain'].split(',')

    # Storing  time
    orderingtime = json.loads(event['invokingEvent'])[
        'notificationCreationTime']
    
    # Get all workdocs users from ds directories
    ds_paginator = ds_client.get_paginator('describe_directories')
    for page in ds_paginator.paginate():
        for directory in page['DirectoryDescriptions']:
            workdocs_paginator = workdocs_client.get_paginator('describe_users')
            for w_page in workdocs_paginator.paginate(OrganizationId=directory['DirectoryId']):
                for user in w_page['Users']:
                    # Get the user's email
                    email = user['EmailAddress']
                    email_domain = email.split('@')[1]
                    # Check if the email domain is in the list of domains
                    if email_domain in domains:
                        compliance_type = 'COMPLIANT'
                    else:
                        compliance_type = 'NON_COMPLIANT'

                    # Submit evaluation to AWS Config
                    config_client.put_evaluations(
                        Evaluations=[
                            {
                                'ComplianceResourceType': 'AWS::::Account',
                                'ComplianceResourceId': event['accountId'],
                                'ComplianceType': compliance_type,
                                'Annotation': f'Workdocs User {email} is {compliance_type} because user email domain is {email_domain}. Valid domains: {domains}.',
                                'OrderingTimestamp': orderingtime
                            },
                        ],
                        ResultToken=event['resultToken']
                    )

   