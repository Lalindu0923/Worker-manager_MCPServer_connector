from mcp.server.fastmcp import FastMCP
import httpx
import json
import random

# ------------------------------------
# Initialize FastMCP for Manager
# ------------------------------------
mcp = FastMCP("Manager")

# ------------------------------------
# Real Worker Configuration
# ------------------------------------
WORKERS = {
    "bumal": {
        "ip": "http://10.93.179.61:8000",
        "floor": "2",
        "section": "A"
    },
    "budhini": {
        "ip": "http://10.93.179.74:8000",
        "floor": "2",
        "section": "B"
    },
}

SIMULATED_WORKERS = {
    "sim_worker_01": {
        "ip": "http://sim-01.local:8000",
        "floor": "1",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 23.5,
            "ram_percent": 41.2,
            "disk_percent": 55.8,
            "uptime_seconds": 86400,
            "battery_percent": 87.0,
            "plugged_in": True
        }
    },
    "sim_worker_02": {
        "ip": "http://sim-02.local:8000",
        "floor": "1",
        "section": "B",
        "mock_stats": {
            "cpu_percent": 67.3,
            "ram_percent": 78.9,
            "disk_percent": 30.1,
            "uptime_seconds": 43200,
            "battery_percent": 52.0,
            "plugged_in": False
        }
    },
    "sim_worker_03": {
        "ip": "http://sim-03.local:8000",
        "floor": "2",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 5.1,
            "ram_percent": 22.4,
            "disk_percent": 88.6,
            "uptime_seconds": 172800,
            "battery_percent": 15.0,
            "plugged_in": False
        }
    },
    "sim_worker_04": {
        "ip": "http://sim-04.local:8000",
        "floor": "2",
        "section": "C",
        "mock_stats": {
            "cpu_percent": 91.7,
            "ram_percent": 95.3,
            "disk_percent": 70.0,
            "uptime_seconds": 3600,
            "battery_percent": 99.0,
            "plugged_in": True
        }
    },
    "sim_worker_05": {
        "ip": "http://sim-05.local:8000",
        "floor": "3",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 44.0,
            "ram_percent": 60.5,
            "disk_percent": 45.2,
            "uptime_seconds": 259200,
            "battery_percent": 73.5,
            "plugged_in": True
        }
    },
    "sim_worker_06": {
        "ip": "http://sim-06.local:8000",
        "floor": "1",
        "section": "C",
        "mock_stats": {
            "cpu_percent": 32.4,
            "ram_percent": 51.3,
            "disk_percent": 62.7,
            "uptime_seconds": 129600,
            "battery_percent": 88.2,
            "plugged_in": True
        }
    },
    "sim_worker_07": {
        "ip": "http://sim-07.local:8000",
        "floor": "2",
        "section": "B",
        "mock_stats": {
            "cpu_percent": 76.8,
            "ram_percent": 82.1,
            "disk_percent": 28.5,
            "uptime_seconds": 86400,
            "battery_percent": 45.6,
            "plugged_in": False
        }
    },
    "sim_worker_08": {
        "ip": "http://sim-08.local:8000",
        "floor": "3",
        "section": "B",
        "mock_stats": {
            "cpu_percent": 12.5,
            "ram_percent": 33.7,
            "disk_percent": 71.2,
            "uptime_seconds": 345600,
            "battery_percent": 92.1,
            "plugged_in": True
        }
    },
    "sim_worker_09": {
        "ip": "http://sim-09.local:8000",
        "floor": "1",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 58.3,
            "ram_percent": 64.9,
            "disk_percent": 41.8,
            "uptime_seconds": 172800,
            "battery_percent": 61.4,
            "plugged_in": False
        }
    },
    "sim_worker_10": {
        "ip": "http://sim-10.local:8000",
        "floor": "2",
        "section": "C",
        "mock_stats": {
            "cpu_percent": 85.2,
            "ram_percent": 91.5,
            "disk_percent": 54.3,
            "uptime_seconds": 7200,
            "battery_percent": 35.8,
            "plugged_in": True
        }
    },
    "sim_worker_11": {
        "ip": "http://sim-11.local:8000",
        "floor": "3",
        "section": "C",
        "mock_stats": {
            "cpu_percent": 19.7,
            "ram_percent": 45.2,
            "disk_percent": 78.9,
            "uptime_seconds": 432000,
            "battery_percent": 81.3,
            "plugged_in": False
        }
    },
    "sim_worker_12": {
        "ip": "http://sim-12.local:8000",
        "floor": "1",
        "section": "B",
        "mock_stats": {
            "cpu_percent": 48.6,
            "ram_percent": 72.4,
            "disk_percent": 35.1,
            "uptime_seconds": 259200,
            "battery_percent": 77.5,
            "plugged_in": True
        }
    },
    "sim_worker_13": {
        "ip": "http://sim-13.local:8000",
        "floor": "2",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 71.4,
            "ram_percent": 86.3,
            "disk_percent": 48.6,
            "uptime_seconds": 93600,
            "battery_percent": 29.2,
            "plugged_in": False
        }
    },
    "sim_worker_14": {
        "ip": "http://sim-14.local:8000",
        "floor": "3",
        "section": "A",
        "mock_stats": {
            "cpu_percent": 44.0,
            "ram_percent": 38.5,
            "disk_percent": 61.2,
            "uptime_seconds": 518400,
            "battery_percent": 94.7,
            "plugged_in": True
        }
    },
    "sim_worker_15": {
        "ip": "http://sim-15.local:8000",
        "floor": "2",
        "section": "B",
        "mock_stats": {
            "cpu_percent": 63.9,
            "ram_percent": 74.2,
            "disk_percent": 52.7,
            "uptime_seconds": 201600,
            "battery_percent": 56.8,
            "plugged_in": True
        }
    },
}

