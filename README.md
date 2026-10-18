# DevDocs Hub

## MCP server

The project includes an MCP server that communicates over stdio. Install the
project dependencies with `uv sync`, configure the required values in `.env`
(see `.env_example`), then launch it with:

```sh
uv run devdocs-hub-mcp
```

When adding it to an MCP client, use the command `uv` with arguments `run`,
`--directory`, the absolute path to this project, and `devdocs-hub-mcp`.
