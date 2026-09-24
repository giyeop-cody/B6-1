#!/usr/bin/env python3
"""Read-only AWS policy simulation. Run with administrator verification credentials."""
import boto3,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
policies=[json.loads((root/'infra'/f).read_text()) for f in ['deployer-policy.json','ec2-deployment-policy.json']]
account=boto3.client('sts').get_caller_identity()['Account']
iam=boto3.client('iam')
aa=boto3.client('accessanalyzer',region_name='ap-northeast-2')
for i,p in enumerate(policies):
 findings=aa.validate_policy(policyDocument=json.dumps(p),policyType='IDENTITY_POLICY')['findings']
 print('VALIDATE',i,json.dumps(findings))
 assert not any(f['findingType'] in ['ERROR','SECURITY_WARNING'] for f in findings)
print('TEMPLATE',boto3.client('cloudformation',region_name='ap-northeast-2').validate_template(TemplateBody=(root/'infra/cloudformation.yml').read_text())['Description'])
base={'aws:PrincipalAccount':account,'aws:RequestedRegion':'ap-northeast-2','aws:CalledViaFirst':'cloudformation.amazonaws.com','aws:ResourceTag/Project':'b6-1','aws:ResourceTag/aws:cloudformation:stack-name':'b6-1-learning'}
arn='arn:aws:ec2:ap-northeast-2:'+account+':'
def test(name,action,resource,expected,changes=None):
 ctx={**base,**(changes or {})}
 entries=[{'ContextKeyName':k,'ContextKeyValues':[str(v)],'ContextKeyType':'boolean' if k=='ec2:Encrypted' else 'numeric' if k=='ec2:VolumeSize' else 'string'} for k,v in ctx.items() if v is not None]
 r=iam.simulate_custom_policy(PolicyInputList=[json.dumps(p) for p in policies],ActionNames=[action],ResourceArns=[resource],ContextEntries=entries)['EvaluationResults'][0]
 actual=r['EvalDecision']=='allowed'
 print(name,r['EvalDecision'],'PASS' if actual==expected else 'FAIL',r.get('MissingContextValues',[]))
 assert actual==expected,name
for action,kind in [('ec2:TerminateInstances','instance/i-00000000000000001'),('ec2:DeleteVpc','vpc/vpc-00000000000000001'),('ec2:AuthorizeSecurityGroupIngress','security-group/sg-00000000000000001')]:
 for suffix,changes,expected in [('own',{},True),('foreign',{'aws:ResourceTag/Project':'other'},False),('untagged',{'aws:ResourceTag/Project':None},False),('different-stack',{'aws:ResourceTag/aws:cloudformation:stack-name':'other'},False),('direct',{'aws:CalledViaFirst':None},False),('other-region',{'aws:RequestedRegion':'ap-southeast-2'},False)]:
  test(action+'-'+suffix,action,arn+kind,expected,changes)
test('retag-existing','ec2:CreateTags',arn+'instance/i-00000000000000001',False,{'aws:RequestTag/Project':'b6-1'})
test('create-own-vpc','ec2:CreateVpc',arn+'vpc/vpc-00000000000000002',True,{'aws:RequestTag/Project':'b6-1'})
test('create-untagged-vpc','ec2:CreateVpc',arn+'vpc/vpc-00000000000000002',False)
test('subnet-other-vpc','ec2:CreateSubnet',arn+'vpc/vpc-00000000000000002',False,{'aws:RequestTag/Project':'b6-1','aws:ResourceTag/Project':'other'})
test('create-tag','ec2:CreateTags',arn+'vpc/vpc-00000000000000002',True,{'aws:RequestTag/Project':'b6-1','ec2:CreateAction':'CreateVpc'})
launch={'aws:RequestTag/Project':'b6-1','ec2:InstanceType':'t3.micro','ec2:MetadataHttpTokens':'required','ec2:Tenancy':'default'}
test('small-instance','ec2:RunInstances',arn+'instance/i-00000000000000002',True,launch)
test('large-instance','ec2:RunInstances',arn+'instance/i-00000000000000002',False,{**launch,'ec2:InstanceType':'m5.large'})
volume={'aws:RequestTag/Project':'b6-1','ec2:VolumeType':'gp3','ec2:Encrypted':'true','ec2:VolumeSize':'8'}
test('encrypted-volume','ec2:RunInstances',arn+'volume/vol-00000000000000002',True,volume)
test('unencrypted-volume','ec2:RunInstances',arn+'volume/vol-00000000000000002',False,{**volume,'ec2:Encrypted':'false'})
test('large-volume','ec2:RunInstances',arn+'volume/vol-00000000000000002',False,{**volume,'ec2:VolumeSize':'100'})
test('foreign-eni','ec2:RunInstances',arn+'network-interface/eni-00000000000000002',False)
test('own-stack','cloudformation:CreateStack','arn:aws:cloudformation:ap-northeast-2:'+account+':stack/b6-1-learning/test',True)
test('foreign-stack','cloudformation:DeleteStack','arn:aws:cloudformation:ap-northeast-2:'+account+':stack/other/test',False)
print('AWS POLICY SIMULATION: ALL PASS')
