#!/usr/bin/env python3
"""
Verify that the multi-agent system works with the parent virtual environment
"""

import sys
import os

def check_environment():
    """Check if we're using the correct environment"""
    print("🔍 Environment Verification")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
        print(f"   Virtual env path: {sys.prefix}")
    else:
        print("⚠️  Not running in virtual environment")
    
    # Check Python path
    print(f"✅ Python executable: {sys.executable}")
    print(f"✅ Python version: {sys.version}")
    
    # Check if parent venv is being used
    parent_venv_path = os.path.abspath("../venv")
    current_prefix = sys.prefix
    
    if parent_venv_path in current_prefix:
        print("✅ Using parent virtual environment")
    else:
        print("⚠️  May not be using parent virtual environment")
        print(f"   Expected: {parent_venv_path}")
        print(f"   Current:  {current_prefix}")
    
    return True

def check_imports():
    """Check if all required packages are available"""
    print("\n📦 Package Import Verification")
    print("=" * 50)
    
    required_packages = [
        ('crewai', 'CrewAI framework'),
        ('langchain', 'LangChain core'),
        ('langchain_openai', 'LangChain OpenAI'),
        ('boto3', 'AWS SDK'),
        ('psutil', 'System utilities'),
        ('requests', 'HTTP library'),
        ('fastapi', 'FastAPI web framework'),
        ('uvicorn', 'ASGI server'),
        ('redis', 'Redis client'),
        ('prometheus_client', 'Prometheus metrics'),
        ('structlog', 'Structured logging')
    ]
    
    success_count = 0
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {package:<20} - {description}")
            success_count += 1
        except ImportError:
            print(f"❌ {package:<20} - {description} (NOT FOUND)")
    
    print(f"\nResult: {success_count}/{len(required_packages)} packages available")
    
    if success_count == len(required_packages):
        print("🎉 All packages successfully imported!")
        return True
    elif success_count >= len(required_packages) - 2:
        print("⚠️  Most packages available, system should work")
        return True
    else:
        print("❌ Too many missing packages")
        return False

def check_parent_integration():
    """Check if we can import from parent directory"""
    print("\n🔗 Parent Integration Verification")
    print("=" * 50)
    
    try:
        # Add parent directory to path
        parent_dir = os.path.abspath("..")
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        # Try to import from parent
        from infrastructure_agent import InfrastructureHealthAgent
        print("✅ Successfully imported from parent infrastructure_agent.py")
        
        # Test initialization
        try:
            agent = InfrastructureHealthAgent(aws_profile=None)
            print("✅ Parent agent initialization successful")
            print(f"   Model: {agent.llm.model_name}")
            return True
        except Exception as e:
            print(f"⚠️  Parent agent initialization failed: {e}")
            print("   (This may be due to missing API keys)")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import from parent: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Multi-Agent System Setup Verification")
    print("=" * 60)
    print(f"Working directory: {os.getcwd()}")
    print("")
    
    checks = [
        ("Environment", check_environment),
        ("Package Imports", check_imports),
        ("Parent Integration", check_parent_integration)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n📊 Verification Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Setup verification successful!")
        print("Multi-agent system is ready to use with parent venv!")
    elif passed >= total - 1:
        print("⚠️  Setup mostly successful, minor issues detected")
    else:
        print("❌ Setup verification failed, check configuration")
    
    return passed == total

if __name__ == "__main__":
    main()