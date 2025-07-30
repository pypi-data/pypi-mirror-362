import boto3
try:
    # Test if bedrock-agentcore service is available
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    print("✅ Bedrock AgentCore APIs are available in public boto3!")
except Exception as e:
    print(f"❌ APIs not yet available: {e}")
    exit(1)
