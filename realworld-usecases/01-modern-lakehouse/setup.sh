#!/bin/bash
# Setup script for Modern Data Lakehouse project

set -e

echo "🚀 Setting up Modern Data Lakehouse project..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check Python version compatibility
check_python_version() {
    local python_cmd=$1
    if command -v $python_cmd &> /dev/null; then
        version=$($python_cmd --version 2>&1 | awk '{print $2}')
        major=$(echo $version | cut -d. -f1)
        minor=$(echo $version | cut -d. -f2)
        
        if [ "$major" -eq 3 ] && [ "$minor" -ge 9 ] && [ "$minor" -le 11 ]; then
            echo "$python_cmd"
            return 0
        fi
    fi
    return 1
}

# Find suitable Python version
echo -e "${BLUE}Checking for compatible Python version (3.9-3.11)...${NC}"

PYTHON_CMD=""
for cmd in python3.11 python3.10 python3.9 python3; do
    if check_python_version $cmd; then
        PYTHON_CMD=$cmd
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Error: Python 3.9-3.11 required${NC}"
    echo -e "${YELLOW}Your Python version is not compatible with PySpark/pandas${NC}"
    echo ""
    echo "Please install Python 3.11:"
    echo "  brew install python@3.11"
    echo ""
    echo "Or use conda:"
    echo "  conda create -n lakehouse python=3.11"
    exit 1
fi

echo -e "${GREEN}✓ Found compatible Python: $PYTHON_CMD${NC}"
$PYTHON_CMD --version

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "${BLUE}Creating project directories...${NC}"
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/sample
mkdir -p logs
mkdir -p tests
mkdir -p scripts

# Copy env example if .env doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file - Please update with your credentials${NC}"
fi

# Create Streamlit secrets directory
mkdir -p ~/.streamlit

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Update .env with your Databricks credentials"
echo "3. Follow the setup guide in docs/setup-guide.md"
echo ""
echo "Happy data engineering! 🎉"
