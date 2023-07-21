from dateutil.parser import parse
import boto3
import json


def lambda_handler(event, context):
    # Create EMR and Config clients
    config = boto3.client('config')
    emr = boto3.client('emr')

    enable_in_transit_encryption = False

    # Storing time
    orderingtime = json.loads(event['invokingEvent'])['notificationCreationTime']

    # Create a paginator for the describe_instances() method
    paginator = emr.get_paginator('list_clusters')

    # Use the paginator to retrieve information about all clusters
    for response in paginator.paginate():

        # Iterate over the clusters in the response
        for cluster in response['Clusters']:
            # Print the cluster ID and state
            print(f"Cluster ID: {cluster['Id']}, State: {cluster['Status']['State']}")

            if cluster['Status']['State'] == 'TERMINATED' or cluster['Status']['State'] == 'TERMINATED_WITH_ERRORS':
                compliance_type = 'NOT_APPLICABLE'
            else:
                # Get Security Configuration Using ClusterID
                try:
                    # Get Security Configuration Using ClusterID
                    cluster_id = emr.describe_cluster(ClusterId=cluster['Id'])
                    sec_config = emr.describe_security_configuration(
                        Name=cluster_id['Cluster']['SecurityConfiguration'])
                    # Parse the JSON string
                    json_dict = json.loads(sec_config['SecurityConfiguration'])
                    # Get the EnableInTransitEncryption value
                    enable_in_transit_encryption = json_dict['EncryptionConfiguration']['EnableInTransitEncryption']
                    # Print the EnableInTransitEncryption value
                    print(f"The EnableInTransitEncryption value is {enable_in_transit_encryption}")
                    # Determine compliance based on require_secure_transport value
                    if str(enable_in_transit_encryption) == 'True':
                        compliance_type = 'COMPLIANT'
                    else:
                        compliance_type = 'NON_COMPLIANT'
                except KeyError:
                    print("Security configuration not found.")
                    compliance_type = 'NON_COMPLIANT'
                    # print(compliance_type)
            # Print Compliance Type
            print(compliance_type)
            status = str(cluster['Status']['State'])
            # Submit evaluation to AWS Config
            config.put_evaluations(
                Evaluations=[
                    {
                        'ComplianceResourceType': 'AWS::EMR::Cluster',
                        'ComplianceResourceId': cluster['Id'],
                        'ComplianceType': compliance_type,
                        'Annotation': f'EMR Cluster is {compliance_type} due to EnableInTransitEncryption = {enable_in_transit_encryption} and Cluster State = {status}',
                        'OrderingTimestamp': parse(orderingtime)
                    },
                ],
                ResultToken=event['resultToken']
            )

