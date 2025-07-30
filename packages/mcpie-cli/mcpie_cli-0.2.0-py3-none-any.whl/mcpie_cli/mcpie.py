import asyncio
import json
import logging
import shlex
import sys
from urllib.parse import urljoin

import click
import yaml
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import Result
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.data import JsonLexer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

# Configure logging to use Rich and output to stderr
# This prevents server logs from polluting stdout when piping
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors by default
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            console=Console(stderr=True),  # Force output to stderr
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False,
        )
    ],
)

# Set up logger for this module
logger = logging.getLogger(__name__)

# Suppress noisy loggers from libraries
logging.getLogger("mcp").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# Main console for regular output (stdout)
console = Console()

# Separate console for status messages and non-essential output (stderr)
console_err = Console(stderr=True)


class OutputConfig:
    """Configuration for output formatting."""

    def __init__(
        self, output_format: str, quiet: bool, verbose: bool, output_file: str | None
    ):
        self.output_format = output_format
        self.quiet = quiet
        self.verbose = verbose
        self.output_file = output_file


class BaseOutputFormatter:
    """Base class for output formatters."""

    def __init__(self, config: OutputConfig):
        self.config = config
        self.output_stream = None
        if config.output_file:
            self.output_stream = open(config.output_file, "w")

    def __del__(self):
        if self.output_stream:
            self.output_stream.close()

    def write(self, content: str):
        """Write content to appropriate stream."""
        if self.output_stream:
            self.output_stream.write(content)
            self.output_stream.flush()
        else:
            print(content, end="")

    def format_result(self, result: Result, title: str = "Result") -> str:
        """Format a result object."""
        raise NotImplementedError

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        """Format a list of items."""
        raise NotImplementedError

    def format_error(self, error: str):
        """Format an error message."""
        if not self.config.quiet:
            print(f"Error: {error}", file=sys.stderr)


class JsonOutputFormatter(BaseOutputFormatter):
    """JSON output formatter."""

    def format_result(self, result: Result, title: str = "Result") -> str:
        if not result:
            return "{}"

        result_dict = result.model_dump(exclude_defaults=True)
        return json.dumps(result_dict, indent=None)

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        if not items:
            return "[]"

        formatted_items = []
        for item in items:
            if hasattr(item, "model_dump"):
                formatted_items.append(item.model_dump(exclude_defaults=True))
            elif isinstance(item, dict):
                formatted_items.append(item)
            else:
                # Convert to dict using specified columns
                item_dict = {}
                for col in columns:
                    if hasattr(item, col):
                        item_dict[col] = getattr(item, col)
                formatted_items.append(item_dict)

        return json.dumps(formatted_items, indent=None)


class PrettyOutputFormatter(BaseOutputFormatter):
    """Pretty JSON output formatter."""

    def format_result(self, result: Result, title: str = "Result") -> str:
        if not result:
            return "{}"

        result_dict = result.model_dump(exclude_defaults=True)
        return json.dumps(result_dict, indent=2)

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        if not items:
            return "[]"

        formatted_items = []
        for item in items:
            if hasattr(item, "model_dump"):
                formatted_items.append(item.model_dump(exclude_defaults=True))
            elif isinstance(item, dict):
                formatted_items.append(item)
            else:
                # Convert to dict using specified columns
                item_dict = {}
                for col in columns:
                    if hasattr(item, col):
                        item_dict[col] = getattr(item, col)
                formatted_items.append(item_dict)

        return json.dumps(formatted_items, indent=2)


class TableOutputFormatter(BaseOutputFormatter):
    """Table output formatter."""

    def format_result(self, result: Result, title: str = "Result") -> str:
        if not result:
            return "No result"

        result_dict = result.model_dump(exclude_defaults=True)

        # For single objects, format as key-value pairs
        if isinstance(result_dict, dict):
            lines = []
            for key, value in result_dict.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, indent=2)
                lines.append(f"{key}: {value}")
            return "\n".join(lines)
        else:
            return str(result_dict)

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        if not items:
            return f"No {title.lower()} available"

        # Calculate column widths
        col_widths = {}
        for col in columns:
            col_widths[col] = len(col)

        # Get all values and calculate max widths
        all_rows = []
        for item in items:
            row = {}
            for col in columns:
                if hasattr(item, col):
                    value = getattr(item, col)
                elif isinstance(item, dict) and col in item:
                    value = item[col]
                else:
                    value = ""

                if isinstance(value, (dict, list)):
                    value = json.dumps(value, indent=2)
                elif value is None:
                    value = ""

                value_str = str(value)
                row[col] = value_str
                col_widths[col] = max(col_widths[col], len(value_str))
            all_rows.append(row)

        # Format table
        lines = []

        # Header
        header = " | ".join(col.ljust(col_widths[col]) for col in columns)
        lines.append(header)
        lines.append("-" * len(header))

        # Rows
        for row in all_rows:
            line = " | ".join(row[col].ljust(col_widths[col]) for col in columns)
            lines.append(line)

        return "\n".join(lines)


class YamlOutputFormatter(BaseOutputFormatter):
    """YAML output formatter."""

    def format_result(self, result: Result, title: str = "Result") -> str:
        if not result:
            return "null"

        result_dict = result.model_dump(exclude_defaults=True)
        return yaml.dump(result_dict, default_flow_style=False)

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        if not items:
            return "[]"

        formatted_items = []
        for item in items:
            if hasattr(item, "model_dump"):
                formatted_items.append(item.model_dump(exclude_defaults=True))
            elif isinstance(item, dict):
                formatted_items.append(item)
            else:
                # Convert to dict using specified columns
                item_dict = {}
                for col in columns:
                    if hasattr(item, col):
                        item_dict[col] = getattr(item, col)
                formatted_items.append(item_dict)

        return yaml.dump(formatted_items, default_flow_style=False)


class RawOutputFormatter(BaseOutputFormatter):
    """Raw output formatter."""

    def format_result(self, result: Result, title: str = "Result") -> str:
        if not result:
            return ""

        # For raw output, try to extract the most relevant content
        result_dict = result.model_dump(exclude_defaults=True)

        # Check for content array (common in MCP responses)
        if isinstance(result_dict, dict) and "content" in result_dict:
            content = result_dict["content"]
            if isinstance(content, list) and len(content) > 0:
                if (
                    len(content) == 1
                    and isinstance(content[0], dict)
                    and "text" in content[0]
                ):
                    return content[0]["text"]

        # Check for contents (resources)
        if isinstance(result_dict, dict) and "contents" in result_dict:
            contents = result_dict["contents"]
            if isinstance(contents, list) and len(contents) > 0:
                content = contents[0]
                if isinstance(content, dict):
                    if "text" in content:
                        return content["text"]
                    elif "blob" in content:
                        return content["blob"]

        # Check for structured content (tool results)
        if isinstance(result_dict, dict) and "structuredContent" in result_dict:
            structured_content = result_dict["structuredContent"]
            if isinstance(structured_content, dict) and "result" in structured_content:
                return str(structured_content["result"])

        # Fall back to string representation
        return str(result_dict)

    def format_list(self, items: list, title: str, columns: list[str]) -> str:
        if not items:
            return ""

        # For raw output, just return the most relevant field from each item
        lines = []
        for item in items:
            if hasattr(item, "name"):
                lines.append(str(getattr(item, "name")))
            elif hasattr(item, "uri"):
                lines.append(str(getattr(item, "uri")))
            elif isinstance(item, dict):
                if "name" in item:
                    lines.append(str(item["name"]))
                elif "uri" in item:
                    lines.append(str(item["uri"]))
                else:
                    lines.append(str(item))
            else:
                lines.append(str(item))

        return "\n".join(lines)


