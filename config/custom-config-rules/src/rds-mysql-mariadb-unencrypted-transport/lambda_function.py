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
        if engine.lower() in ['mysql', 'mariadb']:

            # Get the parameter group name for the current instance
            db_parameter_group = instance['DBParameterGroups'][0]['DBParameterGroupName']

            # Initialize the require_secure_transport variable
            require_secure_transport = None
            # Paginate results until "require_secure_transport" parameter is found
            paginator = rds_client.get_paginator('describe_db_parameters')
            for page in paginator.paginate(DBParameterGroupName=db_parameter_group):


                # Find the require_secure_transport parameter value
                for parameter in page['Parameters']:
                    if parameter['ParameterName'] == 'require_secure_transport':
                        require_secure_transport=parameter.get('ParameterValue')
                        break

            # Determine compliance based on require_secure_transport value
            if require_secure_transport == '1':
                compliance_type='COMPLIANT'
            else:
                compliance_type='NON_COMPLIANT'
        else:
            # If the engine type is not MySQL or MariaDB, mark as non-applicable
            compliance_type='NON_APPLICABLE'

        # Submit evaluation to AWS Config
        config_client.put_evaluations(
            Evaluations=[
                {
                    'ComplianceResourceType': 'AWS::RDS::DBInstance',
                    'ComplianceResourceId': instance_id,
                    'ComplianceType': compliance_type,
                    'Annotation': f'RDS Instance is {compliance_type} due to require_secure_transport = {require_secure_transport}',
                    'OrderingTimestamp': orderingtime
                },
            ],
            ResultToken=event['resultToken']
        )