# 🏢 Corporate Databricks Setup Guide

## Getting Started with Databricks in a Company

### Step-by-Step Process

---

## Phase 1: Getting Access (Week 1)

### 1. Request Access

**Who to Contact:**
```
Your Manager
    ↓
Submit Request
    ↓
Data Platform Team / DevOps
    ↓
Databricks Administrator
    ↓
Access Granted ✅
```

**Common Request Process:**

#### Option A: IT Service Portal
```
1. Go to company IT portal (ServiceNow, Jira, etc.)
2. Search: "Databricks Access Request"
3. Fill form:
   - Your name & email
   - Team/Department
   - Business justification
   - Required permissions (Developer, Viewer, Admin)
4. Manager approval required
5. Wait 1-3 business days
```

#### Option B: Email Request
```
To: data-platform@yourcompany.com
CC: your-manager@yourcompany.com
Subject: Databricks Access Request

Hi Data Platform Team,

I would like to request access to Databricks for [project name].

Details:
- Name: [Your Name]
- Team: [Your Team]
- Use Case: [e.g., Data pipeline development]
- Required Level: [Developer/Contributor]
- Manager Approval: [Attached/CC'd]

Thank you!
```

### 2. Receive Access

**You'll get an email:**
```
Subject: Databricks Access Granted

Your access to Databricks has been granted.

Workspace URL: https://yourcompany.cloud.databricks.com
Environment: Production / Development
Access Level: Developer

Next Steps:
1. Login using SSO
2. Review internal documentation
3. Complete training (if required)
4. Generate personal access token
```

---

## Phase 2: Initial Login (Day 1)

### 1. Access Databricks Workspace

```bash
# Your company's Databricks URL (examples):
https://yourcompany.cloud.databricks.com
https://adb-1234567890.12.azuredatabricks.net
https://dbc-abc12345-6789.cloud.databricks.com
```

### 2. Authentication Methods

#### **Option A: SSO (Single Sign-On) - Most Common**
```
1. Go to Databricks URL
2. Click "Sign in with SSO"
3. Enter company email
4. Redirected to company login (Okta/Azure AD)
5. Enter company credentials + 2FA
6. Logged in ✅
```

#### **Option B: Username/Password**
```
1. Go to Databricks URL
2. Enter provided username
3. Enter temporary password
4. Change password on first login
5. Set up 2FA (if required)
```

#### **Option C: Azure AD / AWS IAM**
```
1. Already logged into Azure/AWS
2. Navigate to Databricks
3. Automatic authentication
4. No separate login needed
```

---

## Phase 3: Generate Access Token (Day 1-2)

### Method 1: Personal Access Token (Most Common)

**Step-by-Step:**

```
1. Login to Databricks workspace

2. Click your profile icon (top-right corner)
   
3. Click "User Settings" or "Settings"

4. Navigate to "Developer" or "Access Tokens" section

5. Click "Generate New Token"

6. Fill in details:
   ┌─────────────────────────────────────┐
   │ Token Name: local-development       │
   │ Lifetime: 90 days                   │
   │ Comment: For local development      │
   └─────────────────────────────────────┘

7. Click "Generate"

8. 🔴 CRITICAL: Copy the token NOW!
   ┌─────────────────────────────────────────────┐
   │ dapi1234567890abcdefghijklmnopqrstuvwxyz   │
   │ [Copy] ← Click this!                        │
   └─────────────────────────────────────────────┘
   
   ⚠️ You will NEVER see this token again!

9. Store securely (see security section below)
```

**Visual Guide:**
```
Databricks UI:

┌─────────────────────────────────────────┐
│  [👤] Your Name ▼                       │ ← Click here
│    ├─ User Settings                     │ ← Then click this
│    ├─ Admin Console                     │
│    └─ Sign Out                          │
└─────────────────────────────────────────┘

Settings Page:
┌─────────────────────────────────────────┐
│ Settings                                │
│                                         │
│ ► General                               │
│ ► Developer                             │ ← Click to expand
│   └─ Access Tokens                      │ ← Navigate here
│       └─ [Generate New Token]           │ ← Click this
└─────────────────────────────────────────┘
```