def get_output_formatter(config: OutputConfig) -> BaseOutputFormatter:
    """Get the appropriate output formatter based on config."""
    if config.output_format == "json":
        return JsonOutputFormatter(config)
    elif config.output_format == "pretty":
        return PrettyOutputFormatter(config)
    elif config.output_format == "table":
        return TableOutputFormatter(config)
    elif config.output_format == "yaml":
        return YamlOutputFormatter(config)
    elif config.output_format == "raw":
        return RawOutputFormatter(config)
    else:
        return JsonOutputFormatter(config)


# Exit codes as defined in the spec
EXIT_SUCCESS = 0
EXIT_CLI_ERROR = 1
EXIT_SERVER_ERROR = 2
EXIT_INVALID_INPUT = 3


def exit_with_code(code: int, message: str = "", quiet: bool = False):
    """Exit with appropriate code and message."""
    if message and not quiet:
        if code == EXIT_SUCCESS:
            print(message)
        else:
            print(message, file=sys.stderr)
    sys.exit(code)


def print_error(message: str, session: "MCPSession | None" = None):
    """Print error message to stderr, respecting quiet mode."""
    if session and session.output_config and session.output_config.quiet:
        return
    if session and session.output_formatter:
        session.output_formatter.format_error(message)
    else:
        print(f"Error: {message}", file=sys.stderr)


def print_warning(message: str, session: "MCPSession | None" = None):
    """Print warning message to stderr, respecting quiet mode."""
    if session and session.output_config and session.output_config.quiet:
        return
    print(f"Warning: {message}", file=sys.stderr)


class CommandConfig:
    """Configuration for a command type."""

    def __init__(self, name: str, aliases: list[str], subcommands: dict[str, object]):
        self.name = name
        self.aliases = aliases
        self.subcommands = subcommands


# Command configurations
COMMANDS = {
    "resources": CommandConfig(
        name="resources",
        aliases=["r"],
        subcommands={
            "list": {"aliases": ["ls"], "description": "List resources"},
            "read": {
                "aliases": [],
                "description": "Read a resource",
                "requires_arg": True,
            },
            "templates": {"aliases": [], "description": "List resource templates"},
            "inspect": {
                "aliases": [],
                "description": "Show detailed resource info",
                "requires_arg": True,
            },
        },
    ),
    "prompts": CommandConfig(
        name="prompts",
        aliases=["p"],
        subcommands={
            "list": {"aliases": ["ls"], "description": "List prompts"},
            "get": {"aliases": [], "description": "Get a prompt", "requires_arg": True},
            "inspect": {
                "aliases": [],
                "description": "Show detailed prompt info",
                "requires_arg": True,
            },
        },
    ),
    "tools": CommandConfig(
        name="tools",
        aliases=["t"],
        subcommands={
            "list": {"aliases": ["ls"], "description": "List tools"},
            "call": {"aliases": [], "description": "Call a tool", "requires_arg": True},
            "inspect": {
                "aliases": [],
                "description": "Show detailed tool info",
                "requires_arg": True,
            },
        },
    ),
    "server": CommandConfig(
        name="server",
        aliases=["s"],
        subcommands={
            "info": {"aliases": [], "description": "Show server information"},
            "ping": {"aliases": [], "description": "Ping the server"},
            "capabilities": {
                "aliases": ["caps"],
                "description": "Show server capabilities",
            },
        },
    ),
}


class MCPCompleter(Completer):
    """Custom completer for MCP commands with auto-completion for tools, prompts, and resources."""

    def __init__(self, session: "MCPSession"):
        self.session = session
        self.base_commands = {
            "help": "Show help information",
            "quit": "Exit the REPL",
            "exit": "Exit the REPL",
            "clear": "Clear the screen",
            "ls": "List resources (alias for resources/list)",
            "discover": "Show all available resources, tools, and prompts",
        }
        # Cache for auto-completion data
        self._tools_cache = None
        self._prompts_cache = None
        self._resources_cache = None
        self._cache_populated = False

    def _populate_cache_sync(self):
        """Populate cache synchronously if possible."""
        if self._cache_populated or not self.session.initialized:
            return

        try:
            # Try to get cached data if session has it
            if hasattr(self.session, "_completion_cache"):
                cache = self.session._completion_cache
                self._tools_cache = cache.get("tools", [])
                self._prompts_cache = cache.get("prompts", [])
                self._resources_cache = cache.get("resources", [])
                self._cache_populated = True
        except:  # noqa: E722
            pass

    async def _get_tools(self) -> list[str]:
        """Get list of available tool names."""
        if self._tools_cache is None and self.session.initialized:
            try:
                result = await self.session.execute_command("tools", "list")
                if result and hasattr(result, "tools"):
                    self._tools_cache = [tool.name for tool in result.tools]
                    # Store in session for sync access
                    if not hasattr(self.session, "_completion_cache"):
                        self.session._completion_cache = {}
                    self.session._completion_cache["tools"] = self._tools_cache
                else:
                    self._tools_cache = []
            except:  # noqa: E722
                self._tools_cache = []
        return self._tools_cache or []

    async def _get_prompts(self) -> list[str]:
        """Get list of available prompt names."""
        if self._prompts_cache is None and self.session.initialized:
            try:
                result = await self.session.execute_command("prompts", "list")
                if result and hasattr(result, "prompts"):
                    self._prompts_cache = [prompt.name for prompt in result.prompts]
                    # Store in session for sync access
                    if not hasattr(self.session, "_completion_cache"):
                        self.session._completion_cache = {}
                    self.session._completion_cache["prompts"] = self._prompts_cache
                else:
                    self._prompts_cache = []
            except:  # noqa: E722
                self._prompts_cache = []
        return self._prompts_cache or []

    async def _get_resources(self) -> list[str]:
        """Get list of available resource URIs."""
        if self._resources_cache is None and self.session.initialized:
            try:
                result = await self.session.execute_command("resources", "list")
                if result and hasattr(result, "resources"):
                    self._resources_cache = [
                        str(resource.uri) for resource in result.resources
                    ]
                    # Store in session for sync access
                    if not hasattr(self.session, "_completion_cache"):
                        self.session._completion_cache = {}
                    self.session._completion_cache["resources"] = self._resources_cache
                else:
                    self._resources_cache = []
            except:  # noqa: E722
                self._resources_cache = []
        return self._resources_cache or []

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        line = document.text_before_cursor
        parts = line.split()

        # Populate cache from session if available
        self._populate_cache_sync()

        # Auto-complete tool names for "t call <tool_name>" and "t inspect <tool_name>"
        if (
            len(parts) >= 2
            and parts[0] in ["t", "tools"]
            and parts[1] in ["call", "inspect"]
            and len(parts) == 3
        ):
            tools = self._tools_cache or []
            for tool in tools:
                if tool.startswith(word):
                    yield Completion(
                        tool,
                        start_position=-len(word),
                        display=f"{tool} (tool)",
                    )
            return

        # Auto-complete prompt names for "p get <prompt_name>" and "p inspect <prompt_name>"
        if (
            len(parts) >= 2
            and parts[0] in ["p", "prompts"]
            and parts[1] in ["get", "inspect"]
            and len(parts) == 3
        ):
            prompts = self._prompts_cache or []
            for prompt in prompts:
                if prompt.startswith(word):
                    yield Completion(
                        prompt,
                        start_position=-len(word),
                        display=f"{prompt} (prompt)",
                    )
            return

        # Auto-complete resource URIs for "r read <uri>" and "r inspect <uri>"
        if (
            len(parts) >= 2
            and parts[0] in ["r", "resources"]
            and parts[1] in ["read", "inspect"]
            and len(parts) == 3
        ):
            resources = self._resources_cache or []
            for resource in resources:
                if resource.startswith(word):
                    yield Completion(
                        resource,
                        start_position=-len(word),
                        display=f"{resource} (resource)",
                    )
            return

        # Handle subcommands - only show when we have exactly 2 parts (command + partial subcommand)
        for cmd_name, cmd_config in COMMANDS.items():
            for alias in [cmd_name] + cmd_config.aliases:
                if line.startswith(f"{alias} ") and len(parts) == 2:
                    subcommands = []
                    for sub_name, sub_config in cmd_config.subcommands.items():
                        subcommands.append(sub_name)
                        subcommands.extend(sub_config.get("aliases", []))

                    for subcmd in subcommands:
                        if subcmd.startswith(word):
                            yield Completion(
                                subcmd, start_position=-len(word), display=subcmd
                            )
                    return

        # Main commands - only show when we don't have any parts yet or just one partial word
        if len(parts) <= 1:
            all_commands = {**self.base_commands}
            for cmd_name, cmd_config in COMMANDS.items():
                all_commands[cmd_name] = f"{cmd_name.title()} commands"
                for alias in cmd_config.aliases:
                    all_commands[alias] = f"{cmd_name.title()} commands"

            for cmd, desc in all_commands.items():
                if cmd.startswith(word):
                    yield Completion(
                        cmd, start_position=-len(word), display=f"{cmd} - {desc}"
                    )


