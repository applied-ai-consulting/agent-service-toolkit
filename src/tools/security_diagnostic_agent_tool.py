# Standard library imports
import json
import logging
import os
import re
import traceback
from typing import List, Dict, Any
import time
import uuid  # Add this import at the top of the file

# Third-party imports
from langchain_core.tools import BaseTool, tool
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_community.tools import ShellTool

from core.llm import call_llm
from agents.utils import validate_and_clean_json

from .logger import get_logger

logger = get_logger(__name__)
def security_diagnostic_agent_tool(user_input: str):
    """
    Your primary role is to analyze security reported problems, generate precise and actionable diagnostic scripts, and evaluate available data to determine the root cause.

    Args:
        user_input (str): The user's description of the security issue or event data from coordination agent.
        diagnostic_script (dict): A dictionary containing the diagnostic script generated for the reported issue.
        diagnostic_script_execution_output (list): A list of outputs from the execution of the diagnostic script.

    Returns:
        Json containing the generated diagnostic script and path location.
    """
    try:
        logger.info(f"Calling security diagnostic Agent....")

        prompt = f"""
        You are the Security Diagnostic Agent. Your role is to analyze reported security problems, generate a diagnostic bash script, and provide it in a structured JSON format.

### Instructions:
1. Generate a bash script tailored to the problem described. 
   - The script must only use **read-only commands** (no commands that modify the system).
   - Include an `echo` statement before each command to explain its purpose.
   - Start the script with a header that describes its purpose, e.g.:
     ```bash
     # Security Diagnostic Script for {user_input} on {user_input}
     ```
     Replace `{user_input}` with the problem description and `{user_input}` with the provided host name.

2. Prefix all commands with `sudo` to ensure they execute with appropriate privileges.
3. The script must include the following default commands:
   - `hostname`
   - Commands to collect relevant security diagnostics (e.g., `df -h`, `lsblk`, etc.).

4. Return the output as a JSON object in the following format:
   ```json
   {{
       "diagnostic_script": "{"the generated bash script"}",
       "path_location": "/path/to/save/script.sh",
       "is_root_cause_identified": "Yes"  # or "No" based on analysis
   }}
   """
     # Assuming `call_llm` will execute the prompt and return a response
        response = call_llm(prompt)  # This function needs to handle the LLM's response and parse it
        # Return the response after cleaning and validating the JSON format
        return validate_and_clean_json(response)


    except Exception as e:
        logger.error(f"Error in security issue identification: {str(e)}")
        return validate_and_clean_json("", default_value="error")

security_diagnostic_agent_tool: BaseTool = tool(security_diagnostic_agent_tool)
security_diagnostic_agent_tool.name = "SecurityDiagnostic"
