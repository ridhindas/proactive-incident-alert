from fastapi import FastAPI
import psutil
import os

app = FastAPI()
memory_leak_storage = []

@app.get("/")
def read_root():
    return {"status": "healthy"}

@app.get("/leak")
def simulate_leak():
    # Adds ~10MB per call to simulate a memory leak
    memory_leak_storage.append(" " * 1024 * 1024 * 10)
    return {"allocated_blocks": len(memory_leak_storage)}

@app.get("/metrics")
def get_metrics():
    # Report the memory usage of this specific container process
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / (1024 * 1024)
    return {"memory_usage_mb": round(mem_mb, 2)}
