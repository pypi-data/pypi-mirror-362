# figma-to-compose-mcp

A Model Context Protocol (MCP) server for generating Jetpack Compose code from Figma nodes.

## Installation

```sh
uvx figma-to-compose-mcp
```

## Usage

Add this to your mcp.json
```sh
"figmaToCompose": {
            "command": "uvx",
            "args": [
                "figma-to-compose-mcp"
            ],
            "env": {
                "FIGMA_TOKEN": "YOUR_FIGMA_TOKEN"
            }
}
```

```sh
Your mcp json should look like this
{
    "servers": {
        "figmaToCompose": {
            "command": "uvx",
            "args": [
                "figma-to-compose-mcp==0.1.4"
            ],
            "env": {
                "FIGMA_TOKEN": "YOUR_FIGMA_TOKEN"
            }
        }
    }
}
```

Set the following environment variables as needed:
- `FIGMA_TOKEN`: Your Figma API token