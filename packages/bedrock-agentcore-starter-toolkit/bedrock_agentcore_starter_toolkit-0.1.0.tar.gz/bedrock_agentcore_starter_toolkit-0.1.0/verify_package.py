try:
    from bedrock_agentcore import BedrockAgentCoreApp, PingStatus
    from bedrock_agentcore.memory import MemoryClient
    
    # Test basic functionality
    app = BedrockAgentCoreApp()
    
    @app.entrypoint
    def handler(payload):
        return {"status": "success", "payload": payload}
    
    print("✅ All imports and basic functionality work!")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
