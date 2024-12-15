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
def guard_diagnostic_agent_tool(user_input: str):
    """Generates a diagnostic script for network infrastructure issues.
    
    Args:
        user_input: The user's description of the network issue or event data from coordination agent.
        
    Returns:
        Json containing the generated diagnostic script and path location.
    """
    try:
        logger.info(f"Calling guard diagnostic  Agent....")
        print("guard agent",user_input)
        prompt = f"""
            Your primary responsibility is to validate diagnostic scripts provided by diagnostic agents, ensuring they are safe and comply with system integrity guidelines. Follow the instructions below in a clear and structured manner:

            Validation Workflow

            1. Receive and Validate the Script:
                - Upon receiving a script file from diagnostic agents, carefully review its contents.
                - Ensure all commands within the script are read-only and designed for gathering diagnostic information without altering the system state.

            2. Prohibited Commands:
                -Review the script to ensure it does not include commands that:
                    - Alter network configurations.
                    - Change file permissions or ownership (e.g., chmod, chown).
                    - Modify system files or configurations (e.g., rm, mv, cp, or editing system-critical files).
                    - Remove the commands which failed to execute and needs some package

            3. Reporting Unsafe Commands:
                - If the script contains any commands that could potentially modify the machine's status, immediately report this to the Supervisor Agent.
                - Include the full list of concerning commands in your report to ensure transparency.

            4. Approval for Execution:
                - If all commands are validated and deemed safe in the bash script then inform the Supervisor Agent that the bash script is cleared and handover all information and bash script given by diagnostic tool/agent to Supervisor Agent of OpsPilot

            Handling Missing Scripts
                - If no script is received from the diagnostic agent:
                    - Report the absence of the script file to the Supervisor Agent of OpsPilot, specifying that you cannot proceed without a valid script.

            Key Considerations

                - Prioritize System Safety: Always err on the side of caution. Do not accept any script that you suspect might compromise the system's security or stability.
                - Clear Communication: Maintain a direct line of communication with the Supervisor Agent of OpsPilot, providing timely updates on validation.
    """

        response = call_llm(prompt)
        print(response)
        return response
        # return validate_and_clean_json(response)

    except Exception as e:
        logger.error(f"Error in market segment identification: {str(e)}")
        return validate_and_clean_json("", default_value="error")

guard_diagnostic_agent_tool: BaseTool = tool(guard_diagnostic_agent_tool)
guard_diagnostic_agent_tool.name = "GuardDiagnostic"

