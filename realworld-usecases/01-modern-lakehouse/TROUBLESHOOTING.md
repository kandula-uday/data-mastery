# 🔧 Troubleshooting Guide

## Common Setup Issues

### ❌ Issue: Python 3.13 Compatibility Error

**Error Message:**
```
ModuleNotFoundError: No module named 'pkg_resources'
ERROR: Failed to build 'pandas'
```

**Root Cause:** Python 3.13 is too new. PySpark and pandas require Python 3.9-3.11.

**Solution:**

#### Option 1: Install Python 3.11 with Homebrew (Recommended)
```bash
# Install Python 3.11
brew install python@3.11

# Clean up and recreate venv
cd "/Users/udayshankar/Documents/ML Projects/data-mastery/realworld-usecases/01-modern-lakehouse"
rm -rf venv

# Create venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### Option 2: Use Conda/Miniconda
```bash
# Install miniconda if you don't have it
# https://docs.conda.io/en/latest/miniconda.html

# Create environment with Python 3.11
conda create -n lakehouse python=3.11 -y
conda activate lakehouse

# Install dependencies
pip install -r requirements.txt
```

#### Option 3: Use pyenv (Python Version Manager)
```bash
# Install pyenv
brew install pyenv

# Install Python 3.11
pyenv install 3.11.8

# Set local version
pyenv local 3.11.8

# Recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ❌ Issue: Command not found: brew

**Solution:**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### ❌ Issue: pip install fails with network error

**Solution:**
```bash
# Try with increased timeout
pip install --timeout=100 -r requirements.txt

# Or install packages individually
pip install pyspark==3.4.1
pip install delta-spark==2.4.0
# ... etc
```

---

### ❌ Issue: Virtual environment activation fails

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**Troubleshooting:**
```bash
# If activation fails, try:
. venv/bin/activate

# Or use full path:
source /full/path/to/venv/bin/activate
```

---

### ❌ Issue: Permission denied on setup.sh

**Solution:**
```bash
chmod +x setup.sh
bash setup.sh
```

---

## Quick Setup Reference

### ✅ Working Setup (Python 3.11)

```bash
# 1. Check Python version
python3.11 --version  # Should be 3.11.x

# 2. Clean start
rm -rf venv

# 3. Create venv with Python 3.11
python3.11 -m venv venv

# 4. Activate
source venv/bin/activate

# 5. Upgrade pip
pip install --upgrade pip setuptools wheel

# 6. Install dependencies
pip install -r requirements.txt

# 7. Verify installation
python -c "import pyspark; print(pyspark.__version__)"
python -c "import pandas; print(pandas.__version__)"
```

---

## Verify Your Setup

After successful installation, run:

```bash
# Activate environment
source venv/bin/activate

# Check Python version
python --version  # Should be 3.9, 3.10, or 3.11

# Check key packages
python -c "import pyspark; import pandas; import delta; print('✓ All packages installed')"

# Test Databricks connection (if credentials configured)
python scripts/test_connection.py
```

---

## Alternative: Docker Setup (Advanced)

If you continue having issues, use Docker:

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EOF

# Build and run
docker build -t lakehouse .
docker run -it lakehouse bash
```

---

## Need More Help?

1. **Check Python compatibility:**
   ```bash
   python3 --version
   # Must be 3.9.x, 3.10.x, or 3.11.x
   ```

2. **List all Python versions on your system:**
   ```bash
   ls -la /usr/local/bin/python*
   # Or
   which -a python3 python3.9 python3.10 python3.11
   ```

3. **Check if conda is available:**
   ```bash
   conda --version
   ```

---

## Recommended: Use Python 3.11

For best compatibility with all data engineering tools:

```bash
# Install Python 3.11
brew install python@3.11

# Always use it for this project
python3.11 -m venv venv
```

This version works perfectly with:
- ✅ PySpark 3.4.1
- ✅ Delta Lake
- ✅ pandas 2.x
- ✅ Databricks packages
- ✅ All other dependencies

---

## Still Having Issues?

Run the diagnostic:

```bash
echo "Python version:"
python3 --version

echo "Available Python versions:"
ls -la /usr/local/bin/python* 2>/dev/null || echo "None in /usr/local/bin"

echo "pip version:"
pip --version 2>/dev/null || echo "pip not found"

echo "Virtual env active?"
echo $VIRTUAL_ENV
```

Copy the output and we can troubleshoot further!
