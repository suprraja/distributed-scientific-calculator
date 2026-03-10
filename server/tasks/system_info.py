import psutil

def get_system_info():
    """
    Collects useful Raspberry Pi / system metrics.
    Returns a dictionary with the data.
    """
    try:
        # CPU usage (average over last second)
        cpu_percent = psutil.cpu_percent(interval=1)

        # CPU temperature (Raspberry Pi specific)
        # Reads from thermal zone (common on Pi OS)
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp_c = float(f.read().strip()) / 1000.0

        # Memory usage
        mem = psutil.virtual_memory()
        mem_used_gb = mem.used / (1024 ** 3)
        mem_total_gb = mem.total / (1024 ** 3)
        mem_percent = mem.percent

        # Load average (1, 5, 15 min)
        load1, load5, load15 = psutil.getloadavg()

        return {
            "status": "success",
            "cpu_percent": round(cpu_percent, 1),
            "temperature_c": round(temp_c, 1),
            "memory_used_gb": round(mem_used_gb, 2),
            "memory_total_gb": round(mem_total_gb, 2),
            "memory_percent": round(mem_percent, 1),
            "load_average": [round(load1, 2), round(load5, 2), round(load15, 2)]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
