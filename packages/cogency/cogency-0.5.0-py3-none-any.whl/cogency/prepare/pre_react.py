"""Pre-ReAct node - memory extraction and tool filtering."""
from typing import List, Optional, Dict, Any

from cogency.llm import BaseLLM
from cogency.tools.base import BaseTool
from cogency.memory.core import MemoryBackend
from cogency.common.types import AgentState
from cogency.utils.tracing import trace_node
from cogency.utils.formatting import PhaseFormatter
from cogency.prepare.memory import should_extract_memory, save_extracted_memory
from cogency.prepare.tools import create_registry_lite, filter_tools_by_exclusion, prepare_tools_for_react
from cogency.prepare.extract import extract_memory_and_filter_tools
from cogency.react.phase_streamer import PhaseStreamer


@trace_node("pre_react")
async def pre_react_node(state: AgentState, *, llm: BaseLLM, tools: List[BaseTool], memory: MemoryBackend, system_prompt: str = None, config: Optional[Dict] = None) -> AgentState:
    """Pre-ReAct: Extract memory + filter tools, then prep for ReAct."""
    query = state["query"]
    context = state["context"]
    user_id = getattr(context, 'user_id', 'default')
    
    # Get streaming callback if available
    streaming_callback = None
    if config and "configurable" in config:
        streaming_callback = config["configurable"].get("streaming_callback")
    
    # Quick heuristic check for memory extraction
    needs_memory_extract = should_extract_memory(query)
    
    # Always stream Pre-React phases for consistency
    if streaming_callback:
        await PhaseStreamer.prepare_reason_phase(
            streaming_callback, 
            "Analyzing query for memory extraction and tool selection"
        )
    
    # Use LLM for dual flow if many tools OR memory needs extraction
    if (tools and len(tools) > 5) or needs_memory_extract:
        # Create registry lite (names + descriptions only)
        registry_lite = create_registry_lite(tools)
        
        # Single LLM call for memory extraction + tool filtering
        result = await extract_memory_and_filter_tools(query, registry_lite, llm)
        
        # Chain 1: Save extracted memory if not null/empty
        if result["memory_summary"] and streaming_callback:
            # Stream memory extraction
            await PhaseStreamer.prepare_memorize_phase(
                streaming_callback,
                f"Saving extracted insight: {result['memory_summary'][:50]}..." if len(result['memory_summary']) > 50 else result['memory_summary']
            )
        
        if result["memory_summary"]:
            await save_extracted_memory(
                result["memory_summary"], 
                memory, 
                user_id,
                tags=result.get("tags", []),
                memory_type=result.get("memory_type", "fact")
            )
        
        # Chain 2: Filter tools by exclusion (conservative)
        filtered_tools = filter_tools_by_exclusion(tools, result["excluded_tools"])
        
        # Stream tool filtering
        if streaming_callback:
            selected_tool_names = [tool.name for tool in filtered_tools]
            await PhaseStreamer.prepare_tooling_phase(
                streaming_callback,
                selected_tool_names
            )
    else:
        # Simple case: use all tools (no filtering)
        filtered_tools = tools
        
        # Always stream tool selection
        if streaming_callback and tools:
            selected_tool_names = [tool.name for tool in filtered_tools]
            await PhaseStreamer.prepare_tooling_phase(
                streaming_callback,
                selected_tool_names
            )
    
    # Chain 3: Prepare tools for ReAct (remove memorize, keep recall)
    # Add zero-tools fallback to prevent react_loop breaks
    prepared_tools = prepare_tools_for_react(filtered_tools)
    state["selected_tools"] = prepared_tools if prepared_tools else tools  # Use all tools as fallback
    
    return state


def _get_streaming_callback(state: AgentState) -> Optional[callable]:
    """Extract streaming callback from state if available."""
    config = state.get("configurable", {})
    return config.get("streaming_callback")