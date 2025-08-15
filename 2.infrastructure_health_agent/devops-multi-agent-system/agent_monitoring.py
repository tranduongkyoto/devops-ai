# agent_monitoring.py
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge
import structlog

# Metrics
AGENT_REQUESTS = Counter('agent_requests_total', 'Total agent requests', ['agent_type', 'status'])
AGENT_DURATION = Histogram('agent_request_duration_seconds', 'Agent request duration', ['agent_type'])
ACTIVE_AGENTS = Gauge('active_agents', 'Number of active agents', ['agent_type'])

# Structured logging
logger = structlog.get_logger()

class AgentMonitoring:
    """Comprehensive monitoring for agent operations"""
  
    @staticmethod
    def track_agent_execution(agent_type: str):
        """Decorator to track agent execution metrics"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                ACTIVE_AGENTS.labels(agent_type=agent_type).inc()
            
                try:
                    result = await func(*args, **kwargs)
                    AGENT_REQUESTS.labels(agent_type=agent_type, status='success').inc()
                    logger.info("Agent execution successful", 
                              agent_type=agent_type, 
                              duration=time.time() - start_time)
                    return result
                
                except Exception as e:
                    AGENT_REQUESTS.labels(agent_type=agent_type, status='error').inc()
                    logger.error("Agent execution failed", 
                               agent_type=agent_type, 
                               error=str(e),
                               duration=time.time() - start_time)
                    raise
                
                finally:
                    AGENT_DURATION.labels(agent_type=agent_type).observe(time.time() - start_time)
                    ACTIVE_AGENTS.labels(agent_type=agent_type).dec()
        
            return wrapper
        return decorator
  
    @staticmethod
    def setup_alerting():
        """Configure alerting rules for agent health"""
        alerting_rules = {
            'agent_error_rate_high': {
                'query': 'rate(agent_requests_total{status="error"}[5m]) > 0.1',
                'for': '2m',
                'labels': {'severity': 'warning'},
                'annotations': {'summary': 'High agent error rate detected'}
            },
            'agent_response_time_high': {
                'query': 'histogram_quantile(0.95, agent_request_duration_seconds) > 30',
                'for': '5m', 
                'labels': {'severity': 'critical'},
                'annotations': {'summary': 'Agent response time too high'}
            }
        }
    
        return alerting_rules
