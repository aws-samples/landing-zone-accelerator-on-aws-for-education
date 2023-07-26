# Configuration Summary
This file serves to provide a general overall summary of the LZA configuration files.

> **_Note_:** LZA administrators are required to review all configuration files and adjust to fit organizational security and compliance needs. This configuration does not inheritly provide full compliance for any framework.___

Visit the [configuration reference](https://awslabs.github.io/landing-zone-accelerator-on-aws/) to explore available customizations for LZA.


## ___Table of Contents___
| Section | Relevant Config File 
| --------------------|--------------|
| [Global Configuration](#global-configuration) | global-config.yaml |
| [Accounts Configuration](#accounts-configuration) | accounts-config.yaml |
| [IAM Configuration](#iam-configuration) | iam-config.yaml |
| [Network Configuration](#network-configuration) | network-config.yaml |
| [Organization Configuration](#organization-configuration) | organization-config.yaml |
| [Security Configuration](#security-configuration) | security-config.yaml |
| [AWS Config Customer Rule Details](#aws-config-customer-rule-details) | security-config.yaml |

### __Global Configuration__
| Configuration Item | Status | Detail | 
| - | - | - |
| Home Region | Defined | us-east-1 |
| Enabled Regions | us-east-1 | Uses Home Region Variable|
| CloudWatch Log Retention | Defined | 3653 Days |
| Termination Protection | Enabled | 
| Control Tower | Enabled |  |
| CDK Options | Defined | <u>Options</u> <br>   centralizeBuckets: true <br> useManagementAccessRole: true |
| SNS Topics | Update Placeholder | Security Topic
| Logging Account | Defined | LogArchive Account |
| Cost and Usage Report | Enabled |
| AWS Budgets | Enabled | Update Notification Email Addresses Placeholder |
| AWS Backup Vault | Enabled |

### __Accounts Configuration__
|  Configuration Item | Status | Detail |
| - | - | - |
| Mandatory AWS Accounts | Defined |  Update Email Address Placeholders|
| Workload AWS Accounts | Defined | SharedServices <br> Network <br> LMS-Prod <br> LMS-Dev <br> SIS-Prod <br> SIS-Dev |



### __IAM Configuration__
| Configuration Item | Status | Detail |
| - | - | - |
| IAM Policy Sets | Defined | Boundary Policy: restricts permissions an identity-based policy can grant an IAM entity |
| IAM Role Sets | IAM Roles Defined | SSM <br> Backup <br> Budgets  |
| IAM Group Sets | Groups Defined | Administrators  |
| IAM User Sets | Users Defined | Break Glass Users | 

### __Network Configuration__
An example network architecture diagram is provided below to demonstrate the intent of using AWS Transit Gateway to connect VPCs in AWS Accounts managed by LZA.
| Configuration Item | Status | Detail |
| - | - | - |
| Delete Default VPC | Enabled |  |
| Transit Gateway | Enabled | Only Infrastructure OU VPCs attached |
| VPC Endpoint Policies | Defined | Default and EC2 VPC endpoints |
| Provisioned VPCs | Defined | -Network Endpoints <br> -Network Inspection <br> -Shared Services  |
| Global VPC Flow Logs | Enabled | Delivery to CloudWatch Logs |  |  

![Network Diagram](images/best_practices_network.jpg) 
<br>

### __Organization Configuration__
| Configuration Item | Status | Detail 
| - | - | - |
| AWS Organizations | Enabled | 
| Organizational Units | Defined | -Security <br> -Infrastructure <br> -Education |
| Quarantine New Accounts | Enabled |
| Service Control Policies | Enabled | 
| Tagging Policies | Enabled | Update cost-center tags in org-tag-policy.json 
| Backup Policy | Enabled |
| Service Control Policies | Enabled | <u>education-scp.json</u> <br> -Block ElastiCache Unencrypted At-Rest <br> -Block ElastiCache Unencrypted In-Transit <br> -ElastiCache Redis command AUTH required <br> -Deny ElastiCache Memcached (No At-Rest Encryption) <br> -Block RDS SQL Express Edition (No At-Rest Encryption) <br> <br> <u>education-scp-2.json</u> <br> -Regionally Block Bucket Creation (Disabled by Default) <br> <br> <u>guardrails-1.json</u> <br> -Restrict LZA modification <br> <br> <u>guardrails-2.json</u> <br> -Restrict LZA modification |


### __Security Configuration__
| Configuration Item | Status | Detail |
| - | - | - |
| AWS Macie | Enabled | |
| AWS GuardDuty | Enabled |
| AWS Audit Manager | Enabled |
| AWS Detective | Disabled |
| AWS SecurityHub | Standards Enabled | -AWS Foundational Security Best Practices v1.0.0 <br> -PCI DSS v3.2.1 <br> -CIS AWS Foundations Benchmark v1.4.0 Standards |
| AWS Access Analyzer | Enabled | | 
| IAM Password Policy | Defined | |
| AWS Config | Enabled | <u>Managed Rules</u> <br> -accelerator-iam-user-group-membership-check <br> -accelerator-securityhub-enabled <br> -accelerator-cloudtrail-enabled <br> -accelerator-rds-logging-enabled <br> -accelerator-cloudwatch-alarm-action-check <br> -accelerator-redshift-cluster-configuration-check <br> -accelerator-cloudtrail-s3-dataevents-enabled <br> -accelerator-emr-kerberos-enabled <br> -accelerator-iam-group-has-users-check <br> -accelerator-s3-bucket-policy-grantee-check <br> -accelerator-lambda-inside-vpc <br> -accelerator-ec2-instances-in-vpc <br> -accelerator-vpc-sg-open-only-to-authorized-ports <br> -accelerator-ec2-instance-no-public-ip <br> -accelerator-elasticsearch-in-vpc-only <br> -accelerator-internet-gateway-authorized-vpc-only <br> -accelerator-iam-no-inline-policy-check <br> -accelerator-elb-acm-certificate-required <br> -accelerator-alb-http-drop-invalid-header-enabled <br> -accelerator-elb-tls-https-listeners-only <br> -accelerator-api-gw-execution-logging-enabled <br> -accelerator-cloudwatch-log-group-encrypted <br> -accelerator-s3-bucket-replication-enabled <br> -accelerator-cw-loggroup-retention-period-check <br> -accelerator-ec2-instance-detailed-monitoring-enabled <br> -accelerator-ec2-volume-inuse-check <br> -accelerator-elb-deletion-protection-enabled <br> -accelerator-cloudtrail-security-trail-enabled <br> -accelerator-elasticache-redis-cluster-automatic-backup-check <br> -accelerator-s3-bucket-versioning-enabled <br> -accelerator-vpc-vpn-2-tunnels-up <br> -accelerator-elb-cross-zone-load-balancing-enabled <br> -accelerator-iam-user-mfa-enabled <br> -accelerator-guardduty-non-archived-findings <br> -accelerator-elasticsearch-node-to-node-encryption-check <br> -accelerator-kms-cmk-not-scheduled-for-deletion <br> -accelerator-api-gw-cache-enabled-and-encrypted <br> -accelerator-sagemaker-endpoint-configuration-kms-key-configured <br> -accelerator-sagemaker-notebook-instance-kms-key-configured <br> -accelerator-dynamodb-table-encrypted-kms <br> -accelerator-dynamodb-throughput-limit-check <br> -accelerator-ebs-in-backup-plan <br> -accelerator-ebs-optimized-instance <br> -accelerator-elbv2-acm-certificate-required <br> -accelerator-lambda-dlq-check <br> -accelerator-no-unrestricted-route-to-igw <br> -accelerator-rds-snapshot-encrypted <br> -accelerator-redshift-cluster-kms-enabled <br> -accelerator-s3-default-encryption-kms <br> -accelerator-secretsmanager-using-cmk <br> -accelerator-wafv2-logging-enabled <br> -accelerator-s3-bucket-default-lock-enabled <br> -accelerator-account-part-of-organizations <br> -accelerator-alb-waf-enabled <br> -accelerator-codebuild-project-artifact-encryption <br> -accelerator-dynamodb-in-backup-plan <br>  -accelerator-restricted-common-ports <br> -accelerator-backup-plan-min-frequency-and-min-retention-check <br> -accelerator-backup-recovery-point-encrypted <br> -accelerator-backup-recovery-point-minimum-retention-check <br> -accelerator-backup-recovery-point-manual-deletion-disabled <br> -accelerator-ec2-resources-protected-by-backup-plan <br> -accelerator-aurora-resources-protected-by-backup-plan <br> -accelerator-rds-resources-protected-by-backup-plan <br> -accelerator-dynamodb-resources-protected-by-backup-plan <br> -accelerator-efs-resources-protected-by-backup-plan <br> -accelerator-fsx-resources-protected-by-backup-plan <br> <br> <u>Custom Rules: Review [Details Table](#aws-config-custom-rule-details)</u> <br> -accelerator-attach-ec2-instance-profile <br> -accelerator-ec2-instance-profile-permission <br> -accelerator-s3-bucket-server-side-encryption-enabled <br> -accelerator-elb-logging-enabled <br> -accelerator-ssm-unencrypted-parameter <br> -accelerator-rds-mysql-mariadb-unencrypted-transport <br> -accelerator-rds-mssql-postgres-unencrypted-transport <br> -accelerator-rds-oracle-unencrypted-transport <br> -accelerator-workdocs-user-domain-detector <br> -accelerator-cognito-password-complexity <br> -accelerator-emr-cluster-unencrypted-transport <br> |

#### AWS Config Custom Rule Details
> **_Disclaimer_:** Testing and validation have been performed on the code in each rule, however, edge cases may exist that are not accounted for. 
> 
> Review the code for each rule in `config/custom-config-rules/src/` to make sure it meets your needs. Open a GitHub Issue to report bugs or feature requests.

| Custom Rule | Intent | Reference |
| - | - | - |
| accelerator-attach-ec2-instance-profile | Ensure EC2 instances have an IAM profile attached. | [Managing EC2 Instance Profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html#instance-profiles-manage-cli-api)|
| accelerator-ec2-instance-profile-permission | EC2 instance profile should include LZA permissions. | [LZA Administrative Role](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/administrative-role.html) | 
| accelerator-s3-bucket-server-side-encryption-enabled | s3 buckets should enforce server-side encryption. | [Protecting Data with Server-Side Encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)|
| accelerator-elb-logging-enabled | ELB access logging should be enabled. | [Access logs for your ALB](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html)|
| accelerator-ssm-unencrypted-parameter |  Don't store sensitive data in a String or StringList parameter. | [What is a Parameter?](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html#what-is-a-parameter) |
| accelerator-rds-mysql-mariadb-unencrypted-transport |  Secure database network connections between client and server. | [Require SSL/TLS for RDS MySQL/MariaDB Connections](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-ssl-connections.html#mysql-ssl-connections.require-ssl) |
| accelerator-rds-mssql-postgres-unencrypted-transport |  Secure database network connections between client and server. | [SSL With MS SQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/SQLServer.Concepts.General.SSL.Using.html) |
| accelerator-rds-oracle-unencrypted-transport |  Secure database network connections between client and server. | [RDS Oracle Encryption Options](https://aws.amazon.com/blogs/apn/oracle-database-encryption-options-on-amazon-rds/) |
| accelerator-workdocs-user-domain-detector |  Monitor user invites outside allowed domain. | [Manage WorkDocs Sites](https://docs.aws.amazon.com/workdocs/latest/adminguide/manage-sites.html#invitation-settings) |
| accelerator-cognito-password-complexity |  Enforce strong passwords for your app users. | [Adding User Pool Password Requirements](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html) |
| accelerator-emr-cluster-unencrypted-transport | Utilize in-transit encryption with EMR. | [EMR Encryption Options](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-data-encryption-options.html) |
#### ___To do/Known Issues:___
- accelerator-emr-cluster-unencrypted-transport: Improve exception handling, only using keyError
- accelerator-attach-ec2-instance-profile: retrieve compliance using API call