# mcp-server-aibtcdev: An aibtcdev MCP server

[![smithery badge](https://smithery.ai/badge/mcp-server-aibtcdev)](https://smithery.ai/protocol/mcp-server-aibtcdev)

> The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that enables
> seamless integration between LLM applications and external data sources and tools. Whether you're building an
> AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to
> connect LLMs with the context they need.

This repository is an example of how to create a MCP server for [aibtcdev](https://aibtc.dev/), a comprehensive platform for AI-powered Bitcoin and blockchain development.

## Overview

An official Model Context Protocol server for interacting with the aibtcdev-backend API. This server provides MCP tools for authentication, trading, DAO management, AI evaluation, social media integration, and more.

## Components

### Tools

#### Trading & Finance

1. `fund_wallet_testnet_stx`
   - Fund wallet with testnet STX tokens from faucet
   - Returns: Funding confirmation

2. `fund_wallet_testnet_sbtc`
   - Fund wallet with testnet sBTC tokens from Faktory faucet
   - Returns: Funding confirmation

#### DAO Management

3. `create_dao_action_proposal`
   - Create a DAO action proposal for sending a message
   - Input:
     - `agent_account_contract` (string): Contract principal of agent account
     - `action_proposals_voting_extension` (string): Contract principal for DAO action proposals
     - `action_proposal_contract_to_execute` (string): Contract principal of action proposal
     - `dao_token_contract_address` (string): Contract principal of DAO token
     - `message` (string): Message to send through DAO proposal system
     - `memo` (string, optional): Optional memo for the proposal
   - Returns: Proposal creation confirmation

4. `veto_dao_action_proposal`
   - Veto an existing DAO action proposal
   - Input:
     - `dao_action_proposal_voting_contract` (string): Contract principal for DAO action proposals
     - `proposal_id` (string): ID of proposal to veto
   - Returns: Veto confirmation

5. `generate_proposal_recommendation`
   - Generate AI-powered proposal recommendations for a DAO
   - Input:
     - `dao_id` (string): ID of the DAO
     - `focus_area` (string, optional): Specific area of focus
     - `specific_needs` (string, optional): Specific needs or requirements
     - `model_name` (string, optional): LLM model to use (default: "gpt-4.1")
     - `temperature` (number, optional): Temperature for LLM generation (default: 0.1)
   - Returns: AI-generated proposal recommendations

#### Agent Account Management

6. `approve_contract_for_agent_account`
   - Approve a contract for use with an agent account
   - Input:
     - `agent_account_contract` (string): Contract principal of agent account
     - `contract_to_approve` (string): Contract principal to approve
   - Returns: Contract approval confirmation

#### AI Evaluation

7. `run_comprehensive_evaluation`
   - Run comprehensive AI evaluation on a proposal
   - Input:
     - `proposal_id` (string): Unique identifier for the proposal
     - `proposal_content` (string, optional): Override proposal content
     - `dao_id` (string, optional): DAO ID for context
     - `custom_system_prompt` (string, optional): Custom system prompt
     - `custom_user_prompt` (string, optional): Custom user prompt
     - `config` (object, optional): Configuration for evaluation agent
   - Returns: Comprehensive evaluation results

## Environment Variables

The configuration of the server is done using environment variables:

| Name                            | Description                                    | Default Value             |
|---------------------------------|------------------------------------------------|---------------------------|
| `AIBTC_API_BASE_URL`           | Base URL for the aibtcdev API                 | `https://api.aibtc.dev`   |
| `AIBTC_BEARER_TOKEN`           | Bearer token for session-based authentication | None                      |
| `AIBTC_API_KEY`                | API key for long-lived authentication         | None                      |

### Authentication Methods

The server automatically uses authentication credentials from environment variables:

1. **Bearer Token**: Session-based authentication
   - Environment variable: `AIBTC_BEARER_TOKEN`
   - Format: `Authorization: Bearer <token>`
   - Use for web applications and temporary access

2. **API Key**: Long-lived authentication  
   - Environment variable: `AIBTC_API_KEY`
   - Format: `X-API-Key: <key>`
   - Use for programmatic access and bots

The server will automatically use the Bearer token if available, otherwise it will fall back to the API key.

> [!IMPORTANT]
> You must provide either `AIBTC_BEARER_TOKEN` or `AIBTC_API_KEY` for authentication.

## Installation

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd mcp-server-aibtcdev

# Install dependencies
pip install -e .
```

Or using uv:

```bash
uv sync
```

### Using Docker

A Dockerfile is available for building and running the MCP server:

```bash
# Build the container
docker build -t mcp-server-aibtcdev .

# Run the container
docker run -p 8000:8000 \
  -e AIBTC_API_KEY="your_api_key" \
  mcp-server-aibtcdev
```

### Installing via Smithery

To install aibtcdev MCP Server for Claude Desktop automatically via [Smithery](https://smithery.ai/protocol/mcp-server-aibtcdev):

```bash
npx @smithery/cli install mcp-server-aibtcdev --client claude
```

### Manual configuration of Claude Desktop

To use this server with the Claude Desktop app, add the following configuration to the "mcpServers" section of your `claude_desktop_config.json`:

```json
{
  "aibtcdev": {
    "command": "uvx",
    "args": ["aibtcdev-mcp-server"],
    "env": {
      "AIBTC_BEARER_TOKEN": "your_bearer_token",
      "AIBTC_API_KEY": "your_api_key"
    }
  }
}
```

## Contributing

If you have suggestions for how mcp-server-aibtcdev could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

### Testing mcp-server-aibtcdev locally

The [MCP inspector](https://github.com/modelcontextprotocol/inspector) is a developer tool for testing and debugging MCP servers. It runs both a client UI (default port 5173) and an MCP proxy server (default port 3000). Open the client UI in your browser to use the inspector.

```shell
AIBTC_BEARER_TOKEN="your_token" \
fastmcp dev src/mcp_server_aibtcdev/server.py
```

Once started, open your browser to http://localhost:5173 to access the inspector interface.

## License

This MCP server is licensed under the Apache License 2.0. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the Apache License 2.0. For more details, please see the LICENSE file in the project repository.
