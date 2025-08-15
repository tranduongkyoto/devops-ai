# agent_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import logging
from typing import Dict, Any

app = FastAPI(title="DevOps Agent Crew API", version="1.0.0")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the agent crew
agent_crew = DevOpsAgentCrew()

class TaskRequest(BaseModel):
    task_type: str  # "incident", "optimization", "analysis"
    description: str
    priority: str = "medium"  # "low", "medium", "high", "critical"
    metadata: Dict[str, Any] = {}

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: str
    execution_time: float
    timestamp: str

@app.post("/execute_task", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """Execute a task using the appropriate agent workflow"""
  
    task_id = f"task_{int(datetime.now().timestamp())}"
    logger.info(f"Executing task {task_id}: {request.task_type}")
  
    try:
        start_time = datetime.now()
    
        if request.task_type == "incident":
            result = await agent_crew.handle_incident(request.description)
        elif request.task_type == "optimization":
            result = await agent_crew.infrastructure_optimization(request.description)
        elif request.task_type == "analysis":
            result = await agent_crew.system_analysis(request.description)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown task type: {request.task_type}")
    
        execution_time = (datetime.now() - start_time).total_seconds()
    
        return TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            execution_time=execution_time,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    try:
        # Test agent initialization
        test_result = await agent_crew.infrastructure_agent.execute("system status check")
        return {"status": "ready", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service not ready")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
