# Standard library imports
import functools
import logging
import operator
import uuid
from datetime import datetime
from typing import Annotated, Literal, Optional, Sequence, Union

# Third-party imports
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.runnables.config import merge_configs

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.prebuilt import ToolNode, create_react_agent, tools_condition
from pydantic import BaseModel
from typing_extensions import TypedDict

from langfuse.callback import CallbackHandler
# Initialize Langfuse CallbackHandler for Langchain (tracing)
langfuse_handler = CallbackHandler()


# Local imports
from graph_utils.logger import get_logger
from graph_utils.tools import (
    network_diagnostic_agent_tool,
    storage_diagnostic_agent_tool,
    compute_diagnostic_agent_tool,
    security_diagnostic_agent_tool,
    guard_diagnostic_agent_tool,
    executor_agent_tool,
    #find and use the existing runbook
    #extract network and deployment diagram information
    #correlate with surrounding alerts
    #confirm possible root cause identified
)


logger = get_logger(__name__)


def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    diagnostic_script: Optional[dict]
    diagnostic_script_execution_output: Optional[list] 
    # filtered_material_codes: Optional[list]
    # material_codes_after_nutritional_analysis: Optional[list]
    # in_campaign_products: Optional[list]
    # shelf_life: Optional[str]
    # dietary_requirements: Optional[list]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            langfuse_callback_config = RunnableConfig(callbacks=[langfuse_handler])
            config=merge_configs(config, langfuse_callback_config),
            passenger_id = configuration.get("passenger_id", None)
            state = {**state, "user_info": passenger_id}
           # print("State", state)
            result = self.runnable.invoke(state)
            print('HERE IS RESULT')
            print(result)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                print('Called Tools List')
                print(result.tool_calls)
                break
        return {"messages": result}

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# members = ["Market_Segment", "Customer_Application", "Product_Type", "Base_Type", "Product_Recommendation", "Technical_Specs", "Delivery_Format", "Nutritional_Guidelines", "Existing_Product_Alternatives", "Yield_Analysis", "Upsell_Opportunities", "Cross_Sell_Opportunities", "Product_Pitch_Generator", "Dietary_Requirements", "Dimension"]

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        # NOTE: follow correct sequence in script, 
        (
            "system",
            """
                You are the Supervisor Agent for OpsPilot, an intelligent system diagnostics coordinator. You are tasked with managing the entire diagnostic process with absolute control and precision. Your role is CRITICAL to ensure issues are resolved efficiently, following the outlined process with NO EXCEPTIONS.

                **Your Core Responsibilities**:

                1. COORDINATION AND ORCHESTRATION:

                    - **EVALUATE INCOMING ISSUES**:
                        - IMMEDIATELY assess the nature of the technical issue or error report.
                        - DECISIVELY determine which diagnostic tools or agents MUST handle specific components of the issue.

                    - **ASSIGN AGENTS**:
                        - ASSIGN tasks ONLY to the most appropriate diagnostic agents/tools.
                        - COMMUNICATE CLEARLY and DIRECTLY which tool or agent is responsible for each step.

                2. SCRIPT REVIEW AND VALIDATION:

                    - After a diagnostic agent/tool provides json data:
                        - If a bash script is found in the json data, get the bash script data.
                        - IMMEDIATELY forward the bash script to the GUARD AGENT/TOOL for a STRICT and IN-DEPTH review.
                        - ENSURE the guard agent/tool checks the script THOROUGHLY for completeness, accuracy, and security compliance.
                        - DEMAND a script from the diagnostic agent/tool WITHOUT DELAY if one is missing or incomplete.
                    - UNDER NO CIRCUMSTANCES should unvalidated scripts be executed.

                3. SCRIPT EXECUTION:

                    - ONCE the GUARD AGENT/TOOL has VERIFIED the script as SAFE:
                        - IMMEDIATELY forward the validated script to the EXECUTOR AGENT/TOOL for execution.
                        - ENSURE that EACH SCRIPT is EXECUTED ONLY ONCE. STRICTLY PROHIBIT re-execution of the same script under any circumstances.

                4. ITERATIVE DIAGNOSTICS (STRICTLY LIMITED TO 3 ITERATIONS):

                    - AFTER the EXECUTOR AGENT/TOOL provides the script execution output:
                        - IMMEDIATELY pass the output to the DIAGNOSTIC AGENT/TOOL for analysis and decision-making.
                        - DEMAND a DECISION from the diagnostic agent/tool:
                            1. CONFIRM the root cause based on available data.
                            2. OR provide a NEW and UNIQUE set of commands for further investigation.
                    - IF additional commands are provided:
                        - VERIFY that these commands are NEW and have NOT been executed previously. 
                        - SEND the commands to the GUARD AGENT/TOOL for validation.
                        - ONCE VALIDATED, execute them via the EXECUTOR AGENT/TOOL WITHOUT DELAY.
                    - YOU MUST ENFORCE the following:
                        - STRICTLY LIMIT this iterative process to a MAXIMUM OF 3 CYCLES.
                        - TERMINATE the process IMMEDIATELY if the root cause is not identified after 3 iterations.
                        - UNDER NO CIRCUMSTANCES should the loop continue beyond 3 cycles.

                5. SUMMARIZE THE ISSUE:

                    - AFTER identifying the root cause OR reaching the iteration limit:
                        - DELIVER a FINAL SUMMARY that MUST include the following:
                            1. **ISSUE SUMMARY**: A concise description of the original issue.
                            2. **ROOT CAUSE**: The identified reason for the issue OR a clear statement that the root cause could not be determined.
                            3. **SUPPORTING REASONING**: A detailed explanation of why this conclusion was reached.
                            4. **POSSIBLE ACTIONS**: Clear and actionable recommendations to resolve or mitigate the issue.
                        - ENSURE the summary is precise, actionable, and leaves NO ROOM FOR CONFUSION.

                FOLLOW THESE INSTRUCTIONS EXACTLY. DEVIATION, FAILURE TO TRACK SCRIPTS, OR ANY REPEATED EXECUTION OF SCRIPTS WILL RESULT IN INEFFICIENT DIAGNOSTICS. YOUR ROLE IS ABSOLUTELY CRUCIAL—PERFORM WITH RIGID CONTROL AND PRECISION.
            """
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)

