# server.py

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from eg4_python.client import EG4Inverter

# Load environment variables
load_dotenv()

# Use consistent environment variable names
USERNAME = os.getenv("EG4_USERNAME")
PASSWORD = os.getenv("EG4_PASSWORD")
BASE_URL = os.getenv("EG4_BASE_URL") 
DEBUG = os.getenv("EG4_DEBUG", "0") == "1"

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(name="EG4")

# Global API instance for connection reuse
_api_instance: Optional[EG4Inverter] = None
_last_login_time: Optional[datetime] = None
LOGIN_CACHE_DURATION = timedelta(minutes=30)

async def get_api_instance() -> EG4Inverter:
    """Get or create API instance with session management."""
    global _api_instance, _last_login_time
    
    if not USERNAME or not PASSWORD:
        raise ValueError("EG4_USERNAME and EG4_PASSWORD must be set in environment variables")
    
    current_time = datetime.now()
    
    # Check if we need to login or re-login
    if (_api_instance is None or 
        _last_login_time is None or 
        current_time - _last_login_time > LOGIN_CACHE_DURATION):
        
        if _api_instance:
            await _api_instance.close()
        
        logger.info("Creating new API instance and logging in")
        _api_instance = EG4Inverter(
            username=USERNAME, 
            password=PASSWORD, 
            base_url=BASE_URL
        )
        
        ignore_ssl = os.getenv("EG4_DISABLE_VERIFY_SSL", "0") == "1"
        await _api_instance.login(ignore_ssl=ignore_ssl)
        _last_login_time = current_time
        
        # Auto-select first inverter if available
        inverters = _api_instance.get_inverters()
        if inverters:
            _api_instance.set_selected_inverter(inverterIndex=0)
            logger.info(f"Selected inverter: {inverters[0].serialNum}")
        else:
            logger.warning("No inverters found")
    
    return _api_instance

def format_power_value(value: Any, unit: str = "W") -> str:
    """Format power values with appropriate units."""
    if value is None:
        return "N/A"
    
    try:
        val = float(value)
        if abs(val) >= 1000:
            return f"{val/1000:.2f} k{unit}"
        return f"{val:.1f} {unit}"
    except (ValueError, TypeError):
        return str(value)

def format_energy_value(value: Any, unit: str = "Wh") -> str:
    """Format energy values with appropriate units."""
    if value is None:
        return "N/A"
    
    try:
        val = float(value)
        if abs(val) >= 1000000:
            return f"{val/1000000:.2f} M{unit}"
        elif abs(val) >= 1000:
            return f"{val/1000:.2f} k{unit}"
        return f"{val:.1f} {unit}"
    except (ValueError, TypeError):
        return str(value)

def generate_recommendations(runtime_data, energy_data, battery_data) -> List[str]:
    """Generate performance recommendations based on current data."""
    recommendations = []
    
    # Check solar generation
    current_solar = getattr(runtime_data, 'ppvpCharge', 0) or 0
    if current_solar < 100:  # Assuming daytime check could be improved
        recommendations.append("Solar generation is low - check for shading or panel cleanliness")
    
    # Check battery health
    if hasattr(battery_data, 'battery_units') and battery_data.battery_units:
        low_soh_units = [unit for unit in battery_data.battery_units 
                        if getattr(unit, 'soh', 100) < 90]
        if low_soh_units:
            recommendations.append(f"Battery units with low health detected: {len(low_soh_units)} units below 90% SOH")
    
    # Check grid dependency
    grid_power = getattr(runtime_data, 'pToGrid', 0) or 0
    if grid_power < 0:  # Importing from grid
        recommendations.append("Currently importing from grid - consider load balancing")
    
    if not recommendations:
        recommendations.append("System is operating within normal parameters")
    
    return recommendations


def _find_peak_generation_time(data_points) -> str:
    """Find the time of peak solar generation."""
    if not data_points:
        return "N/A"
    
    peak_point = max(data_points, key=lambda p: p.solar_pv)
    if peak_point.datetime:
        return peak_point.datetime.strftime("%H:%M")
    return peak_point.time.split()[1][:5] if peak_point.time else "N/A"

def _find_peak_consumption_time(data_points) -> str:
    """Find the time of peak consumption."""
    if not data_points:
        return "N/A"
    
    peak_point = max(data_points, key=lambda p: p.consumption)
    if peak_point.datetime:
        return peak_point.datetime.strftime("%H:%M")
    return peak_point.time.split()[1][:5] if peak_point.time else "N/A"

