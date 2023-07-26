import boto3
import json



def lambda_handler(event, context):
    # Create RDS and Config clients
    rds_client = boto3.client('rds')
    config_client = boto3.client('config')

    # Storing time
    orderingtime = json.loads(event['invokingEvent'])[
        'notificationCreationTime']

    # Get all RDS instances
    response = rds_client.describe_db_instances()
    rds_instances = response['DBInstances']

    # Iterate through all RDS instances
    for instance in rds_instances:
        # Get the engine type and instance identifier
        engine = instance['Engine']
        instance_id = instance['DBInstanceIdentifier']

        # Check if the engine type is MySQL
        if engine.lower() in ['oracle-ee', 'oracle-ee-cdb', 'oracle-se2', 'oracle-se2-cdb']:

            # Get the option groups name for the current instance
            db_option_groups = instance['OptionGroupMemberships'][0]['OptionGroupName']

            # Initialize the require_secure_transport variable
            ssl_configuration = None
            nne_configuration = None
            # Paginate results until "require_secure_transport" parameter is found
            paginator = rds_client.get_paginator('describe_option_groups')
            for page in paginator.paginate(OptionGroupName=db_option_groups):
            

                # Find the require_secure_transport option value
                for optionGroup in page['OptionGroupsList']:
                    if optionGroup['OptionGroupName'] == db_option_groups:
                        for option in optionGroup['Options']:
                            if option['OptionName'] == 'SSL':
                                for setting in option['OptionSettings']:
                                    if setting['Name'] == "SQLNET.SSL_VERSION":
                                        ssl_configuration = setting['Value'] in ['1.2']
                                        break
                                break
                            elif option['OptionName'] == 'NNE':
                                for setting in option['OptionSettings']:
                                    if setting['Name'] == "SQLNET.ENCRYPTION_CLIENT":
                                        nne_configuration = setting['Value'] in ['RC4_256', '3DES168', 'DES40']
                                        break
                                break
                        break

            # Determine compliance based on require_secure_transport value
            if ssl_configuration or nne_configuration:
                compliance_type='COMPLIANT'
            else:
                compliance_type='NON_COMPLIANT'
        else:
            # If the engine type is not Oracle, mark as non-applicable
            compliance_type='NON_APPLICABLE'

        # Submit evaluation to AWS Config
        config_client.put_evaluations(
            Evaluations=[
                {
                    'ComplianceResourceType': 'AWS::RDS::DBInstance',
                    'ComplianceResourceId': instance_id,
                    'ComplianceType': compliance_type,
                    'Annotation': f'RDS Instance is {compliance_type} due to SSL Configuration = {ssl_configuration} and/or NNE Configuration = {nne_configuration}',
                    'OrderingTimestamp': orderingtime
                },
            ],
            ResultToken=event['resultToken']
        )