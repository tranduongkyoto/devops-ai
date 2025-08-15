# sequential_workflow.py
from typing import List, Dict
import asyncio

class SequentialAgentWorkflow:
    """
    Orchestrates agents in a sequential pipeline.
    Perfect for deployment workflows where order matters.
    """
  
    def __init__(self, agents: List[Agent]):
        self.agents = agents
        self.workflow_state = {}
  
    async def execute_workflow(self, initial_task: str) -> Dict:
        """Execute agents sequentially, passing results forward"""
    
        current_input = initial_task
        workflow_results = []
    
        for i, agent in enumerate(self.agents):
            print(f"🔄 Step {i+1}: {agent.role}")
        
            # Execute current agent
            result = await agent.execute(current_input)
        
            # Store result
            workflow_results.append({
                'step': i+1,
                'agent': agent.role,
                'input': current_input,
                'output': result,
                'timestamp': datetime.now().isoformat()
            })
        
            # Pass result to next agent
            current_input = f"Previous step result: {result}\n\nContinue with next phase."
    
        return {
            'workflow_type': 'sequential',
            'total_steps': len(self.agents),
            'execution_time': self._calculate_execution_time(workflow_results),
            'steps': workflow_results,
            'final_result': workflow_results[-1]['output'] if workflow_results else None
        }

# Example: Deployment Pipeline
deployment_workflow = SequentialAgentWorkflow([
    security_agent,      # 1. Security validation
    infrastructure_agent, # 2. Infrastructure preparation  
    deployment_agent,    # 3. Application deployment
    monitoring_agent     # 4. Monitoring setup
])

result = await deployment_workflow.execute_workflow(
    "Deploy version 2.1.0 of our web application to production"
)
