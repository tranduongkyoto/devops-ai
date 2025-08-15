# DevOps Multi-Agent System with CrewAI

A comprehensive multi-agent infrastructure health monitoring and management system built with CrewAI. This system features specialized AI agents that collaborate intelligently for DevOps operations.

## 🚀 System Overview

### **Multi-Agent Architecture**
- **Infrastructure Specialist**: Cloud platforms, scaling, cost optimization
- **Security Specialist**: DevSecOps, compliance, threat modeling  
- **Monitoring Specialist**: SRE, observability, alerting, metrics
- **Deployment Specialist**: CI/CD, releases, pipeline management

### **Key Features**
- ✅ **Real-time Collaboration**: Agents delegate and coordinate tasks
- ✅ **Multiple Workflows**: Sequential, parallel, and conditional execution
- ✅ **Production APIs**: FastAPI server with health checks
- ✅ **Enterprise Security**: RBAC, input validation, secure configuration
- ✅ **Performance Optimization**: Redis caching, parallel execution
- ✅ **Monitoring Integration**: Prometheus metrics, structured logging

## 📋 Prerequisites

### **1. System Requirements**
- Python 3.8 or higher
- Redis server (for caching)
- Git

### **2. LLM API Access**
Choose one:
- **OpenRouter API Key** (recommended): Access to Claude 3.5 Sonnet, GPT-4, and other models
- **OpenAI API Key**: Direct GPT-4 access

### **3. AWS Configuration** (Optional)
- AWS CLI installed and configured
- IAM permissions for EC2, CloudWatch, and other services

## 🛠️ Installation & Setup

### **Step 1: Environment Setup**
```bash
# Navigate to the root project directory
cd /path/to/infrastructure_health_agent

# Activate the existing virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to the multi-agent directory
cd devops-multi-agent-system
```

### **Step 2: Install Dependencies**
```bash
# Install additional packages for multi-agent system
pip install fastapi uvicorn redis prometheus-client structlog

# Note: Core packages (crewai, langchain, boto3, etc.) should already be installed from ../requirements.txt
```

### **Step 3: Configure Environment Variables**

**Option A: OpenRouter (Recommended)**
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
export AWS_PROFILE="your-aws-profile"  # Optional
export AWS_DEFAULT_REGION="us-west-2"  # Optional
export REDIS_URL="redis://localhost:6379"  # Optional
```

**Option B: Direct OpenAI**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export AWS_PROFILE="your-aws-profile"  # Optional
export AWS_DEFAULT_REGION="us-west-2"  # Optional
export REDIS_URL="redis://localhost:6379"  # Optional
```

### **Step 4: Start Redis Server** (Optional but Recommended)
```bash
# On macOS
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# On Docker
docker run -d -p 6379:6379 redis:alpine

# Test Redis connection
redis-cli ping  # Should return PONG
```

### **Step 5: Verify AWS Configuration** (Optional)
```bash
aws configure list
aws sts get-caller-identity
```

## 🧪 Testing the Multi-Agent System

### **Test 1: Basic Agent Initialization**
```bash
# Test individual components
python -c "
from devops_crew import DevOpsAgentCrew
crew = DevOpsAgentCrew()
print('✅ Multi-agent crew initialized successfully')
print(f'Agents: {len(crew.crew.agents)} specialized agents')
"
```

### **Test 2: Simple Incident Response**
```bash
python -c "
from devops_crew import DevOpsAgentCrew
crew = DevOpsAgentCrew()

incident = '''
Test Alert: System health check
- Check current infrastructure status
- Verify all systems are operational
'''

print('🚨 Starting incident response...')
result = crew.handle_incident(incident)
print('✅ Incident response completed')
print(result[:200] + '...' if len(result) > 200 else result)
"
```

### **Test 3: Infrastructure Optimization**
```bash
python -c "
from devops_crew import DevOpsAgentCrew
crew = DevOpsAgentCrew()

requirements = '''
Analyze current infrastructure for:
- Cost optimization opportunities
- Security improvements needed
- Monitoring gaps
'''

print('📊 Starting optimization analysis...')
result = crew.infrastructure_optimization(requirements)
print('✅ Optimization analysis completed')
print(result[:200] + '...' if len(result) > 200 else result)
"
```

### **Test 4: Workflow Testing**

**Sequential Workflow:**
```bash
python sequential_workflow.py
```

**Parallel Workflow:**
```bash
python parallel_workflow.py
```

**Conditional Workflow:**
```bash
python conditional_workflow.py
```

## 🌐 API Server Testing

### **Step 1: Start the API Server**
```bash
# Start the FastAPI server
python agent_server.py

# Or with custom configuration
uvicorn agent_server:app --host 0.0.0.0 --port 8000 --reload
```

### **Step 2: Test Health Endpoints**
```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/ready
```

