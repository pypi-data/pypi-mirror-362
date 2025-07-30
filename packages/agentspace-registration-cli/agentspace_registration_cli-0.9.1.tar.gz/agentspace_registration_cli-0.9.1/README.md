# Agentspace Registration CLI

A command-line interface for managing Google Cloud ADK Agents in Agentspace. This tool allows you to easily register, view, list, and delete your custom agents from your terminal.

## Overview

This script provides a convenient wrapper around the Google Discovery Engine API, simplifying the registration management of ADK agents within an Agentspace application. It was created because there is currently no `gcloud` CLI support for registering and managing agents in Agentspace. The tool handles authentication, request formatting, and provides clear feedback for all operations.

## Prerequisites

*   Python 3.9+
*   Google Cloud SDK installed and authenticated. Run `gcloud auth login` and `gcloud auth application-default login` to set up your credentials.

## Installation

There are two recommended ways to use this tool:

### 1. Via Pip (Recommended)

For easy, system-wide access, you can install this tool from PyPI:

```bash
pip install agentspace-registration-cli
```

*(Note: The package name on PyPI is `agentspace-registration-cli`, but the command to run it is `agentspace-reg`)*

### 2. Direct Download

Alternatively, you can download the script and run it directly:

```bash
curl -O https://raw.githubusercontent.com/0nri/agentspace-registration-cli/main/agentspace_registration_cli.py
chmod +x agentspace_registration_cli.py
```

## Usage

After installation via pip, the tool is available as `agentspace-reg`.

If you downloaded the script directly, you will invoke it with `python agentspace_registration_cli.py`. All examples below use the `agentspace-reg` command.

---

### Register an Agent

To register a new agent, you need to provide its configuration details.

**Example:**
```bash
agentspace-reg register \
  --project_id "your-gcp-project-id" \
  --app_id "your-agentspace-app-id" \
  --display_name "My Awesome Agent" \
  --description "This agent does awesome things." \
  --tool_description "An agent that can be used to do awesome things." \
  --adk_deployment_id "your-adk-deployment-id" \
  --icon_uri "https://example.com/icon.png"
```
Upon success, the script will print the full API response, including the **Agent ID**, which you should save for future operations.

---

### View an Agent

To view the details of a specific, existing agent.

**Example:**
```bash
agentspace-reg view \
  --project_id "your-gcp-project-id" \
  --app_id "your-agentspace-app-id" \
  --agent_id "the-id-of-the-agent-to-view"
```

---

### List All Agents

To list all agents currently registered within an Agentspace application.

**Example:**
```bash
agentspace-reg list \
  --project_id "your-gcp-project-id" \
  --app_id "your-agentspace-app-id"
```

---

### Update an Agent

To update an existing agent, you must provide all required fields, even if they are not being changed.

**Example:**
```bash
agentspace-reg update \
  --project_id "your-gcp-project-id" \
  --app_id "your-agentspace-app-id" \
  --agent_id "the-id-of-the-agent-to-update" \
  --display_name "My Updated Agent" \
  --description "This agent has updated awesome things." \
  --tool_description "An updated agent that can be used to do awesome things." \
  --adk_deployment_id "your-adk-deployment-id"
```

---

### Delete an Agent

To permanently delete an agent. **This action cannot be undone.**

**Example:**
```bash
agentspace-reg delete \
  --project_id "your-gcp-project-id" \
  --app_id "your-agentspace-app-id" \
  --agent_id "the-id-of-the-agent-to-delete"
```

## Command-Line Arguments

| Flag                | Description                                                                 | Required For                  |
| ------------------- | --------------------------------------------------------------------------- | ----------------------------- |
| `--project_id`      | The ID of your Google Cloud project.                                        | All actions                   |
| `--app_id`          | The ID of the Agentspace app.                                               | All actions                   |
| `--agent_id`        | The ID of the agent to view, update, or delete.                             | `view`, `update`, `delete`    |
| `--display_name`    | The display name of the agent.                                              | `register`, `update`          |
| `--description`     | The user-facing description of the agent.                                   | `register`, `update`          |
| `--tool_description`| The LLM-facing prompt that describes the agent's capabilities.              | `register`, `update`          |
| `--adk_deployment_id`| The ID of the reasoning engine where the ADK agent is deployed.             | `register`, `update`          |
| `--icon_uri`        | Optional: A public URI for the agent's icon.                                | `register`, `update`          |
| `--auth_ids`        | Optional: A comma-separated list of authorization resource IDs.             | `register`, `update`          |
