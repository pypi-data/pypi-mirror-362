# ASI1 MCP CLI

A powerful command-line interface for interacting with the ASI:One LLM and Model Context Protocol (MCP) servers. This CLI provides seamless access to AI capabilities combined with real-time web search, file operations, and more.

## Features

- 🤖 **ASI:One AI Integration** - Powered by ASI:One's advanced language model
- 🔍 **Brave Search** - Real-time web search capabilities
- 📁 **File Operations** - Read, write, and manage files
- 🎥 **YouTube Integration** - Video summarization and analysis
- 💾 **Conversation Memory** - Persistent chat history
- 🛠️ **MCP Server Support** - Extensible with additional MCP servers

## Quick Start

### Installation

```bash
pip install asi1-mcp-cli
```

### Setup

1. **Create configuration directory:**
   ```bash
   mkdir -p ~/.asi1
   ```

2. **Create configuration file:**
   ```bash
   # Copy the example config
   cp $(python -c "import asi1_mcp_cli; import os; print(os.path.join(os.path.dirname(asi1_mcp_cli.__file__), '..', 'asi1-mcp-server-config-example.json'))") ~/.asi1/config.json
   ```

3. **Edit the configuration:**
   ```bash
   nano ~/.asi1/config.json
   ```

   Update the following fields:
   - `api_key`: Your ASI:One API key
   - `BRAVE_API_KEY`: Your Brave Search API key (optional)

### Usage

#### Basic Conversation
```bash
asi1 "What is the capital of France?"
```

#### Web Search
```bash
asi1 "What are the latest developments in quantum computing?"
```

#### List Available Prompts
```bash
asi1 --list-prompts
```

#### Use Specific Prompt Templates
```bash
# Code review
asi1 --prompt review

# Git commit
asi1 --prompt commit

# YouTube video summary
asi1 --prompt yt --url "https://www.youtube.com/watch?v=example"
```

## Configuration

The configuration file (`~/.asi1/config.json`) supports:

### LLM Settings
- `provider`: LLM provider (use "asi-one" for ASI:One)
- `model`: Model name (e.g., "asi1-mini")
- `api_key`: Your API key
- `temperature`: Response creativity (0.0-1.0)
- `base_url`: API endpoint

### MCP Servers
- **Brave Search**: Web search capabilities
- **YouTube**: Video analysis and summarization
- **File Operations**: Read/write files
- **Commands**: Execute system commands (with confirmation)

## Prompt Templates

### Built-in Templates

1. **review** - Code review assistant
   - Analyzes git changes and provides feedback

2. **commit** - Git commit assistant
   - Creates conventional commit messages

3. **yt** - YouTube video summarizer
   - Summarizes video content with bullet points

### Custom Templates

Add your own prompt templates to the configuration:

```json
{
  "prompts": {
    "my_template": {
      "template": "You are a helpful assistant. {user_input}",
      "arguments": []
    }
  }
}
```

## Examples

### Software Development
```bash
# Code review
asi1 --prompt review

# Create commit message
asi1 --prompt commit

# Ask about programming
asi1 "How do I implement a REST API in Python?"
```

### Research & Information
```bash
# Current events
asi1 "What are the latest developments in AI?"

# Technical research
asi1 "What are the differences between React and Vue.js?"

# Market analysis
asi1 "What's the current state of the cryptocurrency market?"
```

### Content Creation
```bash
# Video summarization
asi1 --prompt yt --url "https://www.youtube.com/watch?v=example"

# Writing assistance
asi1 "Help me write a professional email to a client"
```

## Troubleshooting

### Common Issues

1. **"No module named 'langchain_openai'"**
   ```bash
   pip install langchain-openai
   ```

2. **"404 page not found"**
   - Check your `base_url` in config (should be `https://api.asi1.ai/v1`)

3. **MCP server errors**
   - Some servers require additional setup (e.g., API keys)
   - Check the server configuration in your config file

### Getting Help

- Check the configuration file syntax
- Ensure all required dependencies are installed
- Verify API keys are correct
- Check network connectivity

## Development

### Local Development Setup

```bash
git clone <repository-url>
cd asi1-mcp-cli
pip install -e .
```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.