class MCPSession:
    """Interactive MCP session manager."""

    def __init__(
        self,
        cmd_or_url: str,
        metadata: dict[str, str] | None = None,
        force_sse: bool = False,
        output_config: OutputConfig | None = None,
        debug_mode: bool = False,
    ):
        self.cmd_or_url = cmd_or_url
        self.metadata = metadata or {}
        self.force_sse = force_sse  # Force SSE instead of Streamable HTTP
        self.debug_mode = debug_mode  # Debug mode flag
        self.session: ClientSession | None = None
        self.client = None
        self.initialized = False
        self.server_info = None
        self.clean_output = False
        self.session_id_callback = None  # For Streamable HTTP
        self.output_config = output_config
        self.output_formatter = (
            get_output_formatter(output_config) if output_config else None
        )
        self._completion_cache = {}

    async def connect(self) -> None:
        """Initialize connection to MCP server."""
        # Determine which console to use for status messages
        status_console = console_err if self.clean_output else console

        try:
            if self.cmd_or_url.startswith(("http://", "https://")):
                # HTTP transport - try Streamable HTTP first, fallback to SSE
                url = self.cmd_or_url
                headers = self.metadata or None

                if self.force_sse:
                    if not (self.output_config and self.output_config.quiet):
                        status_console.print(
                            "[cyan]→ Using SSE transport (forced)[/cyan]"
                        )
                    await self._connect_sse(url, headers)
                else:
                    try:
                        if not (self.output_config and self.output_config.quiet):
                            status_console.print(
                                "[cyan]→ Attempting Streamable HTTP transport...[/cyan]"
                            )
                        await self._connect_streamable_http(url, headers)
                    except Exception as e:
                        if not (self.output_config and self.output_config.quiet):
                            status_console.print(
                                f"[yellow]→ Streamable HTTP failed ({e}), falling back to SSE...[/yellow]"
                            )
                        await self._connect_sse(url, headers)
            else:
                # STDIO transport
                await self._connect_stdio()

            # Initialize session
            if not (self.output_config and self.output_config.quiet):
                status_console.print("[cyan]→ Initializing MCP session...[/cyan]")
            init_result = await self.session.initialize()
            self.server_info = init_result
            self.initialized = True

            if not self.clean_output:
                status_console.print("[green]✓ Connected to MCP server[/green]")

            # Show server info automatically - handle different object types safely
            if self.server_info and not self.clean_output:
                try:
                    # Try different ways to access server info
                    server_info = None
                    protocol_version = None

                    if hasattr(self.server_info, "serverInfo"):
                        server_info = self.server_info.serverInfo
                    elif hasattr(self.server_info, "server_info"):
                        server_info = self.server_info.server_info
                    elif (
                        isinstance(self.server_info, dict)
                        and "serverInfo" in self.server_info
                    ):
                        server_info = self.server_info["serverInfo"]

                    if hasattr(self.server_info, "protocolVersion"):
                        protocol_version = self.server_info.protocolVersion
                    elif hasattr(self.server_info, "protocol_version"):
                        protocol_version = self.server_info.protocol_version
                    elif (
                        isinstance(self.server_info, dict)
                        and "protocolVersion" in self.server_info
                    ):
                        protocol_version = self.server_info["protocolVersion"]

                    if server_info:
                        server_name = "Unknown"
                        server_version = "Unknown"

                        if isinstance(server_info, dict):
                            server_name = server_info.get("name", "Unknown")
                            server_version = server_info.get("version", "Unknown")
                        elif hasattr(server_info, "name"):
                            server_name = server_info.name
                            server_version = getattr(server_info, "version", "Unknown")

                        # Show session ID if using Streamable HTTP
                        session_info = ""
                        if self.session_id_callback:
                            session_id = self.session_id_callback()
                            if session_id:
                                session_info = f" (Session: {session_id[:8]}...)"

                        status_console.print(
                            f"[dim]Server: {server_name} v{server_version} (Protocol: {protocol_version or 'Unknown'}){session_info}[/dim]"
                        )
                except Exception:
                    # If we can't parse server info, just continue silently
                    pass

        except Exception as e:
            status_console.print(f"[red]✗ Failed to connect: {e}[/red]")
            raise

    async def _connect_streamable_http(
        self, url: str, headers: dict[str, str] | None = None
    ) -> None:
        """Connect using Streamable HTTP transport."""
        # Determine which console to use for status messages
        status_console = console_err if self.clean_output else console

        # Streamable HTTP typically uses a /mcp endpoint (FastMCP default)
        # but can also be /message or other paths depending on implementation
        streamable_paths = ["/mcp", "/message", "/messages"]

        if not any(url.endswith(path) for path in streamable_paths):
            # Try /mcp first (FastMCP default), then fallback to /message
            if url.endswith("/"):
                url = url + "mcp"
            else:
                url = url + "/mcp"
            if not self.clean_output:
                status_console.print(
                    f"[cyan]→ Auto-detecting Streamable HTTP endpoint: {url}[/cyan]"
                )

        self.client = streamablehttp_client(url=url, headers=headers)
        read, write, session_id_callback = await self.client.__aenter__()
        self.session = ClientSession(read, write)
        self.session_id_callback = session_id_callback
        await self.session.__aenter__()

    async def _connect_sse(
        self, url: str, headers: dict[str, str] | None = None
    ) -> None:
        """Connect using SSE transport."""
        # Determine which console to use for status messages
        status_console = console_err if self.clean_output else console

        # SSE transport - Auto-handle endpoint detection like the blog post describes
        if not url.endswith("/sse"):
            url = urljoin(url, "/sse")
            if not (self.output_config and self.output_config.quiet):
                status_console.print(
                    f"[cyan]→ Auto-detecting SSE endpoint: {url}[/cyan]"
                )

        self.client = sse_client(url=url, headers=headers)
        read, write = await self.client.__aenter__()
        self.session = ClientSession(read, write)
        await self.session.__aenter__()

    async def _connect_stdio(self) -> None:
        """Connect using STDIO transport."""
        elements = shlex.split(self.cmd_or_url)
        if not elements:
            raise ValueError("stdio command is empty")

        command, args = elements[0], elements[1:]

        # Prepare environment with logging suppression
        env = self.metadata.copy() if self.metadata else {}

        # Set common environment variables to suppress server logs
        # These are commonly used by Python logging frameworks
        env.setdefault("PYTHONUNBUFFERED", "1")  # Ensure output is not buffered

        # If not in debug mode, try to suppress server logging
        if not (hasattr(self, "debug_mode") and self.debug_mode):
            # Common environment variables to suppress logs
            env.setdefault("LOG_LEVEL", "ERROR")
            env.setdefault("LOGLEVEL", "ERROR")
            env.setdefault("PYTHON_LOG_LEVEL", "ERROR")
            env.setdefault("MCP_LOG_LEVEL", "ERROR")
            env.setdefault("FASTMCP_LOG_LEVEL", "ERROR")
            # Suppress FastAPI/Uvicorn logs specifically
            env.setdefault("UVICORN_LOG_LEVEL", "error")
            env.setdefault("UVICORN_ACCESS_LOG", "0")

        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env,
        )
        self.client = stdio_client(server_params)
        read, write = await self.client.__aenter__()
        self.session = ClientSession(read, write)
        await self.session.__aenter__()

    async def disconnect(self) -> None:
        """Close the MCP session."""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.client:
            await self.client.__aexit__(None, None, None)
        self.initialized = False

    async def execute_command(
        self, cmd_type: str, subcmd: str, *args, **kwargs
    ) -> Result:
        """Execute a command of the given type."""
        if not self.initialized:
            raise RuntimeError("Session not initialized")

        if cmd_type == "resources":
            if subcmd in ["list", "ls"]:
                return await self.session.list_resources()
            elif subcmd == "read":
                return await self.session.read_resource(*args, **kwargs)
            elif subcmd == "templates":
                return await self.session.list_resource_templates()

        elif cmd_type == "prompts":
            if subcmd in ["list", "ls"]:
                return await self.session.list_prompts()
            elif subcmd == "get":
                return await self.session.get_prompt(*args, **kwargs)

        elif cmd_type == "tools":
            if subcmd in ["list", "ls"]:
                return await self.session.list_tools()
            elif subcmd == "call":
                return await self.session.call_tool(*args, **kwargs)

        elif cmd_type == "server":
            if subcmd == "ping":
                # MCP ping functionality from the blog post
                return await self.session.ping()

        raise ValueError(f"Unknown command: {cmd_type} {subcmd}")

    async def get_tool_schema(self, tool_name: str) -> dict[str, object] | None:
        """Get the input schema for a tool."""
        try:
            result = await self.execute_command("tools", "list")
            if result and hasattr(result, "tools"):
                for tool in result.tools:
                    if tool.name == tool_name:
                        return tool.inputSchema
        except:  # noqa: E722
            pass
        return None

    async def get_tool_info(self, tool_name: str) -> dict[str, object] | None:
        """Get detailed information about a tool."""
        try:
            result = await self.execute_command("tools", "list")
            if result and hasattr(result, "tools"):
                for tool in result.tools:
                    if tool.name == tool_name:
                        return {
                            "name": tool.name,
                            "description": getattr(tool, "description", ""),
                            "inputSchema": getattr(tool, "inputSchema", {}),
                        }
        except:  # noqa: E722
            pass
        return None

    async def get_prompt_schema(
        self, prompt_name: str
    ) -> list[dict[str, object]] | None:
        """Get the arguments schema for a prompt."""
        try:
            result = await self.execute_command("prompts", "list")
            if result and hasattr(result, "prompts"):
                for prompt in result.prompts:
                    if prompt.name == prompt_name:
                        return prompt.arguments or []
        except:  # noqa: E722
            pass
        return None

    async def get_prompt_info(self, prompt_name: str) -> dict[str, object] | None:
        """Get detailed information about a prompt."""
        try:
            result = await self.execute_command("prompts", "list")
            if result and hasattr(result, "prompts"):
                for prompt in result.prompts:
                    if prompt.name == prompt_name:
                        return {
                            "name": prompt.name,
                            "description": getattr(prompt, "description", ""),
                            "arguments": getattr(prompt, "arguments", []),
                        }
        except:  # noqa: E722
            pass
        return None

    async def get_resource_info(self, resource_uri: str) -> dict[str, object] | None:
        """Get detailed information about a resource."""
        try:
            result = await self.execute_command("resources", "list")
            if result and hasattr(result, "resources"):
                for resource in result.resources:
                    if str(resource.uri) == resource_uri:
                        return {
                            "uri": str(resource.uri),
                            "name": getattr(resource, "name", ""),
                            "description": getattr(resource, "description", ""),
                            "mimeType": getattr(resource, "mimeType", ""),
                        }
        except:  # noqa: E722
            pass
        return None


