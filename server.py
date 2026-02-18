from mcp.server.fastmcp import FastMCP
import httpx
import json


""" This MCP server connects to real worker machines on the network to fetch live system metrics.
    It also includes demo worker data for testing and comparison.
    this include real workers.
"""
# ------------------------------------
# Configuration - ADD YOUR REAL WORKERS HERE!
# ------------------------------------
# To add more workers: Just add another dictionary to the list below
REAL_WORKERS = [
    {
        "name": "bumal's Laptop",
        "ip": "10.189.47.62",
        "port": 8000
    },
    
    {
        "name": "buddhini's Laptop",
        "ip": "10.189.47.74",
        "port": 8000
    }
    
]

FAKE_WORKERS = [
    {
        "worker_id": "demo-worker-02",
        "worker_name": "Demo Worker 2",
        "worker_ip": "DEMO",
        "battery_percent": "25%",
        "plugged_in": False,
        "cpu_usage": "78%",
        "cpu_cores_physical": 4,
        "cpu_cores_logical": 8,
        "cpu_frequency_mhz": 2800,
        "ram_total_gb": 8.0,
        "ram_used_percent": "85%",
        "ram_available_gb": 1.2,
        "disk_total_gb": 256.0,
        "disk_used_percent": "92%",  # Low storage!
        "disk_free_gb": 20.0,
        "network_sent_mb": 450.0,
        "network_received_mb": 1200.0,
        "running_processes": 189,
        "system_uptime_seconds": 259200
    },
    {
        "worker_id": "demo-worker-03",
        "worker_name": "Demo Worker 3",
        "worker_ip": "DEMO",
        "battery_percent": "95%",
        "plugged_in": True,
        "cpu_usage": "15%",
        "cpu_cores_physical": 12,
        "cpu_cores_logical": 24,
        "cpu_frequency_mhz": 4200,
        "ram_total_gb": 32.0,
        "ram_used_percent": "42%",
        "ram_available_gb": 18.5,
        "disk_total_gb": 2048.0,
        "disk_used_percent": "38%",
        "disk_free_gb": 1269.0,
        "network_sent_mb": 780.0,
        "network_received_mb": 2100.0,
        "running_processes": 142,
        "system_uptime_seconds": 432000
    },
    {
        "worker_id": "demo-worker-04",
        "worker_name": "Demo Worker 4",
        "worker_ip": "DEMO",
        "battery_percent": "10%",  # Low battery!
        "plugged_in": False,
        "cpu_usage": "55%",
        "cpu_cores_physical": 6,
        "cpu_cores_logical": 12,
        "cpu_frequency_mhz": 3100,
        "ram_total_gb": 16.0,
        "ram_used_percent": "68%",
        "ram_available_gb": 5.1,
        "disk_total_gb": 512.0,
        "disk_used_percent": "73%",
        "disk_free_gb": 138.0,
        "network_sent_mb": 1500.0,
        "network_received_mb": 3800.0,
        "running_processes": 201,
        "system_uptime_seconds": 86400
    }
]
# ========== END FAKE DEMO WORKERS ==========

# ------------------------------------
# Create MCP Server
# ------------------------------------
mcp = FastMCP("worker-system-monitor-live")

# ------------------------------------
# Helper Function (Internal Use)
# ------------------------------------
def fetch_worker_data(worker_ip, worker_port, worker_name):
    """
    Internal helper to fetch data from a single worker.
    Returns formatted worker data or error status.
    """
    try:
        url = f"http://{worker_ip}:{worker_port}/sse/tools/call"
        payload = {
            "params": {
                "name": "get_worker_status"
            }
        }
        
        response = httpx.post(url, json=payload, timeout=10.0)
        
        if response.status_code == 200:
            data = response.text.strip()
            if data.startswith("data: "):
                json_str = data[6:]
                worker_data = json.loads(json_str)
                return {
                    "status": "success",
                    "worker_name": worker_name,
                    "worker_ip": worker_ip,
                    **worker_data
                }
        
        return {
            "status": "error",
            "worker_name": worker_name,
            "worker_ip": worker_ip,
            "message": f"HTTP {response.status_code}"
        }
            
    except httpx.ConnectError:
        return {
            "status": "error",
            "worker_name": worker_name,
            "worker_ip": worker_ip,
            "message": "Cannot connect - check if worker is running and firewall allows connections"
        }
    except Exception as e:
        return {
            "status": "error",
            "worker_name": worker_name,
            "worker_ip": worker_ip,
            "message": str(e)
        }

