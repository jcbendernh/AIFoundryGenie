# AIFoundryGenie

AIFoundryGenie is a Python-based framework designed to facilitate the creation, management, and execution of AI agents that are connected to a Databricks Genie Space. 

## Overview 
User Input → Script → Azure AI Agent → Databricks Genie → Database Query → Results → Formatted Response → User

## Prerequisites
Before using AIFoundryGenie, ensure you have:

- **Python 3.8+** installed on your system
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) installed on your system.
- **Databricks workspace** with access to Genie Spaces.  <BR>For more information check out [Set up and manage an AI/BI Genie space](https://learn.microsoft.com/en-us/azure/databricks/genie/set-up)
- An Azure AI Foundry Project created.  <BR>For more information check out [Create a project for Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry&pivots=fdp-project).
- A Databricks Connected Resource created in the AI Foundry Project.  <BR>For more information check out [How to add a new connection in Azure AI Foundry portal](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/connections-add?pivots=fdp-project)
- **Required Python packages** (see [`src/requirements.txt`](src/requirements.txt))

### Databricks Setup
- Access to a Databricks workspace
- Genie Space configured with appropriate data sources
- Proper permissions to query data through Genie

## Summary
This repository includes:
- [`sample_agent_adb_genie.py`](src/sample_agent_adb_genie.py) - A sample AI agent that:
  - Connects to Databricks Genie through Azure AI Foundry
  - Creates an AI agent with access to Genie's data query capabilities
  - Implements a function tool (`ask_genie`) to query Databricks Genie spaces
  - Demonstrates end-to-end conversation flow with data-driven responses
  - Shows how to authenticate and establish connections between Azure AI Foundry and Databricks
- [`ask_agent.py`](src/ask_agent.py) - A command-line interface tool that:
  - Provides interactive chat with an existing Azure AI Foundry agent
  - Supports both single-question mode and continuous conversation mode
  - Automatically sets up Databricks Genie integration for data queries
  - Handles authentication and connection management transparently
  - Enables terminal-based agent interactions for testing and development

## Getting Started
I highly suggest forking this repo and then using Visual Studio Code with the [Azure AI Foundry extension](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/get-started-projects-vs-code) installed for the best development experience.

This repo based off of the Python scripts for [`Azure-Samples /
AI-Foundry-Connections`](https://github.com/Azure-Samples/AI-Foundry-Connections/tree/main)



