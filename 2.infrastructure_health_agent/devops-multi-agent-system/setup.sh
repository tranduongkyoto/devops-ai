#!/bin/bash

# setup.sh - Quick setup script for DevOps Multi-Agent System

set -e

echo "🚀 DevOps Multi-Agent System - Quick Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "devops_crew.py" ]]; then
    print_error "Please run this script from the devops-multi-agent-system directory"
    exit 1
fi

# Check if parent venv exists
if [[ ! -d "../venv" ]]; then
    print_error "Parent virtual environment not found at ../venv"
    print_info "Please run the main setup first from the parent directory"
    exit 1
fi

# Step 1: Check Python version
echo ""
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1)
print_info "Found: $python_version"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python version is compatible"
else
    print_error "Python 3.8 or higher required"
    exit 1
fi

# Step 2: Use existing virtual environment
echo ""
echo "🔧 Using existing virtual environment..."
source ../venv/bin/activate
print_status "Activated parent virtual environment"

# Step 3: Install additional dependencies
echo ""
echo "📦 Installing additional dependencies..."

# Install additional packages needed for multi-agent system
print_info "Installing additional packages for multi-agent system..."
pip install fastapi uvicorn redis prometheus-client structlog

# Verify core packages are installed
print_info "Verifying core packages..."
python -c "import crewai, langchain, boto3, psutil" 2>/dev/null && print_status "Core packages verified" || print_warning "Some core packages may be missing"

print_status "Dependencies installed successfully"

# Step 4: Check for API keys
echo ""
echo "🔑 Checking API configuration..."

if [[ -n "$OPENROUTER_API_KEY" ]]; then
    print_status "OpenRouter API key found"
elif [[ -n "$OPENAI_API_KEY" ]]; then
    print_status "OpenAI API key found"
else
    print_warning "No API key found!"
    echo ""
    echo "Please set one of the following environment variables:"
    echo "  export OPENROUTER_API_KEY='your-key-here'  (recommended)"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    echo "You can add this to your ~/.bashrc or ~/.zshrc file"
fi

# Step 5: Check Redis (optional)
echo ""
echo "📡 Checking Redis availability..."

if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        print_status "Redis is running and accessible"
    else
        print_warning "Redis installed but not running"
        echo "  Start with: redis-server"
        echo "  Or use Docker: docker run -d -p 6379:6379 redis:alpine"
    fi
else
    print_warning "Redis not installed (optional for caching)"
    echo "  Install with: brew install redis  (macOS)"
    echo "  Install with: sudo apt-get install redis-server  (Ubuntu)"
    echo "  Or use Docker: docker run -d -p 6379:6379 redis:alpine"
fi

# Step 6: Check AWS configuration (optional)
echo ""
echo "☁️ Checking AWS configuration..."

if command -v aws &> /dev/null; then
    if aws sts get-caller-identity &> /dev/null; then
        print_status "AWS CLI configured and working"
    else
        print_warning "AWS CLI installed but not configured"
        echo "  Configure with: aws configure"
    fi
else
    print_warning "AWS CLI not installed (optional for cloud features)"
    echo "  Install from: https://aws.amazon.com/cli/"
fi

# Step 7: Run test
echo ""
echo "🧪 Running system test..."

if python test_multi_agent.py; then
    print_status "System test completed successfully!"
else
    print_error "System test failed. Check the output above for issues."
fi

# Step 8: Final instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo ""
echo "1. Ensure you're in the multi-agent directory with parent venv activated:"
echo "   cd devops-multi-agent-system && source ../venv/bin/activate"
echo ""
echo "2. Set your API key (if not already set):"
echo "   export OPENROUTER_API_KEY='your-key-here'"
echo ""
echo "3. Test the multi-agent system:"
echo "   python test_multi_agent.py"
echo ""
echo "4. Run a simple demo:"
echo "   python devops_crew.py"
echo ""
echo "5. Start the API server:"
echo "   python agent_server.py"
echo ""
echo "6. View the full documentation:"
echo "   cat README.md"
echo ""

if [[ -z "$OPENROUTER_API_KEY" && -z "$OPENAI_API_KEY" ]]; then
    echo ""
    print_warning "Remember to set your API key before running the agents!"
fi

print_status "Multi-agent DevOps system is ready to use!"