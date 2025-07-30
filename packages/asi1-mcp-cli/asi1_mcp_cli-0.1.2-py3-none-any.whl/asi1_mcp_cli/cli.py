#!/usr/bin/env python3

"""
ASI1 MCP CLI: A command-line interface for interacting with ASI:One LLM and MCP servers.
"""

from datetime import datetime
import argparse
import asyncio
import os
from typing import Annotated, TypedDict
import uuid
import sys
import re
import anyio
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.prebuilt import create_react_agent
from langgraph.managed import IsLastStep
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from rich.console import Console
from rich.table import Table
import base64
import filetype
import mimetypes

from .input import *
from .const import *
from .output import *
from .storage import *
from .tool import *
from .prompt import *
from .memory import *
from .config import AppConfig, copy_example_config

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    is_last_step: IsLastStep
    today_datetime: str
    memories: str
    remaining_steps: int

async def run() -> None:
    """Run the ASI1 MCP CLI agent."""
    args = setup_argument_parser()
    query, is_conversation_continuation = parse_query(args)
    app_config = AppConfig.load()
    
    if args.list_tools:
        await handle_list_tools(app_config, args)
        return
    
    if args.show_memories:
        await handle_show_memories()
        return
        
    if args.list_prompts:
        handle_list_prompts()
        return
        
    if args.init:
        handle_init_config()
        return
        
    await handle_conversation(args, query, is_conversation_continuation, app_config)