# ------------------------------------
# Tool: Get Worker Status (from real machine)
# ------------------------------------
@mcp.tool(
    description=(
        "Retrieve real-time system metrics from the first connected worker laptop. "
        "Returns battery status, CPU usage, RAM, disk, network stats, "
        "running processes, and system uptime. This data comes from a live "
        "worker machine on the network. For multiple workers, use get_all_workers() instead."
    )
)
def get_worker_status():
    """
    Connects to the FIRST worker machine and retrieves live system data.
    For backward compatibility - returns data from first worker in REAL_WORKERS list.
    """
    if not REAL_WORKERS:
        return {
            "status": "error",
            "message": "No real workers configured. Add workers to REAL_WORKERS list at top of file."
        }
    
    first_worker = REAL_WORKERS[0]
    return fetch_worker_data(
        first_worker["ip"],
        first_worker["port"],
        first_worker["name"]
    )


@mcp.tool(
    description=(
        "Test connection to all configured worker machines. Returns connection status "
        "for each worker including IP, port, and reachability. Use this to verify "
        "which workers are online before requesting detailed system metrics."
    )
)
def test_worker_connection():
    """
    Tests connection to ALL configured real workers.
    Returns status for each worker in REAL_WORKERS list.
    """
    if not REAL_WORKERS:
        return {
            "status": "error",
            "message": "No real workers configured. Add workers to REAL_WORKERS list at top of file."
        }
    
    results = []
    for worker in REAL_WORKERS:
        try:
            url = f"http://{worker['ip']}:{worker['port']}/sse"
            response = httpx.get(url, timeout=5.0)
            
            results.append({
                "worker_name": worker["name"],
                "status": "connected",
                "worker_ip": worker["ip"],
                "worker_port": worker["port"],
                "http_status": response.status_code,
                "message": "Reachable!"
            })
        except Exception as e:
            results.append({
                "worker_name": worker["name"],
                "status": "disconnected",
                "worker_ip": worker["ip"],
                "worker_port": worker["port"],
                "error": str(e),
                "message": "Cannot reach worker"
            })
    
    return {
        "total_workers": len(results),
        "workers": results
    }


# ========== FAKE WORKERS TOOL ==========
@mcp.tool(
    description=(
        "Get status of ALL workers (both real and demo). Returns a combined list "
        "of ALL real worker machines plus demo workers. Use this to compare multiple "
        "machines, identify issues like low storage or battery, filter by specs, "
        "or analyze performance across all workers. Each worker includes ID, name, "
        "IP (or 'DEMO'), battery, CPU, RAM, disk, network stats, and uptime."
    )
)
def get_all_workers():
    """
    Returns all workers: ALL real workers (from network) + demo workers (fake data).
    Useful for comparative analysis across multiple machines.
    """
    all_workers = []
    
    # Fetch data from ALL real workers
    for idx, worker in enumerate(REAL_WORKERS, start=1):
        real_worker_data = fetch_worker_data(
            worker["ip"],
            worker["port"],
            worker["name"]
        )
        
        # Format worker data
        formatted_worker = {
            "worker_id": f"real-worker-{idx:02d}",
            "worker_name": f"{worker['name']} (Real)",
            **real_worker_data
        }
        all_workers.append(formatted_worker)
    
    # Add fake/demo workers
    all_workers.extend(FAKE_WORKERS)
    
    return {
        "total_workers": len(all_workers),
        "real_workers_count": len(REAL_WORKERS),
        "demo_workers_count": len(FAKE_WORKERS),
        "workers": all_workers
    }
# ========== END FAKE WORKERS TOOL - DELETE UP TO HERE ==========


# ------------------------------------
# Start MCP Server
# ------------------------------------
if __name__ == "__main__":
    import sys
    sys.stderr.write("=" * 60 + "\n")
    sys.stderr.write("Live Worker Monitor MCP Server\n")
    sys.stderr.write("=" * 60 + "\n")
    sys.stderr.write(f"Configured Real Workers: {len(REAL_WORKERS)}\n")
    for idx, worker in enumerate(REAL_WORKERS, start=1):
        sys.stderr.write(f"  {idx}. {worker['name']} - {worker['ip']}:{worker['port']}\n")
    sys.stderr.write("\n")
    sys.stderr.write("To add more workers: Edit REAL_WORKERS list at top of file\n")
    sys.stderr.write("\n")
    sys.stderr.write("Available tools:\n")
    sys.stderr.write("  1. test_worker_connection - Check all workers\n")
    sys.stderr.write("  2. get_worker_status - Get first worker's metrics\n")
    sys.stderr.write("  3. get_all_workers - Get ALL workers (real + demo)\n")
    sys.stderr.write("=" * 60 + "\n")
    mcp.run()