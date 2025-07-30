[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/omniscience-labs-omni-mqtt-mcp-badge.png)](https://mseep.ai/app/omniscience-labs-omni-mqtt-mcp)

# OMNI-MQTT-MCP

MQTT MCP Server with configurable transport options via CLI: **STDIO** (default), **Streamable HTTP** (recommended for web), and **SSE** (deprecated).

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run with STDIO (default - for local development)
python mqtt_mcp_server.py

# Run with Streamable HTTP (recommended for web)
python mqtt_mcp_server.py --transport streamable-http

# Run with SSE (deprecated)
python mqtt_mcp_server.py --transport sse
```

## 📋 Transport Options

Choose your transport with the `--transport` CLI argument:

### 1. **STDIO Transport** (Default) ✅
```bash
python mqtt_mcp_server.py --transport stdio
# or simply:
python mqtt_mcp_server.py
```
- **Best for**: Local development, Claude Desktop integration
- **Pros**: Simple, secure, works with MCP clients like Claude Desktop
- **Cons**: Local only, no remote access

### 2. **Streamable HTTP** (Recommended for Web) 🌐
```bash
python mqtt_mcp_server.py --transport streamable-http
python mqtt_mcp_server.py --transport streamable-http --host 0.0.0.0 --http-port 9000
```
- **Best for**: Web deployments, remote access, microservices
- **Default URL**: `http://127.0.0.1:8000/mcp`
- **Pros**: Modern, efficient, supports multiple clients, easy deployment
- **Cons**: Requires network setup, security considerations

### 3. **SSE (Server-Sent Events)** ⚠️ Deprecated
```bash
python mqtt_mcp_server.py --transport sse
```
- **Best for**: Legacy deployments (not recommended for new projects)
- **Default URL**: `http://127.0.0.1:8000/sse`
- **Status**: Being phased out in favor of Streamable HTTP

## 🛠 Available Tools

- **`mqtt_publish`**: Publish messages to MQTT topics
- **`mqtt_subscribe`**: Subscribe to MQTT topics and receive messages

## ⚙️ Configuration Options

### MQTT Configuration
```bash
python mqtt_mcp_server.py \
  --broker localhost \
  --port 1883 \
  --client-id mcp-mqtt-client \
  --username your_username \
  --password your_password
```

### Transport Configuration
```bash
python mqtt_mcp_server.py \
  --transport streamable-http \
  --host 127.0.0.1 \
  --http-port 8000 \
  --path /mcp
```

### All Options
```bash
python mqtt_mcp_server.py --help
```

### Environment Variables

You can also use environment variables for MQTT settings:
```bash
export MQTT_BROKER_ADDRESS=localhost
export MQTT_PORT=1883
export MQTT_CLIENT_ID=mcp-mqtt-client
export MQTT_USERNAME=your_username
export MQTT_PASSWORD=your_password

python mqtt_mcp_server.py --transport streamable-http
```

## 🧪 Testing

### Test HTTP Server
```bash
# Terminal 1: Start server
python mqtt_mcp_server.py --transport streamable-http

# Terminal 2: Test it
python test_http_client.py
```

### Test with Claude Desktop

Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "mqtt": {
      "command": "python",
      "args": ["/path/to/mqtt_mcp_server.py"],
      "env": {
        "MQTT_BROKER_ADDRESS": "localhost",
        "MQTT_PORT": "1883"
      }
    }
  }
}
```

## 🔧 Development

### Using the MCP CLI

```bash
# Run in development mode with MCP Inspector
mcp dev mqtt_mcp_server.py

# Run with specific transport via MCP CLI
mcp run mqtt_mcp_server.py -- --transport streamable-http --http-port 9000
```

## 📚 Examples

### Local Development
```bash
# Default STDIO for Claude Desktop
python mqtt_mcp_server.py
```

### Web Deployment
```bash
# HTTP server on port 8000
python mqtt_mcp_server.py --transport streamable-http

# HTTP server on custom port and host
python mqtt_mcp_server.py --transport streamable-http --host 0.0.0.0 --http-port 9000

# Custom path
python mqtt_mcp_server.py --transport streamable-http --path /api/mcp
```

### Production with Custom MQTT
```bash
python mqtt_mcp_server.py \
  --transport streamable-http \
  --broker mqtt.example.com \
  --port 8883 \
  --username prod_user \
  --password secret123 \
  --host 0.0.0.0 \
  --http-port 80
```

## 🤔 Which Transport Should I Choose?

| Use Case | Command | Why? |
|----------|---------|------|
| **Local development** | `python mqtt_mcp_server.py` | Simple, secure, works with Claude Desktop |
| **Web deployment** | `python mqtt_mcp_server.py --transport streamable-http` | Modern, efficient, easy to deploy |
| **Remote AI agents** | `python mqtt_mcp_server.py --transport streamable-http --host 0.0.0.0` | Supports authentication, scalable |
| **Legacy systems** | `python mqtt_mcp_server.py --transport sse` | Only if you're already using SSE |

## 🐳 Docker with Ngrok

Run the server inside Docker and automatically expose it with an ngrok tunnel.

### Build
```bash
docker build -t mqtt-mcp-ngrok .
```

### Run
```bash
docker run -d \
  -p 8000:8000 \
  -e NGROK_AUTHTOKEN=<YOUR_TOKEN> \
  -e TRANSPORT=sse \
  -e FASTMCP_PORT=8000 \
  -e MQTT_BROKER_ADDRESS=mqtt.example.com \
  -e MQTT_PORT=8883 \
  -e MQTT_CLIENT_ID=my-client \
  -e MQTT_USERNAME=prod_user \
  -e MQTT_PASSWORD=secret123 \
  mqtt-mcp-ngrok
```
The container exposes the MCP server via ngrok. Pass environment variables to
configure the MQTT broker and server transport. Check the container logs to
discover the public URL.

## 📚 Learn More

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://gofastmcp.com/)

## 🔒 Security Notes

- **STDIO**: Runs locally, inherently secure
- **HTTP/SSE**: Consider adding authentication for production deployments
- **MQTT**: Configure MQTT broker security (TLS, authentication)