def print_result_structured(
    result: Result, session: MCPSession, title: str = "Result"
) -> None:
    """Print result using the configured output formatter."""
    if not result:
        return

    # Use the output formatter if available
    if session.output_formatter:
        formatted_output = session.output_formatter.format_result(result, title)
        session.output_formatter.write(formatted_output)
        if formatted_output and not formatted_output.endswith("\n"):
            session.output_formatter.write("\n")
    elif session.clean_output:
        # Fallback to old clean output behavior
        try:
            result_dict = result.model_dump(exclude_defaults=True)

            # For tool calls, extract structuredContent if available
            if "content" in result_dict and isinstance(result_dict["content"], list):
                # Check for structuredContent first
                if "structuredContent" in result_dict:
                    structured_content = result_dict["structuredContent"]
                    if (
                        isinstance(structured_content, dict)
                        and "result" in structured_content
                    ):
                        # Output just the result value
                        print(json.dumps(structured_content["result"]))
                    else:
                        # Output the entire structuredContent
                        print(json.dumps(structured_content, indent=2))
                    return

                # Fall back to extracting text content
                content_items = result_dict["content"]
                if len(content_items) == 1 and content_items[0].get("type") == "text":
                    # Single text response - output just the text
                    print(content_items[0]["text"])
                    return

            # For resources, extract the actual content
            if "contents" in result_dict:
                contents = result_dict["contents"]
                if isinstance(contents, list) and len(contents) == 1:
                    content = contents[0]
                    if "text" in content:
                        print(content["text"])
                        return
                    elif "blob" in content:
                        print(content["blob"])
                        return

            # For lists (tools, prompts, resources), extract the core array
            for key in ["tools", "prompts", "resources", "templates"]:
                if key in result_dict:
                    print(json.dumps(result_dict[key], indent=2))
                    return

            # Default: output the full result without MCP wrapper
            print(json.dumps(result_dict, indent=2))

        except Exception:
            # Fallback to normal output if structured extraction fails
            print_result(result, title)
    else:
        # Normal pretty output
        print_result(result, title)


