#!/bin/bash

# ============================================================================
# Airflow Setup Script for Lakehouse Taxi Pipeline
# ============================================================================

set -e  # Exit on error

echo "🚀 Setting up Apache Airflow for Lakehouse Pipeline..."

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "📂 Project Root: $PROJECT_ROOT"
echo "📂 Airflow Home: $SCRIPT_DIR"

# ============================================================================
# 1. SET ENVIRONMENT VARIABLES
# ============================================================================

export AIRFLOW_HOME="$SCRIPT_DIR"
export AIRFLOW__CORE__DAGS_FOLDER="$SCRIPT_DIR/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="sqlite:///$SCRIPT_DIR/airflow.db"

echo "✅ Environment variables set"

# ============================================================================
# 2. CREATE VIRTUAL ENVIRONMENT (OPTIONAL)
# ============================================================================

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# ============================================================================
# 3. INSTALL AIRFLOW
# ============================================================================

echo "📦 Installing Apache Airflow..."
pip install --upgrade pip
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "✅ Airflow installed"

# ============================================================================
# 4. INITIALIZE AIRFLOW DATABASE
# ============================================================================

echo "🗄️  Initializing Airflow database..."
airflow db init
echo "✅ Database initialized"

# ============================================================================
# 5. CREATE ADMIN USER
# ============================================================================

echo "👤 Creating Airflow admin user..."
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || echo "User already exists"

echo "✅ Admin user created (username: admin, password: admin)"

# ============================================================================
# 6. CREATE AIRFLOW VARIABLE FOR DATABRICKS TOKEN
# ============================================================================

echo "🔑 Setting up Airflow Variables..."

# Check if DATABRICKS_TOKEN is set
if [ -z "$DATABRICKS_TOKEN" ]; then
    echo "⚠️  DATABRICKS_TOKEN not found in environment"
    echo "   You can set it later with:"
    echo "   airflow variables set DATABRICKS_TOKEN 'your_token_here'"
else
    airflow variables set DATABRICKS_TOKEN "$DATABRICKS_TOKEN"
    echo "✅ DATABRICKS_TOKEN variable set"
fi

# ============================================================================
# 7. CREATE DIRECTORIES
# ============================================================================

echo "📁 Creating required directories..."
mkdir -p "$SCRIPT_DIR/logs"
mkdir -p "$SCRIPT_DIR/plugins"
mkdir -p "$SCRIPT_DIR/dags"
echo "✅ Directories created"

# ============================================================================
# SETUP COMPLETE
# ============================================================================

echo ""
echo "✅ ============================================="
echo "✅  AIRFLOW SETUP COMPLETE!"
echo "✅ ============================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Start Airflow Webserver:"
echo "   cd $SCRIPT_DIR"
echo "   source venv/bin/activate"
echo "   airflow webserver --port 8080"
echo ""
echo "2. Start Airflow Scheduler (in new terminal):"
echo "   cd $SCRIPT_DIR"
echo "   source venv/bin/activate"
echo "   airflow scheduler"
echo ""
echo "3. Access Airflow UI:"
echo "   http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "4. Enable the DAG:"
echo "   - Go to DAGs page"
echo "   - Find 'lakehouse_taxi_pipeline'"
echo "   - Toggle it ON"
echo ""
echo "5. Set DATABRICKS_TOKEN (if not set):"
echo "   airflow variables set DATABRICKS_TOKEN 'dapi...'"
echo ""
echo "🎉 Happy orchestrating!"
