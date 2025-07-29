"""Memory-aware agent interface for AgentDK.

This module provides a reusable interface for agents that need memory integration,
including conversation continuity, user preference support, and memory investigation tooling.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
import os

from .memory_manager import MemoryManager
from .memory_tools import MemoryTools
from ..agent.session_manager import SessionManager
from ..agent.agent_interface import AgentInterface
from ..core.logging_config import get_logger


class MemoryAwareSession(ABC):
    """Abstract base class for agents with memory integration.
    
    Provides conversation continuity, user preference support,
    and memory investigation tooling for any agent implementation.
    
    This class handles all memory-related functionality, allowing
    concrete agent implementations to focus on their core logic
    while gaining memory capabilities.
    """

    def __init__(
        self, 
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        enable_memory: bool = True,
        resume_session: Optional[bool] = None,
        # Backward compatibility parameters
        memory: Optional[bool] = None,
        user_id: str = "default",
        memory_config: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ):
        """Initialize MemoryAwareAgent with unified parameters and optional memory integration.
        
        Args:
            llm: Language model instance
            config: Agent configuration dictionary
            name: Agent name for identification
            prompt: System prompt for the agent
            enable_memory: Whether to enable memory system (default: True)
            resume_session: Whether to resume from previous session (None = no session management)
            memory: [DEPRECATED] Use enable_memory instead
            user_id: User identifier for scoped memory
            memory_config: Optional memory configuration
            **kwargs: Additional configuration parameters
        """
        # Handle backward compatibility for memory parameter
        if memory is not None:
            enable_memory = memory
        

        self.name = name or self.__class__.__name__.lower().replace("agent", "")
        self.enable_memory = enable_memory
        self.user_id = user_id
        self.resume_session = resume_session
        
        # Initialize logger
        self.logger = get_logger()
        
        # Initialize session manager for user-facing agents
        self.session_manager = None
        if resume_session is not None:
            # Parameter presence indicates user-facing agent
            # Use provided name or derive from class name for session management
            agent_name = self.name or self.__class__.__name__.lower().replace("agent", "").replace("app", "app")
            self.session_manager = SessionManager(agent_name)
        
        # Initialize memory system if enabled
        self.memory = None
        self.memory_tools = None
        
        if self.enable_memory:
            try:
                self.memory = MemoryManager(
                    config=memory_config,
                    user_id=user_id
                )
                self.memory_tools = MemoryTools(self.memory)
                self.logger.debug(f"Memory system initialized for user {user_id}")
            except Exception as e:
                self.logger.debug(f"Memory initialization failed: {e}")
                self.logger.debug("Continuing without memory...")
                self.enable_memory = False
    
    def memory_tool(self, command: str) -> str:
        """Memory investigation tool interface.
        
        Args:
            command: CLI-style memory command
            
        Returns:
            Formatted response from memory tools
        """
        if not self.enable_memory:
            return "❌ Memory system disabled"
        
        if not self.memory_tools:
            return "❌ Memory system not available"
        
        return self.memory_tools.execute(command)
    
    def get_memory_context(self, query: str) -> Optional[str]:
        """Get memory context for a query.
        
        Args:
            query: User's input query
            
        Returns:
            Memory context string or None if not available
        """
        if not self.enable_memory or not self.memory:
            return None
        
        try:
            return self.memory.get_llm_context(query)
        except Exception as e:
            self.logger.debug(f"Memory context retrieval failed: {e}")
            return None
    
    def store_interaction(self, query: str, response: str) -> None:
        """Store an interaction in memory.
        
        Args:
            query: User's input query
            response: Agent's response
        """
        if not self.enable_memory or not self.memory:
            return
        
        try:
            self.memory.store_interaction(query, response)
        except Exception as e:
            self.logger.debug(f"Memory storage failed: {e}")
    
    def get_memory_aware_prompt(self, base_prompt: str) -> str:
        """Enhance a base prompt with memory awareness.
        
        Args:
            base_prompt: The agent's base prompt
            
        Returns:
            Enhanced prompt with memory awareness
        """
        if not self.enable_memory or not self.memory:
            return base_prompt
        
        memory_enhancement = """

MEMORY AWARENESS:
- You have access to conversation history and user preferences via memory_context
- Use memory context to understand user preferences (e.g., preferred response format)
- Reference previous conversations when relevant
- Maintain conversation continuity across sessions

