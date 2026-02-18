from mcp.server.fastmcp import FastMCP
import psutil
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import StreamingResponse
import json
import time

# -------------------------------------------------
# 1. Initialize FastMCP
# -------------------------------------------------
mcp = FastMCP("Worker-One")

# -------------------------------------------------
# 2. Tool: Get Worker Status 
# -------------------------------------------------
@mcp.tool(
    description=(
        "Retrieve comprehensive real-time system metrics from this worker laptop "
        "using psutil. The returned data includes battery status (percentage and "
        "charging state), CPU utilization, physical and logical core counts, CPU "
        "frequency, total and available RAM, RAM usage percentage, disk capacity "
        "and usage, network data sent and received, number of running processes, "
        "and system uptime in seconds. "
        "This information can be used by an admin or AI assistant to perform "
        "monitoring, comparison, filtering, trend analysis, and health assessment "
        "across multiple worker machines without requiring additional tools."
    )
)
def get_worker_status():
    """
    Returns detailed system status of this worker laptop.
    """

    # Battery info
    battery = psutil.sensors_battery()

    # CPU info
    cpu_freq = psutil.cpu_freq()

    # RAM info
    memory = psutil.virtual_memory()

    # Disk info
    disk = psutil.disk_usage('/')

    # Network info
    net = psutil.net_io_counters()

    # ⏱Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    return {
        # Battery
        "battery_percent": f"{battery.percent}%" if battery else "N/A",
        "plugged_in": battery.power_plugged if battery else "N/A",

        # CPU
        "cpu_usage": f"{psutil.cpu_percent(interval=1)}%",
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "cpu_cores_logical": psutil.cpu_count(logical=True),
        "cpu_frequency_mhz": round(cpu_freq.current, 2) if cpu_freq else "N/A",

        # RAM
        "ram_total_gb": round(memory.total / (1024**3), 2),
        "ram_used_percent": f"{memory.percent}%",
        "ram_available_gb": round(memory.available / (1024**3), 2),

        # Disk
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "disk_used_percent": f"{disk.percent}%",
        "disk_free_gb": round(disk.free / (1024**3), 2),

        # Network
        "network_sent_mb": round(net.bytes_sent / (1024**2), 2),
        "network_received_mb": round(net.bytes_recv / (1024**2), 2),

        # Processes
        "running_processes": len(psutil.pids()),

        # Uptime
        "system_uptime_seconds": uptime_seconds
    }

# -------------------------------------------------
# 3. SSE Handler
# -------------------------------------------------
async def handle_sse(request):
    """Handle SSE connections and tool calls"""

    if request.method == "POST":
        body = await request.json()
        tool_name = body.get("params", {}).get("name", "")

        if tool_name == "get_worker_status":
            result = get_worker_status()
            return StreamingResponse(
                iter([f"data: {json.dumps(result)}\n\n"]),
                media_type="text/event-stream"
            )

    return StreamingResponse(iter([]), media_type="text/event-stream")

# -------------------------------------------------
# 4. Run Server
# -------------------------------------------------
if __name__ == "__main__":
    app = Starlette(routes=[
        Route("/sse", handle_sse, methods=["GET", "POST"]),
        Route("/sse/tools/call", handle_sse, methods=["POST"]),
    ])

    print("=" * 50)
    print("Worker is active at port 8000")
    print("Listening on all network interfaces (0.0.0.0:8000)")
    print("=" * 50)

    uvicorn.run(app, host="0.0.0.0", port=8000)