# ------------------------------------
# Helper: Get simulated stats (with slight random variance for realism)
# ------------------------------------
def get_simulated_stats(worker_name: str) -> dict:
    base = SIMULATED_WORKERS[worker_name]["mock_stats"]
    return {
        "cpu_percent": round(base["cpu_percent"] + random.uniform(-2, 2), 1),
        "ram_percent": round(base["ram_percent"] + random.uniform(-1, 1), 1),
        "disk_percent": round(base["disk_percent"], 1),
        "uptime_seconds": base["uptime_seconds"],
        "battery_percent": round(base["battery_percent"] + random.uniform(-0.5, 0.5), 1),
        "plugged_in": base["plugged_in"]
    }

# ------------------------------------
# Helper Function: Check Connection
# ------------------------------------
async def check_worker_connection(ip: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{ip}/sse/tools/call",
                json={
                    "method": "tools/call",
                    "params": {"name": "get_worker_status", "arguments": {}}
                }
            )
            if response.status_code == 200:
                return "Connected"
    except:
        pass
    return "Not Connected"

# ------------------------------------
# Tool 1: List All Workers
# ------------------------------------
@mcp.tool(
    description=(
        "Returns a summary of all workers under management, including their IP address, "
        "floor, section, and connection status. Includes both real workers and simulated "
        "test workers (prefixed with 'sim_'). Use this when asked for a general "
        "overview or summary of all workers."
    )
)
async def list_workers() -> dict:
    """Returns all workers (real + simulated) with connection status."""

    results = {}

    # Real workers — check actual connection
    for name, info in WORKERS.items():
        status = await check_worker_connection(info["ip"])
        results[name] = {
            "ip": info["ip"],
            "floor": info["floor"],
            "section": info["section"],
            "status": status,
            "type": "real"
        }

    # Simulated workers — always "Connected"
    for name, info in SIMULATED_WORKERS.items():
        results[name] = {
            "ip": info["ip"],
            "floor": info["floor"],
            "section": info["section"],
            "status": "Connected (Simulated)",
            "type": "simulated"
        }

    return {
        "total_workers": len(results),
        "real_workers": len(WORKERS),
        "simulated_workers": len(SIMULATED_WORKERS),
        "workers": results
    }