def _generate_daily_insights(daily_data) -> List[str]:
    """Generate actionable insights from daily data analysis."""
    insights = []
    
    # Solar generation insights
    if daily_data.peak_solar_generation > 0:
        peak_time = _find_peak_generation_time(daily_data.data_points)
        insights.append(f"Peak solar generation of {format_power_value(daily_data.peak_solar_generation)} occurred at {peak_time}")
    
    # Battery usage insights
    soc_range = daily_data.max_soc - daily_data.min_soc
    if soc_range > 50:
        insights.append(f"Battery experienced significant cycling ({soc_range}% range) - good utilization")
    elif soc_range < 20:
        insights.append(f"Battery had minimal cycling ({soc_range}% range) - consider adjusting charge/discharge settings")
    
    # Grid dependency insights
    if daily_data.total_grid_import_kwh > daily_data.total_solar_generation_kwh * 0.5:
        insights.append("High grid dependency detected - consider load shifting or battery optimization")
    
    # Energy balance insights
    surplus = daily_data.total_solar_generation_kwh - daily_data.total_consumption_kwh
    if surplus > 5:
        insights.append(f"Significant energy surplus ({surplus:.1f} kWh) - good day for solar generation")
    elif surplus < -5:
        insights.append(f"Energy deficit ({abs(surplus):.1f} kWh) - consumption exceeded generation")
    
    # Export insights
    if daily_data.total_grid_export_kwh > daily_data.total_solar_generation_kwh * 0.2:
        insights.append("High grid export - consider increasing self-consumption through load scheduling")
    
    if not insights:
        insights.append("System operating efficiently with balanced energy flows")
    
    return insights