def print_result(result: Result, title: str = "Result") -> None:
    """Pretty print MCP result."""
    if not result:
        console.print(f"[yellow]No {title.lower()} available[/yellow]")
        return

    # Convert to JSON for pretty printing
    json_str = result.model_dump_json(indent=2, exclude_defaults=True)
    syntax = Syntax(json_str, "json", theme="monokai")

    panel = Panel(syntax, title=title, border_style="blue")
    console.print(panel)


def print_table(
    data: list[object],
    title: str,
    columns: list[str],
    session: "MCPSession | None" = None,
) -> None:
    """Print data in a table format using the configured output formatter."""
    if not data:
        if session and session.output_formatter:
            formatted_output = session.output_formatter.format_list([], title, columns)
            session.output_formatter.write(formatted_output)
            if formatted_output and not formatted_output.endswith("\n"):
                session.output_formatter.write("\n")
        else:
            console.print(f"[yellow]No {title.lower()} available[/yellow]")
        return

    # Use the output formatter if available
    if session and session.output_formatter:
        formatted_output = session.output_formatter.format_list(data, title, columns)
        session.output_formatter.write(formatted_output)
        if formatted_output and not formatted_output.endswith("\n"):
            session.output_formatter.write("\n")
    else:
        # Fallback to rich table output
        table = Table(title=title, show_header=True, header_style="bold magenta")

        for col in columns:
            table.add_column(col)

        for item in data:
            row = []
            for col in columns:
                # Handle both dict access and attribute access
                if hasattr(item, col):
                    value = getattr(item, col)
                elif isinstance(item, dict) and col in item:
                    value = item[col]
                else:
                    value = ""

                # Convert complex objects to strings
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, indent=2)
                elif value is None:
                    value = ""

                row.append(str(value))
            table.add_row(*row)

        console.print(table)


def print_inspection(info: dict[str, object], title: str) -> None:
    """Print detailed inspection information."""
    table = Table(title=f"{title} Details", show_header=True, header_style="bold cyan")
    table.add_column("Property", style="bold")
    table.add_column("Value")

    for key, value in info.items():
        if isinstance(value, (dict, list)):
            # Pretty print complex objects
            json_str = json.dumps(value, indent=2)
            syntax = Syntax(json_str, "json", theme="monokai")
            table.add_row(key, syntax)
        else:
            table.add_row(key, str(value) if value else "")

    console.print(table)


def parse_arguments_smart(
    arg_str: str, schema: dict[str, object] | None = None
) -> dict[str, object]:
    """Parse arguments with smart inference for simple cases."""
    if not arg_str.strip():
        return {}

    # Try to parse as JSON first
    try:
        return json.loads(arg_str)
    except json.JSONDecodeError:
        pass

    # If we have schema information, try to infer argument order
    if schema and "properties" in schema:
        properties = schema["properties"]
        required = schema.get("required", [])

        # For simple cases with space-separated values, map to required parameters in order
        parts = arg_str.split()
        if len(parts) <= len(required):
            result = {}
            for i, part in enumerate(parts):
                if i < len(required):
                    param_name = required[i]
                    param_schema = properties.get(param_name, {})

                    # Try to convert based on type
                    param_type = param_schema.get("type", "string")
                    if param_type == "integer":
                        try:
                            result[param_name] = int(part)
                        except ValueError:
                            result[param_name] = part
                    elif param_type == "number":
                        try:
                            result[param_name] = float(part)
                        except ValueError:
                            result[param_name] = part
                    elif param_type == "boolean":
                        result[param_name] = part.lower() in ["true", "1", "yes", "on"]
                    else:
                        result[param_name] = part
            return result

    # Fall back to simple key=value parsing
    args = {}
    for pair in arg_str.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            args[key.strip()] = value.strip()
    return args


async def prompt_for_arguments(
    session: MCPSession, cmd_type: str, name: str
) -> dict[str, object]:
    """Interactively prompt for required arguments."""
    arguments = {}

    if cmd_type == "tools":
        schema = await session.get_tool_schema(name)
        if schema and "properties" in schema:
            required = schema.get("required", [])
            properties = schema["properties"]

            console.print(
                f"[cyan]Tool '{name}' requires arguments. Please provide:[/cyan]"
            )

            for param_name in required:
                param_info = properties.get(param_name, {})
                param_type = param_info.get("type", "string")
                description = param_info.get("description", "")

                prompt_text = f"  {param_name}"
                if param_type != "string":
                    prompt_text += f" ({param_type})"
                if description:
                    prompt_text += f" - {description}"
                prompt_text += ": "

                value = input(prompt_text)

                # Convert based on type
                if param_type == "integer":
                    try:
                        arguments[param_name] = int(value)
                    except ValueError:
                        arguments[param_name] = value
                elif param_type == "number":
                    try:
                        arguments[param_name] = float(value)
                    except ValueError:
                        arguments[param_name] = value
                elif param_type == "boolean":
                    arguments[param_name] = value.lower() in ["true", "1", "yes", "on"]
                else:
                    arguments[param_name] = value

    elif cmd_type == "prompts":
        prompt_args = await session.get_prompt_schema(name)
        if prompt_args:
            console.print(
                f"[cyan]Prompt '{name}' requires arguments. Please provide:[/cyan]"
            )

            for arg_info in prompt_args:
                arg_name = arg_info.get("name", "")
                description = arg_info.get("description", "")
                required = arg_info.get("required", False)

                if required:
                    prompt_text = f"  {arg_name}"
                    if description:
                        prompt_text += f" - {description}"
                    prompt_text += ": "

                    value = input(prompt_text)
                    arguments[arg_name] = value

    return arguments


