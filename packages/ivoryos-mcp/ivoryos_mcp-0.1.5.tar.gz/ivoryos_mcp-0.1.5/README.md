# IvoryOS MCP server

![](https://badge.mcpx.dev?type=server 'MCP Server')
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Serve as a robot control interface using [IvoryOS](https://gitlab.com/heingroup/ivoryos) and Model Context Protocol (MCP) to design, manage workflows, and interact with the current hardware/software execution layer.

## 🚀 Quickstart with [Claude Desktop](https://claude.ai/download)
Install [uv](https://docs.astral.sh/uv/).
Open up the configuration file, and add IvoryOS MCP config.
* macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
* Windows: %APPDATA%\Claude\claude_desktop_config.json
```json
{
  "mcpServers": {
    "IvoryOS MCP": {
      "command": "uvx",
      "args": [
        "ivoryos-mcp"
      ],
      "env": {
        "IVORYOS_URL": "http://127.0.0.1:8000/ivoryos",
        "IVORYOS_USERNAME": "<IVORYOS_USERNAME>",
        "IVORYOS_PASSWORD": "<IVORYOS_PASSWORD>"
      }
    }
  }
}
```

## 📦 Installation
Install [uv](https://docs.astral.sh/uv/).
### 1. Clone the Repository

```bash
git clone https://gitlab.com/heingroup/ivoryos-mpc
cd ivoryos-mcp
```
### 2. Install dependencies
When using IDE (e.g. PyCharm), the `uv` environment might be configured, you can skip this section.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r uv.lock
```
## ⚙️ Configuration
Option 1: in `.env`, change ivoryOS url and login credentials. 
```
IVORYOS_URL=http://127.0.0.1:8000/ivoryos
IVORYOS_USERNAME=admin
IVORYOS_PASSWORD=admin
```


Option 2: In `ivoryos_mcp/server.py`, change ivoryOS url and login credentials. 
```python
url = "http://127.0.0.1:8000/ivoryos"
login_data = {
    "username": "admin",
    "password": "admin",
}
```

## 🚀 Install the server (in [Claude Desktop](https://claude.ai/download))
```bash
mcp install ivoryos_mcp/server.py
```

## ✨ Features
| **Category**            | **Feature**              | **Route**                                  | **Description**                                        |
|-------------------------|--------------------------|--------------------------------------------|--------------------------------------------------------|
| **ℹ️ General Tools**    | `platform-info`          | `GET /api/control`                         | Get ivoryOS info and signature of the platform         |
|                         | `execution-status`       | `GET /api/runner/status`                   | Check if system is busy and current/last task status   |
| **ℹ️ Workflow Design**  | `list-workflow-scripts`  | `GET /database/scripts/<deck_name>`        | List all workflow scripts from the database            |
|                         | `load-workflow-script`   | `GET /database/scripts/edit/<script_name>` | Load a workflow script from the database               |
|                         | `submit-workflow-script` | `POST /api/design/submit`                  | Save a workflow Python script to the database          |
| **ℹ️ Workflow Data**    | `list-workflow-data`     | `GET /database/workflows/`                 | List available workflow execution data                 |
|                         | `load-workflow-data`     | `GET /database/workflows/<workflow_id>`    | Load execution log and data file                       |
| **🤖 Direct Control**   | `execute-task`           | `POST /api/control`                        | Call platform function directly                        |
| **🤖 Workflow Run**     | `run-workflow-repeat`    | `POST /design/campaign`                    | Run workflow scripts repeatedly with static parameters |
|                         | `run-workflow-kwargs`    | `POST /design/campaign`                    | Run workflow scripts with dynamic parameters           |
|                         | `run-workflow-campaign`  | `POST /design/campaign`                    | Run workflow campaign with an optimizer                |
| **🤖 Workflow Control** | `pause-and-resume`       | `GET /api/runner/pause`                    | Pause or resume the workflow execution                 |
|                         | `abort-pending-workflow` | `GET /api/runner/abort_pending`            | Finish current iteration, abort future executions      |
|                         | `stop-current-workflow`  | `GET /api/runner/abort_current`            | Safe stop of current workflow                          |

> ⚠️ ℹ️ are resources, but decorated as tool due to the current issue with MCP Python SDK and Claude Desktop integration.  
> It's recommended to only use **`allow always`** for ℹ️ tasks  
> and use **`allow once`** for 🤖 tasks. 
> These tasks will trigger actual actions on your hosted Python code.



## 🧪 Examples
The example prompt uses the abstract SDL example.
### Platform info
![status.gif](https://gitlab.com/heingroup/ivoryos-suite/ivoryos-mcp/-/raw/main/docs/status.gif)

### Load prebuilt workflow script 
![load script.gif](https://gitlab.com/heingroup/ivoryos-suite/ivoryos-mcp/-/raw/main/docs/load%20script.gif)