# Infrastructure Health Agent

An intelligent DevOps agent that monitors and manages infrastructure health across AWS and local systems using LangChain and AI-powered analysis.

## Features

- **System Monitoring**: CPU, memory, disk usage tracking
- **AWS Integration**: EC2 instance monitoring and CloudWatch metrics
- **Automated Health Checks**: Comprehensive infrastructure assessments
- **AI-Powered Analysis**: Intelligent problem diagnosis and recommendations
- **Real-time Insights**: Proactive monitoring and alerting

## Prerequisites

### 1. Python Environment
- Python 3.8 or higher
- pip package manager

### 2. AWS Configuration
- AWS CLI installed and configured
- AWS credentials with appropriate permissions:
  - EC2 read permissions (`ec2:DescribeInstances`)
  - CloudWatch read permissions (`cloudwatch:GetMetricStatistics`)
- AWS profile configured (optional but recommended)

### 3. LLM API Key
Choose one of the following:
- **OpenRouter API Key** (recommended): Access to multiple models including Claude 3.5 Sonnet
- **OpenAI API Key**: Direct access to GPT-4 models

## Quick Start

### **Single Agent System** (Original)
```bash
# Basic setup test
source venv/bin/activate && python test_setup.py

# Test individual monitoring tools (no API key required)
source venv/bin/activate && python test_tools.py

# Built-in test
source venv/bin/activate && python infrastructure_agent.py --test
```

### **🚀 Multi-Agent System** (New - CrewAI)
```bash
# Setup multi-agent system (uses existing venv)
source venv/bin/activate
cd devops-multi-agent-system && ./setup.sh

# Test the multi-agent crew
python test_multi_agent.py

# Run live demo with scenarios
python demo.py
```

## Installation

### Step 1: Clone and Setup
```bash
cd /path/to/infrastructure_health_agent

# Create virtual environment (if this fails, see troubleshooting below)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file or set environment variables:

**Option A: OpenRouter (Recommended)**
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
export AWS_PROFILE="your-aws-profile-name"  # Optional
export AWS_DEFAULT_REGION="us-west-2"      # Optional
```

**Option B: Direct OpenAI**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export AWS_PROFILE="your-aws-profile-name"  # Optional
export AWS_DEFAULT_REGION="us-west-2"      # Optional
```

**Getting API Keys:**
- OpenRouter: Sign up at [openrouter.ai](https://openrouter.ai) - provides access to Claude 3.5 Sonnet, GPT-4, and other models
- OpenAI: Get your key from [platform.openai.com](https://platform.openai.com/api-keys)

### Step 4: Verify AWS Configuration
```bash
aws configure list
aws ec2 describe-instances --region us-west-2 --max-items 1
```

## Usage

### Basic Usage
```python
from infrastructure_agent import InfrastructureHealthAgent

# Initialize agent
agent = InfrastructureHealthAgent(
    aws_profile="your-profile",  # Optional
    aws_region="us-west-2"       # Optional
)

# Run health check
result = agent.run("Perform a comprehensive infrastructure health check")
print(result)
```

### Running the Demo

First, test basic functionality (no credentials required):
```bash
source venv/bin/activate  # Always activate venv first
python infrastructure_agent.py --test
```

Then run the full demo (requires OpenAI API key and AWS credentials):
```bash
source venv/bin/activate
python infrastructure_agent.py
```

## Testing Guide

### Test 1: Local System Health Check
```python
agent = InfrastructureHealthAgent()
response = agent.run("Check the health of this local system. Show CPU, memory, and disk usage.")
print(response)
```

**Expected Output**: JSON report with current system metrics and health status.

### Test 2: AWS EC2 Status Check
```python
response = agent.run("List all EC2 instances and their current status.")
print(response)
```

**Expected Output**: List of EC2 instances with their states, IPs, and basic information.

### Test 3: CloudWatch Metrics Analysis
```python
response = agent.run("Get CloudWatch metrics for instance i-1234567890abcdef0 and analyze performance.")
print(response)
```

**Expected Output**: CloudWatch CPU utilization data and AI analysis.

### Test 4: Comprehensive Health Assessment
```python
response = agent.run(
    "Perform a full infrastructure health check including local system and AWS resources. "
    "Identify any issues and provide recommendations."
)
print(response)
```

**Expected Output**: Complete health report with recommendations.

### Test 5: Problem Investigation
```python
response = agent.run(
    "I'm seeing high CPU alerts. Investigate which systems are affected and suggest solutions."
)
print(response)
```

**Expected Output**: Detailed investigation results with actionable recommendations.

## Available Agent Commands

The agent responds to natural language queries. Here are example commands:

### Monitoring Commands
- "Check system health"
- "Show me CPU usage trends"
- "What's the memory utilization?"
- "List all running EC2 instances"

### Diagnostic Commands
- "Investigate high CPU usage"
- "Why is disk space running low?"
- "Analyze performance issues"
- "Check for any failing services"

### Optimization Commands
- "Suggest cost optimization opportunities"
- "Recommend performance improvements"
- "Identify underutilized resources"
- "What instances can be downsized?"

## Troubleshooting

### Common Issues

#### 1. API Key Errors
```
Error: Either OPENROUTER_API_KEY or OPENAI_API_KEY must be set
Error code: 401 - Incorrect API key provided
```
**Solution**: 
- **Recommended**: Set `OPENROUTER_API_KEY` for access to multiple models
- **Alternative**: Set `OPENAI_API_KEY` for direct OpenAI access  
- Ensure your API key is valid and account has sufficient credits
- For OpenRouter: Check your key at [openrouter.ai/keys](https://openrouter.ai/keys)
- For OpenAI: Check your key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Test individual tools with: `python test_tools.py` (no API key required)

#### 2. AWS Credentials Issues
```
Error: Unable to locate credentials
```
**Solution**: 
- Run `aws configure` to set up credentials
- Verify AWS profile with `aws configure list`
- Check IAM permissions for EC2 and CloudWatch

#### 3. Permission Denied Errors
```
Error: Access denied for EC2 operations
```
**Solution**: Ensure your AWS user/role has these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "cloudwatch:GetMetricStatistics"
            ],
            "Resource": "*"
        }
    ]
}
```

