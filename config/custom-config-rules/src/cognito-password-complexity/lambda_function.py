# AWS Config Custom rule to evaluate compliance for AWS Cognito user pools having defined parameters for password policy.
#
# The following parameters must be set in AWS Config for the rule to not return error:
# RequireUppercase: (boolean)
# RequireLowercase: (boolean)
# RequireNumbers: (boolean)
# RequireSymbols: (boolean)
# TemporaryPasswordValidityDays: (integer)
# MinimumLength: (integer)
#
# Rule type: Periodic
# 
# Note: Uses paginator but list_user_pools() requires a MaxResult paramaeter (set to 60).
#


import json
import boto3


def lambda_handler(event, context):
    # Initialize the AWS Config client
    config_client = boto3.client('config')

    # Initialize the Cognito Identity Provider client
    cognito_client = boto3.client('cognito-idp')

    # Get the required parameter values from the AWS Config rule parameters
    try:
        rule_parameters = json.loads(event['ruleParameters'])
        require_uppercase = rule_parameters['RequireUppercase']
        require_lowercase = rule_parameters['RequireLowercase']
        require_numbers = rule_parameters['RequireNumbers']
        require_symbols = rule_parameters['RequireSymbols']
        temp_password_validity_days = int(
            rule_parameters['TemporaryPasswordValidityDays'])
        minimum_length = int(rule_parameters['MinimumLength'])
    except cognito_client.exceptions.InvalidParameterValueException as err:
        # If any required parameters are missing, report an error
        raise err

    # Get all user pools using paginator
    user_pools = []
    paginator = cognito_client.get_paginator('list_user_pools')
    for page in paginator.paginate(MaxResults=60):
        user_pools.extend(page['UserPools'])

    # Check password policy for each user pool
    for pool in user_pools:
        pool_id = pool['Id']
        pool_name = pool['Name']

        # Get the password policy for the user pool
        password_policy_response = cognito_client.describe_user_pool(UserPoolId=pool_id)
        password_policy = password_policy_response['UserPool']['Policies']['PasswordPolicy']

# Evaluate the password policy parameters
        compliance_reason = []
        if password_policy['MinimumLength'] < minimum_length:
            compliance_reason.append(
                f"Minimum length less than {minimum_length}")
        if require_uppercase and not password_policy['RequireUppercase']:
            compliance_reason.append(
                f"Uppercase characters required")
        if require_lowercase and not password_policy['RequireLowercase']:
            compliance_reason.append(
                f"Lowercase characters required")
        if require_numbers and not password_policy['RequireNumbers']:
            compliance_reason.append(
                f"Numbers required")
        if require_symbols and not password_policy['RequireSymbols']:
            compliance_reason.append(
                f"Special characters required")
        if password_policy['TemporaryPasswordValidityDays'] > temp_password_validity_days:
            compliance_reason.append(
                f"Temp password validity greater than {temp_password_validity_days}")

        if compliance_reason:
            # If any compliance reason was found, the user pool is non-compliant
            evaluation = 'NON_COMPLIANT'
            compliance_reason = f"{pool_name} has a non-compliant password policy: {'; '.join(compliance_reason)}"
        else:
            # If no compliance reasons were found, the user pool is compliant
            evaluation = 'COMPLIANT'
            compliance_reason = f"{pool_name} has a compliant password policy."
        # Send the evaluation result to AWS Config
        config_client.put_evaluations(
            Evaluations=[
                {
                    'ComplianceResourceType': 'AWS::Cognito::UserPool',
                    'ComplianceResourceId': pool_id,
                    'ComplianceType': evaluation,
                    'Annotation': compliance_reason,
                    'OrderingTimestamp': json.loads(event['invokingEvent'])['notificationCreationTime']
                },
            ],
            ResultToken=event['resultToken']
        )