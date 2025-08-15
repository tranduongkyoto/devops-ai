#!/usr/bin/env python3
"""
Test the infrastructure monitoring tools individually without requiring OpenAI API
"""

def test_individual_tools():
    """Test each monitoring tool independently"""
    from infrastructure_agent import InfrastructureHealthAgent
    import os
    
    print("🔧 Testing Individual Infrastructure Tools")
    print("=" * 50)
    
    # Create agent instance (this might fail if AWS not configured)
    try:
        agent = InfrastructureHealthAgent(aws_profile=None)
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"⚠️ Agent initialization failed: {e}")
        print("🔄 Testing individual components...")
        test_system_metrics_only()
        return
    
    # Test 1: System Metrics (always works)
    print("\n📊 Testing System Metrics Tool...")
    try:
        tools = agent._create_tools()
        system_tool = None
        for tool in tools:
            if tool.name == "system_metrics":
                system_tool = tool
                break
        
        if system_tool:
            result = system_tool._run()
            print("✅ System metrics tool working:")
            import json
            metrics = json.loads(result)
            print(f"   - CPU: {metrics['cpu_percent']}%")
            print(f"   - Memory: {metrics['memory']['percent']}%")
            print(f"   - Disk: {metrics['disk']['percent']}%")
        else:
            print("❌ System metrics tool not found")
    except Exception as e:
        print(f"❌ System metrics test failed: {e}")
    
    # Test 2: Health Check Tool
    print("\n🏥 Testing Health Check Tool...")
    try:
        health_tool = None
        for tool in tools:
            if tool.name == "health_check":
                health_tool = tool
                break
        
        if health_tool:
            result = health_tool._run()
            print("✅ Health check tool working:")
            health_data = json.loads(result)
            print(f"   - Overall Status: {health_data['status']}")
            for check in health_data['checks']:
                print(f"   - {check['check']}: {check['value']} ({check['status']})")
        else:
            print("❌ Health check tool not found")
    except Exception as e:
        print(f"❌ Health check test failed: {e}")
    
    # Test 3: AWS Tools (might fail without proper AWS config)
    print("\n☁️ Testing AWS Tools...")
    try:
        ec2_tool = None
        for tool in tools:
            if tool.name == "ec2_status":
                ec2_tool = tool
                break
        
        if ec2_tool:
            result = ec2_tool._run()
            if "Error" not in result:
                print("✅ EC2 status tool working")
                instances = json.loads(result)
                print(f"   - Found {len(instances)} EC2 instances")
            else:
                print(f"⚠️ EC2 tool error (expected if no AWS access): {result}")
        else:
            print("❌ EC2 tool not found")
    except Exception as e:
        print(f"⚠️ AWS tools test failed (expected): {e}")
    
    print("\n🎉 Individual tools test completed!")


def test_system_metrics_only():
    """Test just system metrics when full agent fails"""
    print("\n📊 Testing System Metrics Only...")
    
    try:
        import psutil
        import json
        from datetime import datetime
        
        # Manual system metrics test
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            }
        }
        
        print("✅ System metrics working:")
        print(f"   - CPU: {metrics['cpu_percent']}%")
        print(f"   - Memory: {metrics['memory']['percent']}%")
        print(f"   - Disk: {metrics['disk']['percent']}%")
        print(f"   - Timestamp: {metrics['timestamp']}")
        
    except Exception as e:
        print(f"❌ System metrics failed: {e}")


if __name__ == "__main__":
    test_individual_tools()