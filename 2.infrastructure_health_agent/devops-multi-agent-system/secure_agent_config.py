# secure_agent_config.py
class SecureAgentConfiguration:
    """Security best practices for production agent deployment"""
  
    @staticmethod
    def configure_secure_llm():
        """Configure LLM with security constraints"""
        return ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for consistent responses
            max_tokens=4000,  # Limit response length
            request_timeout=30,  # Prevent hanging requests
            max_retries=3,  # Limit retry attempts
            # Add API key rotation logic
        )
  
    @staticmethod
    def implement_input_validation():
        """Validate and sanitize agent inputs"""
        def validate_task_input(task: str) -> str:
            # Remove potentially dangerous commands
            dangerous_patterns = [
                r'rm\s+-rf',
                r'sudo\s+',
                r'curl\s+.*\|\s*sh',
                r'wget\s+.*\|\s*sh',
            ]
        
            for pattern in dangerous_patterns:
                if re.search(pattern, task, re.IGNORECASE):
                    raise ValueError(f"Potentially dangerous command detected: {pattern}")
        
            # Limit input length
            if len(task) > 10000:
                raise ValueError("Task description too long")
        
            return task
    
        return validate_task_input
  
    @staticmethod
    def configure_rbac():
        """Role-based access control for agents"""
        agent_permissions = {
            'infrastructure_agent': [
                'aws:ec2:DescribeInstances',
                'aws:ec2:StartInstances', 
                'aws:ec2:StopInstances',
                'aws:cloudwatch:GetMetricStatistics'
            ],
            'security_agent': [
                'aws:iam:ListUsers',
                'aws:guardduty:GetFindings',
                'aws:securityhub:GetFindings'
            ],
            'monitoring_agent': [
                'aws:cloudwatch:*',
                'aws:logs:*'
            ],
            'deployment_agent': [
                'aws:codedeploy:*',
                'kubernetes:apps:deployments'
            ]
        }
    
        return agent_permissions
