# parallel_workflow.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelAgentWorkflow:
    """
    Orchestrates agents in parallel for independent tasks.
    Perfect for comprehensive system analysis.
    """
  
    def __init__(self, agents: List[Agent]):
        self.agents = agents
  
    async def execute_parallel(self, task: str) -> Dict:
        """Execute all agents in parallel"""
    
        print(f"🚀 Starting parallel execution with {len(self.agents)} agents")
    
        # Create tasks for all agents
        tasks = []
        for agent in self.agents:
            task_coroutine = agent.execute_async(task)
            tasks.append(task_coroutine)
    
        # Execute all tasks concurrently
        start_time = datetime.now()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        execution_time = (datetime.now() - start_time).total_seconds()
    
        # Process results
        agent_results = []
        for i, (agent, result) in enumerate(zip(self.agents, results)):
            if isinstance(result, Exception):
                agent_result = {
                    'agent': agent.role,
                    'status': 'error',
                    'error': str(result),
                    'output': None
                }
            else:
                agent_result = {
                    'agent': agent.role,
                    'status': 'success',
                    'error': None,
                    'output': result
                }
            agent_results.append(agent_result)
    
        return {
            'workflow_type': 'parallel',
            'execution_time': execution_time,
            'total_agents': len(self.agents),
            'successful_agents': len([r for r in agent_results if r['status'] == 'success']),
            'failed_agents': len([r for r in agent_results if r['status'] == 'error']),
            'results': agent_results
        }

# Example: System Analysis
analysis_workflow = ParallelAgentWorkflow([
    infrastructure_agent,
    security_agent,
    monitoring_agent,
    deployment_agent
])

result = await analysis_workflow.execute_parallel(
    "Analyze our production environment for optimization opportunities"
)
