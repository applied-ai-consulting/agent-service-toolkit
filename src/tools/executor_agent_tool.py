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
def executor_agent_tool(user_input: str):
    '''
    Executes a bash script on a remote server via SSH.
    
    Args:
        user_input (str): JSON string containing bash script, event_id, SSH details
        Example: 
                {
                    "event_id": "12345",
                    "script": """#!/bin/bash
                        # This is a generated diagnostic script
                        echo "Collecting system information..."
                        hostname
                        df -h
                        echo "Done.""",
                    "ssh_details": {
                        "hostip": ip,
                        "user": ubuntu,
                    }
                }
    Returns:
        str: Data collected after executing bash script
    '''
        
    try:
        logger.info(f"Calling Executor Agent with user input {user_input}")
        if not user_input:
            logger.error("No input received.")
            return "No input received."
        
        ## Ensure user_input is a JSON string if it's a dictionary
        if isinstance(user_input, dict):
            user_input = json.dumps(user_input)

        user_input = validate_and_clean_json(user_input)
        logger.info(f"Cleaned user input: {user_input}")
        #user_input = json.loads(user_input) 
        
        # Extract details
        event_id = user_input.get("event_id")
        bash_script = user_input.get("script")
        ssh_details = user_input.get("ssh_details", {})
 
        if bash_script:    
            # Define the directory and file path
            scripts_dir = "./opspilot/diagnostic_scripts"
            #scripts_dir="/app/data_collection/diagnostic_scripts"
            os.makedirs(scripts_dir, exist_ok=True)  # Ensure the directory exists
            uuid_value =uuid.uuid4()
            
            script_path = os.path.join(scripts_dir, f"{event_id}_{uuid_value}.sh")  # Use UUID with event_id
        
            # Write the script to a file
            with open(script_path, "w") as script_file:
                script_file.write(bash_script)
            
            logger.info(f"Bash script saved to {script_path}")
            # print(f"Script saved at: {script_path}")
        
            ssh_key=os.environ.get('PEM_FILE_PATH')
            user=os.environ.get('USER_NAME')

            os.chmod(ssh_key, 0o600)
            ssh_command = f"ssh -o StrictHostKeyChecking=no -i {ssh_key} {user}@{ssh_details.get('hostip')} 'bash -s' < {script_path}"


            logger.info(f"Executing SSH command: {ssh_command}")

            # Execute the script via SSH
            execution_result = os.popen(ssh_command).read()
        
            if execution_result:
                #data_collector_dir = "/app/data_collection/data_collector"
                data_collector_dir = "./opspilot/data_collector"
                os.makedirs(data_collector_dir, exist_ok=True)  # Ensure the directory exists
                
                data_coll_dir_path = os.path.join(data_collector_dir, f"{event_id}_{uuid_value}.log")

                # Write the log to a file
                with open(data_coll_dir_path, "w") as log_file:
                    log_file.write(execution_result)

            #NOTE: Only pass path , don't provide prompt
                response = execution_result
            return response
        
    except Exception as e:
        logger.error(f"Error in security issue identification: {str(e)}")
        return validate_and_clean_json("", default_value="error")

executor_agent_tool: BaseTool = tool(executor_agent_tool)
executor_agent_tool.name = "Executor"

