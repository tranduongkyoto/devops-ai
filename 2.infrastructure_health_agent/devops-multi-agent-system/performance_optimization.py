# performance_optimization.py
import asyncio
from functools import lru_cache
from typing import Dict, Any
import redis

class AgentPerformanceOptimizer:
    """Optimize agent performance for production workloads"""
  
    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.response_cache = {}
  
    @lru_cache(maxsize=1000)
    def cache_tool_results(self, tool_name: str, parameters: str) -> Any:
        """Cache expensive tool operations"""
        cache_key = f"tool:{tool_name}:{hash(parameters)}"
    
        # Try to get from Redis cache
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
    
        return None
  
    def store_tool_result(self, tool_name: str, parameters: str, result: Any, ttl: int = 300):
        """Store tool result in cache"""
        cache_key = f"tool:{tool_name}:{hash(parameters)}"
        self.redis_client.setex(cache_key, ttl, json.dumps(result, default=str))
  
    async def batch_tool_execution(self, tool_requests: List[Dict]) -> List[Any]:
        """Execute multiple tool requests in parallel"""
    
        async def execute_single_tool(request):
            tool_name = request['tool']
            parameters = request['parameters']
        
            # Check cache first
            cached = self.cache_tool_results(tool_name, str(parameters))
            if cached:
                return cached
        
            # Execute tool
            result = await request['tool_instance'].execute(parameters)
        
            # Store in cache
            self.store_tool_result(tool_name, str(parameters), result)
        
            return result
    
        # Execute all tools in parallel
        results = await asyncio.gather(*[execute_single_tool(req) for req in tool_requests])
        return results
  
    def optimize_agent_memory(self, agent):
        """Optimize agent memory usage"""
        # Limit conversation history
        if hasattr(agent, 'memory') and len(agent.memory.chat_memory.messages) > 50:
            # Keep only the last 30 messages
            agent.memory.chat_memory.messages = agent.memory.chat_memory.messages[-30:]
    
        # Clear tool caches periodically
        if len(self.response_cache) > 1000:
            self.response_cache.clear()