USER PREFERENCE SUPPORT:
- Check memory_context for user preferences like response_format
- If user prefers "table" format, ensure responses are formatted accordingly
- Respect user's established preferences from previous interactions"""
        
        return base_prompt + memory_enhancement
    
    def process_with_memory(self, query: str) -> Dict[str, Any]:
        """Process a query with memory enhancement.
        
        This method prepares the input with memory context and handles
        memory storage after processing. Concrete implementations should
        call this method and use the enhanced input.
        
        Args:
            query: User's input query
            
        Returns:
            Dictionary with enhanced input and memory context
        """
        # Get memory context if available
        memory_context = self.get_memory_context(query)
        
        # Prepare enhanced input with memory context
        enhanced_input = {"messages": [{"role": "user", "content": query}]}
        if memory_context:
            enhanced_input["memory_context"] = memory_context
        
        return enhanced_input
    
    def finalize_with_memory(self, query: str, response: str) -> str:
        """Finalize processing by storing interaction in memory.
        
        Args:
            query: Original user query
            response: Agent's response
            
        Returns:
            The response (unchanged)
        """
        # Store interaction in memory
        self.store_interaction(query, response)
        return response
    
    def restore_from_session(self, session_context: list) -> bool:
        """Restore agent state from CLI session context.
        
        Args:
            session_context: List of previous interactions from CLI session
            
        Returns:
            bool: True if restoration successful, False otherwise
        """
        if not self.enable_memory or not self.memory or not session_context:
            return False
        
        try:
            # Restore interactions to memory system
            for interaction in session_context:
                user_input = interaction.get('user_input', '')
                agent_response = interaction.get('agent_response', '')
                
                if user_input and agent_response:
                    self.memory.store_interaction(user_input, agent_response)
            
            self.logger.debug(f"Restored {len(session_context)} interactions from session")
            return True
            
        except Exception as e:
            self.logger.debug(f"Session restoration failed: {e}")
            return False
    
    def get_session_state(self) -> dict:
        """Get current session state for CLI persistence.
        
        Returns:
            Dictionary containing session state data
        """
        if not self.enable_memory or not self.memory:
            return {}
        
        try:
            # Get recent interactions from working memory
            working_memory = getattr(self.memory, 'working_memory', None)
            if working_memory and hasattr(working_memory, 'get_context'):
                recent_context = working_memory.get_context()
                
                # Convert to CLI session format
                interactions = []
                for item in recent_context:
                    content = item.get('content', '')
                    if content.startswith('User: '):
                        # This is a user message, look for corresponding assistant response
                        user_input = content[6:]  # Remove 'User: ' prefix
                        interactions.append({'user_input': user_input, 'agent_response': ''})
                    elif content.startswith('Assistant: ') and interactions:
                        # This is an assistant response, add to last interaction
                        agent_response = content[11:]  # Remove 'Assistant: ' prefix
                        interactions[-1]['agent_response'] = agent_response
                
                return {
                    'memory_state': {
                        'working_memory': recent_context,
                        'interaction_count': len(interactions)
                    },
                    'interactions': interactions
                }
            
            return {}
            
        except Exception as e:
            self.logger.debug(f"Failed to get session state: {e}")
            return {}
    
    # User preference management methods
    def set_preference(self, category: str, key: str, value: Any) -> str:
        """Set a user preference.
        
        Args:
            category: Preference category (ui, agent, system)
            key: Preference key
            value: Preference value
            
        Returns:
            Status message
        """
        if not self.enable_memory:
            return "❌ Memory system disabled"
        
        if not self.memory:
            return "❌ Memory system not available"
        
        try:
            self.memory.set_preference(category, key, value)
            return f"✅ Preference set: {category}.{key} = {value}"
        except Exception as e:
            return f"❌ Failed to set preference: {e}"
    
    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """Get a user preference.
        
        Args:
            category: Preference category
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        if not self.enable_memory or not self.memory:
            return default
        
        try:
            return self.memory.get_preference(category, key, default)
        except Exception as e:
            self.logger.debug(f"Failed to get preference: {e}")
            return default
    
    def get_memory_stats(self) -> str:
        """Get formatted memory statistics.
        
        Returns:
            Formatted memory statistics
        """
        if not self.enable_memory:
            return "❌ Memory system disabled"
        
        if not self.memory_tools:
            return "❌ Memory system not available"
        
        return self.memory_tools.execute("stats --detailed")
    
    def _format_memory_context(self, memory_context: dict) -> str:
        """Format memory context in a readable way for LLM.
        
        Args:
            memory_context: Raw memory context dictionary
            
        Returns:
            Formatted memory context string
        """
        if not memory_context or 'memory_context' not in memory_context:
            return "No recent conversation history"
        
        context_data = memory_context['memory_context']
        formatted_lines = []
        
        # Format working memory (recent conversation)
        working_memory = context_data.get('working', [])
        if working_memory:
            formatted_lines.append("Recent conversation:")
            for item in working_memory[-3:]:  # Last 3 items
                content = item.get('content', '')
                if content.startswith('User:'):
                    formatted_lines.append(f"  {content}")
                elif content.startswith('Assistant:'):
                    formatted_lines.append(f"  {content}")
        
        # Format factual memory (user preferences)
        factual_memory = context_data.get('factual', [])
        if factual_memory:
            formatted_lines.append("User preferences:")
            for item in factual_memory:
                content = item.get('content', '')
                formatted_lines.append(f"  - {content}")
        
        return "\n".join(formatted_lines) if formatted_lines else "No relevant context available"



    def parse_memory_context(self, user_prompt: str) -> tuple[str, str]:
        """Parse memory context from formatted user prompt.

        Args:
            user_prompt: User prompt that may contain memory context

        Returns:
            Tuple of (actual_query, memory_context)
        """
        # Check if the prompt contains memory context formatting
        if "User query: " in user_prompt and "Memory context: " in user_prompt:
            try:
                # Split by the first occurrence of "Memory context:"
                parts = user_prompt.split("Memory context: ", 1)
                if len(parts) == 2:
                    # Extract the user query from the first part
                    first_part = parts[0].strip()
                    if first_part.startswith("User query: "):
                        actual_query = first_part.replace("User query: ", "").strip()
                    else:
                        actual_query = first_part.strip()

                    # The memory context is everything after "Memory context: "
                    memory_context = parts[1].strip()

                    return actual_query, memory_context

            except Exception as e:
                self.logger.warning(f"Failed to parse memory context: {e}")
                return user_prompt, ""

        # No memory context found, return original prompt
        return user_prompt, ""