async def discover_all(mcp_session: MCPSession) -> None:
    """Show a comprehensive overview of all available resources, tools, and prompts."""
    console.print(
        Panel.fit(
            "[bold cyan]🔍 Discovering MCP Server Capabilities[/bold cyan]",
            border_style="cyan",
        )
    )

    # Initialize completion cache
    if not hasattr(mcp_session, "_completion_cache"):
        mcp_session._completion_cache = {}

    # Resources
    try:
        result = await mcp_session.execute_command("resources", "list")
        if result and hasattr(result, "resources") and result.resources:
            # Cache for completion
            mcp_session._completion_cache["resources"] = [
                str(resource.uri) for resource in result.resources
            ]
            print_table(
                result.resources,
                "📁 Available Resources",
                ["uri", "name", "description"],
                mcp_session,
            )
            console.print("[dim]💡 Try: r read <uri> or r inspect <uri>[/dim]\n")
        else:
            mcp_session._completion_cache["resources"] = []
            console.print("[yellow]📁 No resources available[/yellow]\n")
    except Exception as e:
        mcp_session._completion_cache["resources"] = []
        print_error(f"📁 Error listing resources: {e}", mcp_session)

    # Tools
    try:
        result = await mcp_session.execute_command("tools", "list")
        if result and hasattr(result, "tools") and result.tools:
            # Cache for completion
            mcp_session._completion_cache["tools"] = [
                tool.name for tool in result.tools
            ]
            print_table(
                result.tools, "🔧 Available Tools", ["name", "description"], mcp_session
            )
            console.print(
                "[dim]💡 Try: t call <name> [args] or t inspect <name>[/dim]\n"
            )
        else:
            mcp_session._completion_cache["tools"] = []
            console.print("[yellow]🔧 No tools available[/yellow]\n")
    except Exception as e:
        mcp_session._completion_cache["tools"] = []
        print_error(f"🔧 Error listing tools: {e}", mcp_session)

    # Prompts
    try:
        result = await mcp_session.execute_command("prompts", "list")
        if result and hasattr(result, "prompts") and result.prompts:
            # Cache for completion
            mcp_session._completion_cache["prompts"] = [
                prompt.name for prompt in result.prompts
            ]
            print_table(
                result.prompts,
                "💬 Available Prompts",
                ["name", "description"],
                mcp_session,
            )
            console.print(
                "[dim]💡 Try: p get <name> [args] or p inspect <name>[/dim]\n"
            )
        else:
            mcp_session._completion_cache["prompts"] = []
            console.print("[yellow]💬 No prompts available[/yellow]\n")
    except Exception as e:
        mcp_session._completion_cache["prompts"] = []
        print_error(f"💬 Error listing prompts: {e}", mcp_session)


def show_help() -> None:
    """Show help information."""
    help_text = """
[bold cyan]MCP Interactive Client - Easy MCP Server Interaction[/bold cyan]

[bold]Discovery Commands:[/bold]
  discover             - Show all available resources, tools, and prompts
  ls                   - List resources (quick access)

[bold]Resource Commands:[/bold]
  r list (or r ls)     - List resources  
  r read <uri>         - Read a resource
  r inspect <uri>      - Show detailed resource information
  r templates          - List resource templates

[bold]Tool Commands:[/bold]
  t list (or t ls)     - List tools
  t call <name> [args] - Call a tool
  t inspect <name>     - Show detailed tool information and schema

[bold]Prompt Commands:[/bold]
  p list (or p ls)     - List prompts
  p get <name> [args]  - Get a prompt
  p inspect <name>     - Show detailed prompt information and schema

[bold]Server Commands:[/bold]
  s info               - Show server information
  s ping               - Ping the server (test connection)
  s capabilities       - Show server capabilities

[bold]Other Commands:[/bold]
  help                 - Show this help
  clear                - Clear screen
  quit/exit            - Exit the REPL

[bold]Arguments:[/bold]
  JSON format:         '{"key": "value", "num": 42}'
  Simple format:       value1 value2 (auto-mapped to required params)
  Key=value:           key1=value1,key2=value2
  Interactive:         Leave empty to be prompted for required args

[bold]Pain-Free Features:[/bold]
  ✓ Auto-detects Streamable HTTP (/message) and SSE (/sse) endpoints
  ✓ Manages sessions automatically
  ✓ Tab completion for tool/prompt/resource names
  ✓ Smart argument parsing and type conversion
  ✓ Interactive prompting for required parameters
  ✓ Detailed inspection of schemas and metadata
  ✓ One-command discovery of all capabilities

[bold]Examples:[/bold]
  discover                                 # See everything available
  ls                                       # Quick resource list
  r read config://app                      # Read a resource
  t inspect calculator                     # See tool schema before using
  t call add 5 3                          # Smart inference
  t call add '{"a": 5, "b": 3}'           # JSON format
  t call add                              # Interactive prompting
  s ping                                  # Test connection
"""
    console.print(Panel(help_text, title="Help", border_style="green"))


