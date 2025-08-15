#!/usr/bin/env python3
"""
Demo script for DevOps Multi-Agent System
Shows the agents in action with different scenarios
"""

import time
from datetime import datetime

def demo_incident_response():
    """Demonstrate incident response workflow"""
    print("🚨 Demo 1: Incident Response")
    print("=" * 50)
    
    try:
        from devops_crew import DevOpsAgentCrew
        
        # Initialize the crew
        crew = DevOpsAgentCrew()
        print("✅ Multi-agent crew initialized")
        
        # Simulate a production incident
        incident = """
        PRODUCTION ALERT - URGENT
        
        Service: Web Application (prod-web-app)
        Issue: High response times and increased error rates
        
        Details:
        - Average response time: 200ms → 2800ms (1400% increase)
        - Error rate: 0.1% → 4.2% (4200% increase) 
        - Started: 10 minutes ago
        - Affected users: ~15,000 active sessions
        - Load balancer health checks failing
        
        Symptoms:
        - Database connection timeouts
        - Memory usage at 85% on app servers
        - Unusual CPU spikes on database server
        
        Initial investigation shows recent deployment 30 minutes ago.
        """
        
        print("📋 Incident Details:")
        print(incident)
        print("\n🔄 Starting multi-agent incident response...")
        
        start_time = time.time()
        response = crew.handle_incident(incident)
        execution_time = time.time() - start_time
        
        print(f"⏱️  Response completed in {execution_time:.2f} seconds")
        print("\n📊 Incident Response Summary:")
        print("-" * 40)
        print(response)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_infrastructure_optimization():
    """Demonstrate infrastructure optimization workflow"""
    print("\n\n📈 Demo 2: Infrastructure Optimization")
    print("=" * 50)
    
    try:
        from devops_crew import DevOpsAgentCrew
        
        crew = DevOpsAgentCrew()
        
        # Optimization requirements
        requirements = """
        INFRASTRUCTURE OPTIMIZATION REQUEST
        
        Business Goals:
        - Reduce infrastructure costs by 40% over next 6 months
        - Improve system reliability and uptime to 99.9%
        - Enhance security posture and compliance
        - Enable faster deployment cycles (current: weekly → daily)
        
        Current Environment:
        - AWS multi-region deployment (us-east-1, us-west-2)
        - 25 EC2 instances (mix of t3.large, m5.xlarge, c5.2xlarge)
        - RDS PostgreSQL (db.r5.xlarge)
        - Application Load Balancer + CloudFront CDN
        - Manual deployment process taking 2-3 hours
        
        Constraints:
        - Zero downtime requirement
        - Must maintain SOC2 compliance
        - Team of 3 DevOps engineers
        - Budget approval needed for major changes
        
        Pain Points:
        - Over-provisioned instances during low traffic
        - Manual scaling decisions
        - Inconsistent monitoring across services
        - Security patches applied manually
        """
        
        print("📋 Optimization Request:")
        print(requirements[:400] + "..." if len(requirements) > 400 else requirements)
        print("\n🔄 Starting multi-agent optimization analysis...")
        
        start_time = time.time()
        optimization = crew.infrastructure_optimization(requirements)
        execution_time = time.time() - start_time
        
        print(f"⏱️  Analysis completed in {execution_time:.2f} seconds")
        print("\n📊 Optimization Plan Summary:")
        print("-" * 40)
        print(optimization)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def demo_agent_coordination():
    """Demonstrate how agents coordinate and delegate tasks"""
    print("\n\n🤝 Demo 3: Agent Coordination")
    print("=" * 50)
    
    try:
        from devops_crew import DevOpsAgentCrew
        
        crew = DevOpsAgentCrew()
        print("✅ Multi-agent crew ready")
        
        # Show agent details
        print("\n👥 Available Agents:")
        for i, agent in enumerate(crew.crew.agents, 1):
            print(f"   {i}. {agent.role}")
            print(f"      Goal: {agent.goal[:60]}...")
        
        # Complex scenario requiring coordination
        complex_task = """
        MULTI-DOMAIN CHALLENGE
        
        Scenario: Preparing for Black Friday traffic surge
        
        Expected Changes:
        - Traffic increase: 10x normal load
        - Geographic distribution: Global (US, EU, APAC)
        - Duration: 72-hour peak period
        - Critical services: Payment processing, inventory, user accounts
        
        Requirements:
        1. Infrastructure scaling strategy
        2. Security hardening for increased attack surface
        3. Enhanced monitoring and alerting
        4. Deployment freeze and rollback procedures
        
        Each agent should contribute their expertise and coordinate with others.
        """
        
        print("📋 Complex Coordination Task:")
        print(complex_task[:300] + "...")
        print("\n🔄 Starting coordinated multi-agent response...")
        
        start_time = time.time()
        
        # Use infrastructure optimization as it allows for coordination
        result = crew.infrastructure_optimization(complex_task)
        
        execution_time = time.time() - start_time
        
        print(f"⏱️  Coordination completed in {execution_time:.2f} seconds")
        print("\n📊 Coordinated Response:")
        print("-" * 40)
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Run the complete demo"""
    print("🚀 DevOps Multi-Agent System - Live Demo")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    print("This demo showcases:")
    print("✨ Multi-agent collaboration and task delegation")
    print("✨ Specialized expertise from different agent roles") 
    print("✨ Real-world DevOps scenarios and solutions")
    print("✨ Agent coordination and intelligent workflows")
    print("")
    
    demos = [
        ("Incident Response", demo_incident_response),
        ("Infrastructure Optimization", demo_infrastructure_optimization), 
        ("Agent Coordination", demo_agent_coordination)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n🎬 Starting {demo_name} Demo...")
            result = demo_func()
            results.append((demo_name, result))
            
            if result:
                print(f"✅ {demo_name} demo completed successfully")
            else:
                print(f"❌ {demo_name} demo failed")
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ {demo_name} demo crashed: {e}")
            results.append((demo_name, False))
    
    # Final summary
    print("\n\n📊 Demo Summary")
    print("=" * 50)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for demo_name, result in results:
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{status} - {demo_name}")
    
    print(f"\nResults: {successful}/{total} demos successful")
    
    if successful == total:
        print("🎉 All demos completed successfully!")
        print("The multi-agent system is working perfectly!")
    elif successful > 0:
        print("⚠️  Some demos completed. System is partially functional.")
    else:
        print("❌ No demos completed. Check your configuration.")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n🚀 Ready for production deployment!")

if __name__ == "__main__":
    main()