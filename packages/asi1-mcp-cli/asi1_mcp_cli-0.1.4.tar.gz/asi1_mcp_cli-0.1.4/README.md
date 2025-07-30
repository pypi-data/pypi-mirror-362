# FETCH.AI MCP CLI

A powerful CLI for interacting with the ASI:One LLM and Model Context Protocol (MCP) servers, now with beautiful branding and agent-to-agent chat!

---

## 🚀 Features

- **Beautiful CLI Header**: Eye-catching ASCII art and welcome message every time you start the CLI.
- **Agent Chat**: Send messages to other agents using `asi1 agent chat --address <agent_address> --message "..."`.
- **LLM/MCP Queries**: Use `asi1 <query>` or `asi1 run <query>` for natural language queries to the LLM or MCP server.
- **Prompt Templates**: Use pre-defined prompt templates for code review, commit messages, and YouTube summaries.
- **Backwards Compatible**: Old usage patterns still work—no need to change your workflow!
- **Call Agent, MCP Server, and LLM**: The CLI can route your query to an agent, the MCP server, or the LLM as needed.

---

## 🖥️ Example Usage

### 1. Show the CLI header and help
```sh
asi1 --help
```

### 2. Ask the LLM or MCP server a question
```sh
asi1 What is the capital of France?
asi1 run "Build a chat bot in JavaScript and HTML"
```

### 3. Use a prompt template
```sh
asi1 run p review
asi1 run p commit
asi1 run p yt https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 4. Chat with another agent
```sh
asi1 agent chat --address <agent_address> --message "Get the latest tweet from Elon Musk"
```

---

## 🧠 Prompt Templates

You can use prompt templates for common tasks:
- `review`: Code review for your current git diff
- `commit`: Generate a Conventional Commit message for your changes
- `yt`: Summarize a YouTube video by URL

Example:
```sh
asi1 run p yt https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## 🆕 Recent Improvements
- Premium, colorful CLI header with FETCH.AI MCP CLI branding
- Agent chat with auto-exit after first response
- Backward compatibility for LLM/MCP queries
- Improved help and usage examples
- Prompt templates for review, commit, and YouTube summary

---

## 🤝 Get Help
- Run `asi1 --help` for usage and examples
- For issues, open an issue on GitHub or contact the maintainers

---

Enjoy using the FETCH.AI MCP CLI! Powered by fetch.ai and ASI:One LLM.
