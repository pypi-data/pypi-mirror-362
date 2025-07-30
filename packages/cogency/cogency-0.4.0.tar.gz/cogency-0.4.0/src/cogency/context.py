import json
from typing import TYPE_CHECKING, Any, Dict, List, Optional

# Avoid circular import
if TYPE_CHECKING:
    pass


# Context: Conversation state (user input + message history)
# AgentState: LangGraph workflow state container (includes Context + execution trace)
class Context:
    """Agent operational context."""

    def __init__(
        self,
        current_input: str,
        messages: List[Dict[str, str]] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None,
        max_history: Optional[int] = None,
    ):
        self.current_input = current_input
        self.messages = messages if messages is not None else []
        self.tool_results = tool_results if tool_results is not None else []
        self.max_history = max_history

    def add_message(self, role: str, content: str, trace_id: Optional[str] = None):
        """Add message to history with optional trace linkage."""
        message_dict = {"role": role, "content": content}
        if trace_id:
            message_dict["trace_id"] = trace_id
        self.messages.append(message_dict)
        self._apply_history_limit()

    def _apply_history_limit(self):
        """Apply sliding window if max_history is set."""
        if self.max_history is not None and len(self.messages) > self.max_history:
            if self.max_history == 0:
                self.messages = []
            else:
                self.messages = self.messages[-self.max_history:]

    def add_tool_result(self, tool_name: str, args: dict, output: dict):
        """Add tool execution result to history."""
        self.tool_results.append({"tool_name": tool_name, "args": args, "output": output})

    def get_clean_conversation(self) -> List[Dict[str, str]]:
        """Returns conversation without execution trace data and internal JSON."""

        clean_messages = []
        for msg in self.messages:
            content = msg["content"]
            # Filter out internal JSON messages
            try:
                # Only try to parse if content is a string
                if isinstance(content, str):
                    data = json.loads(content)
                    if data.get("action") in [
                        "tool_needed",
                        "direct_response",
                    ] or data.get("status") in ["continue", "complete", "error"]:
                        continue
            except (json.JSONDecodeError, TypeError):
                pass
            # Filter out tool calls and system messages
            if content.startswith("TOOL_CALL:") or msg["role"] == "system":
                continue
            clean_messages.append({"role": msg["role"], "content": content})
        return clean_messages

    def __repr__(self):
        return (
            f"Context(current_input='{self.current_input}', messages={len(self.messages)} messages)"
        )