### Method 2: Service Account Token (Production)

**Who Provides:** Data Platform Team / DevOps

**How to Request:**
```
To: data-platform@yourcompany.com
Subject: Service Account Token Request

Hi Team,

I need a service account token for automated job:

Project: [Name]
Purpose: [Scheduled ETL pipeline]
Environment: Production
Expiration: Never (or 1 year)
Permissions Needed: [Read/Write to specific tables]

Thanks!
```

**How You Receive It:**
```
Option 1: Secure Vault
- Admin stores in HashiCorp Vault
- You retrieve using vault CLI
- Token never sent via email

Option 2: Encrypted Channel
- Shared via 1Password / LastPass
- Secure link with password
- Auto-expires in 24 hours

Option 3: Configuration Management
- Stored in Azure Key Vault / AWS Secrets Manager
- Your application reads from there
- Never exposed directly
```

---

## Phase 4: Secure Token Storage

### ❌ NEVER DO THIS:

```python
# ❌ Hardcoded in code
databricks_token = "dapi1234567890"

# ❌ In git repository
# config.py with token

# ❌ Plain text file
# token.txt

# ❌ Shared via Slack/Email
```

### ✅ DO THIS:

#### **1. Local Development: .env File**

```bash
# Create .env file
cat > .env << EOF
DATABRICKS_HOST=https://yourcompany.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef...
DATABRICKS_CLUSTER_ID=1234-567890-abc123
EOF

# Secure it
chmod 600 .env

# Add to .gitignore
echo ".env" >> .gitignore
```

**Use in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("DATABRICKS_TOKEN")
host = os.getenv("DATABRICKS_HOST")
```

#### **2. Production: Secret Management**

**Option A: Azure Key Vault**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://mycompany-vault.vault.azure.net/",
    credential=credential
)

token = client.get_secret("databricks-token").value
```

**Option B: AWS Secrets Manager**
```python
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='databricks/token')
token = response['SecretString']
```

**Option C: HashiCorp Vault**
```python
import hvac

client = hvac.Client(url='https://vault.company.com')
secret = client.secrets.kv.v2.read_secret_version(
    path='databricks/token'
)
token = secret['data']['data']['token']
```

#### **3. CI/CD: Environment Variables**

**GitHub Actions:**
```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run pipeline
        env:
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
        run: python pipeline.py
```

**Azure DevOps:**
```yaml
# azure-pipelines.yml
variables:
  - group: databricks-secrets  # Created in Pipeline Library

steps:
- script: |
    python pipeline.py
  env:
    DATABRICKS_TOKEN: $(databricks-token)
```

---

## Phase 5: Find Required Information

### What You Need for Development:

```bash
# 1. Workspace URL
DATABRICKS_HOST=https://yourcompany.cloud.databricks.com

# 2. Access Token (from Phase 3)
DATABRICKS_TOKEN=dapi1234567890...

# 3. Cluster ID (from Databricks UI)
DATABRICKS_CLUSTER_ID=1234-567890-abc123

# 4. SQL Warehouse HTTP Path (for queries)
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/abc123def456
```

### How to Find Cluster ID:

```
1. Login to Databricks
2. Click "Compute" in sidebar
3. Click on your cluster name
4. Look at URL or cluster details:

   URL: .../clusters/1234-567890-abc123
                      ↑
                Cluster ID

   Or in details page:
   ┌──────────────────────────────────┐
   │ Cluster Details                  │
   │ Cluster ID: 1234-567890-abc123   │ ← Copy this
   │ Status: Running                  │
   └──────────────────────────────────┘
```

### How to Find SQL Warehouse HTTP Path:

```
1. Login to Databricks
2. Click "SQL" in sidebar
3. Click "SQL Warehouses"
4. Click on your warehouse
5. Go to "Connection Details" tab
6. Find "HTTP Path":

   ┌────────────────────────────────────────────┐
   │ Connection Details                         │
   │                                            │
   │ Server hostname:                           │
   │   yourcompany.cloud.databricks.com         │
   │                                            │
   │ HTTP Path:                                 │
   │   /sql/1.0/warehouses/abc123def456         │ ← Copy this
   │   [Copy] button                            │
   └────────────────────────────────────────────┘
```

