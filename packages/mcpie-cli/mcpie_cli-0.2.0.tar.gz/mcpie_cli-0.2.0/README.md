# mcpie 🥧 MCP Client for Humans

Command-line tool and REPL for MCP (Model Context Protocol) servers.

Like **httpie** for HTTP, but for MCP servers! 🥧

## Features

- Interactive REPL with tab completion and command history
- **Multiple output formats**: JSON, pretty JSON, table, YAML, raw
- **Pipe-friendly**: Clean stdout/stderr separation, stdin input, file output
- **Script-ready**: Proper exit codes, quiet mode, output redirection
- Short aliases: `ls`, `r list`, `t call add 5 3`, `p get name`
- Rich tables and syntax-highlighted JSON output
- Multiple transport support: STDIO, Streamable HTTP, and SSE (deprecated)
- Smart argument parsing (JSON, key=value, or interactive prompting)

## Installation

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) then:

```bash
uv sync
```

```bash
uv tool install .
```

From pypi:

```bash
uv tool install mcpie-cli
```

```bash
uvx mcpie-cli
```

## Quick Start

### Interactive Mode

```bash
# Start interactive client
mcpie "python server.py"           # STDIO transport
mcpie "http://localhost:8000"      # Streamable HTTP transport (with SSE fallback)

# Inside the REPL
mcp> discover                     # See everything available
mcp> ls                          # List resources
mcp> t call add 5 3              # Call tool with smart parsing
mcp> r read config://app         # Read resource
mcp> help                        # Show all commands
```

### Script-Friendly Usage

```bash
# Different output formats
mcpie "python server.py" t call add 5 3 --output json    # {"content": [{"type": "text", "text": "8"}]}
mcpie "python server.py" t call add 5 3 --output raw     # 8
mcpie "python server.py" t call add 5 3 --output pretty  # Indented JSON
mcpie "python server.py" t call add 5 3 --output table   # Tabular format
mcpie "python server.py" t call add 5 3 --output yaml    # YAML format

# Save output to file
mcpie "python server.py" t call add 5 3 -o result.json --output json

# Pipe-friendly (quiet mode)
mcpie "python server.py" t call add 5 3 --output raw --quiet | wc -l

# Read from stdin
echo '{"a": 5, "b": 3}' | mcpie "python server.py" t call add --stdin
echo "5 3" | mcpie "python server.py" t call add --stdin
```

## CLI Options

### Output Control

- `--output FORMAT`, `-f FORMAT` - Output format: `json`, `pretty`, `table`, `yaml`, `raw`
- `--output-file FILE`, `-o FILE` - Save output to file instead of stdout
- `--quiet`, `-q` - Suppress non-essential output (stderr messages)

### Input Control

- `--stdin` - Read command arguments from stdin (JSON or space-separated)

### Transport Options

- `-H "Key:Value"` - Add HTTP headers (for HTTP transport)
- `-e "KEY:value"` - Set environment variables
- `--force-sse` - Force SSE transport (if server doesn't support Streamable HTTP)

## Output Formats

### JSON (`--output json`)
Compact JSON output suitable for parsing:
```json
{"content": [{"type": "text", "text": "8"}], "structuredContent": {"result": 8}}
```

### Pretty JSON (`--output pretty`)
Indented JSON for human reading:
```json
{
  "content": [
    {
      "type": "text",
      "text": "8"
    }
  ],
  "structuredContent": {
    "result": 8
  }
}
```

### Table (`--output table`)
Tabular format for lists and structured data:
```
┌─────────┬───────────┐
│ Field   │ Value     │
├─────────┼───────────┤
│ result  │ 8         │
└─────────┴───────────┘
```

### YAML (`--output yaml`)
YAML format for configuration-like output:
```yaml
content:
  - type: text
    text: '8'
structuredContent:
  result: 8
```

### Raw (`--output raw`)
Extract just the essential result value:
```
8
```

## Exit Codes

mcpie uses proper exit codes for scripting:

- `0` - Success
- `1` - CLI error (invalid arguments, missing files, etc.)
- `2` - Server error (connection failed, server returned error)
- `3` - Invalid input (malformed JSON, invalid parameters)

## Commands

**Discovery:**
- `discover` - Show all capabilities
- `ls` - List resources (alias for `r list`)

**Resources:** `r list`, `r read <uri>`, `r templates`
 
**Tools:** `t list`, `t call <name> [args]`, `t inspect <name>`
 
**Prompts:** `p list`, `p get <name> [args]`, `p inspect <name>`
 
**Server:** `s info`, `s ping`, `s capabilities`

## Examples

### Interactive Usage

```bash
# Different argument formats
t call add 5 3                        # Auto-mapped to parameters
t call add '{"a": 5, "b": 3}'         # JSON format
t call add                             # Interactive prompting

# With headers/env vars for HTTP transport
mcpie -H "Authorization:token" http://localhost:8000
mcpie -e "API_KEY:secret" "python server.py"

# Force SSE transport (if server doesn't support Streamable HTTP)
mcpie --force-sse http://localhost:8000
```

### Scripting Examples

```bash
# Get raw result for use in scripts
RESULT=$(mcpie "python server.py" t call add 5 3 --output raw --quiet)
echo "The sum is: $RESULT"

# Save structured data to file
mcpie "python server.py" r read config://app --output yaml -o config.yaml

# Process multiple inputs
echo '{"a": 1, "b": 2}' | mcpie "python server.py" t call add --stdin --output raw
echo '{"a": 3, "b": 4}' | mcpie "python server.py" t call add --stdin --output raw

# Chain operations
mcpie "python server.py" t call add 5 3 --output raw | \
  xargs -I {} mcpie "python server.py" t call add {} 2 --output raw

# Error handling in scripts
if ! mcpie "python server.py" t call add 5 3 --quiet; then
  echo "Command failed with exit code: $?"
fi
```

### Pipe-Friendly Features

```bash
# Clean output suitable for piping
mcpie "python server.py" t call process_text "hello world" --output raw --quiet

# Read from stdin, output to file
echo '{"text": "hello", "operation": "uppercase"}' | \
  mcpie "python server.py" t call process_text --stdin --output json -o result.json

# Combine with other tools
mcpie "python server.py" r list --output json --quiet | jq '.[] | .name'
```

That's it! Type `help` in the REPL for more details.
