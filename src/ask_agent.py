# Script to ask questions to an existing agent via terminal

import json
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from databricks.sdk import WorkspaceClient
from databricks_ai_bridge.genie import Genie
from azure.ai.agents.models import (FunctionTool, ToolSet)
from typing import Any, Callable, Set

# Configuration
os.environ["DATABRICKS_SDK_UPSTREAM"] = "AzureAIFoundry"
os.environ["DATABRICKS_SDK_UPSTREAM_VERSION"] = "1.0.0"

FOUNDRY_PROJECT_ENDPOINT = "<FOUNDRY PROJECT ENDPOINT>" # e.g., "https://<your-foundry-instance>.azure.ai/projects/<project-id>"
FOUNDRY_DATABRICKS_CONNECTION_NAME = "<FOUNDRY DATABRICKS CONNECTION NAME>"  # e.g., "my-databricks-connection"
AGENT_ID = "<FOUNDRY AGENT ID>" # The ID of the agent you want to interact with, e.g., "asst_ABCdefghijkl12345678910"
DATABRICKS_ENTRA_ID_AUDIENCE_SCOPE = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default"

# Global Genie instance for function calling
genie = None

def ask_genie(questions: str) -> str:
    """Ask Databricks Genie a question about NYC taxi data."""
    if genie is None:
        return json.dumps({"error": "Genie is not initialized"})
    
    try:
        response = genie.ask_question(questions)
        return json.dumps({
            "query": response.query,
            "result": response.result, 
            "description": response.description
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

def setup_genie_if_needed(project_client):
    """Setup Genie connection if the agent needs it."""
    global genie
    
    try:
        # Get the Databricks connection
        connection = project_client.connections.get(FOUNDRY_DATABRICKS_CONNECTION_NAME)
        genie_space_id = connection.metadata['genie_space_id']
        
        # Create Databricks workspace client
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        databricks_client = WorkspaceClient(
            host=connection.target,
            token=credential.get_token(DATABRICKS_ENTRA_ID_AUDIENCE_SCOPE).token,
        )
        
        # Initialize Genie
        genie = Genie(genie_space_id, client=databricks_client)
        
        # Create and enable toolset for function calling
        toolset = ToolSet()
        functions = FunctionTool(functions={ask_genie})
        toolset.add(functions)
        project_client.agents.enable_auto_function_calls(toolset)
        
        print("Genie functionality enabled for this session")
    except Exception as e:
        print(f"Could not enable Genie functionality: {e}")
        print("The agent will work without Genie functions")

def ask_agent_question(question: str):
    """Send a question to the agent and get the response."""
    
    # Initialize Azure credential and project client
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    project_client = AIProjectClient(FOUNDRY_PROJECT_ENDPOINT, credential)
    
    # Setup Genie if needed
    setup_genie_if_needed(project_client)
    
    with project_client:
        try:
            # Verify the agent exists
            agent = project_client.agents.get_agent(AGENT_ID)
            print(f"Connected to agent: {agent.name}")
            
            # Create a new thread for this conversation
            thread = project_client.agents.threads.create()
            
            # Send the user's question
            project_client.agents.messages.create(
                thread_id=thread.id,
                role="user",
                content=question
            )
            
            print(f"Question sent: {question}")
            print("Processing...")
            
            # Process the run
            run = project_client.agents.runs.create_and_process(
                thread_id=thread.id,
                agent_id=AGENT_ID
            )
            
            if run.status == "completed":
                print("Response received:")
                
                # Get the agent's response
                messages = project_client.agents.messages.list(thread_id=thread.id)
                for msg in messages:
                    if msg.role == "assistant":
                        if hasattr(msg.content[0], 'text'):
                            content = msg.content[0].text.value
                        else:
                            content = str(msg.content)
                        print(f"Agent: {content}")
                        break
            else:
                print(f"Run failed with status: {run.status}")
                
        except Exception as e:
            print(f"Error communicating with agent: {e}")

def interactive_mode():
    """Run in interactive mode where user can ask multiple questions."""
    print("=" * 60)
    print("Interactive Agent Chat")
    print("=" * 60)
    print(f"Connected to Agent ID: {AGENT_ID}")
    print("Type 'quit' or 'exit' to end the session")
    print("=" * 60)
    
    while True:
        try:
            question = input("\nYour question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not question:
                print("Please enter a question.")
                continue
                
            print("-" * 40)
            ask_agent_question(question)
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function - can be used for single question or interactive mode."""
    import sys
    
    if len(sys.argv) > 1:
        # Single question mode - question passed as command line argument
        question = " ".join(sys.argv[1:])
        print(f"Asking agent: {question}")
        print("-" * 40)
        ask_agent_question(question)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
