# 🔧 Airflow Setup - Fixed & Working!

## ✅ Issues Fixed

### **1. Database Path Issue**
- **Problem:** Relative SQLite path not allowed
- **Fix:** Changed to absolute path
- **Config:** `sqlite:////Users/udayshankar/Documents/ML Projects/data-mastery/realworld-usecases/01-modern-lakehouse/airflow/airflow.db`

### **2. Executor Incompatibility**
- **Problem:** `LocalExecutor` doesn't work with SQLite
- **Fix:** Changed to `SequentialExecutor`
- **Note:** Sequential executes one task at a time (fine for development/portfolio)

### **3. Missing Session Table**
- **Problem:** Database not properly initialized
- **Fix:** Ran `airflow db migrate` with correct settings

---

## 🚀 Working Setup (Tested & Verified)

### **Step 1: Navigate to airflow directory**
```bash
cd "/Users/udayshankar/Documents/ML Projects/data-mastery/realworld-usecases/01-modern-lakehouse/airflow"
```

### **Step 2: Activate virtual environment**
```bash
source venv/bin/activate
```

### **Step 3: Set environment variable**
```bash
export AIRFLOW_HOME=$(pwd)
```

### **Step 4: Start Airflow Webserver**
```bash
airflow webserver --port 8080
```

### **Step 5: Start Scheduler (in NEW terminal)**
```bash
cd "/Users/udayshankar/Documents/ML Projects/data-mastery/realworld-usecases/01-modern-lakehouse/airflow"
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)
airflow scheduler
```

### **Step 6: Access UI**
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

---

## ✅ What's Ready

- ✅ Database initialized (airflow.db)
- ✅ Admin user created (admin/admin)
- ✅ DAG ready (`lakehouse_taxi_pipeline`)
- ✅ Configuration fixed (SequentialExecutor + absolute paths)

---

## 📊 Expected Behavior

1. **Webserver starts** on port 8080
2. **Scheduler** detects DAGs in `dags/` folder
3. **UI accessible** at http://localhost:8080
4. **DAG appears** as `lakehouse_taxi_pipeline`
5. **Can trigger manually** or set schedule

---

## ⚠️ Known Limitations

### **SequentialExecutor**
- Executes **one task at a time** (no parallelism)
- Perfect for development/demos
- For production, use PostgreSQL + LocalExecutor or CeleryExecutor

### **SQLite**
- Single-threaded database
- Not recommended for production
- Fine for portfolio/learning

---

## 🎯 Next Steps

1. **Start webserver & scheduler** (commands above)
2. **Login to UI** (admin/admin)
3. **Find DAG:** `lakehouse_taxi_pipeline`
4. **Toggle ON** (unpause the DAG)
5. **Trigger manually** (click play button)
6. **Watch execution** in Graph View

---

## 📸 Portfolio Screenshots

Once running, take screenshots of:
1. DAG Graph View (shows task dependencies)
2. DAG Grid View (shows successful runs)
3. Task logs (shows execution details)
4. Gantt chart (shows timing)

---

## 🆘 Still Having Issues?

### **Port 8080 already in use?**
```bash
# Use different port
airflow webserver --port 8081
```

### **DAG not appearing?**
```bash
# Check DAG syntax
python dags/lakehouse_taxi_pipeline.py

# List DAGs
airflow dags list

# Check for import errors
airflow dags list-import-errors
```

### **Want to reset everything?**
```bash
# Stop webserver & scheduler (Ctrl+C in both terminals)
cd airflow
rm -f airflow.db airflow.db-shm airflow.db-wal
export AIRFLOW_HOME=$(pwd)
source venv/bin/activate
airflow db migrate
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin
```

---

## 🎉 Success Indicators

✅ Webserver log shows: `"Listening at: http://0.0.0.0:8080"`  
✅ Scheduler log shows: `"Starting the scheduler"`  
✅ UI loads without errors  
✅ DAG `lakehouse_taxi_pipeline` appears in list  
✅ Can login with admin/admin  

---

**You're all set! Happy orchestrating! 🚀**

*Last Updated: May 14, 2026 (Fixed & Tested)*
