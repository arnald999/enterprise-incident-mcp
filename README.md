# Enterprise Incident MCP Server

A production-oriented MCP server that exposes incident-management resources, tools, and prompts to AI agents.

## MVP Capabilities

- List incidents
- Get incident by ID
- Search incidents
- Create incident
- Assign incident
- Update incident
- Create Jira ticket placeholder
- Create GitHub issue placeholder
- Incident triage, RCA, and postmortem prompts

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run

```bash
python -m enterprise_incident_mcp.server
```

## Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m enterprise_incident_mcp.server
```
