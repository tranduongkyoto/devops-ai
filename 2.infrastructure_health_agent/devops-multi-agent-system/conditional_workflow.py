# conditional_workflow.py
class ConditionalAgentWorkflow:
    """
    Dynamic workflow that adapts based on agent outputs.
    Perfect for incident response where the path depends on findings.
    """
  
    def __init__(self):
        self.decision_tree = {}
  
    def add_decision_node(self, condition: callable, true_agent: Agent, false_agent: Agent):
        """Add a decision point in the workflow"""
        self.decision_tree[condition] = (true_agent, false_agent)
  
    async def execute_conditional(self, initial_task: str) -> Dict:
        """Execute workflow with conditional branching"""
    
        workflow_path = []
        current_task = initial_task
    
        # Start with initial assessment
        assessment = await self.infrastructure_agent.execute(
            f"Assess the situation: {current_task}"
        )
    
        # Make decisions based on assessment
        if "security" in assessment.lower() or "breach" in assessment.lower():
            # Security incident path
            next_agent = self.security_agent
            workflow_path.append("security_branch")
        elif "performance" in assessment.lower() or "slow" in assessment.lower():
            # Performance issue path
            next_agent = self.monitoring_agent
            workflow_path.append("performance_branch")
        else:
            # General infrastructure path
            next_agent = self.infrastructure_agent
            workflow_path.append("infrastructure_branch")
    
        # Execute the chosen path
        result = await next_agent.execute(current_task)
    
        return {
            'workflow_type': 'conditional',
            'path_taken': workflow_path,
            'decision_factors': assessment,
            'final_result': result
        }
