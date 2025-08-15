# AWS EC2 MCP Server

A Model Context Protocol (MCP) server for safe AWS EC2 instance management. This tool provides controlled EC2 operations through the MCP protocol with proper error handling and state validation.

## Features

- **Resource Discovery**: List EC2 instances and VPCs
- **Instance Management**: Start/stop EC2 instances safely
- **Status Monitoring**: Get comprehensive instance health status
- **Snapshot Creation**: Create EBS volume snapshots
- **Security**: Defensive operations with state checking

## Prerequisites

- Python 3.8 or higher
- AWS account with EC2 permissions
- Valid AWS credentials configured

## Setup and Installation

### 1. Install Python
```bash
python3 --version  # Verify Python installation
```

### 2. Configure AWS Credentials

Choose one of the following methods:

**Option A: AWS CLI**
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format
```

**Option B: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

**Option C: IAM Role (if running on EC2)**
```bash
# No setup needed - uses instance profile automatically
```

### 3. Create Virtual Environment

**If you get `python3-venv` error, use this alternative:**

```bash
# Option A: Install virtualenv (recommended if venv fails)
pip3 install --user virtualenv
python3 -m virtualenv venv

# Option B: Standard venv (if python3-venv is installed)
python3 -m venv venv
```

**Activate the environment:**
```bash
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Verify AWS Access
```bash
python3 -c "import boto3; print(boto3.client('ec2').describe_regions())"
```

## Running the Server

### Start MCP Server
```bash
python3 ec2_mcp_server.py
```

The server runs in stdio mode and waits for MCP client connections.

## Testing

### Run Test Client
Open a new terminal window and run:

```bash
# Activate the same virtual environment
source venv/bin/activate

# Run the test client
python3 test_client.py
```

### Expected Test Output
```
🔍 Testing resource listing...
Found X resources:
  - EC2 Instance: instance-name (i-xxxxx)
  - VPC: vpc-xxxxx

🛠️ Testing tool listing...
Found 4 tools:
  - start_instance: Start an EC2 instance
  - stop_instance: Stop an EC2 instance
  - get_instance_status: Get current status
  - create_snapshot: Create EBS snapshots

📖 Testing resource reading...
Resource content preview: EC2 Instance Details: {...

⚡ Testing tool execution...
Tool execution test skipped (requires real instance ID)
```

### Manual Testing with Real Instance

To test with a real EC2 instance, modify `test_client.py` line 48:

```python
# Replace with your actual instance ID
result = await read.call_tool("get_instance_status", 
    {"instance_id": "i-your-real-instance-id"})
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `start_instance` | Start an EC2 instance | `instance_id` (required) |
| `stop_instance` | Stop an EC2 instance | `instance_id` (required) |
| `get_instance_status` | Get instance status and health | `instance_id` (required) |
| `create_snapshot` | Create EBS volume snapshots | `instance_id` (required), `description` (optional) |

## Available Resources

- **EC2 Instances**: `ec2://instance/{instance_id}`
- **VPCs**: `ec2://vpc/{vpc_id}`

## Troubleshooting

### Common Issues

**AWS Credentials Not Found**
```bash
# Check credentials
aws sts get-caller-identity
```

**Permission Denied**
- Ensure your AWS user/role has EC2 permissions:
  - `ec2:DescribeInstances`
  - `ec2:DescribeVpcs`
  - `ec2:StartInstances`
  - `ec2:StopInstances`
  - `ec2:CreateSnapshot`

**Wrong Region**
```bash
# Verify correct AWS region
echo $AWS_DEFAULT_REGION
```

**Virtual Environment Creation Error**
```bash
# Error: Command '[...venv/bin/python3', '-m', 'ensurepip'...] returned non-zero exit status 1
# Solution: Install virtualenv package
pip3 install --user virtualenv
python3 -m virtualenv venv
```

**Missing Dependencies**
```bash
# Check installed packages
pip list
```

### Monitoring

- Server logs appear in the terminal where you started `ec2_mcp_server.py`
- Look for AWS API calls and responses
- Error messages include detailed information for debugging

## Security Considerations

- This tool performs read operations and controlled write operations only
- State checking prevents dangerous operations (e.g., stopping already stopped instances)
- All operations are logged for audit purposes
- Uses least-privilege AWS permissions

## Architecture

The server implements the Model Context Protocol (MCP) to provide:
- **Resources**: Read-only access to EC2 metadata
- **Tools**: Controlled EC2 management operations
- **Safety**: Defensive programming with error handling

## License

This project is for educational and operational use in managing AWS infrastructure safely.