# infrastructure_agent.py
import os
import json
from datetime import datetime
from typing import List, Dict, Any

from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

import boto3
import psutil

class InfrastructureHealthAgent:
    """
    An intelligent agent that monitors and manages infrastructure health.
    Can work with AWS, local systems, and integrate with our MCP servers.
    """
  
    def __init__(self, aws_profile: str = None, aws_region: str = "us-west-2"):
        # Initialize LLM with OpenRouter
        import os
        
        # Get API key from environment
        api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Either OPENROUTER_API_KEY or OPENAI_API_KEY must be set")
        
        # Configure for OpenRouter if using OPENROUTER_API_KEY
        if os.getenv('OPENROUTER_API_KEY'):
            self.llm = ChatOpenAI(
                model="openai/gpt-oss-20b:free",  # High-quality model via OpenRouter
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=0.1,
                default_headers={
                    "HTTP-Referer": "https://github.com/your-repo/infrastructure-agent",
                    "X-Title": "Infrastructure Health Agent"
                }
            )
        else:
            # Fallback to direct OpenAI
            self.llm = ChatOpenAI(
                model="gpt-4",
                api_key=api_key,
                temperature=0.1
            )
    
        # Initialize AWS clients
        session = boto3.Session(profile_name=aws_profile)
        self.ec2_client = session.client('ec2', region_name=aws_region)
        self.cloudwatch_client = session.client('cloudwatch', region_name=aws_region)
    
        # Initialize agent tools
        self.tools = self._create_tools()
    
        # Create agent
        self.agent = self._create_agent()
    
        # Create agent executor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
  
    def _create_agent(self):
        """Create the LangChain agent with proper prompting"""
    
        system_message = """You are an expert DevOps Infrastructure Agent. Your role is to:

1. Monitor infrastructure health across cloud and on-premises systems
2. Diagnose problems and suggest solutions
3. Automate routine maintenance tasks
4. Provide clear, actionable insights

Guidelines:
- Always gather comprehensive data before making recommendations
- Prioritize system stability and security
- Explain your reasoning and provide step-by-step plans
- Use the available tools to get real-time information
- When in doubt, recommend safe, conservative actions

You have access to tools for:
- AWS EC2 instance monitoring
- System metrics collection
- CloudWatch metrics analysis
- Infrastructure health checks
"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    
        return create_openai_functions_agent(self.llm, self.tools, prompt)

    def _create_tools(self) -> List[BaseTool]:
        """Create the tools that the agent can use"""
        return [
            self._create_ec2_status_tool(),
            self._create_system_metrics_tool(),
            self._create_cloudwatch_metrics_tool(),
            self._create_health_check_tool()
        ]

    def _create_ec2_status_tool(self) -> BaseTool:
        """Tool to check EC2 instance status"""
        
        ec2_client = self.ec2_client  # Capture client in closure

        class EC2StatusTool(BaseTool):
            name: str = "ec2_status"
            description: str = "Get the status of EC2 instances. Use this to check if instances are running, stopped, or have issues."

            def _run(self, query: str = "") -> str:
                try:
                    response = ec2_client.describe_instances()

                    instances = []
                    for reservation in response['Reservations']:
                        for instance in reservation['Instances']:
                            instance_info = {
                                'InstanceId': instance['InstanceId'],
                                'InstanceType': instance['InstanceType'],
                                'State': instance['State']['Name'],
                                'LaunchTime': instance['LaunchTime'].isoformat(),
                                'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                                'PrivateIP': instance.get('PrivateIpAddress', 'N/A'),
                                'Name': self._get_instance_name(instance)
                            }
                            instances.append(instance_info)

                    return json.dumps(instances, indent=2)

                except Exception as e:
                    return f"Error getting EC2 status: {str(e)}"

            def _get_instance_name(self, instance):
                """Extract instance name from tags"""
                tags = instance.get('Tags', [])
                for tag in tags:
                    if tag['Key'] == 'Name':
                        return tag['Value']
                return 'Unnamed'

        return EC2StatusTool()

    def _create_system_metrics_tool(self) -> BaseTool:
        """Tool to get local system metrics"""

        class SystemMetricsTool(BaseTool):
            name: str = "system_metrics"
            description: str = "Get current system metrics like CPU, memory, disk usage. Use this to check local system health."

            def _run(self, query: str = "") -> str:
                try:
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
                        },
                        'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else 'N/A'
                    }

                    return json.dumps(metrics, indent=2)

                except Exception as e:
                    return f"Error getting system metrics: {str(e)}"

        return SystemMetricsTool()

    def _create_cloudwatch_metrics_tool(self) -> BaseTool:
        """Tool to get CloudWatch metrics"""
        
        cloudwatch_client = self.cloudwatch_client  # Capture client in closure

        class CloudWatchMetricsTool(BaseTool):
            name: str = "cloudwatch_metrics"
            description: str = "Get CloudWatch metrics for AWS resources. Specify instance ID to get detailed metrics."

            def _run(self, instance_id: str = "") -> str:
                try:
                    from datetime import timedelta

                    end_time = datetime.utcnow()
                    start_time = end_time - timedelta(hours=1)  # Last hour

                    # Get CPU utilization
                    cpu_response = cloudwatch_client.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            }
                        ],
                        StartTime=start_time,
                        EndTime=end_time,
                        Period=300,  # 5 minutes
                        Statistics=['Average', 'Maximum']
                    )

                    metrics = {
                        'instance_id': instance_id,
                        'time_range': f"{start_time.isoformat()} to {end_time.isoformat()}",
                        'cpu_utilization': cpu_response['Datapoints']
                    }

                    return json.dumps(metrics, indent=2, default=str)

                except Exception as e:
                    return f"Error getting CloudWatch metrics: {str(e)}"

        return CloudWatchMetricsTool()

    def _create_health_check_tool(self) -> BaseTool:
        """Tool to perform comprehensive health checks"""

        class HealthCheckTool(BaseTool):
            name: str = "health_check"
            description: str = "Perform a comprehensive health check across all monitored systems."

            def _run(self, query: str = "") -> str:
                try:
                    health_report = {
                        'timestamp': datetime.now().isoformat(),
                        'status': 'checking',
                        'checks': []
                    }

                    # Check system resources
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = psutil.virtual_memory().percent
                    disk_percent = psutil.disk_usage('/').percent

                    # CPU Check
                    cpu_status = "healthy" if cpu_percent < 80 else "warning" if cpu_percent < 95 else "critical"
                    health_report['checks'].append({
                        'check': 'CPU Usage',
                        'value': f"{cpu_percent}%",
                        'status': cpu_status,
                        'threshold': '80% warning, 95% critical'
                    })

                    # Memory Check
                    memory_status = "healthy" if memory_percent < 85 else "warning" if memory_percent < 95 else "critical"
                    health_report['checks'].append({
                        'check': 'Memory Usage',
                        'value': f"{memory_percent}%",
                        'status': memory_status,
                        'threshold': '85% warning, 95% critical'
                    })

                    # Disk Check
                    disk_status = "healthy" if disk_percent < 90 else "warning" if disk_percent < 98 else "critical"
                    health_report['checks'].append({
                        'check': 'Disk Usage',
                        'value': f"{disk_percent}%",
                        'status': disk_status,
                        'threshold': '90% warning, 98% critical'
                    })

                    # Overall status
                    statuses = [check['status'] for check in health_report['checks']]
                    if 'critical' in statuses:
                        health_report['status'] = 'critical'
                    elif 'warning' in statuses:
                        health_report['status'] = 'warning'
                    else:
                        health_report['status'] = 'healthy'

                    return json.dumps(health_report, indent=2)

                except Exception as e:
                    return f"Error performing health check: {str(e)}"

        return HealthCheckTool()

    def run(self, task: str) -> str:
        """Execute a task using the agent"""
        try:
            result = self.executor.invoke({"input": task})
            return result["output"]
        except Exception as e:
            return f"Error executing task: {str(e)}"


# Usage Examples
def main():
    """Demonstrate the Infrastructure Health Agent"""

    # Initialize the agent (use None for default profile or no AWS config)
    try:
        agent = InfrastructureHealthAgent(aws_profile=None)
    except Exception as e:
        print(f"❌ AWS Configuration Error: {e}")
        print("ℹ️ Please configure AWS credentials or see README.md for setup instructions")
        return

    # Example 1: General health check
    print("=== Example 1: Infrastructure Health Check ===")
    response = agent.run(
        "Perform a comprehensive health check of our infrastructure. "
        "Check both local system and AWS EC2 instances. "
        "Provide recommendations for any issues found."
    )
    print(response)

    # Example 2: Specific investigation
    print("\n=== Example 2: High CPU Investigation ===")
    response = agent.run(
        "I'm seeing alerts about high CPU usage. "
        "Investigate which systems are affected and suggest solutions."
    )
    print(response)

    # Example 3: Proactive monitoring
    print("\n=== Example 3: Proactive Optimization ===")
    response = agent.run(
        "Analyze our current infrastructure utilization. "
        "Identify opportunities for cost optimization and performance improvement."
    )
    print(response)


def test_basic_functionality():
    """Test basic functionality without AWS credentials"""
    import os
    
    print("🧪 Testing Infrastructure Health Agent Setup...")
    
    # Test 1: Import check
    try:
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test 2: Basic system metrics (no AWS required)
    try:
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        print(f"✅ System metrics accessible - CPU: {cpu_percent}%, Memory: {memory.percent}%")
    except Exception as e:
        print(f"❌ System metrics error: {e}")
    
    # Test 3: API key check
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if openrouter_key:
        print("✅ OpenRouter API key found (preferred)")
    elif openai_key:
        print("✅ OpenAI API key found")
    else:
        print("⚠️ No API key found - set OPENROUTER_API_KEY or OPENAI_API_KEY")
    
    # Test 4: AWS credentials check
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            print("✅ AWS credentials found")
        else:
            print("⚠️ AWS credentials not configured")
    except Exception as e:
        print(f"⚠️ AWS configuration issue: {e}")
    
    print("\n🎉 Basic setup test completed!")
    print("📖 See README.md for full setup instructions")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_basic_functionality()
    else:
        main()