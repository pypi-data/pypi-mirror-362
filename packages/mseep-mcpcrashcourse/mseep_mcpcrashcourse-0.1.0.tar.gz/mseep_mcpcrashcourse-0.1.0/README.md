A simple demo of MCP python sdk.

## MCP Crash Course


## uv commands

start a new project
```bash
uv init <project-name>
```

create a virtual environment
```bash
uv venv
```

activate the virtual environment
```bash
uv venv --activate
```

install the dependencies
```bash
uv add <package>
uv add -r requirements.txt
uv sync
```

run application
```bash
uv run app.py
```

run the development server
```bash
uv run dev
```

build the project
```bash
uv run build
```

Run server using MCP Inspector :

- Install MCP python sdk

```bash
uv add "mcp[cli]"
```

- Run mcp inspector

```bash
uv run mcp dev server/weather.py
```

MCP Inspector is up and running at http://127.0.0.1:6274

Add server to claude desktop :

- run command
```bash
uv run mcp install .\server\weather.py
```
- query "what is weather alert in CA" in claude desktop

Add server to cursor :

- goto preferences > settings > mcp and copy paste claude config
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\Users\\Suraj\\Desktop\\Python\\mcp-crash-course\\mcpcrashcourse\\server\\weather.py"
      ]
    }
  }
}
```
- Then do a query in cursor chat


Directly consume server in code - using mcp-use :

- Install mcp-use

```bash
uv add mcp-use
```

- Install langchain-groq

```bash
uv add langchain-groq
```

- run client

```bash
uv run server/client.py
```