async def handle_command(mcp_session: MCPSession, cmd: str, parts: list[str]) -> None:
    """Handle a command using the abstracted command system."""

    # Handle special commands
    if cmd == "discover":
        await discover_all(mcp_session)
        return

    # Handle standalone ls command
    if cmd == "ls":
        result = await mcp_session.execute_command("resources", "list")
        if result and hasattr(result, "resources"):
            print_table(
                result.resources,
                "Resources",
                ["uri", "name", "description"],
                mcp_session,
            )
        else:
            print_result_structured(result, mcp_session, "Resources")
        return

    # Find matching command configuration
    cmd_config = None
    cmd_type = None

    for cmd_name, config in COMMANDS.items():
        if cmd in [cmd_name] + config.aliases:
            cmd_config = config
            cmd_type = cmd_name
            break

    if not cmd_config:
        console.print(
            f"[red]Error: Unknown command '{cmd}'. Type 'help' for available commands.[/red]"
        )
        return

    if len(parts) < 2:
        console.print(
            f"[red]Error: Missing subcommand. Use '{cmd} list', '{cmd} read', etc.[/red]"
        )
        return

    subcmd = parts[1].lower()

    # Find matching subcommand
    subcmd_config = None
    subcmd_name = None

    for sub_name, sub_config in cmd_config.subcommands.items():
        if subcmd in [sub_name] + sub_config.get("aliases", []):
            subcmd_config = sub_config
            subcmd_name = sub_name
            break

    if not subcmd_config:
        available = []
        for sub_name, sub_config in cmd_config.subcommands.items():
            aliases = sub_config.get("aliases", [])
            if aliases:
                available.append(f"{sub_name} (or {', '.join(aliases)})")
            else:
                available.append(sub_name)
        console.print(
            f"[red]Error: Unknown subcommand '{subcmd}'. Available: {', '.join(available)}[/red]"
        )
        return

    # Handle subcommands that require arguments
    if subcmd_config.get("requires_arg") and len(parts) < 3:
        if subcmd_name == "read":
            console.print(f"[red]Error: Missing URI. Usage: {cmd} read <uri>[/red]")
        elif subcmd_name == "inspect":
            if cmd_type == "tools":
                console.print(
                    f"[red]Error: Missing tool name. Usage: {cmd} inspect <name>[/red]"
                )
            elif cmd_type == "prompts":
                console.print(
                    f"[red]Error: Missing prompt name. Usage: {cmd} inspect <name>[/red]"
                )
            elif cmd_type == "resources":
                console.print(
                    f"[red]Error: Missing resource URI. Usage: {cmd} inspect <uri>[/red]"
                )
        elif subcmd_name in ["get", "call"]:
            console.print(
                f"[red]Error: Missing name. Usage: {cmd} {subcmd_name} <name> [args][/red]"
            )
        return

    # At this point, cmd_type and subcmd_name are guaranteed to be non-None
    assert cmd_type is not None and subcmd_name is not None

    # Execute the command
    try:
        if subcmd_name in ["list", "templates"]:
            result = await mcp_session.execute_command(cmd_type, subcmd_name)

            # Display results based on command type
            if cmd_type == "resources":
                if subcmd_name == "list" and result and hasattr(result, "resources"):
                    print_table(
                        result.resources,
                        "Resources",
                        ["uri", "name", "description"],
                        mcp_session,
                    )
                elif (
                    subcmd_name == "templates"
                    and result
                    and hasattr(result, "templates")
                ):
                    print_table(
                        result.templates,
                        "Resource Templates",
                        ["uri", "name", "description"],
                        mcp_session,
                    )
                else:
                    print_result_structured(result, mcp_session, cmd_type.title())
            elif cmd_type == "prompts":
                if result and hasattr(result, "prompts"):
                    print_table(
                        result.prompts, "Prompts", ["name", "description"], mcp_session
                    )
                else:
                    print_result_structured(result, mcp_session, "Prompts")
            elif cmd_type == "tools":
                if result and hasattr(result, "tools"):
                    print_table(
                        result.tools, "Tools", ["name", "description"], mcp_session
                    )
                else:
                    print_result_structured(result, mcp_session, "Tools")

        elif subcmd_name == "info":
            if cmd_type == "server":
                if mcp_session.server_info:
                    print_result(mcp_session.server_info, "Server Information")
                else:
                    console.print("[yellow]No server information available[/yellow]")

        elif subcmd_name == "ping":
            if cmd_type == "server":
                try:
                    result = await mcp_session.execute_command(cmd_type, subcmd_name)
                    console.print("[green]✓ Server is alive and responding[/green]")
                    if result:
                        print_result(result, "Ping Result")
                except Exception as e:
                    console.print(f"[red]✗ Ping failed: {e}[/red]")

        elif subcmd_name in ["capabilities", "caps"]:
            if cmd_type == "server" and mcp_session.server_info:
                try:
                    capabilities = None

                    # Try different ways to access capabilities
                    if hasattr(mcp_session.server_info, "capabilities"):
                        capabilities = mcp_session.server_info.capabilities
                    elif (
                        isinstance(mcp_session.server_info, dict)
                        and "capabilities" in mcp_session.server_info
                    ):
                        capabilities = mcp_session.server_info["capabilities"]

                    if capabilities:
                        # Convert capabilities to JSON for pretty printing
                        if hasattr(capabilities, "model_dump"):
                            # Pydantic model
                            json_str = capabilities.model_dump_json(
                                indent=2, exclude_defaults=True
                            )
                        else:
                            # dict or other object
                            json_str = json.dumps(capabilities, indent=2, default=str)

                        syntax = Syntax(json_str, "json", theme="monokai")
                        panel = Panel(
                            syntax, title="Server Capabilities", border_style="blue"
                        )
                        console.print(panel)
                    else:
                        console.print(
                            "[yellow]No capabilities information available[/yellow]"
                        )
                except Exception as e:
                    console.print(
                        f"[yellow]Could not retrieve capabilities: {e}[/yellow]"
                    )
            else:
                console.print("[yellow]No server information available[/yellow]")

        elif subcmd_name == "inspect":
            name_or_uri = parts[2]

            if cmd_type == "tools":
                info = await mcp_session.get_tool_info(name_or_uri)
                if info:
                    print_inspection(info, f"Tool: {name_or_uri}")
                else:
                    console.print(f"[red]Tool '{name_or_uri}' not found[/red]")
            elif cmd_type == "prompts":
                info = await mcp_session.get_prompt_info(name_or_uri)
                if info:
                    print_inspection(info, f"Prompt: {name_or_uri}")
                else:
                    console.print(f"[red]Prompt '{name_or_uri}' not found[/red]")
            elif cmd_type == "resources":
                info = await mcp_session.get_resource_info(name_or_uri)
                if info:
                    print_inspection(info, f"Resource: {name_or_uri}")
                else:
                    console.print(f"[red]Resource '{name_or_uri}' not found[/red]")

        elif subcmd_name == "read":
            uri = parts[2]
            result = await mcp_session.execute_command(cmd_type, subcmd_name, uri=uri)
            if mcp_session.clean_output:
                print_result_structured(result, mcp_session)
            else:
                print_result(result, f"Resource: {uri}")

        elif subcmd_name in ["get", "call"]:
            name = parts[2]

            # Handle arguments with smart parsing and interactive prompting
            if len(parts) > 3:
                # Arguments provided
                arg_string = " ".join(parts[3:])

                # Get schema for smart parsing
                schema = None
                if subcmd_name == "call":
                    schema = await mcp_session.get_tool_schema(name)

                arguments = parse_arguments_smart(arg_string, schema)
            else:
                # No arguments provided - try interactive prompting
                arguments = await prompt_for_arguments(mcp_session, cmd_type, name)

            result = await mcp_session.execute_command(
                cmd_type, subcmd_name, name=name, arguments=arguments
            )

            # Use structured output for tool calls and prompt gets
            if mcp_session.clean_output:
                print_result_structured(result, mcp_session)
            else:
                print_result(result, f"{cmd_type.title()}: {name}")

    except Exception as e:
        console.print(f"[red]Error executing {cmd_type} {subcmd_name}: {e}[/red]")


