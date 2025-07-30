# EG4 MCP Server

An MCP (Model Context Protocol) Server for the EG4 Solar Inverter Monitoring API, providing comprehensive solar system monitoring and analysis capabilities.

## Features

- 🔌 **Real-time monitoring** - Current production, consumption, and system status
- 📊 **Performance analysis** - Efficiency metrics and grid independence calculations
- 🔋 **Battery health monitoring** - SOH, SOC, and cycle count tracking
- ⚠️ **Smart alerts** - Proactive issue detection and notifications
- 🛠️ **Maintenance insights** - Automated recommendations and scheduling
- 📈 **Historical data** - Energy production and consumption trends
- 🏥 **System health scoring** - Component-level health assessment

## Installation

### Quick start (dev mode)

```bash
# 1. create & activate venv
cd eg4_mcp_server
python -m venv .venv
.venv\Scripts\activate   # PowerShell: .venv\Scripts\Activate.ps1

# 2. install requirements
pip install -r requirements.txt

# 3. run the server
python server.py

### Prerequisites

- Python 3.10 or higher
- EG4 inverter with online monitoring account
- Access to EG4 monitoring portal credentials

### Install from PyPI
```bash
pip install eg4-mcp-server
```

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eg4-mcp-server.git
cd eg4-mcp-server
```

2. Install dependencies:
```bash
pip install -e .
```

## Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Edit `.env` with your EG4 credentials:
```env
EG4_USERNAME=your_eg4_username
EG4_PASSWORD=your_eg4_password
EG4_BASE_URL=https://monitor.eg4electronics.com
EG4_DISABLE_VERIFY_SSL=0
```

## Usage

### Running the MCP Server

Start the server directly:
```bash
python server.py
```

Or use the MCP CLI:
```bash
mcp run server.py
```

### Available Tools

| Tool | Description |
|------|-------------|
| `Fetch_Configuration` | Get complete system configuration and status |
| `Get_System_Details` | Detailed system information and inverter specs |
| `Get_Current_Production` | Real-time production and consumption data |
| `Get_Performance_Analysis` | Performance metrics and efficiency analysis |
| `Get_Historical_Data` | Historical energy data and trends |
| `Get_System_Alerts` | System health alerts and warnings |
| `Get_System_Health` | Comprehensive health scoring |
| `Get_Maintenance_Insights` | Maintenance recommendations and scheduling |

### Example Usage with Claude

1. **Check current system status:**
   ```
   What's my solar system producing right now?
   ```

2. **Get performance analysis:**
   ```
   How is my solar system performing this week?
   ```

3. **Check for alerts:**
   ```
   Are there any issues with my solar system?
   ```

4. **Get maintenance recommendations:**
   ```
   What maintenance does my solar system need?
   ```

## Integration with AI Assistants

This MCP server is designed to work with AI assistants that support the Model Context Protocol, such as:

- **Claude Desktop** - Add to your MCP configuration
- **Other MCP-compatible clients**

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "eg4": {
      "command": "python",
      "args": ["-m", "eg4_mcp_server"],
      "env": {
        "EG4_USERNAME": "your_username",
        "EG4_PASSWORD": "your_password"
      }
    }
  }
}
```

## API Reference

### Tool Parameters

Most tools accept optional parameters:

- `system_id` (int, optional): Specific system ID (defaults to first system)
- `days_back` (int): Number of days for historical data (default varies by tool)
- `threshold_percent` (float): Performance threshold for maintenance insights

### Response Format

All tools return JSON responses with:
- `timestamp`: ISO format timestamp
- `data`: Tool-specific data structure
- `error`: Error message if applicable

Example response:
```json
{
  "timestamp": "2025-06-24T10:30:00",
  "system_status": "Normal",
  "current_production": {
    "solar_power": "2.5 kW",
    "battery_discharge": "0.0 W",
    "home_consumption": "1.8 kW"
  }
}
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Make your changes and run tests:
   ```bash
   pytest
   ```

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify your EG4 credentials in `.env`
   - Check if your account has API access

2. **SSL Certificate Errors**
   - Set `EG4_DISABLE_VERIFY_SSL=1` in your `.env` file
   - This disables SSL verification (use with caution)

3. **No Inverters Found**
   - Ensure your account has associated inverters
   - Check if inverters are online in the EG4 portal

4. **Connection Timeouts**
   - Check your internet connection
   - Verify the `EG4_BASE_URL` is correct

### Debug Mode

Enable verbose logging by setting the environment variable:
```bash
export EG4_DEBUG=1
python server.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [eg4_inverter_api](https://github.com/twistedroutes/eg4_inverter_api) library
- Powered by the [Model Context Protocol](https://modelcontextprotocol.io/)
- Special thanks to the EG4 community for reverse-engineering efforts

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## Support

- 📖 **Documentation**: Check this README and inline tool documentation
- 🐛 **Bug Reports**: [Open an issue](https://github.com/yourusername/eg4-mcp-server/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/yourusername/eg4-mcp-server/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/eg4-mcp-server/discussions)

---

**Note**: This project is not officially affiliated with EG4 Electronics. It's a community-driven project for interfacing with EG4 monitoring systems.