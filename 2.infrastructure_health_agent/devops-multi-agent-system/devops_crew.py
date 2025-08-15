# devops_crew.py
import os
from datetime import datetime
from typing import List, Dict

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

class DevOpsAgentCrew:
    """
    A multi-agent system for comprehensive DevOps operations.
    Each agent specializes in a specific domain but can collaborate.
    """
  
    def __init__(self):
        import os

        # Get API key from environment
        api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("Either OPENROUTER_API_KEY or OPENAI_API_KEY must be set")

        # Configure for OpenRouter if using OPENROUTER_API_KEY
        if os.getenv('OPENROUTER_API_KEY'):
            self.llm = ChatOpenAI(
                model="openai/gpt-4.1-nano",  # High-quality model via OpenRouter
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
        # Create specialized agents
        self.infrastructure_agent = self._create_infrastructure_agent()
        self.security_agent = self._create_security_agent()
        self.monitoring_agent = self._create_monitoring_agent()
        self.deployment_agent = self._create_deployment_agent()
    
        # Create the crew
        self.crew = self._create_crew()
  
    def _create_infrastructure_agent(self) -> Agent:
        """Infrastructure specialist agent"""
        return Agent(
            role="Infrastructure Specialist",
            goal="Manage and optimize cloud infrastructure, ensure high availability and performance",
            backstory="""You are a seasoned Infrastructure Engineer with deep expertise in cloud platforms, 
            particularly AWS. You understand infrastructure patterns, scaling strategies, and cost optimization. 
            You work closely with other team members to ensure infrastructure supports application and security requirements.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self._get_infrastructure_tools()
        )
  
    def _create_security_agent(self) -> Agent:
        """Security specialist agent"""
        return Agent(
            role="Security Specialist", 
            goal="Ensure infrastructure security, compliance, and implement security best practices",
            backstory="""You are a cybersecurity expert specializing in DevSecOps. You understand security 
            frameworks, compliance requirements, and threat modeling. You review infrastructure changes for 
            security implications and implement security controls.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self._get_security_tools()
        )
  
    def _create_monitoring_agent(self) -> Agent:
        """Monitoring and observability specialist"""
        return Agent(
            role="Monitoring Specialist",
            goal="Implement comprehensive monitoring, alerting, and observability solutions",
            backstory="""You are an SRE expert focused on monitoring, metrics, and observability. You design 
            alerting strategies, create dashboards, and ensure system reliability through proactive monitoring. 
            You help other agents understand system behavior and performance trends.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self._get_monitoring_tools()
        )
  
    def _create_deployment_agent(self) -> Agent:
        """Deployment and CI/CD specialist"""
        return Agent(
            role="Deployment Specialist",
            goal="Manage CI/CD pipelines, deployments, and release strategies",
            backstory="""You are a DevOps engineer specializing in continuous integration and deployment. 
            You design deployment pipelines, implement blue-green deployments, and ensure reliable releases. 
            You coordinate with infrastructure and security teams for safe deployments.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=self._get_deployment_tools()
        )

    def _get_infrastructure_tools(self) -> List[BaseTool]:
        """Get tools for infrastructure management"""
        # For now, return empty list - tools will be added later
        return []
    
    def _get_security_tools(self) -> List[BaseTool]:
        """Get tools for security analysis"""
        # For now, return empty list - tools will be added later
        return []
    
    def _get_monitoring_tools(self) -> List[BaseTool]:
        """Get tools for monitoring and observability"""
        # For now, return empty list - tools will be added later
        return []
    
    def _get_deployment_tools(self) -> List[BaseTool]:
        """Get tools for deployment and CI/CD"""
        # For now, return empty list - tools will be added later
        return []

    def _create_crew(self, tasks: List[Task] = None) -> Crew:
        """Create the crew with task delegation capabilities"""
        return Crew(
            agents=[
                self.infrastructure_agent,
                self.security_agent,
                self.monitoring_agent,
                self.deployment_agent
            ],
            tasks=tasks or [],
            process=Process.hierarchical,  # Infrastructure agent leads
            manager_llm=self.llm,
            verbose=True
        )

    def handle_incident(self, incident_description: str) -> str:
        """Handle a production incident using the full crew"""

        # Define the incident response tasks
        tasks = [
            Task(
                description=f"""
                Incident Report: {incident_description}

                As the Infrastructure Specialist, lead the incident response:
                1. Assess the current infrastructure state
                2. Identify affected systems and services
                3. Coordinate with other specialists for comprehensive analysis
                4. Provide immediate stabilization recommendations

                Delegate specific tasks to other agents as needed.
                """,
                agent=self.infrastructure_agent,
                expected_output="Comprehensive incident assessment with immediate action plan"
            ),

            Task(
                description=f"""
                Security Analysis for incident: {incident_description}

                Analyze the security implications:
                1. Check if this could be a security incident
                2. Review access logs and security events
                3. Assess potential data exposure or compromise
                4. Recommend security hardening measures
                """,
                agent=self.security_agent,
                expected_output="Security impact assessment and recommendations"
            ),

            Task(
                description=f"""
                Monitoring Analysis for incident: {incident_description}

                Provide observability insights:
                1. Analyze relevant metrics and logs
                2. Identify patterns or anomalies leading to the incident
                3. Set up additional monitoring if needed
                4. Create alerts to prevent recurrence
                """,
                agent=self.monitoring_agent,
                expected_output="Monitoring analysis and preventive measures"
            ),

            Task(
                description=f"""
                Deployment Impact Analysis for incident: {incident_description}

                Assess deployment-related factors:
                1. Check if recent deployments contributed to the incident
                2. Evaluate rollback options if applicable
                3. Review deployment pipeline health
                4. Recommend deployment process improvements
                """,
                agent=self.deployment_agent,
                expected_output="Deployment analysis and process recommendations"
            )
        ]

        # Create a crew specifically for this incident
        incident_crew = self._create_crew(tasks)
        
        # Execute the incident response
        result = incident_crew.kickoff()
        return result

    def infrastructure_optimization(self, requirements: str) -> str:
        """Optimize infrastructure based on requirements"""

        optimization_task = Task(
            description=f"""
            Infrastructure Optimization Request: {requirements}

            Lead a comprehensive infrastructure optimization initiative:
            1. Analyze current infrastructure state and usage patterns
            2. Coordinate with Security team for compliance requirements
            3. Work with Monitoring team for performance baselines
            4. Collaborate with Deployment team for rollout strategy

            Provide a detailed optimization plan with timeline and risk assessment.
            """,
            agent=self.infrastructure_agent,
            expected_output="Comprehensive infrastructure optimization plan"
        )

        # Create a crew specifically for this optimization
        optimization_crew = self._create_crew([optimization_task])
        
        result = optimization_crew.kickoff()
        return result


# Usage Examples
def demonstrate_multi_agent_system():
    """Show the multi-agent system in action"""

    crew = DevOpsAgentCrew()

    # Example 1: Incident Response
    print("=== Multi-Agent Incident Response ===")
    incident = """
    Production Alert: High response times detected on web application.
    - Average response time increased from 200ms to 3000ms
    - Error rate increased from 0.1% to 5%
    - Started approximately 15 minutes ago
    - Affects primary user-facing application
    """

    response = crew.handle_incident(incident)
    print(f"Incident Response:\n{response}")

    # Example 2: Infrastructure Optimization
    print("\n=== Multi-Agent Infrastructure Optimization ===")
    requirements = """
    Optimize our infrastructure for:
    - 50% cost reduction over 6 months
    - Improved security posture
    - Better monitoring and alerting
    - Zero-downtime deployment capability
    """

    optimization = crew.infrastructure_optimization(requirements)
    print(f"Optimization Plan:\n{optimization}")


if __name__ == "__main__":
    demonstrate_multi_agent_system()