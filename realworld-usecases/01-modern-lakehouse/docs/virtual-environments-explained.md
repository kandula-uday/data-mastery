# 🎓 Virtual Environments Explained

## What is a Virtual Environment?

A virtual environment is an **isolated Python installation** that contains:
- Python interpreter (python executable)
- pip (package installer)
- Installed packages
- Scripts and utilities

## Visual Example

### Without Virtual Environment (Global)
```
System:
/usr/bin/python3.11
    └── packages/
        ├── pandas 2.0
        ├── numpy 1.24
        └── requests 2.31

Your Projects:
Project_A/  ← Uses global Python (pandas 2.0)
Project_B/  ← Uses global Python (pandas 2.0) 
            ⚠️ What if this needs pandas 1.5?
```

### With Virtual Environment (Isolated)
```
System:
/usr/bin/python3.11
    └── (clean, minimal packages)

Project_A/
├── code.py
└── venv/  ← Isolated Python
    ├── bin/python3.11
    └── lib/python3.11/site-packages/
        ├── pandas 2.0  ✅
        └── numpy 1.24

Project_B/
├── code.py  
└── venv/  ← Different isolated Python
    ├── bin/python3.11
    └── lib/python3.11/site-packages/
        ├── pandas 1.5  ✅
        └── numpy 1.21
```

## Commands Explained

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

**What this does:**
```
Creates folder structure:
venv/
├── bin/
│   ├── python3       # Copy of Python interpreter
│   ├── pip           # Package installer
│   └── activate      # Activation script
├── lib/
│   └── python3.11/
│       └── site-packages/  # Where packages install
└── pyvenv.cfg        # Configuration file
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

**What this does:**
```
Before activation:
$ which python
/usr/bin/python3

$ echo $PATH
/usr/bin:/usr/local/bin

After activation:
$ which python
/Users/you/project/venv/bin/python  ← Now using venv Python!

$ echo $PATH
/Users/you/project/venv/bin:/usr/bin:/usr/local/bin
                          ↑
            venv is now FIRST in PATH
```

**Visual indicator:**
```bash
# Before
you@computer:~/project$ 

# After activation
(venv) you@computer:~/project$  ← Notice "(venv)" prefix
```

### 3. Install Packages

```bash
pip install pandas
```

**Where it installs:**
```
WITHOUT venv active:
→ Installs to: /usr/local/lib/python3.11/site-packages/
  (Global, affects all projects)

WITH venv active:
→ Installs to: /Users/you/project/venv/lib/python3.11/site-packages/
  (Isolated, only this project)
```

### 4. Verify Installation

```bash
which python
# Output: /Users/you/project/venv/bin/python ✅

pip list
# Shows only packages in THIS venv
```

### 5. Deactivate

```bash
deactivate
```

**What this does:**
```
Restores original PATH:
(venv) you@computer:~/project$ deactivate
you@computer:~/project$ 

$ which python
/usr/bin/python3  ← Back to system Python
```

---

## Real Example: Your Data Mastery Project

### Setup Process

```bash
# 1. Navigate to project
cd ~/Documents/ML\ Projects/data-mastery/realworld-usecases/01-modern-lakehouse

# 2. Create virtual environment with Python 3.11
python3.11 -m venv venv

# What happened:
# Created: venv/ folder with Python 3.11
# Size: ~20 MB (Python + pip only)

# 3. Activate it
source venv/bin/activate

# What happened:
# Modified PATH to use venv/bin/ first
# Changed prompt to show (venv)

# 4. Verify
which python
# /Users/udayshankar/.../01-modern-lakehouse/venv/bin/python ✅

python --version
# Python 3.11.15 ✅

# 5. Install packages
pip install pyspark==3.4.1 pandas==1.5.3

# What happened:
# Downloaded packages from PyPI
# Installed to: venv/lib/python3.11/site-packages/
# Now size: ~500 MB (with all packages)

# 6. Verify installation
pip list
# Shows: pyspark, pandas, and their dependencies

# 7. Use in code
python my_script.py
# Uses venv's Python and packages

# 8. When done
deactivate
# Back to system Python
```

---

## Why This Matters for Data Engineering

### Scenario: Multiple Databricks Versions

```bash
# Client A uses Databricks Runtime 10.4 LTS (old)
Project_ClientA/
└── venv/
    └── site-packages/
        ├── pyspark 3.2.0
        └── pandas 1.3.5

# Client B uses Databricks Runtime 13.3 LTS (new)
Project_ClientB/
└── venv/
    └── site-packages/
        ├── pyspark 3.4.1
        └── pandas 1.5.3
```

**Without venvs**: Impossible to work on both clients!  
**With venvs**: Switch between environments easily ✅

---

## Best Practices

### 1. Always Create venv per Project
```bash
cd my-project
python3 -m venv venv  # Standard name: "venv"
```

### 2. Add to .gitignore
```bash
echo "venv/" >> .gitignore
# Never commit virtual environments to git!
```

### 3. Document Requirements
```bash
pip freeze > requirements.txt
# Others can recreate your environment:
# pip install -r requirements.txt
```

### 4. Use Consistent Python Version
```bash
# Not just "python3"
python3.11 -m venv venv  # Specific version
```

### 5. Activate Before Work
```bash
# Every time you start working:
cd my-project
source venv/bin/activate  # Don't forget this!
```

---

## Troubleshooting

### "pip: command not found"
```bash
# Make sure venv is activated
source venv/bin/activate

# Then pip should work
which pip
# Should show: /path/to/project/venv/bin/pip
```

### "Module not found" Error
```bash
# Probably venv not activated
source venv/bin/activate
pip install missing-module
```

### Wrong Python Version
```bash
# Delete venv and recreate with correct version
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Errors
```bash
# Never use sudo with venv!
# ❌ sudo pip install package
# ✅ pip install package (with venv active)
```

---

## Advanced: Compare venv vs conda

| Feature | venv (built-in) | conda |
|---------|----------------|-------|
| Installation | Built into Python | Requires installation |
| Packages | Python only (PyPI) | Python + system packages |
| Speed | Fast | Slower |
| Size | Small (~20 MB) | Large (~300 MB) |
| Best for | Python projects | Data science (needs C/C++ libs) |

### When to use conda:
- Need non-Python packages (CUDA, MKL)
- Complex scientific computing
- Multiple languages in one env

### When to use venv:
- Pure Python projects ✅ (Like our lakehouse project!)
- Standard development
- CI/CD pipelines
- Docker containers

---

## Summary

**Virtual Environment = Isolated Python installation per project**

**Key Benefits:**
1. Dependency isolation
2. Version control
3. Reproducibility
4. Clean system

**Essential Commands:**
```bash
python3 -m venv venv        # Create
source venv/bin/activate    # Activate
pip install package         # Install
deactivate                  # Deactivate
```

**Always remember:**
- Create one venv per project
- Activate before working
- Add to .gitignore
- Document in requirements.txt

---

This is fundamental knowledge every Python developer needs! 🎓
