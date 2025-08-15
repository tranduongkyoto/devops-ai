#!/usr/bin/env python3
"""
Test the basic structure of the multi-agent system without API calls
"""

import os
import sys
from unittest.mock import MagicMock, patch

def test_basic_structure():
    """Test that all components can be imported and initialized"""
    print("🧪 Testing Multi-Agent System Basic Structure")
    print("=" * 60)
    
    # Mock the LLM to avoid API calls
    with patch('devops_crew.ChatOpenAI') as mock_llm:
        mock_llm.return_value = MagicMock()
        
        # Mock environment variable for API key
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'}):
            try:
                from devops_crew import DevOpsAgentCrew
                
                print("✅ Successfully imported DevOpsAgentCrew")
                
                # Initialize crew
                crew = DevOpsAgentCrew()
                print("✅ Multi-agent crew initialized")
                
                # Check agents
                agents = crew.crew.agents
                print(f"✅ Found {len(agents)} agents:")
                for agent in agents:
                    print(f"   - {agent.role}")
                
                # Check that crew has the required methods
                assert hasattr(crew, 'handle_incident'), "handle_incident method missing"
                assert hasattr(crew, 'infrastructure_optimization'), "infrastructure_optimization method missing"
                print("✅ All required methods present")
                
                # Test agent tool methods
                tool_methods = [
                    '_get_infrastructure_tools',
                    '_get_security_tools', 
                    '_get_monitoring_tools',
                    '_get_deployment_tools'
                ]
                
                for method in tool_methods:
                    assert hasattr(crew, method), f"{method} missing"
                    tools = getattr(crew, method)()
                    assert isinstance(tools, list), f"{method} should return a list"
                
                print("✅ All agent tool methods working")
                
                print("\n🎉 Basic structure test PASSED!")
                print("Multi-agent system structure is correct")
                return True
                
            except Exception as e:
                print(f"❌ Error during initialization: {e}")
                return False

def test_crew_configuration():
    """Test crew configuration"""
    print("\n🔧 Testing Crew Configuration")
    print("=" * 50)
    
    with patch('devops_crew.ChatOpenAI') as mock_llm:
        mock_llm.return_value = MagicMock()
        
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'}):
            try:
                from devops_crew import DevOpsAgentCrew
                from crewai import Task
                
                crew = DevOpsAgentCrew()
                
                # Test creating crew with tasks
                test_task = Task(
                    description="Test task",
                    agent=crew.infrastructure_agent,
                    expected_output="Test output"
                )
                
                test_crew = crew._create_crew([test_task])
                assert len(test_crew.tasks) == 1, "Task not added to crew"
                print("✅ Crew creation with tasks works")
                
                # Test creating empty crew
                empty_crew = crew._create_crew()
                assert len(empty_crew.tasks) == 0, "Empty crew should have no tasks"
                print("✅ Empty crew creation works")
                
                print("🎉 Crew configuration test PASSED!")
                return True
                
            except Exception as e:
                print(f"❌ Crew configuration error: {e}")
                return False

def main():
    """Run all basic structure tests"""
    print("🚀 Multi-Agent System Structure Verification")
    print("=" * 70)
    print(f"Working directory: {os.getcwd()}")
    print("")
    
    tests = [
        ("Basic Structure", test_basic_structure),
        ("Crew Configuration", test_crew_configuration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
        print()
    
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
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure tests passed!")
        print("Multi-agent system structure is ready!")
    else:
        print("❌ Some tests failed - check configuration")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)