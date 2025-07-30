# DCS Jupyter

A [Jupyter](https://jupyter.org/) kernel for live connection to DCS (Digital Combat Simulator) scripting environment. Execute [Lua](https://www.lua.org/) code in Jupyter notebooks that communicates directly with a running DCS mission via UDP socket connection.

## Features

- Execute Lua code directly in DCS from Jupyter notebooks
- Real-time communication with running DCS missions
- Support for both [Jupyter Console](https://jupyter-console.readthedocs.io/) and [JupyterLab](https://jupyterlab.readthedocs.io/)
- Easy installation and kernel management
- Cross-platform support (Windows, Linux, macOS)

## Installation

### Requirements
- Python 3.11 or higher
- [DCS World](https://www.digitalcombatsimulator.com/) (Digital Combat Simulator)

### Install Dependencies (Windows)

If you don't have Python and [pipx](https://pipx.pypa.io/) installed:

1. **Install Python:**
   - Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation in Command Prompt: `python --version`

2. **Install pipx:**
   Open Command Prompt and run:
   ```cmd
   python -m pip install --user pipx
   python -m pipx ensurepath
   ```
   - Restart Command Prompt after installation
   - Verify installation: `pipx --version`

### Install Package

```bash
# Basic installation
pipx install dcs-jupyter

# With JupyterLab and extras (vim bindings, rich output, Dracula theme)
pipx install "dcs-jupyter[lab]"
```

Also available via [`pip`](https://pip.pypa.io/) or [`uv`](https://docs.astral.sh/uv/) package managers.

## Basic Setup (Windows)

### 1. Patch DCS

In `dcs_install_dir/Scripts/MissionScripting.lua`, find this section (around line 16):

```lua
do
  sanitizeModule('os')
  sanitizeModule('io')
  sanitizeModule('lfs')
  _G['require'] = nil
  _G['loadlib'] = nil
  _G['package'] = nil
end
```

**Add this code BEFORE the above `do` block:**

```lua
-- Initialize DCS Jupyter before security restrictions
if not _G['dcs_jupyter_udp'] then
    package.path = package.path..";.\\LuaSocket\\?.lua"
    package.cpath = package.cpath..";.\\LuaSocket\\?.dll"
    local socket = require("socket")
    local udp = assert(socket.udp())
    assert(udp:settimeout(0))
    assert(udp:setsockname("127.0.0.1", 8042))
    _G['dcs_jupyter_udp'] = udp
    
    -- Pre-store DCS user directory for script loading
    local lfs = require("lfs")
    _G['dcs_jupyter_user_dir'] = lfs.writedir()
end
```

**Leave the original `do` block unchanged.** This maintains DCS security while enabling the kernel connection.

### 2. Install DCS Plugin

Load the `dcs_plugin/jupyter_kernel_connection.lua` script in your DCS mission using one of these methods:

**Option A: Copy-paste script content**
- Open Mission Editor → Triggers → New Trigger
- Set Event: Mission Start, Action: Do Script
- Copy entire contents of `jupyter_kernel_connection.lua` into the text box

**Option B: Do Script File action**
- Place `jupyter_kernel_connection.lua` anywhere
- Mission Editor → Triggers → New Trigger
- Set Event: Mission Start, Action: Do Script File
- Select the script file
- *Note: File contents are loaded once and saved internally to mission. Updating the file won't affect the mission.*

**Option C: Dynamic loading**
- Place `jupyter_kernel_connection.lua` anywhere in your DCS user directory (under 'Saved Games')
- Mission Editor → Triggers → New Trigger
- Set Event: Mission Start, Action: Do Script
- Use: `assert(loadfile(_G['dcs_jupyter_user_dir'] .. "/Scripts/jupyter_kernel_connection.lua"))()`
- *Advantage: Reloads script on every mission restart*
- *You can place the script in any subdirectory by changing the path after `dcs_jupyter_user_dir`*

### 3. Configure Network Settings

The kernel uses localhost (`127.0.0.1:8042`) by default, which works for native Windows installations.

## Usage

### Quick Start with Console

```bash
dcs-jupyter-console
```

Automatically installs the DCS kernel if needed and starts Jupyter Console with DCS Lua kernel.

### Start with JupyterLab

```bash
dcs-jupyter-lab
```

Automatically installs the DCS kernel if needed and starts JupyterLab.


## Examples

### Download Example Notebooks

Get started with these example notebooks:

- **Airport Terrain Demo** - Explore DCS terrain and airfield data
  - [Download](https://raw.githubusercontent.com/SamiAhola/dcs-jupyter/main/example/notebook/airport_terrain_demo.ipynb) | [View with outputs](https://github.com/SamiAhola/dcs-jupyter/blob/main/example/notebook/airport_terrain_demo.ipynb)
- **Vehicle Control** - Control units and vehicles in DCS
  - [Download](https://raw.githubusercontent.com/SamiAhola/dcs-jupyter/main/example/notebook/vehicle_control.ipynb) | [View with outputs](https://github.com/SamiAhola/dcs-jupyter/blob/main/example/notebook/vehicle_control.ipynb)

*Right-click "Download" links and select "Save link as..." to save to your computer.*

### Basic Usage

Once connected, you can execute Lua code directly in DCS:

```lua
-- Display message in DCS (visible in game)
trigger.action.outText("Hello from DCS Jupyter!", 10)

-- Get current mission time and display it
local currentTime = timer.getTime()
trigger.action.outText("Mission time: " .. math.floor(currentTime) .. " seconds", 5)

-- Create smoke at a specific location
local smokePos = {x = 0, y = 0, z = 0}  -- Adjust coordinates as needed
trigger.action.smoke(smokePos, trigger.smokeColor.Red)

-- Get all red coalition groups
local redGroups = coalition.getGroups(coalition.side.RED)
trigger.action.outText("Red coalition has " .. #redGroups .. " groups", 8)

```
Return current mission time:
```lua
return timer.getTime()
```

Get structured data for analysis:
```lua
-- Get all airfields with their properties
local airfields = {}
for coalition_id = 0, 2 do
    local airfield_list = coalition.getAirbases(coalition_id)
    for _, airfield in pairs(airfield_list) do
        airfields[#airfields + 1] = {
            name = airfield:getName(),
            coalition = coalition_id,
            position = airfield:getPosition().p,
            category = airfield:getDesc().category
        }
    end
end
return net.lua2json(airfields)
```

## Configuration

**Default settings:** `127.0.0.1:8042`, 10 second timeout. See Advanced Setup for customization.

## Troubleshooting

### Connection Issues

- Ensure DCS is running with the Lua plugin loaded
- Check firewall settings allow UDP traffic on port 8042
- Verify IP address is correct (127.0.0.1 for Windows, host IP for WSL2)

### Kernel Not Found

If the kernel isn't recognized:
```bash
# Reinstall kernel
jupyter kernelspec uninstall dcs-lua
dcs-jupyter-console  # Will reinstall automatically
```

### WSL2 Connection Problems

- WSL2 users need to modify IP addresses manually (see Advanced Setup)
- Use Windows host IP address instead of localhost
- Consider using native Windows installation for simpler setup

## Advanced Setup

### WSL2 Users

The default localhost configuration should work for most WSL2 setups. If you experience connection issues, you may need to use the Windows host IP:

1. **Find Windows host IP:** `cat /etc/resolv.conf | grep nameserver`
2. **Edit IP in the patching code:** Replace `127.0.0.1` with your Windows host IP in the MissionScripting.lua patch above
3. **Edit IP in kernel:** `src/dcs_jupyter/kernel.py`: `SOCKET_ADDR = 'YOUR_HOST_IP'`
4. **Configure Windows Firewall** for UDP port 8042 (might be needed)

### Manual Kernel Installation

```bash
# Install kernel manually
jupyter kernelspec install kernel_spec/dcs-lua --user

# List installed kernels
jupyter kernelspec list

# Start Jupyter with DCS kernel
jupyter console --kernel=dcs-lua
```

### Custom IP/Port Configuration

Edit `SOCKET_ADDR` and `PORT` constants in both `src/dcs_jupyter/kernel.py` and `dcs_plugin/jupyter_kernel_connection.lua` with identical values.

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Open an issue on GitHub with detailed information about your problem
