from time import time
from mcp.server.fastmcp import FastMCP

# ------------------------------------
# Create MCP Server
# ------------------------------------
mcp = FastMCP("worker-system-monitor")

# ------------------------------------
# Fake Worker Data (Simulated laptops)
# ------------------------------------
workers = [
    {
        "worker_id": "worker-01",
        "name": "Worker One",
        "battery_percent": 82,
        "plugged_in": True,

        "cpu_usage_percent": 18,
        "cpu_cores_physical": 6,
        "cpu_cores_logical": 12,
        "cpu_frequency_mhz": 3200,

        "ram_total_gb": 8,
        "ram_used_percent": 64,
        "ram_available_gb": 2.9,

        "disk_total_gb": 512,
        "disk_used_percent": 70,
        "disk_free_gb": 153,

        "network_sent_mb": 1200,
        "network_received_mb": 3400,

        "running_processes": 145,
        "system_uptime_seconds": 86400
    },

    {
        "worker_id": "worker-02",
        "name": "Worker Two",
        "battery_percent": 55,
        "plugged_in": False,

        "cpu_usage_percent": 35,
        "cpu_cores_physical": 8,
        "cpu_cores_logical": 16,
        "cpu_frequency_mhz": 3600,

        "ram_total_gb": 16,
        "ram_used_percent": 48,
        "ram_available_gb": 8.3,

        "disk_total_gb": 1024,
        "disk_used_percent": 62,
        "disk_free_gb": 389,

        "network_sent_mb": 890,
        "network_received_mb": 2100,

        "running_processes": 172,
        "system_uptime_seconds": 172800
    },

    {
        "worker_id": "worker-03",
        "name": "Worker Three",
        "battery_percent": 91,
        "plugged_in": True,

        "cpu_usage_percent": 12,
        "cpu_cores_physical": 12,
        "cpu_cores_logical": 24,
        "cpu_frequency_mhz": 4200,

        "ram_total_gb": 32,
        "ram_used_percent": 41,
        "ram_available_gb": 18.9,

        "disk_total_gb": 2048,
        "disk_used_percent": 45,
        "disk_free_gb": 1126,

        "network_sent_mb": 540,
        "network_received_mb": 980,

        "running_processes": 133,
        "system_uptime_seconds": 259200
    },

    {
        "worker_id": "worker-04",
        "name": "Worker Four",
        "battery_percent": 19,
        "plugged_in": False,

        "cpu_usage_percent": 67,
        "cpu_cores_physical": 4,
        "cpu_cores_logical": 4,
        "cpu_frequency_mhz": 2100,

        "ram_total_gb": 4,
        "ram_used_percent": 88,
        "ram_available_gb": 0.4,

        "disk_total_gb": 256,
        "disk_used_percent": 91,
        "disk_free_gb": 23,

        "network_sent_mb": 3400,
        "network_received_mb": 7800,

        "running_processes": 221,
        "system_uptime_seconds": 43200
    },

    {
        "worker_id": "worker-05",
        "name": "Worker Five",
        "battery_percent": 63,
        "plugged_in": True,

        "cpu_usage_percent": 29,
        "cpu_cores_physical": 8,
        "cpu_cores_logical": 16,
        "cpu_frequency_mhz": 3500,

        "ram_total_gb": 16,
        "ram_used_percent": 52,
        "ram_available_gb": 7.6,

        "disk_total_gb": 1024,
        "disk_used_percent": 58,
        "disk_free_gb": 430,

        "network_sent_mb": 1100,
        "network_received_mb": 2600,

        "running_processes": 160,
        "system_uptime_seconds": 129600
    }
]

@mcp.tool(
    description=(
        "Health check tool used to confirm that this worker MCP server "
        "is running and reachable. Returns basic status information "
        "such as server state, worker name, and current timestamp. "
        "This tool should be used before requesting detailed system metrics."
    )
)
def health_check():
    return {
        "server_status": "running",
        "timestamp": int(time()),
        "workers_health": [
            {
                "worker_id": worker["worker_id"],
                "name": worker["name"],
                "status": "online"
            }
            for worker in workers
        ]
    }

# ------------------------------------
# Battery Status Tool 
# ------------------------------------
@mcp.tool(
    description=(
        "Returns battery percentage and charging status "
        "for all workers separately. "
        "Useful for detecting low battery devices."
    )
)
def get_battery_status():
    return {
        "battery_status": [
            {
                "worker_id": worker["worker_id"],
                "name": worker["name"],
                "battery_percent": worker["battery_percent"],
                "plugged_in": worker["plugged_in"]
            }
            for worker in workers
        ]
    }

# ------------------------------------
# RAM Status Tool
# ------------------------------------
@mcp.tool(
    description=(
        "Returns RAM usage details "
        "for all workers separately."
    )
)
def get_ram_status():
    return {
        "ram_status": [
            {
                "worker_id": worker["worker_id"],
                "name": worker["name"],
                "ram_total_gb": worker["ram_total_gb"],
                "ram_used_percent": worker["ram_used_percent"],
                "ram_available_gb": worker["ram_available_gb"]
            }
            for worker in workers
        ]
    }


# ------------------------------------
# CPU Status Tool 
# ------------------------------------
@mcp.tool(
    description=(
        "Returns CPU usage and core information "
        "for all workers separately."
    )
)
def get_cpu_status():
    return {
        "cpu_status": [
            {
                "worker_id": worker["worker_id"],
                "name": worker["name"],
                "cpu_usage_percent": worker["cpu_usage_percent"],
                "cpu_cores_physical": worker["cpu_cores_physical"],
                "cpu_cores_logical": worker["cpu_cores_logical"],
                "cpu_frequency_mhz": worker["cpu_frequency_mhz"]
            }
            for worker in workers
        ]
    }


# ------------------------------------
# Disk Status Tool
# ------------------------------------
@mcp.tool(
    description=(
        "Returns disk storage details "
        "for all workers separately."
    )
)
def get_disk_status():
    return {
        "disk_status": [
            {
                "worker_id": worker["worker_id"],
                "name": worker["name"],
                "disk_total_gb": worker["disk_total_gb"],
                "disk_used_percent": worker["disk_used_percent"],
                "disk_free_gb": worker["disk_free_gb"]
            }
            for worker in workers
        ]
    }


# ------------------------------------
# Generic Data Tool (BEST PRACTICE)
# ------------------------------------
@mcp.tool(
    description=(
        "Return system details of all workers. "
        "Each worker includes: "
        "id (worker identifier), "
        "name (worker name), "
        "ram_gb (installed RAM size in gigabytes), "
        "battery (battery percentage). "
        "This data can be used by admins to filter, compare, "
        "and analyze worker laptops such as identifying "
        "high-RAM machines or low-battery devices. "
        "Also returns a separate list of worker names."
    )
)

def get_all_workers_info():

    return {
        "workers": workers,
        "names": [worker["name"] for worker in workers]
    }

# ------------------------------------
# Start MCP Server
# ------------------------------------
if __name__ == "__main__":
    print("Worker One MCP server is running")
    print("Ready to receive MCP tool calls")
    mcp.run()