### **Step 3: Test Task Execution**
```bash
# Incident response via API
curl -X POST "http://localhost:8000/execute_task" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "incident",
    "description": "High CPU usage detected on web servers",
    "priority": "high"
  }'

# Infrastructure optimization via API
curl -X POST "http://localhost:8000/execute_task" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "optimization", 
    "description": "Analyze infrastructure for cost reduction",
    "priority": "medium"
  }'
```

## 📊 Monitoring & Metrics

### **Step 1: Enable Prometheus Metrics**
```bash
# Start the server with metrics enabled
python -c "
from agent_monitoring import AgentMonitoring
from prometheus_client import start_http_server

# Start metrics server
start_http_server(8001)
print('📊 Metrics server started on port 8001')

# Keep running
import time
while True:
    time.sleep(1)
"
```

### **Step 2: View Metrics**
```bash
# View Prometheus metrics
curl http://localhost:8001/metrics

# Key metrics to monitor:
# - agent_requests_total
# - agent_request_duration_seconds  
# - active_agents
```

## 🔄 Complete Demo Workflow

### **Run the Full Demonstration**
```bash
# Execute the complete multi-agent demonstration
python devops_crew.py
```

This will run:
1. **Incident Response Simulation**: Multi-agent collaboration for production alerts
2. **Infrastructure Optimization**: Comprehensive analysis and recommendations
3. **Agent Coordination**: Shows how agents delegate and collaborate

## 🛡️ Security Testing

### **Test Input Validation**
```bash
python -c "
from secure_agent_config import SecureAgentConfiguration
validator = SecureAgentConfiguration.implement_input_validation()

# Test safe input
try:
    result = validator('Check system status')
    print('✅ Safe input validated')
except ValueError as e:
    print(f'❌ Input rejected: {e}')

# Test dangerous input  
try:
    result = validator('rm -rf /')
    print('❌ Dangerous input not caught!')
except ValueError as e:
    print(f'✅ Dangerous input blocked: {e}')
"
```

### **Test RBAC Configuration**
```bash
python -c "
from secure_agent_config import SecureAgentConfiguration
permissions = SecureAgentConfiguration.configure_rbac()

print('🔒 Agent Permissions:')
for agent, perms in permissions.items():
    print(f'  {agent}: {len(perms)} permissions')
    for perm in perms[:2]:  # Show first 2
        print(f'    - {perm}')
"
```

## 🚀 Production Deployment

### **Step 1: Docker Deployment**
```bash
# Create Dockerfile (example)
cat > Dockerfile << EOF
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "agent_server:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Build and run
docker build -t devops-agents .
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your-key devops-agents
```

### **Step 2: Environment Configuration**
```bash
# Production environment variables
export ENVIRONMENT=production
export LOG_LEVEL=INFO
export REDIS_URL=redis://prod-redis:6379
export METRICS_PORT=8001
```

## 📈 Performance Optimization

### **Enable Caching**
```bash
python -c "
from performance_optimization import AgentPerformanceOptimizer
optimizer = AgentPerformanceOptimizer()
print('⚡ Performance optimization enabled')
print('📦 Cache configuration ready')
"
```

### **Monitor Performance**
```bash
# Check agent response times
curl http://localhost:8001/metrics | grep agent_request_duration

# Monitor active agents
curl http://localhost:8001/metrics | grep active_agents
```

## 🐛 Troubleshooting

### **Common Issues**

#### **1. CrewAI Import Errors**
```bash
# Fix: Reinstall CrewAI
pip uninstall crewai crewai-tools
pip install crewai>=0.1.0 crewai-tools>=0.1.0
```

#### **2. Redis Connection Failed**
```bash
# Check Redis status
redis-cli ping

# Start Redis if not running
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:alpine
```

#### **3. API Key Issues**
```bash
# Verify API key is set
echo $OPENROUTER_API_KEY | head -c 20

# Test API key
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  https://openrouter.ai/api/v1/models
```

#### **4. Agent Execution Timeout**
```bash
# Increase timeout in configuration
python -c "
from secure_agent_config import SecureAgentConfiguration
llm = SecureAgentConfiguration.configure_secure_llm()
print('LLM configured with timeouts')
"
```

### **Debug Mode**
```bash
# Run with verbose logging
export LOG_LEVEL=DEBUG
python devops_crew.py

# Enable CrewAI debug mode
python -c "
from devops_crew import DevOpsAgentCrew
crew = DevOpsAgentCrew()
crew.crew.verbose = True
"
```

## 📚 Next Steps

1. **Customize Agents**: Modify agent roles and tools in `devops_crew.py`
2. **Add New Workflows**: Create custom workflow patterns
3. **Integrate Monitoring**: Connect to your existing monitoring stack
4. **Scale Deployment**: Use Kubernetes for production scaling
5. **Extend APIs**: Add custom endpoints in `agent_server.py`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open pull request

## 📄 License

This project is for internal DevOps use. Ensure compliance with your organization's security policies.

---

**🎉 Your Multi-Agent DevOps System is Ready!**

The system combines the power of specialized AI agents with enterprise-grade security, monitoring, and performance optimization for comprehensive DevOps automation.