#### 4. Virtual Environment Creation Issues
```
Error: Command '['.../venv/bin/python3', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
```
**Solution**: Use alternative venv creation method:
```bash
# Remove any existing venv
rm -rf venv

# Create venv without pip
python3 -m venv venv --without-pip
source venv/bin/activate

# Install pip manually
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm get-pip.py

# Install dependencies
pip install -r requirements.txt
```

#### 5. Missing Dependencies
```
ImportError: No module named 'langchain'
```
**Solution**: Install requirements: `pip install -r requirements.txt`

### Debug Mode
Enable verbose logging by modifying the agent initialization:
```python
agent = InfrastructureHealthAgent()
agent.executor.verbose = True  # Enable detailed logging
```

## Configuration Options

### AWS Configuration
```python
agent = InfrastructureHealthAgent(
    aws_profile="production",    # AWS profile name
    aws_region="eu-west-1"      # AWS region
)
```

### LLM Configuration
The agent automatically configures based on available API keys:

**OpenRouter Configuration** (when OPENROUTER_API_KEY is set):
- Model: `anthropic/claude-3.5-sonnet` (high-quality reasoning)
- Base URL: `https://openrouter.ai/api/v1`
- Temperature: 0.1 (consistent responses)

**OpenAI Configuration** (when OPENAI_API_KEY is set):
- Model: `gpt-4`
- Direct OpenAI API access
- Temperature: 0.1 (consistent responses)

**Available OpenRouter Models:**
- `anthropic/claude-3.5-sonnet` (recommended)
- `openai/gpt-4`
- `google/gemini-pro`
- `meta-llama/llama-3.1-70b-instruct`

To change models, modify the `model` parameter in `infrastructure_agent.py`.

## Health Check Thresholds

The agent uses these default thresholds:

| Metric | Warning | Critical |
|--------|---------|----------|
| CPU Usage | >80% | >95% |
| Memory Usage | >85% | >95% |
| Disk Usage | >90% | >98% |

Modify thresholds in the `_create_health_check_tool()` method.

## 🚀 Multi-Agent System (CrewAI)

In addition to the single-agent system, we now have a **comprehensive multi-agent DevOps system** built with CrewAI:

### **Agent Specializations:**
- 🏗️ **Infrastructure Specialist**: Cloud platforms, scaling, cost optimization
- 🔒 **Security Specialist**: DevSecOps, compliance, threat modeling
- 📊 **Monitoring Specialist**: SRE, observability, alerting, metrics  
- 🚀 **Deployment Specialist**: CI/CD, releases, pipeline management

### **Key Features:**
- ✅ **Agent Collaboration**: Intelligent task delegation and coordination
- ✅ **Multiple Workflows**: Sequential, parallel, and conditional execution
- ✅ **Production APIs**: FastAPI server with monitoring
- ✅ **Enterprise Security**: RBAC, input validation, secure configs
- ✅ **Performance Optimization**: Redis caching, parallel execution

### **Quick Setup:**
```bash
# From the root project directory
source venv/bin/activate
cd devops-multi-agent-system
./setup.sh                       # Automated setup (uses parent venv)
python verify_setup.py           # Verify parent venv integration
python test_basic_structure.py   # Test system structure
python test_multi_agent.py       # Comprehensive testing (requires API key)
```

**📖 Full Documentation**: See `devops-multi-agent-system/README.md` for complete setup and usage instructions.

## Security Considerations

- Store API keys securely using environment variables
- Use IAM roles with minimal required permissions
- Regularly rotate API keys and AWS credentials
- Monitor agent usage and API calls
- Review and audit health check results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Submit a pull request

## License

This project is for internal DevOps use. Ensure compliance with your organization's security policies.