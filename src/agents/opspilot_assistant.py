from datetime import datetime
from typing import Annotated, Literal, Optional, Sequence, Union

from langchain_community.tools import DuckDuckGoSearchResults, OpenWeatherMapQueryRun
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import RunnableConfig, RunnableLambda, RunnableSerializable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed import RemainingSteps
from langgraph.prebuilt import ToolNode

from agents.llama_guard import LlamaGuard, LlamaGuardOutput, SafetyAssessment
from tools.executor_agent_tool import executor_agent_tool
from tools.network_diagnostic_agent_tool import network_diagnostic_agent_tool
from tools.storage_diagnostic_agent_tool import storage_diagnostic_agent_tool
from tools.compute_diagnostic_agent_tool import compute_diagnostic_agent_tool
from tools.security_diagnostic_agent_tool import security_diagnostic_agent_tool
from tools.guard_diagnostic_agent_tool import guard_diagnostic_agent_tool
from core import get_model, settings


class AgentState(MessagesState, total=False):
    """`total=False` is PEP589 specs.

    documentation: https://typing.readthedocs.io/en/latest/spec/typeddict.html#totality
    """
    messages: Annotated[list[AnyMessage], add_messages]
    diagnostic_script: Optional[dict]
    diagnostic_script_execution_output: Optional[list] 
    safety: LlamaGuardOutput
    remaining_steps: RemainingSteps

# web_search = DuckDuckGoSearchResults(name="WebSearch")
tools = [network_diagnostic_agent_tool, storage_diagnostic_agent_tool, compute_diagnostic_agent_tool, 
    security_diagnostic_agent_tool, guard_diagnostic_agent_tool, executor_agent_tool]

instructions = f"""
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


def wrap_model(model: BaseChatModel) -> RunnableSerializable[AgentState, AIMessage]:
    model = model.bind_tools(tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="StateModifier",
    )
    return preprocessor | model


def format_safety_message(safety: LlamaGuardOutput) -> AIMessage:
    content = (
        f"This conversation was flagged for unsafe content: {', '.join(safety.unsafe_categories)}"
    )
    return AIMessage(content=content)


async def acall_model(state: AgentState, config: RunnableConfig) -> AgentState:
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    # Run llama guard check here to avoid returning the message if it's unsafe
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("Agent", state["messages"] + [response])
    if safety_output.safety_assessment == SafetyAssessment.UNSAFE:
        return {"messages": [format_safety_message(safety_output)], "safety": safety_output}

    if state["remaining_steps"] < 2 and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="Sorry, need more steps to process this request.",
                )
            ]
        }
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


async def llama_guard_input(state: AgentState, config: RunnableConfig) -> AgentState:
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("User", state["messages"])
    return {"safety": safety_output}


async def block_unsafe_content(state: AgentState, config: RunnableConfig) -> AgentState:
    safety: LlamaGuardOutput = state["safety"]
    return {"messages": [format_safety_message(safety)]}


# Define the graph
agent = StateGraph(AgentState)
agent.add_node("model", acall_model)
agent.add_node("tools", ToolNode(tools))
agent.add_node("guard_input", llama_guard_input)
agent.add_node("block_unsafe_content", block_unsafe_content)
agent.set_entry_point("guard_input")


# Check for unsafe input and block further processing if found
def check_safety(state: AgentState) -> Literal["unsafe", "safe"]:
    safety: LlamaGuardOutput = state["safety"]
    match safety.safety_assessment:
        case SafetyAssessment.UNSAFE:
            return "unsafe"
        case _:
            return "safe"


agent.add_conditional_edges(
    "guard_input", check_safety, {"unsafe": "block_unsafe_content", "safe": "model"}
)

# Always END after blocking unsafe content
agent.add_edge("block_unsafe_content", END)

# Always run "model" after "tools"
agent.add_edge("tools", "model")


# After "model", if there are tool calls, run "tools". Otherwise END.
def pending_tool_calls(state: AgentState) -> Literal["tools", "done"]:
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise TypeError(f"Expected AIMessage, got {type(last_message)}")
    if last_message.tool_calls:
        return "tools"
    return "done"


agent.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", "done": END})

opspilot_assistant = agent.compile(checkpointer=MemorySaver())
