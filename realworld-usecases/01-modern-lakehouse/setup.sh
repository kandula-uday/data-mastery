#!/bin/bash
# Setup script for Modern Data Lakehouse project

set -e

echo "🚀 Setting up Modern Data Lakehouse project..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
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