---

## Phase 6: Test Connection

### Create Test Script:

```python
# test_databricks_connection.py
from databricks import sql
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    """Test Databricks connection"""
    print("🔍 Testing Databricks connection...")
    
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST").replace("https://", ""),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 'Connection successful!' as message")
        result = cursor.fetchone()
        
        print(f"✅ Success! {result[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

### Run Test:

```bash
# Activate venv
source venv/bin/activate

# Run test
python test_databricks_connection.py

# Expected output:
# 🔍 Testing Databricks connection...
# ✅ Success! Connection successful!
```

---

## Common Corporate Scenarios

### Scenario 1: Multiple Environments

```bash
# .env.dev (Development)
DATABRICKS_HOST=https://dev.databricks.company.com
DATABRICKS_TOKEN=dapi_dev_token...

# .env.prod (Production)  
DATABRICKS_HOST=https://prod.databricks.company.com
DATABRICKS_TOKEN=dapi_prod_token...

# Switch between environments:
cp .env.dev .env  # Use dev
cp .env.prod .env # Use prod
```

### Scenario 2: Team Shared Resources

```
Your team might have:
- Shared cluster: "team-analytics-cluster"
- Shared workspace folder: /Users/team-name/
- Shared SQL warehouse: "team-warehouse"
- Shared secrets scope: "team-secrets"

Ask your team lead for:
- Cluster ID to use
- Folder permissions
- Naming conventions
- Best practices documentation
```

### Scenario 3: Token Expiration

```
Tokens expire! Set reminders:

Day 1: Generate token (90 days expiration)
Day 80: Get reminder (10 days before expiration)
Day 85: Generate new token
Day 90: Old token stops working

Pro tip: Generate new token before old one expires!
```

---

## Troubleshooting

### "Invalid token"
```
Possible causes:
1. Token expired
2. Wrong token (check copy/paste)
3. Token revoked by admin
4. Wrong environment (dev token on prod)

Solution:
- Generate new token
- Check token carefully
- Contact admin if revoked
```

### "Permission denied"
```
Possible causes:
1. Insufficient permissions
2. Resource not accessible
3. IP restricted

Solution:
- Request permission from admin
- Check if you're on VPN (if required)
- Verify resource path
```

### "Cluster not found"
```
Possible causes:
1. Wrong cluster ID
2. Cluster terminated
3. No access to cluster

Solution:
- Verify cluster ID in UI
- Check cluster status
- Request access if needed
```

---

## Quick Reference

### Getting Help in Your Company

```
1. Internal Documentation
   - Confluence/Wiki
   - Read team docs first!

2. Slack Channels
   - #data-engineering
   - #databricks-support
   - #data-platform

3. Office Hours
   - Data platform team office hours
   - Weekly Q&A sessions

4. Direct Contact
   - Your tech lead
   - Data platform team
   - Databricks admin
```

### First Week Checklist

```
□ Request Databricks access
□ Wait for approval email
□ Login to workspace
□ Complete required training
□ Generate personal access token
□ Store token securely in .env
□ Find your cluster ID
□ Find SQL warehouse path
□ Test connection
□ Join team Slack channels
□ Read internal documentation
□ Ask senior engineer for review
```

---

## Summary

**Access Token in Corporate Environment:**

1. **Request access** → Manager/IT Portal
2. **Get approved** → Data Platform Team
3. **Login** → SSO/Company credentials
4. **Generate token** → User Settings → Developer → Access Tokens
5. **Store securely** → .env file (local) or Secret vault (production)
6. **Test** → Run connection test script

**Key Points:**
- ✅ Token is YOUR responsibility to keep secure
- ✅ Never commit to git
- ✅ Regenerate before expiration
- ✅ Use secret management for production
- ✅ Ask your team for help!

**Remember:** Every company is slightly different. Always check your company's internal documentation first! 📚