def setup_argument_parser() -> argparse.Namespace:
    """Setup and return the argument parser."""
    parser = argparse.ArgumentParser(
        description='Run ASI:One LLM with MCP servers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  asi1 "What is the capital of France?"     Ask a simple question
  asi1 c "tell me more"                     Continue previous conversation
  asi1 p review                             Use a prompt template
  cat file.txt | asi1                       Process input from a file
  asi1 --list-tools                         Show available tools
  asi1 --list-prompts                       Show available prompt templates
  asi1 --no-confirmations "search web"      Run tools without confirmation
        """
    )
    parser.add_argument('query', nargs='*', default=[],
                       help='The query to process (default: read from stdin). '
                            'Special prefixes:\n'
                            '  c: Continue previous conversation\n'
                            '  p: Use prompt template')
    parser.add_argument('--list-tools', action='store_true',
                       help='List all available LLM tools')
    parser.add_argument('--list-prompts', action='store_true',
                       help='List all available prompts')
    parser.add_argument('--no-confirmations', action='store_true',
                       help='Bypass tool confirmation requirements')
    parser.add_argument('--force-refresh', action='store_true',
                       help='Force refresh of tools capabilities')
    parser.add_argument('--text-only', action='store_true',
                       help='Print output as raw text instead of parsing markdown')
    parser.add_argument('--no-tools', action='store_true',
                       help='Do not add any tools')
    parser.add_argument('--no-intermediates', action='store_true',
                       help='Only print the final message')
    parser.add_argument('--show-memories', action='store_true',
                       help='Show user memories')
    parser.add_argument('--model',
                       help='Override the model specified in config')
    parser.add_argument('--init', action='store_true',
                       help='Initialize configuration file')
    return parser.parse_args()

async def handle_list_tools(app_config: AppConfig, args: argparse.Namespace) -> None:
    """Handle the --list-tools command."""
    server_configs = [
        McpServerConfig(
            server_name=name,
            server_param=StdioServerParameters(
                command=config.command,
                args=config.args or [],
                env={**(config.env or {}), **os.environ}
            ),
            exclude_tools=config.exclude_tools or []
        )
        for name, config in app_config.get_enabled_servers().items()
    ]
    toolkits, tools = await load_tools(server_configs, args.no_tools, args.force_refresh)
    
    console = Console()
    table = Table(title="Available ASI:One MCP Tools")
    table.add_column("Toolkit", style="cyan")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description", style="green")

    for tool in tools:
        if isinstance(tool, McpTool):
            table.add_row(tool.toolkit_name, tool.name, tool.description)

    console.print(table)

    for toolkit in toolkits:
        await toolkit.close()

async def handle_show_memories() -> None:
    """Handle the --show-memories command."""
    store = SqliteStore(SQLITE_DB)
    memories = await get_memories(store)
    console = Console()
    table = Table(title="ASI:One LLM Memories")
    for memory in memories:
        table.add_row(memory)
    console.print(table)

def handle_list_prompts() -> None:
    """Handle the --list-prompts command."""
    console = Console()
    table = Table(title="Available Prompt Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Template")
    table.add_column("Arguments")
    
    for name, template in prompt_templates.items():
        table.add_row(name, template, ", ".join(re.findall(r'\{(\w+)\}', template)))
        
    console.print(table)

def handle_init_config() -> None:
    """Handle the --init command."""
    console = Console()
    try:
        config_path = copy_example_config()
        console.print(f"✅ Configuration file created at: {config_path}")
        console.print("\n📝 Next steps:")
        console.print("1. Edit the configuration file to add your API keys:")
        console.print(f"   nano {config_path}")
        console.print("2. Update the following fields:")
        console.print("   - api_key: Your ASI:One API key")
        console.print("   - BRAVE_API_KEY: Your Brave Search API key (optional)")
        console.print("\n3. Start using the CLI:")
        console.print("   asi1 'Hello, how can you help me?'")
    except Exception as e:
        console.print(f"❌ Error creating configuration file: {e}")
        sys.exit(1)

async def load_tools(server_configs: list[McpServerConfig], no_tools: bool, force_refresh: bool) -> tuple[list, list]:
    """Load and convert MCP tools to LangChain tools."""
    if no_tools:
        return [], []
        
    toolkits = []
    langchain_tools = []
    
    async def convert_toolkit(server_config: McpServerConfig):
        try:
            toolkit = await convert_mcp_to_langchain_tools(server_config, force_refresh)
            if toolkit and toolkit.get_tools():
                toolkits.append(toolkit)
                langchain_tools.extend(toolkit.get_tools())
        except Exception as e:
            print(f"Warning: Failed to load toolkit for {server_config.server_name}: {e}")
            # Continue with other toolkits even if this one fails
            print(f"Warning: Failed to load toolkit for {server_config.server_name}: {e}")
            # Continue with other toolkits even if this one fails

    # Load toolkits sequentially to avoid task group issues
    for server_config in server_configs:
        await convert_toolkit(server_config)
            
    langchain_tools.append(save_memory)
    return toolkits, langchain_tools

async def handle_conversation(args: argparse.Namespace, query: HumanMessage, 
                            is_conversation_continuation: bool, app_config: AppConfig) -> None:
    """Handle the main conversation flow."""
    server_configs = [
        McpServerConfig(
            server_name=name,
            server_param=StdioServerParameters(
                command=config.command,
                args=config.args or [],
                env={**(config.env or {}), **os.environ}
            ),
            exclude_tools=config.exclude_tools or []
        )
        for name, config in app_config.get_enabled_servers().items()
    ]
    toolkits, tools = await load_tools(server_configs, args.no_tools, args.force_refresh)
    
    extra_body = {}
    if app_config.llm.base_url and "asi-one" in app_config.llm.base_url:
        extra_body = {"web3_enabled": True}
    if args.model:
        app_config.llm.model = args.model
        
    # Use OpenAI provider for ASI1 API since it's OpenAI-compatible
    provider = "openai" if app_config.llm.provider == "asi-one" else app_config.llm.provider
        
    model: BaseChatModel = init_chat_model(
        model=app_config.llm.model,
        model_provider=provider,
        api_key=app_config.llm.api_key,
        temperature=app_config.llm.temperature,
        base_url=app_config.llm.base_url,
        default_headers={
            "X-Title": "asi1-mcp-cli",
            "HTTP-Referer": "https://github.com/asi-one/asi1-mcp-cli",
        },
        extra_body=extra_body
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", app_config.system_prompt),
        ("placeholder", "{messages}")
    ])

    conversation_manager = ConversationManager(SQLITE_DB)
    
    async with AsyncSqliteSaver.from_conn_string(SQLITE_DB) as checkpointer:
        store = SqliteStore(SQLITE_DB)
        memories = await get_memories(store)
        formatted_memories = "\n".join(f"- {memory}" for memory in memories)
        agent_executor = create_react_agent(
            model, tools, state_schema=AgentState, 
            checkpointer=checkpointer, store=store
        )
        
        thread_id = (await conversation_manager.get_last_id() if is_conversation_continuation 
                    else uuid.uuid4().hex)

        input_messages = AgentState(
            messages=[query], 
            today_datetime=datetime.now().isoformat(),
            memories=formatted_memories,
            remaining_steps=3
        )

        output = OutputHandler(text_only=args.text_only, only_last_message=args.no_intermediates)
        output.start()
        try:
            async for chunk in agent_executor.astream(
                input_messages,
                stream_mode=["messages", "values"],
                config={"configurable": {"thread_id": thread_id, "user_id": "myself"}, 
                       "recursion_limit": 100}
            ):
                output.update(chunk)
                if not args.no_confirmations:
                    if not output.confirm_tool_call(app_config.__dict__, chunk):
                        break
        except Exception as e:
            output.update_error(e)
        finally:
            output.finish()

        await conversation_manager.save_id(thread_id, checkpointer.conn)

    for toolkit in toolkits:
        await toolkit.close()

def parse_query(args: argparse.Namespace) -> tuple[HumanMessage, bool]:
    """
    Parse the query from command line arguments.
    Returns a tuple of (HumanMessage, is_conversation_continuation).
    """
    query_parts = ' '.join(args.query).split()
    stdin_content = ""
    stdin_image = None
    is_continuation = False

    if query_parts and query_parts[0] == 'cb':
        query_parts = query_parts[1:]
        clipboard_result = get_clipboard_content()
        if clipboard_result:
            content, mime_type = clipboard_result
            if mime_type:
                stdin_image = base64.b64encode(content).decode('utf-8')
            else:
                stdin_content = content
        else:
            print("No content found in clipboard")
            raise Exception("Clipboard is empty")
    elif not sys.stdin.isatty():
        stdin_data = sys.stdin.buffer.read()
        kind = filetype.guess(stdin_data)
        image_type = kind.extension if kind else None
        if image_type:
            stdin_image = base64.b64encode(stdin_data).decode('utf-8')
            mime_type = mimetypes.guess_type(f"dummy.{image_type}")[0] or f"image/{image_type}"
        else:
            stdin_content = stdin_data.decode('utf-8').strip()

    query_text = ""
    if query_parts:
        if query_parts[0] == 'c':
            is_continuation = True
            query_text = ' '.join(query_parts[1:])
        elif query_parts[0] == 'p' and len(query_parts) >= 2:
            template_name = query_parts[1]
            if template_name not in prompt_templates:
                print(f"Error: Prompt template '{template_name}' not found.")
                print("Available templates:", ", ".join(prompt_templates.keys()))
                return HumanMessage(content=""), False

            template = prompt_templates[template_name]
            template_args = query_parts[2:]
            try:
                var_names = re.findall(r'\{(\w+)\}', template)
                template_vars = dict(zip(var_names, template_args))
                query_text = template.format(**template_vars)
            except KeyError as e:
                print(f"Error: Missing argument {e}")
                return HumanMessage(content=""), False
        else:
            query_text = ' '.join(query_parts)

    if stdin_content and query_text:
        query_text = f"{stdin_content}\n\n{query_text}"
    elif stdin_content:
        query_text = stdin_content
    elif not query_text and not stdin_image:
        return HumanMessage(content=""), False

    if stdin_image:
        content = [
            {"type": "text", "text": query_text or "What do you see in this image?"},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{stdin_image}"}}
        ]
    else:
        content = query_text

    return HumanMessage(content=content), is_continuation

def main() -> None:
    """Entry point of the script."""
    asyncio.run(run())

if __name__ == "__main__":
    main()