# ------------------------------------
# Generic Helper Function: Call Worker Tool by IP
# ------------------------------------
async def call_worker_tool(ip: str, tool_name: str, arguments: dict = None):
    """Generic function to call any tool on a worker using its IP."""

    if arguments is None:
        arguments = {}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{ip}/sse/tools/call",
                json={
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                text = response.text
                if text.startswith("data: "):
                    json_data = text.replace("data: ", "").strip()
                    return json.loads(json_data)
                else:
                    return {"raw_response": text}

            return {
                "error": f"HTTP {response.status_code}",
                "details": response.text
            }

    except Exception as e:
        return {"error": str(e)}

# ------------------------------------
# Tool 2: Get Battery by Worker Name
# ------------------------------------
@mcp.tool(
    description=(
        "Returns battery information of a specific worker by name. "
        "Works for both real and simulated (sim_*) workers. "
        "Returns battery percentage and charging status (plugged_in)."
    )
)
async def get_worker_info(worker_name: str) -> dict:
    """Returns battery info of a specific worker (real or simulated)."""

    # Check simulated workers first
    if worker_name in SIMULATED_WORKERS:
        stats = get_simulated_stats(worker_name)
        return {
            "battery_percent": stats["battery_percent"],
            "plugged_in": stats["plugged_in"],
            "source": "simulated"
        }

    if worker_name not in WORKERS:
        return {"error": f"Worker '{worker_name}' not found in real or simulated workers."}

    worker_ip = WORKERS[worker_name]["ip"]
    result = await call_worker_tool(worker_ip, "get_worker_status")

    if "error" in result:
        return result

    return {
        "battery_percent": result.get("battery_percent", "N/A"),
        "plugged_in": result.get("plugged_in", "N/A"),
        "source": "real"
    }

# ------------------------------------
# Tool 3: Get System Stats by Floor & Section
# ------------------------------------
@mcp.tool(
    description=(
        "Returns complete system status of all workers (real + simulated) located "
        "in a given floor and section. Includes CPU, RAM, disk, uptime, and battery. "
        "Use this when filtering workers by location."
    )
)
async def get_system_stats_by_location(floor: str, section: str) -> dict:
    """Returns system stats of workers in given floor & section (real + simulated)."""

    results = {}

    # Real workers
    for name, info in WORKERS.items():
        if info["floor"] == floor and info["section"] == section:
            stats = await call_worker_tool(info["ip"], "get_worker_status")
            results[name] = {
                "ip": info["ip"],
                "type": "real",
                "status": "error" if "error" in stats else "success",
                "system_stats": stats
            }

    # Simulated workers
    for name, info in SIMULATED_WORKERS.items():
        if info["floor"] == floor and info["section"] == section:
            stats = get_simulated_stats(name)
            results[name] = {
                "ip": info["ip"],
                "type": "simulated",
                "status": "success",
                "system_stats": stats
            }

    if not results:
        return {"message": f"No workers found on floor {floor}, section {section}."}

    return results

# ------------------------------------
# Tool 4: Get System Stats by Worker Name
# ------------------------------------
@mcp.tool(
    description=(
        "Returns full system statistics of a specific worker by name (real or simulated). "
        "Stats include CPU, RAM, disk usage, uptime, and battery information."
    )
)
async def get_worker_system_stats(worker_name: str) -> dict:
    """Returns system stats of a specific worker (real or simulated)."""

    # Simulated worker
    if worker_name in SIMULATED_WORKERS:
        stats = get_simulated_stats(worker_name)
        return {**stats, "source": "simulated"}

    if worker_name not in WORKERS:
        return {"error": f"Worker '{worker_name}' not found in real or simulated workers."}

    worker_ip = WORKERS[worker_name]["ip"]
    return await call_worker_tool(worker_ip, "get_worker_status")

# ------------------------------------
# Tool 5: Get All Workers System Stats
# ------------------------------------
@mcp.tool(
    description=(
        "Returns complete system statistics for ALL workers — both real and simulated. "
        "Includes CPU, RAM, disk usage, uptime, battery, floor, section, and type. "
        "Use this when a full system-wide overview is needed."
    )
)
async def get_all_workers_system_stats() -> dict:
    """Returns system stats for all workers (real + simulated)."""

    results = {}

    # Real workers
    for name, info in WORKERS.items():
        stats = await call_worker_tool(info["ip"], "get_worker_status")
        results[name] = {
            "ip": info["ip"],
            "floor": info["floor"],
            "section": info["section"],
            "type": "real",
            "status": "error" if "error" in stats else "success",
            "stats": stats
        }

    # Simulated workers
    for name, info in SIMULATED_WORKERS.items():
        stats = get_simulated_stats(name)
        results[name] = {
            "ip": info["ip"],
            "floor": info["floor"],
            "section": info["section"],
            "type": "simulated",
            "status": "success",
            "stats": stats
        }

    return {
        "total_workers": len(results),
        "real_workers": len(WORKERS),
        "simulated_workers": len(SIMULATED_WORKERS),
        "workers": results
    }

# ------------------------------------
# Run Manager
# ------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Manager MCP Server - Hybrid Approach")
    print(f"Total Real Workers:      {len(WORKERS)}")
    print(f"Total Simulated Workers: {len(SIMULATED_WORKERS)}")
    print("=" * 60)
    print("Manager MCP Server is running...")
    mcp.run(transport="stdio")