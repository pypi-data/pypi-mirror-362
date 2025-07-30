# slidespeak-mcp

An MCP Server that allows you to create PowerPoint presentations. Powered by SlideSpeak, you can now create presentations using the SlideSpeak MCP. Automate reports, presentations an other slide decks. Start today!

## Requirements

- Docker ([Download Docker Desktop for free here](https://docs.docker.com/get-started/introduction/get-docker-desktop/))

## Usage with Claude Desktop

To use this with Claude Desktop, add the following to your claude_desktop_config.json:

### Docker

```json
{
  "mcpServers": {
    "slidespeak": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "SLIDESPEAK_API_KEY",
        "slidespeak/slidespeak-mcp:latest"
      ],
      "env": {
        "SLIDESPEAK_API_KEY": "YOUR-API-KEY-HERE"
      }
    }
  }
}
```

## Getting an API key

Visit this page in order to get an API key for Slidespeak: https://slidespeak.co/slidespeak-api/

## Development of SlideSpeak MCP

The following information is related to development of the SlideSpeak MCP. These steps are not needed to use the MCP.

### Building the Docker Image

This is for local testing, if you want to publish a new docker container check out the "Making a new version" section
below.

```bash
docker build . -t slidespeak/slidespeak-mcp:TAG-HERE
```

### Development

#### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Create virtual environment and activate it

uv venv
source .venv/bin/activate

#### Install dependencies

```bash
uv pip install -r requirements.txt
```

### Using the server directly without Docker

Add the following to your claude_desktop_config.json:

```json
{
  "mcpServers": {
    "slidespeak": {
      "command": "/path/to/.local/bin/uv",
      "args": [
        "--directory",
        "/path/to/slidespeak-mcp",
        "run",
        "slidespeak.py"
      ],
      "env": {
        "SLIDESPEAK_API_KEY": "API-KEY-HERE"
      }
    }
  }
}
```

### Making a new release

Version naming should be in the format of `MAJOR.MINOR.PATCH` (e.g., `1.0.0`).

The version needs to be updated in the following files:

- pyproject.toml -> version
- slidespeak.py -> USER_AGENT

Make a new release in GitHub and tag it with the version number.
This will trigger a GitHub Action.
The release will be automatically built and pushed to Docker Hub.

https://hub.docker.com/r/slidespeak/slidespeak-mcp
