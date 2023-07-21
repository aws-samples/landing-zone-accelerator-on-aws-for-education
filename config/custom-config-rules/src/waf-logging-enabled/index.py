import boto3
import json
import os

#
# This Lambda function determines if WAF web ACLs have logging enabled
#
# Trigger Type: Config: Change Triggered
# Scope of Changes: AWS::WAF::WebACL, AWS::WAFv2::WebACL & AWS::WAFRegional::WebACL
#

def is_applicable(config_item, event):
  status = config_item['configurationItemStatus']
  event_left_scope = event['eventLeftScope']
  test = ((status in ['OK', 'ResourceDiscovered']) and
    event_left_scope == False)
  return test

def evaluate_compliance(config_item):
  wafArn = config_item['ARN']
  hasConfig = False

  client = ''
  if (config_item['resourceType'] == 'AWS::WAF::WebACL'):
    client = boto3.client('waf')
  elif (config_item['resourceType'] == 'AWS::WAFRegional::WebACL'):
    client = boto3.client('waf-regional')
  elif (config_item['resourceType'] == 'AWS::WAFv2::WebACL'):
    client = boto3.client('wafv2')

  try:
    response = client.get_logging_configuration(ResourceArn=wafArn)
    hasConfig = True
  except:
    pass

  if not hasConfig:
    return 'NON_COMPLIANT'
  else:
    return 'COMPLIANT'
    
def handler(event, context):
  print('## ENVIRONMENT VARIABLES')
  print(os.environ)
  print('## EVENT')
  print(event)
  
  invoking_event = json.loads(event['invokingEvent'])

  #check if event has valid configurationItem, otherwise quit
  if 'configurationItem' not in invoking_event.keys():
    raise Exception('Error: configurationItem is not defined')
    
  compliance_value = 'NOT_APPLICABLE'
  
  
  if is_applicable(invoking_event['configurationItem'], event):
    compliance_value = evaluate_compliance(invoking_event['configurationItem'])

  config = boto3.client('config')
  response = config.put_evaluations(
    Evaluations=[
      {
      'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
      'ComplianceResourceId': invoking_event['configurationItem']['resourceId'],
      'ComplianceType': compliance_value,
      'OrderingTimestamp': invoking_event['configurationItem']['configurationItemCaptureTime']
      },
    ],
    ResultToken=event['resultToken'])