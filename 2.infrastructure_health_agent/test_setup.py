#!/usr/bin/env python3
"""
Simple test script to verify Infrastructure Health Agent setup
"""

def test_setup():
    """Run comprehensive setup tests"""
    
    print("🔧 Infrastructure Health Agent - Setup Test")
    print("=" * 50)
    
    # Test imports
    try:
        import langchain
        import boto3
        import psutil
        print("✅ All required packages imported successfully")
        print(f"   - LangChain: {langchain.__version__}")
        print(f"   - Boto3: {boto3.__version__}")
        print(f"   - psutil: {psutil.__version__}")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test system metrics
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        print(f"✅ System metrics working:")
        print(f"   - CPU: {cpu}%")
        print(f"   - Memory: {memory.percent}% ({memory.available // (1024**3)}GB available)")
        print(f"   - Disk: {disk.percent}% used")
    except Exception as e:
        print(f"❌ System metrics failed: {e}")
        return False
    
    # Test environment
    import os
    
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if openrouter_key:
        print(f"✅ OpenRouter API key configured (ends with: ...{openrouter_key[-8:]})")
    elif openai_key:
        print(f"✅ OpenAI API key configured (ends with: ...{openai_key[-8:]})")
    else:
        print("⚠️  No API key set - configure OPENROUTER_API_KEY or OPENAI_API_KEY")
    
    # Test AWS
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print("✅ AWS credentials configured")
        else:
            print("⚠️  AWS credentials not found")
    except Exception as e:
        print(f"⚠️  AWS setup issue: {e}")
    
    print("\n🎉 Setup test completed!")
    print("📚 Ready to run infrastructure health monitoring!")
    
    return True

if __name__ == "__main__":
    test_setup()