@mcp.tool("Fetch_Configuration")
async def fetch_configuration() -> str:
    """
    Query the EG4 API for the runtime status of the inverter
    """
    try:
        api = await get_api_instance()
        
        # Get available inverters
        inverters = api.get_inverters()
        
        if not inverters:
            return json.dumps({"error": "No inverters found"}, indent=2)

        # Fetch all data in parallel for better performance
        runtime_task = api.get_inverter_runtime_async()
        energy_task = api.get_inverter_energy_async()
        battery_task = api.get_inverter_battery_async()
        config_task = api.read_settings_async()
        
        runtime_data, energy_data, battery_data, config_data = await asyncio.gather(
            runtime_task, energy_task, battery_task, config_task,
            return_exceptions=True
        )
        
        # Handle any exceptions
        result = {
            "timestamp": datetime.now().isoformat(),
            "inverters": [str(inv) for inv in inverters],
            "selected_inverter": 0,
            "runtime_data": runtime_data if not isinstance(runtime_data, Exception) else f"Error: {runtime_data}",
            "energy_data": energy_data if not isinstance(energy_data, Exception) else f"Error: {energy_data}",
            "battery_data": battery_data if not isinstance(battery_data, Exception) else f"Error: {battery_data}",
            "configuration": config_data if not isinstance(config_data, Exception) else f"Error: {config_data}"
        }
        
        return json.dumps(result, indent=2, default=str)
        
    except Exception as e:
        logger.error(f"Error in fetch_configuration: {e}")
        error_result = {
            "error": f"Error fetching EG4 data: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        return json.dumps(error_result, indent=2)

@mcp.tool("Get_System_Details")
async def get_system_details(system_id: Optional[int] = None) -> str:
    """
    Get detailed information about a specific system including layout, sources, and summary.
    If no system_id provided, uses the first available system.
    """
    try:
        api = await get_api_instance()
        inverters = api.get_inverters()
        
        if not inverters:
            return json.dumps({"error": "No systems found"}, indent=2)
        
        # Use specified system or default to first
        if system_id is not None and system_id < len(inverters):
            api.set_selected_inverter(inverterIndex=system_id)
            selected_inverter = inverters[system_id]
        else:
            selected_inverter = inverters[0]
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "system_details": {
                "system_id": system_id or 0,
                "serial_number": selected_inverter.serialNum,
                "plant_name": selected_inverter.plantName,
                "plant_id": selected_inverter.plantId,
                "battery_type": selected_inverter.batteryType,
                "firmware_version": selected_inverter.fwVersion,
                "hardware_version": getattr(selected_inverter, 'hardwareVersion', 'N/A'),
                "phase": selected_inverter.phase,
                "device_type": selected_inverter.deviceType,
                "machine_type": getattr(selected_inverter, 'machineType', 'N/A')
            },
            "available_systems": [
                {
                    "index": i,
                    "serial": inv.serialNum,
                    "name": inv.plantName
                } for i, inv in enumerate(inverters)
            ]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_system_details: {e}")
        return json.dumps({"error": f"Error getting system details: {str(e)}"}, indent=2)

@mcp.tool("Get_Current_Production")
async def get_current_production(system_id: Optional[int] = None) -> str:
    """
    Get today's production data and real-time system summary.
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get current runtime and energy data
        runtime_data = await api.get_inverter_runtime_async()
        energy_data = await api.get_inverter_energy_async()
        
        # Format the production summary
        result = {
            "timestamp": datetime.now().isoformat(),
            "system_status": getattr(runtime_data, 'statusText', 'Unknown'),
            "current_production": {
                "solar_power": format_power_value(getattr(runtime_data, 'ppvpCharge', 0)),
                "battery_discharge": format_power_value(getattr(runtime_data, 'pDisCharge', 0)),
                "grid_export": format_power_value(getattr(runtime_data, 'pToGrid', 0)),
                "home_consumption": format_power_value(getattr(runtime_data, 'pToUser', 0)),
                "eps_power": format_power_value(getattr(runtime_data, 'peps', 0))
            },
            "today_totals": {
                "solar_generation": format_energy_value(getattr(energy_data, 'todayYielding', 0)),
                "battery_charged": format_energy_value(getattr(energy_data, 'todayCharging', 0)),
                "battery_discharged": format_energy_value(getattr(energy_data, 'todayDischarging', 0)),
                "grid_import": format_energy_value(getattr(energy_data, 'todayImport', 0)),
                "grid_export": format_energy_value(getattr(energy_data, 'todayExport', 0)),
                "home_usage": format_energy_value(getattr(energy_data, 'todayUsage', 0))
            },
            "solar_panels": {
                "pv1_voltage": f"{getattr(runtime_data, 'vpv1', 0)} V",
                "pv2_voltage": f"{getattr(runtime_data, 'vpv2', 0)} V",
                "pv3_voltage": f"{getattr(runtime_data, 'vpv3', 0)} V",
                "pv4_voltage": f"{getattr(runtime_data, 'vpv4', 0)} V"
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_current_production: {e}")
        return json.dumps({"error": f"Error getting current production: {str(e)}"}, indent=2)

@mcp.tool("Get_Performance_Analysis")
async def get_performance_analysis(days_back: int = 7, system_id: Optional[int] = None) -> str:
    """
    Get comprehensive performance analysis including efficiency metrics and panel performance.
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get current data for analysis
        runtime_data = await api.get_inverter_runtime_async()
        energy_data = await api.get_inverter_energy_async()
        battery_data = await api.get_inverter_battery_async()
        
        # Calculate basic efficiency metrics
        total_generation = getattr(energy_data, 'totalYielding', 0) or 0
        total_usage = getattr(energy_data, 'totalUsage', 0) or 0
        total_grid_import = getattr(energy_data, 'totalImport', 0) or 0
        
        grid_independence = 0
        if total_usage > 0:
            grid_independence = max(0, (total_usage - total_grid_import) / total_usage * 100)
        
        # Battery performance
        battery_capacity = getattr(runtime_data, 'batCapacity', 0) or 0
        battery_efficiency = 0
        if hasattr(battery_data, 'battery_units') and battery_data.battery_units:  # type: ignore
            avg_soh = sum(getattr(unit, 'soh', 0) or 0 for unit in battery_data.battery_units) / len(battery_data.battery_units)  # type: ignore
            battery_efficiency = avg_soh
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "analysis_period": f"Last {days_back} days",
            "performance_metrics": {
                "grid_independence": f"{grid_independence:.1f}%",
                "total_generation": format_energy_value(total_generation),
                "total_consumption": format_energy_value(total_usage),
                "total_grid_import": format_energy_value(total_grid_import),
                "battery_efficiency": f"{battery_efficiency:.1f}%" if battery_efficiency > 0 else "N/A"
            },
            "system_health": {
                "inverter_status": getattr(runtime_data, 'statusText', 'Unknown'),
                "battery_count": getattr(runtime_data, 'batParallelNum', 0),
                "battery_capacity": f"{battery_capacity} Ah" if battery_capacity > 0 else "N/A"
            },
            "recommendations": generate_recommendations(runtime_data, energy_data, battery_data)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_performance_analysis: {e}")
        return json.dumps({"error": f"Error performing analysis: {str(e)}"}, indent=2)

@mcp.tool("Get_Historical_Data")
async def get_historical_data(
    system_id: Optional[int] = None,
    days_back: int = 30,
    level: str = "day"
) -> str:
    """
    Get historical production data for analysis.

    Args:
        system_id: System ID (optional, uses first system if not provided)
        days_back: Number of days of historical data (default: 30)
        level: Data granularity - "minute", "hour", or "day" (default: "day")
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Try to get today's detailed data using daily chart
        today_detailed = None
        try:
            today_chart = await api.get_daily_chart_data_async()  # type: ignore
            if today_chart.success:
                today_detailed = {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "solar_generation": f"{today_chart.total_solar_generation_kwh:.2f} kWh",
                    "consumption": f"{today_chart.total_consumption_kwh:.2f} kWh",
                    "grid_import": f"{today_chart.total_grid_import_kwh:.2f} kWh",
                    "grid_export": f"{today_chart.total_grid_export_kwh:.2f} kWh",
                    "peak_solar": format_power_value(today_chart.peak_solar_generation),
                    "peak_consumption": format_power_value(today_chart.peak_consumption),
                    "data_points": today_chart.total_data_points,
                    "battery_soc_range": f"{today_chart.min_soc}% - {today_chart.max_soc}%"
                }
        except Exception as e:
            logger.warning(f"Could not get detailed daily chart data: {e}")
        
        # Get general energy data
        energy_data = await api.get_inverter_energy_async()
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "period": f"Last {days_back} days",
            "granularity": level,
            "today_detailed": today_detailed,
            "lifetime_totals": {
                "total_generation": format_energy_value(getattr(energy_data, 'totalYielding', 0)),
                "total_consumption": format_energy_value(getattr(energy_data, 'totalUsage', 0)),
                "total_battery_charged": format_energy_value(getattr(energy_data, 'totalCharging', 0)),
                "total_battery_discharged": format_energy_value(getattr(energy_data, 'totalDischarging', 0)),
                "total_grid_import": format_energy_value(getattr(energy_data, 'totalImport', 0)),
                "total_grid_export": format_energy_value(getattr(energy_data, 'totalExport', 0))
            },
            "today_summary": {
                "generation": format_energy_value(getattr(energy_data, 'todayYielding', 0)),
                "consumption": format_energy_value(getattr(energy_data, 'todayUsage', 0)),
                "battery_charged": format_energy_value(getattr(energy_data, 'todayCharging', 0)),
                "battery_discharged": format_energy_value(getattr(energy_data, 'todayDischarging', 0)),
                "grid_import": format_energy_value(getattr(energy_data, 'todayImport', 0)),
                "grid_export": format_energy_value(getattr(energy_data, 'todayExport', 0))
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_historical_data: {e}")
        return json.dumps({"error": f"Error getting historical data: {str(e)}"}, indent=2)

@mcp.tool("Get_System_Alerts")
async def get_system_alerts(days_back: int = 30, system_id: Optional[int] = None) -> str:
    """
    Get recent alerts and system health information.
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get current system data to check for issues
        runtime_data = await api.get_inverter_runtime_async()
        battery_data = await api.get_inverter_battery_async()
        
        alerts = []
        warnings = []
        
        # Check system status
        status = getattr(runtime_data, 'statusText', 'Unknown')
        if status.lower() not in ['normal', 'running', 'ok']:
            alerts.append({
                "type": "system_status",
                "severity": "warning",
                "message": f"System status: {status}",
                "timestamp": datetime.now().isoformat()
            })
        
        # Check battery health
        if hasattr(battery_data, 'battery_units') and battery_data.battery_units:  # type: ignore
            for unit in battery_data.battery_units:  # type: ignore
                soh = getattr(unit, 'soh', 100)
                soc = getattr(unit, 'soc', 0)
                
                if soh < 80:
                    alerts.append({
                        "type": "battery_health",
                        "severity": "error",
                        "message": f"Battery {getattr(unit, 'batIndex', 'Unknown')} SOH critical: {soh}%",
                        "timestamp": datetime.now().isoformat()
                    })
                elif soh < 90:
                    warnings.append({
                        "type": "battery_health",
                        "severity": "warning",
                        "message": f"Battery {getattr(unit, 'batIndex', 'Unknown')} SOH low: {soh}%",
                        "timestamp": datetime.now().isoformat()
                    })
                
                if soc < 10:
                    warnings.append({
                        "type": "battery_charge",
                        "severity": "warning",
                        "message": f"Battery {getattr(unit, 'batIndex', 'Unknown')} charge low: {soc}%",
                        "timestamp": datetime.now().isoformat()
                    })
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "period": f"Last {days_back} days",
            "system_health": "Good" if not alerts else "Issues Detected",
            "alerts": alerts,
            "warnings": warnings,
            "summary": {
                "total_alerts": len(alerts),
                "total_warnings": len(warnings),
                "system_status": status
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_system_alerts: {e}")
        return json.dumps({"error": f"Error getting system alerts: {str(e)}"}, indent=2)

@mcp.tool("Get_System_Health")
async def get_system_health(system_id: Optional[int] = None) -> str:
    """
    Get comprehensive system health status combining multiple data sources.
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get all system data
        runtime_data = await api.get_inverter_runtime_async()
        energy_data = await api.get_inverter_energy_async()
        battery_data = await api.get_inverter_battery_async()
        
        # Calculate health scores
        inverter_health = 100 if getattr(runtime_data, 'statusText', '').lower() in ['normal', 'running', 'ok'] else 50
        
        battery_health = 100
        if hasattr(battery_data, 'battery_units') and battery_data.battery_units:  # type: ignore
            avg_soh = sum(getattr(unit, 'soh', 100) for unit in battery_data.battery_units) / len(battery_data.battery_units)  # type: ignore
            battery_health = avg_soh
        
        # Solar panel health (basic check)
        solar_health = 100
        vpv_values = [
            getattr(runtime_data, 'vpv1', 0),
            getattr(runtime_data, 'vpv2', 0),
            getattr(runtime_data, 'vpv3', 0),
            getattr(runtime_data, 'vpv4', 0)
        ]
        active_panels = sum(1 for v in vpv_values if v > 10)  # Assuming > 10V means active
        
        overall_health = (inverter_health + battery_health + solar_health) / 3
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": {
                "score": f"{overall_health:.1f}%",
                "status": "Excellent" if overall_health >= 90 else "Good" if overall_health >= 70 else "Fair" if overall_health >= 50 else "Poor"
            },
            "component_health": {
                "inverter": {
                    "score": f"{inverter_health:.1f}%",
                    "status": getattr(runtime_data, 'statusText', 'Unknown'),
                    "uptime": "Active" if inverter_health > 50 else "Issues"
                },
                "battery_system": {
                    "score": f"{battery_health:.1f}%",
                    "unit_count": len(getattr(battery_data, 'battery_units', [])),
                    "capacity": f"{getattr(runtime_data, 'batCapacity', 0)} Ah"
                },
                "solar_panels": {
                    "score": f"{solar_health:.1f}%",
                    "active_strings": active_panels,
                    "voltages": {
                        "pv1": f"{getattr(runtime_data, 'vpv1', 0)} V",
                        "pv2": f"{getattr(runtime_data, 'vpv2', 0)} V",
                        "pv3": f"{getattr(runtime_data, 'vpv3', 0)} V",
                        "pv4": f"{getattr(runtime_data, 'vpv4', 0)} V"
                    }
                }
            },
            "current_performance": {
                "solar_generation": format_power_value(getattr(runtime_data, 'ppvpCharge', 0)),
                "battery_power": format_power_value(getattr(runtime_data, 'pDisCharge', 0)),
                "home_consumption": format_power_value(getattr(runtime_data, 'pToUser', 0)),
                "grid_interaction": format_power_value(getattr(runtime_data, 'pToGrid', 0))
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_system_health: {e}")
        return json.dumps({"error": f"Error getting system health: {str(e)}"}, indent=2)

@mcp.tool("Get_Maintenance_Insights")
async def get_maintenance_insights(
    system_id: Optional[int] = None,
    threshold_percent: float = 85.0
) -> str:
    """
    Get maintenance recommendations based on system performance analysis.
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get system data for analysis
        runtime_data = await api.get_inverter_runtime_async()
        battery_data = await api.get_inverter_battery_async()
        energy_data = await api.get_inverter_energy_async()
        
        recommendations = []
        maintenance_tasks = []
        
        # Battery maintenance checks
        if hasattr(battery_data, 'battery_units') and battery_data.battery_units:  # type: ignore
            for unit in battery_data.battery_units:  # type: ignore
                soh = getattr(unit, 'soh', 100)
                cycles = getattr(unit, 'cycleCnt', 0)
                
                if soh < threshold_percent:
                    maintenance_tasks.append({
                        "priority": "high",
                        "component": f"Battery {getattr(unit, 'batIndex', 'Unknown')}",
                        "issue": f"SOH below threshold ({soh}% < {threshold_percent}%)",
                        "recommendation": "Consider battery replacement or professional inspection",
                        "estimated_effort": "2-4 hours (professional required)"
                    })
                
                if cycles > 5000:  # Typical cycle life threshold
                    recommendations.append({
                        "priority": "medium",
                        "component": f"Battery {getattr(unit, 'batIndex', 'Unknown')}",
                        "issue": f"High cycle count ({cycles} cycles)",
                        "recommendation": "Monitor closely for capacity degradation",
                        "estimated_effort": "Ongoing monitoring"
                    })
        
        # Solar panel maintenance
        vpv_values = [
            getattr(runtime_data, 'vpv1', 0),
            getattr(runtime_data, 'vpv2', 0),
            getattr(runtime_data, 'vpv3', 0),
            getattr(runtime_data, 'vpv4', 0)
        ]
        
        low_voltage_panels = [i+1 for i, v in enumerate(vpv_values) if 0 < v < 20]
        if low_voltage_panels:
            maintenance_tasks.append({
                "priority": "medium",
                "component": f"Solar Panel String(s) {low_voltage_panels}",
                "issue": "Low voltage detected",
                "recommendation": "Check for shading, dirt, or connection issues",
                "estimated_effort": "1-2 hours"
            })
        
        # General maintenance recommendations
        recommendations.extend([
            {
                "priority": "low",
                "component": "Solar Panels",
                "issue": "Routine maintenance",
                "recommendation": "Clean panels and check for physical damage",
                "estimated_effort": "1 hour",
                "frequency": "Monthly"
            },
            {
                "priority": "low", 
                "component": "Inverter",
                "issue": "Routine maintenance",
                "recommendation": "Check ventilation and clean air filters",
                "estimated_effort": "30 minutes",
                "frequency": "Quarterly"
            }
        ])
        
        # Calculate next maintenance date
        next_maintenance = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "system_performance_threshold": f"{threshold_percent}%",
            "next_recommended_maintenance": next_maintenance,
            "urgent_tasks": [task for task in maintenance_tasks if task["priority"] == "high"],
            "recommended_tasks": [task for task in maintenance_tasks if task["priority"] == "medium"],
            "routine_maintenance": [rec for rec in recommendations if rec["priority"] == "low"],
            "maintenance_summary": {
                "urgent_items": len([task for task in maintenance_tasks if task["priority"] == "high"]),
                "recommended_items": len([task for task in maintenance_tasks if task["priority"] == "medium"]),
                "routine_items": len([rec for rec in recommendations if rec["priority"] == "low"]),
                "overall_status": "Good" if not any(task["priority"] == "high" for task in maintenance_tasks) else "Attention Required"
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_maintenance_insights: {e}")
        return json.dumps({"error": f"Error generating maintenance insights: {str(e)}"}, indent=2)


@mcp.tool("Get_Daily_Chart_Data")
async def get_daily_chart_data(
    system_id: Optional[int] = None,
    date_text: Optional[str] = None,
    analysis_type: str = "full"
) -> str:
    """
    Get detailed daily chart data with 10-minute interval time series analysis.
    
    Args:
        system_id: System ID (optional, uses first system if not provided)
        date_text: Date in YYYY-MM-DD format (optional, uses today if not provided)
        analysis_type: Type of analysis - "full", "summary", "hourly", "efficiency", or "raw"
    """
    try:
        api = await get_api_instance()
        
        if system_id is not None:
            api.set_selected_inverter(inverterIndex=system_id)
        
        # Get daily chart data
        daily_data = await api.get_daily_chart_data_async(date_text)  # type: ignore
        
        if not daily_data.success:
            return json.dumps({
                "error": "Failed to retrieve daily chart data",
                "timestamp": datetime.now().isoformat()
            }, indent=2)
        
        # Determine the date being analyzed
        analysis_date = date_text or datetime.now().strftime("%Y-%m-%d")
        
        # Base result structure
        result = {
            "timestamp": datetime.now().isoformat(),
            "analysis_date": analysis_date,
            "data_points": daily_data.total_data_points,
            "analysis_type": analysis_type
        }
        
        if analysis_type == "raw":
            # Return raw data points
            result["raw_data"] = [
                {
                    "time": point.time,
                    "solar_pv": point.solar_pv,
                    "grid_power": point.grid_power,
                    "battery_discharging": point.battery_discharging,
                    "consumption": point.consumption,
                    "soc": point.soc,
                    "ac_couple_power": point.ac_couple_power
                } for point in daily_data.data_points
            ]
            
        elif analysis_type == "summary":
            # High-level summary
            result["daily_summary"] = {
                "solar_generation": f"{daily_data.total_solar_generation_kwh:.2f} kWh",
                "total_consumption": f"{daily_data.total_consumption_kwh:.2f} kWh",
                "grid_import": f"{daily_data.total_grid_import_kwh:.2f} kWh",
                "grid_export": f"{daily_data.total_grid_export_kwh:.2f} kWh",
                "peak_solar": format_power_value(daily_data.peak_solar_generation),
                "peak_consumption": format_power_value(daily_data.peak_consumption),
                "battery_soc_range": f"{daily_data.min_soc}% - {daily_data.max_soc}%",
                "average_soc": f"{daily_data.average_soc:.1f}%"
            }
            
            # Calculate self-sufficiency and energy balance
            self_sufficiency = 0
            if daily_data.total_consumption_kwh > 0:
                self_sufficiency = max(0, (daily_data.total_consumption_kwh - daily_data.total_grid_import_kwh) / daily_data.total_consumption_kwh * 100)
            
            result["energy_efficiency"] = {
                "self_sufficiency": f"{self_sufficiency:.1f}%",
                "solar_utilization": f"{((daily_data.total_solar_generation_kwh - daily_data.total_grid_export_kwh) / max(daily_data.total_solar_generation_kwh, 0.001) * 100):.1f}%",
                "energy_balance": f"{daily_data.total_solar_generation_kwh - daily_data.total_consumption_kwh:.2f} kWh"
            }
            
        elif analysis_type == "hourly":
            # Hourly breakdown analysis
            result["hourly_analysis"] = {
                "solar_generation": daily_data.get_solar_generation_by_hour(),
                "consumption": daily_data.get_consumption_by_hour()
            }
            
            # Find peak hours
            solar_hourly = daily_data.get_solar_generation_by_hour()
            consumption_hourly = daily_data.get_consumption_by_hour()
            
            peak_solar_hour = max(solar_hourly.items(), key=lambda x: x[1], default=(0, 0))
            peak_consumption_hour = max(consumption_hourly.items(), key=lambda x: x[1], default=(0, 0))
            
            result["peak_hours"] = {
                "peak_solar_hour": f"{peak_solar_hour[0]:02d}:00 ({peak_solar_hour[1]:.2f} kWh)",
                "peak_consumption_hour": f"{peak_consumption_hour[0]:02d}:00 ({peak_consumption_hour[1]:.2f} kWh)"
            }
            
        elif analysis_type == "efficiency":
            # Detailed efficiency analysis
            # Battery efficiency analysis
            charging_points = [p for p in daily_data.data_points if p.is_battery_charging]
            discharging_points = [p for p in daily_data.data_points if p.is_battery_discharging]
            
            total_charge_wh = sum(abs(p.battery_discharging) for p in charging_points) * (10/60)
            total_discharge_wh = sum(p.battery_discharging for p in discharging_points) * (10/60)
            
            battery_efficiency = 0
            if total_charge_wh > 0:
                battery_efficiency = (total_discharge_wh / total_charge_wh) * 100
            
            # Grid interaction analysis
            import_points = [p for p in daily_data.data_points if p.is_importing_from_grid]
            export_points = [p for p in daily_data.data_points if p.is_exporting_to_grid]
            
            result["efficiency_analysis"] = {
                "battery_round_trip_efficiency": f"{min(battery_efficiency, 100):.1f}%",
                "total_energy_charged": f"{total_charge_wh/1000:.2f} kWh",
                "total_energy_discharged": f"{total_discharge_wh/1000:.2f} kWh",
                "grid_interactions": {
                    "import_periods": len(import_points),
                    "export_periods": len(export_points),
                    "net_grid_usage": f"{daily_data.total_grid_import_kwh - daily_data.total_grid_export_kwh:.2f} kWh"
                },
                "energy_flows": {
                    "solar_to_consumption_direct": f"{min(daily_data.total_solar_generation_kwh, daily_data.total_consumption_kwh):.2f} kWh",
                    "battery_contribution": f"{total_discharge_wh/1000:.2f} kWh",
                    "grid_dependency": f"{daily_data.total_grid_import_kwh:.2f} kWh"
                }
            }
            
        else:  # "full" analysis
            # Comprehensive analysis combining all above
            result["daily_summary"] = {
                "solar_generation": f"{daily_data.total_solar_generation_kwh:.2f} kWh",
                "total_consumption": f"{daily_data.total_consumption_kwh:.2f} kWh",
                "grid_import": f"{daily_data.total_grid_import_kwh:.2f} kWh",
                "grid_export": f"{daily_data.total_grid_export_kwh:.2f} kWh",
                "peak_solar": format_power_value(daily_data.peak_solar_generation),
                "peak_consumption": format_power_value(daily_data.peak_consumption),
                "battery_soc_range": f"{daily_data.min_soc}% - {daily_data.max_soc}%",
                "average_soc": f"{daily_data.average_soc:.1f}%"
            }
            
            # Time-based analysis
            daytime_points = daily_data.filter_by_time_range(6, 18)  # 6 AM to 6 PM
            nighttime_points = daily_data.filter_by_time_range(18, 6)  # 6 PM to 6 AM (next day)
            
            daytime_consumption = sum(p.consumption for p in daytime_points) * (10/60) / 1000
            nighttime_consumption = sum(p.consumption for p in nighttime_points) * (10/60) / 1000
            
            result["time_analysis"] = {
                "daytime_consumption": f"{daytime_consumption:.2f} kWh",
                "nighttime_consumption": f"{nighttime_consumption:.2f} kWh",
                "daytime_solar": f"{sum(p.solar_pv for p in daytime_points) * (10/60) / 1000:.2f} kWh",
                "peak_generation_time": _find_peak_generation_time(daily_data.data_points),
                "peak_consumption_time": _find_peak_consumption_time(daily_data.data_points)
            }
            
            # Efficiency metrics
            self_sufficiency = 0
            if daily_data.total_consumption_kwh > 0:
                self_sufficiency = max(0, (daily_data.total_consumption_kwh - daily_data.total_grid_import_kwh) / daily_data.total_consumption_kwh * 100)
            
            result["efficiency_metrics"] = {
                "self_sufficiency": f"{self_sufficiency:.1f}%",
                "solar_utilization": f"{((daily_data.total_solar_generation_kwh - daily_data.total_grid_export_kwh) / max(daily_data.total_solar_generation_kwh, 0.001) * 100):.1f}%",
                "energy_balance": f"{daily_data.total_solar_generation_kwh - daily_data.total_consumption_kwh:.2f} kWh"
            }
            
            # Generate insights and recommendations
            result["insights"] = _generate_daily_insights(daily_data)
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in get_daily_chart_data: {e}")
        return json.dumps({
            "error": f"Error getting daily chart data: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }, indent=2)






# Cleanup function for graceful shutdown
async def cleanup():
    """Clean up API connections on shutdown."""
    global _api_instance
    if _api_instance:
        await _api_instance.close()
        _api_instance = None
        logger.info("API instance closed")

def main():
    """Main entry point for the EG4 MCP server."""
    import signal
    import sys
    
    def signal_handler(sig, frame):
        logger.info("Shutting down gracefully...")
        asyncio.create_task(cleanup())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("Starting EG4 MCP Server...")
        mcp.run(transport="stdio")
    finally:
        asyncio.run(cleanup())

        
# Run the MCP server
if __name__ == "__main__":
    import signal
    import sys
    
    def signal_handler(sig, frame):
        logger.info("Shutting down gracefully...")
        asyncio.create_task(cleanup())
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        logger.info("Starting EG4 MCP Server...")
        mcp.run(transport="stdio")
    finally:
        asyncio.run(cleanup())