# 6. Handle Script Execution
#                 - Only provide the bash script to the executor agent/tool along with the issue/alert ID, hostname, and host IP. Do not include any additional explanations.
#                 - Return the alert ID, hostname, and host IP as a dictionary in the response to the executor agent/tool.


assistant_tools = [
    storage_diagnostic_agent_tool,
    network_diagnostic_agent_tool,
    compute_diagnostic_agent_tool,
    security_diagnostic_agent_tool,
    guard_diagnostic_agent_tool,
    executor_agent_tool
]

assistant_runnable = assistant_prompt | llm.bind_tools(assistant_tools)

builder = StateGraph(State)
# Define nodes: these do the work
builder.add_node("Ops_Assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(assistant_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "Ops_Assistant")
builder.add_conditional_edges(
    "Ops_Assistant",
    tools_condition
)
builder.add_edge("tools", "Ops_Assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
opspilot_assistant = builder.compile(checkpointer=memory)
# opspilot_assistant.get_graph().draw_png("agent_diagram.png")




def invoke_opspilot_assistant(user_input: str):
     # Add required configuration keys
    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4()),  # Generate unique thread ID
            "checkpoint_ns": "barry_callabout",  # Add namespace
            "checkpoint_id": str(uuid.uuid4()),  # Generate unique checkpoint ID
        },
        "callbacks": [langfuse_handler],  # For observability via Langfuse
        "recursion_limit": 100
    }
        
    for s in opspilot_assistant.stream(
    {"messages": user_input},
        config,
    ):
        print("herer sis")
        print(s)
        if "__end__" not in s:
            for node_name, node_output in s.items():
                print("node_output----------------",node_output)
                if 'messages' in node_output:
                    messages = node_output['messages']
                    if not isinstance(messages, list):
                        messages = [messages]

                    for message in messages:
                        if hasattr(message, 'content'):
                            message_content = message.content
                            # Include the agent/tool name in the response
                            
                            message_content += f"\n\nResponse provided by: {node_name}"  # Add this line
                        
        # Return the final message for state management
        return {"messages": [AIMessage(content=message_content)]}