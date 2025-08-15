#!/usr/bin/env python3
"""
Test script for the DevOps Multi-Agent System
"""

import os
import sys
import time
from datetime import datetime

def test_environment():
    """Test environment setup"""
    print("🔧 Testing Environment Setup")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor} - Compatible")
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} - Requires 3.8+")
        return False
    
    # Check API keys
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if openrouter_key:
        print(f"✅ OpenRouter API key found (ends with: ...{openrouter_key[-8:]})")
    elif openai_key:
        print(f"✅ OpenAI API key found (ends with: ...{openai_key[-8:]})")
    else:
        print("⚠️  No API key found - set OPENROUTER_API_KEY or OPENAI_API_KEY")
    
    # Check AWS configuration (optional)
    aws_profile = os.getenv('AWS_PROFILE')
    if aws_profile:
        print(f"✅ AWS profile configured: {aws_profile}")
    else:
        print("ℹ️  AWS profile not set (optional)")
    
    print("🎉 Environment test completed!\n")
    return True

def test_imports():
    """Test required imports"""
    print("📦 Testing Package Imports")
    print("=" * 50)
    
    try:
        import crewai
        print(f"✅ CrewAI imported successfully - Version available")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False
    
    try:
        from crewai import Agent, Task, Crew, Process
        print("✅ CrewAI core components imported")
    except ImportError as e:
        print(f"❌ CrewAI components import failed: {e}")
        return False
    
    try:
        import langchain_openai
        print("✅ LangChain OpenAI integration imported")
    except ImportError as e:
        print(f"❌ LangChain OpenAI import failed: {e}")
        return False
    
    try:
        import boto3
        print("✅ AWS SDK (boto3) imported")
    except ImportError as e:
        print(f"❌ Boto3 import failed: {e}")
        return False
    
    try:
        import psutil
        print("✅ System utilities (psutil) imported")
    except ImportError as e:
        print(f"❌ Psutil import failed: {e}")
        return False
    
    print("🎉 All imports successful!\n")
    return True

def test_agent_initialization():
    """Test agent crew initialization"""
    print("🤖 Testing Agent Initialization")
    print("=" * 50)
    
    try:
        from devops_crew import DevOpsAgentCrew
        print("✅ DevOps crew module imported")
        
        # Initialize the crew
        print("🔄 Initializing agent crew...")
        crew = DevOpsAgentCrew()
        print("✅ Agent crew initialized successfully")
        
        # Check agents
        agents = crew.crew.agents
        print(f"✅ Found {len(agents)} specialized agents:")
        for agent in agents:
            print(f"   - {agent.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False

def test_simple_task():
    """Test a simple task execution"""
    print("🎯 Testing Simple Task Execution")
    print("=" * 50)
    
    try:
        from devops_crew import DevOpsAgentCrew
        
        crew = DevOpsAgentCrew()
        print("✅ Crew ready for task execution")
        
        # Simple test task
        test_task = """
        Test Task: System Health Check
        
        Perform a basic assessment of system health:
        - Check if all agents are responsive
        - Verify agent coordination capabilities
        - Provide a simple status report
        
        This is a test to verify the multi-agent system is working.
        """
        
        print("🔄 Executing test task...")
        start_time = time.time()
        
        # Use infrastructure optimization as it's simpler
        result = crew.infrastructure_optimization(test_task)
        
        execution_time = time.time() - start_time
        print(f"✅ Task completed in {execution_time:.2f} seconds")
        
        # Show summary of result
        result_preview = result[:300] + "..." if len(result) > 300 else result
        print(f"📋 Result preview:\n{result_preview}")
        
        return True
        
    except Exception as e:
        print(f"❌ Task execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_redis_connection():
    """Test Redis connection (optional)"""
    print("📡 Testing Redis Connection")
    print("=" * 50)
    
    try:
        import redis
        
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        client = redis.from_url(redis_url)
        
        # Test connection
        response = client.ping()
        if response:
            print("✅ Redis connection successful")
            print(f"   Connected to: {redis_url}")
            
            # Test basic operations
            client.set('test_key', 'test_value', ex=10)
            value = client.get('test_key')
            if value:
                print("✅ Redis read/write operations working")
            
            return True
        else:
            print("❌ Redis ping failed")
            return False
            
    except ImportError:
        print("⚠️  Redis package not installed (optional for caching)")
        return True
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("ℹ️  Redis is optional - system will work without caching")
        return True

def run_complete_test():
    """Run all tests"""
    print("🚀 DevOps Multi-Agent System - Complete Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().isoformat()}")
    print("")
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("Agent Initialization", test_agent_initialization),
        ("Redis Connection", test_redis_connection),
        ("Simple Task", test_simple_task),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print("")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
            print("")
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print("")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-agent system is ready!")
    elif passed >= total - 1:
        print("⚠️  Most tests passed. System should work with minor issues.")
    else:
        print("❌ Multiple test failures. Check configuration and dependencies.")
    
    print(f"Completed at: {datetime.now().isoformat()}")

if __name__ == "__main__":
    run_complete_test()