async def run_repl(mcp_session: MCPSession) -> None:
    """Run the interactive REPL."""
    # Setup prompt session
    session = PromptSession(
        completer=MCPCompleter(mcp_session),
        history=FileHistory(".mcp_history"),
        lexer=PygmentsLexer(JsonLexer),
        style=Style.from_dict(
            {
                "prompt": "ansicyan bold",
            }
        ),
    )

    console.print(
        Panel.fit(
            "[bold green]🚀 MCP Interactive Client[/bold green]\n"
            "Making MCP servers easy to use!\n"
            "[dim]Type 'discover' to see what's available, 'help' for commands, 'quit' to exit[/dim]",
            border_style="blue",
        )
    )

    # Auto-discover capabilities on startup
    try:
        await discover_all(mcp_session)
    except Exception as e:
        console.print(f"[yellow]Could not auto-discover capabilities: {e}[/yellow]")

    while True:
        try:
            # Get command
            command = await session.prompt_async("mcp> ")
            command = command.strip()

            if not command:
                continue

            # Parse command
            parts = command.split()
            cmd = parts[0].lower()

            # Handle utility commands
            if cmd in ["quit", "exit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            elif cmd == "help":
                show_help()

            elif cmd == "clear":
                console.clear()

            else:
                # Handle MCP commands using the abstracted system
                await handle_command(mcp_session, cmd, parts)

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'quit' to exit[/yellow]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


@click.command()
@click.argument("cmd_or_url", required=True)
@click.option(
    "--env",
    "-e",
    multiple=True,
    help="Environment variables (key:value) for STDIO transport",
)
@click.option(
    "--header", "-H", multiple=True, help="HTTP headers (key:value) for HTTP transport"
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Use rich formatting and detailed output (default: clean output)",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress all non-essential output (no headers, progress, banners)",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "pretty", "table", "yaml", "raw"]),
    default="json",
    help="Output format (default: json in non-REPL mode, pretty in REPL mode)",
)
@click.option(
    "-f",
    "--output-file",
    type=click.Path(),
    help="Write output to a file instead of stdout",
)
@click.option(
    "--stdin",
    is_flag=True,
    help="Accept input from stdin (JSON or arguments)",
)
@click.option(
    "--force-sse",
    is_flag=True,
    help="Force SSE transport instead of Streamable HTTP for HTTP URLs",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging to stderr (shows detailed protocol messages)",
)
@click.argument("commands", nargs=-1, required=False)
def main(
    cmd_or_url: str,
    env: tuple[str],
    header: tuple[str],
    verbose: bool,
    quiet: bool,
    output: str,
    output_file: str,
    stdin: bool,
    force_sse: bool,
    debug: bool,
    commands: tuple[str],
):
    """Interactive MCP client with REPL interface and command-line execution.

    Eliminates the pain points of manual MCP interaction:
    • Auto-detects Streamable HTTP and SSE endpoints
    • Manages sessions automatically
    • Provides discovery and inspection tools
    • Smart argument parsing and completion
    • Interactive prompting for parameters

    INTERACTIVE MODE (always uses rich formatting):
      python main.py "http://localhost:5001"      # Streamable HTTP transport
      python main.py "python server.py"           # STDIO transport

    COMMAND-LINE MODE (clean output by default):
      python main.py "uv run server.py" -- tool call add 9 10
      python main.py "http://localhost:5001" -- discover
      python main.py "python server.py" -- tool list | jq '.tools[].name'
      echo "config://app" | python main.py "server.py" -- resource read

    TRANSPORT OPTIONS:
      HTTP URLs: Uses Streamable HTTP by default, falls back to SSE
      Use --force-sse to explicitly use SSE transport for HTTP URLs

    Use '--' to separate server command from MCP commands to execute.
    Use --verbose for rich formatting in command-line mode.
    """

    # Configure logging level based on flags
    if debug:
        # Debug mode: show all logs including from libraries
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("mcp").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    elif verbose and not commands:
        # Interactive verbose mode: show info logs
        logging.getLogger().setLevel(logging.INFO)
        logger.info("Verbose logging enabled")
    elif quiet:
        # Quiet mode: only show errors
        logging.getLogger().setLevel(logging.ERROR)
    # Otherwise keep the default WARNING level

    # Parse metadata
    metadata = {}
    for item in env + header:
        if ":" in item:
            key, value = item.split(":", 1)
            metadata[key] = value

    # Handle stdin input if requested
    stdin_input = None
    if stdin:
        if not sys.stdin.isatty():
            stdin_input = sys.stdin.read().strip()
            # If stdin is empty after stripping, treat it as no input
            if not stdin_input:
                exit_with_code(
                    EXIT_INVALID_INPUT,
                    "Error: --stdin flag requires input from stdin",
                    quiet,
                )
        else:
            exit_with_code(
                EXIT_INVALID_INPUT,
                "Error: --stdin flag requires input from stdin",
                quiet,
            )

    # Create output configuration
    # In interactive mode, default to pretty output unless specified
    # In command-line mode, use specified output format (default: json)
    actual_output_format = output
    if not commands and output == "json":
        actual_output_format = "pretty"  # Default to pretty in REPL mode

    output_config = OutputConfig(
        output_format=actual_output_format,
        quiet=quiet,
        verbose=verbose,
        output_file=output_file,
    )

    async def run():
        mcp_session = MCPSession(
            cmd_or_url,
            metadata,
            force_sse,
            output_config=output_config,
            debug_mode=debug,
        )
        # In interactive mode, always use rich output
        # In command-line mode, use clean output unless --verbose
        mcp_session.clean_output = not verbose and bool(commands)
        try:
            await mcp_session.connect()

            # Check if we have commands to execute (non-interactive mode)
            if commands:
                await run_commands(mcp_session, commands, stdin_input)
            else:
                # Interactive REPL mode (always verbose)
                mcp_session.clean_output = False
                await run_repl(mcp_session)
        finally:
            await mcp_session.disconnect()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        exit_with_code(EXIT_CLI_ERROR, "Interrupted by user", quiet)
    except json.JSONDecodeError as e:
        exit_with_code(EXIT_INVALID_INPUT, f"Invalid JSON input: {e}", quiet)
    except Exception as e:
        # Check if it's a server-related error
        if "server" in str(e).lower() or "mcp" in str(e).lower():
            exit_with_code(EXIT_SERVER_ERROR, f"Server error: {e}", quiet)
        else:
            exit_with_code(EXIT_CLI_ERROR, f"Fatal error: {e}", quiet)


async def run_commands(
    mcp_session: MCPSession, commands: tuple[str], stdin_input: str | None = None
) -> None:
    """Execute commands in non-interactive mode."""
    # Join all command arguments into a single command string
    command_string = " ".join(commands)

    # Handle stdin input
    if stdin_input:
        # Try to parse stdin as JSON first
        try:
            stdin_data = json.loads(stdin_input)
            # If it's a dict, it could be arguments for a command
            if isinstance(stdin_data, dict) and command_string:
                # For commands that accept arguments, use the JSON as arguments
                parts = command_string.split()
                if len(parts) >= 2 and parts[1] in ["call", "get"]:
                    # Convert dict to JSON string and append to command
                    command_string += f" '{json.dumps(stdin_data)}'"
                elif len(parts) >= 2 and parts[1] == "read":
                    # For read commands, extract the URI/name from the JSON
                    if isinstance(stdin_data, dict) and "uri" in stdin_data:
                        command_string += f" {stdin_data['uri']}"
                    elif isinstance(stdin_data, dict) and "name" in stdin_data:
                        command_string += f" {stdin_data['name']}"
            elif isinstance(stdin_data, dict) and not command_string:
                # If we have JSON input but no command, check if it contains URI/name for resource read
                if "uri" in stdin_data:
                    command_string = f"resource read {stdin_data['uri']}"
                elif "name" in stdin_data:
                    command_string = f"resource read {stdin_data['name']}"
                else:
                    # Generic JSON without URI/name, default to resource read with the whole JSON
                    command_string = f"resource read '{json.dumps(stdin_data)}'"
        except json.JSONDecodeError:
            # If not valid JSON, treat as plain text
            if stdin_input and not command_string:
                # If we have stdin input but no command, assume it's a resource URI to read
                command_string = f"resource read {stdin_input}"
            elif (
                stdin_input
                and "read" in command_string
                and len(command_string.split()) == 2
            ):
                # If command is like "resource read" and we have stdin, use stdin as the URI
                command_string += f" {stdin_input}"

    # Check if we should read from stdin (for backward compatibility)
    # Only do this if stdin_input was not explicitly provided (None vs empty string)
    elif stdin_input is None and not sys.stdin.isatty():
        stdin_input = sys.stdin.read().strip()
        if stdin_input and not command_string:
            # If we have stdin input but no command, assume it's a resource URI to read
            command_string = f"resource read {stdin_input}"
        elif (
            stdin_input
            and "read" in command_string
            and len(command_string.split()) == 2
        ):
            # If command is like "resource read" and we have stdin, use stdin as the URI
            command_string += f" {stdin_input}"

    # Parse the command
    parts = command_string.split()
    if not parts:
        # Instead of exiting, call handle_command with empty parts to let it handle the error
        await handle_command(mcp_session, "", [])
        return

    cmd = parts[0].lower()

    try:
        # Handle the command using the same logic as interactive mode
        if cmd in ["quit", "exit"]:
            return
        elif cmd == "help":
            show_help()
        elif cmd == "clear":
            # No-op in non-interactive mode
            pass
        else:
            # Handle MCP commands
            await handle_command(mcp_session, cmd, parts)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
