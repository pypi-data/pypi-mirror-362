"""
LLM Policy Execution and Tool Calling

Base classes and implementations for LLM policies that work with MCP environments.
Extracted from mcp_env.py to improve modularity and enable OpenAI integration.
"""

import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ...playback_policy import PlaybackPolicyBase
from ..types import MCPToolCall

logger = logging.getLogger(__name__)


class LLMBasePolicy(PlaybackPolicyBase, ABC):
    """
    Base class for LLM policies that work with MCP environments via tool calling.

    This abstraction enables shared code between FireworksPolicy and OpenAIPolicy.
    Maintains conversation history per environment for proper OpenAI-style trajectories.
    """

    def __init__(
        self,
        model_id: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        **kwargs,
    ):
        """
        Initialize base policy with automatic record/playback detection.

        Args:
            model_id: Model identifier
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate per request
        """
        # Check for automatic playback mode
        playback_file = os.environ.get("REWARD_KIT_PLAYBACK_FILE")
        _playback_actions = None

        if playback_file and os.path.exists(playback_file):
            logger.info(f"🎬 Auto-detected playback mode: {playback_file}")
            _playback_actions = self._load_trajectory_file(playback_file)
            if not _playback_actions:
                logger.warning(
                    f"⚠️  Failed to load playback file, switching to recording mode"
                )
                _playback_actions = None
        elif playback_file:
            logger.info(
                f"📝 Auto-detected recording mode: {playback_file} (file will be created)"
            )

        # Initialize playback functionality
        super().__init__(_playback_actions=_playback_actions, **kwargs)

        # Store policy configuration
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Initialize conversation state tracking for proper OpenAI trajectories
        self.conversation_histories = {}  # {env_index: [messages]}
        self.initialized = False

    @abstractmethod
    async def _make_llm_call(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """
        Make an LLM API call. Subclasses must implement this.

        Args:
            messages: Conversation messages
            tools: Available tools in OpenAI format

        Returns:
            LLM response with choices[0].message containing content and tool_calls
        """
        pass

    @abstractmethod
    def _convert_mcp_tools_to_llm_format(self, mcp_tools: List[Dict]) -> List[Dict]:
        """
        Convert MCP tool schemas to LLM-specific format.

        Args:
            mcp_tools: List of MCP tool definitions

        Returns:
            List of LLM-compatible tool definitions
        """
        pass

    def initialize_conversations(
        self, n_envs: int, system_prompts: List[str], initial_user_prompts: List[str]
    ):
        """Initialize conversation histories for each environment."""
        self.conversation_histories = {}
        for i in range(n_envs):
            self.conversation_histories[i] = [
                {"role": "system", "content": system_prompts[i]},
                {"role": "user", "content": initial_user_prompts[i]},
            ]
        self.initialized = True

    def add_tool_response(
        self,
        env_index: int,
        tool_call: MCPToolCall,
        tool_response: str,
        reward: float = 0.0,
        terminated: bool = False,
        info: Dict[str, Any] = None,
    ):
        """Add tool call and response to conversation history with control plane metadata."""
        if env_index not in self.conversation_histories:
            return

        conversation = self.conversation_histories[env_index]

        # Find the most recent assistant message with tool calls to get the correct call_id
        call_id = None
        for i in range(len(conversation) - 1, -1, -1):
            if (
                conversation[i]["role"] == "assistant"
                and "tool_calls" in conversation[i]
            ):
                # Find the tool call that matches our tool_name
                for tc in conversation[i]["tool_calls"]:
                    if tc["function"]["name"] == tool_call.tool_name:
                        call_id = tc["id"]
                        break
                if call_id:
                    break

        # Fallback if no matching tool call found
        if not call_id:
            call_id = f"call_{env_index}_{len(conversation)}"

        # Add tool response with control plane metadata
        tool_message = {
            "role": "tool",
            "tool_call_id": call_id,
            "content": tool_response,
        }

        # Add control plane metadata if provided
        if reward != 0.0 or terminated or info:

            tool_message["metadata"] = {
                "reward": reward,
                "terminated": terminated,
                "info": info or {},
            }

        conversation.append(tool_message)

    def log_conversation_state_for_playback(self, env_index: int, step: int):
        """
        Log the current conversation state in the format required for playback.

        Expected format: {"env_index": 0, "step": 0, "messages": [{..}, {..}]}

        Args:
            env_index: Environment index
            step: Current step number
        """
        # Use REWARD_KIT_PLAYBACK_FILE environment variable for recording
        playback_file = os.environ.get("REWARD_KIT_PLAYBACK_FILE")
        if not playback_file:
            return  # No recording file specified

        conversation = self.conversation_histories.get(env_index, [])
        if not conversation:
            return

        playback_entry = {
            "env_index": env_index,
            "step": step,
            "messages": conversation.copy(),
        }

        with open(playback_file, "a") as f:
            f.write(json.dumps(playback_entry) + "\n")

    async def _generate_live_tool_calls(
        self,
        tool_schemas: List[List[Dict]],
        observations: List[Any],
        system_prompts: List[str],
        user_prompts: List[str],
    ) -> List[MCPToolCall]:
        """
        Generate tool calls for all environments using LLM in live mode.

        For first call: Initialize conversations with system + user prompts
        For subsequent calls: Use existing conversation history for continuity

        Args:
            tool_schemas: Available MCP tools for each environment [env][tool]
            observations: Current observations from each environment
            system_prompts: System prompts from dataset (environment-specific)
            user_prompts: Formatted user prompts for current state

        Returns:
            List of tool calls to execute via MCP protocol
        """
        if not observations:
            return []

        # Initialize conversations on first call
        if not self.initialized:
            self.initialize_conversations(
                len(observations), system_prompts, user_prompts
            )

        logger.debug(
            f"🤖 Generating tool calls for {len(observations)} environments using {self.model_id}"
        )

        # Make parallel API calls using conversation history
        tasks = []
        for i, tools in enumerate(tool_schemas):
            task = asyncio.create_task(self._generate_tool_call_with_history(tools, i))
            tasks.append(task)

        # Wait for all API calls to complete
        tool_calls = await asyncio.gather(*tasks, return_exceptions=True)

        # Process responses and handle exceptions
        result_calls = []
        for i, tool_call in enumerate(tool_calls):
            if isinstance(tool_call, Exception):
                logger.warning(
                    f"Tool call generation {i} failed: {tool_call}, using fallback"
                )
                # Use first available tool as fallback
                if tool_schemas[i]:
                    fallback_tool = tool_schemas[i][0]
                    fallback_call = MCPToolCall(
                        tool_name=fallback_tool["name"], arguments={}
                    )
                    result_calls.append(fallback_call)
                else:
                    logger.error(f"No tools available for environment {i}")
                    result_calls.append(MCPToolCall("unknown", {}))
            elif tool_call is None:
                # No tool call generated (e.g., success message with no tools) - use special termination signal
                logger.info(
                    f"Environment {i}: No tool call generated, using termination signal"
                )
                result_calls.append(
                    MCPToolCall("_no_tool_call", {"reason": "no_tool_call_generated"})
                )
            else:
                result_calls.append(tool_call)

        logger.debug(f"🎯 Generated {len(result_calls)} tool calls")
        return result_calls

    async def _generate_tool_call_with_history(
        self, tools: List[Dict], env_index: int
    ) -> MCPToolCall:
        """
        Generate a tool call using conversation history for proper OpenAI trajectories.

        Args:
            tools: Available MCP tools for this environment
            env_index: Environment index

        Returns:
            MCPToolCall object
        """
        try:
            # Get conversation history for this environment
            messages = self.conversation_histories.get(env_index, [])
            if not messages:
                raise RuntimeError(
                    f"No conversation history for environment {env_index}"
                )

            # Convert MCP tools to LLM format
            llm_tools = self._convert_mcp_tools_to_llm_format(tools)

            logger.debug(
                f"Environment {env_index} - Converted {len(tools)} MCP tools to {len(llm_tools)} LLM tools"
            )
            logger.debug(
                f"Environment {env_index} - Conversation length: {len(messages)} messages"
            )

            # Make API call with conversation history
            response = await self._make_llm_call(messages, llm_tools)

            # ADD ASSISTANT MESSAGE TO ACTUAL CONVERSATION HISTORY
            # This is crucial for proper tool call ID management in add_tool_response
            assistant_message_for_history = {
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            }

            # Add tool calls if present with the actual API response IDs
            if response["choices"][0]["message"].get("tool_calls"):
                assistant_message_for_history["tool_calls"] = response["choices"][0][
                    "message"
                ]["tool_calls"]

            # Add to actual conversation history
            messages.append(assistant_message_for_history)

            # Extract tool call from response
            message = response["choices"][0]["message"]
            logger.debug(f"Environment {env_index} - Response message: {message}")

            if message.get("tool_calls") and len(message["tool_calls"]) > 0:
                tool_call = message["tool_calls"][0]
                logger.debug(
                    f"Environment {env_index} - Using tool call: {tool_call['function']['name']}({tool_call['function']['arguments']})"
                )

                return MCPToolCall(
                    tool_name=tool_call["function"]["name"],
                    arguments=json.loads(tool_call["function"]["arguments"]),
                )
            else:
                # No tool calls in response - this is normal when episode ends or LLM provides only text
                logger.info(
                    f"No tool calls in response for env {env_index}, message content: {message.get('content')}"
                )
                return None

        except Exception as e:
            logger.error(f"LLM API call failed for env {env_index}: {e}")
            raise e

    async def __call__(
        self,
        tool_schemas: List[List[Dict]],
        observations: List[Any],
        system_prompts: List[str],
        user_prompts: List[str],
    ) -> List[MCPToolCall]:
        """
        Override to ensure conversation histories are maintained in both live and playback modes.

        This is crucial for OpenAI format logging which requires conversation_histories.
        """
        # Initialize conversations if not already done (important for both modes)
        if not hasattr(self, "initialized") or not self.initialized:
            self.initialize_conversations(
                len(observations), system_prompts, user_prompts
            )

        if self._is_playback:
            # In playback mode, populate conversation histories with recorded messages
            tool_calls = []
            n_envs = len(tool_schemas)

            for env_index in range(n_envs):
                # Get recorded messages for this environment and step
                messages = self._get_playback_messages(env_index)

                if messages is None:
                    # No more recorded actions - signal early termination
                    tool_calls.append(
                        MCPToolCall(
                            "_playback_terminate",
                            {"reason": "no_more_recorded_actions"},
                        )
                    )
                    logger.info(
                        f"🎬 Environment {env_index}: No more recorded actions, signaling termination"
                    )
                    continue

                # Store the recorded messages in conversation history for OpenAI logging
                self.conversation_histories[env_index] = messages.copy()

                # Extract tool call from the last assistant message with tool_calls
                tool_call = self._extract_tool_call_from_messages(messages, env_index)
                tool_calls.append(tool_call)

            return tool_calls
        else:
            # Live mode - use the inherited behavior
            return await self._generate_live_tool_calls(
                tool_schemas, observations, system_prompts, user_prompts
            )


class FireworksPolicy(LLMBasePolicy):
    """
    Fireworks AI policy implementation that works with ANY MCP environment via tool calling.

    NO environment-specific logic - everything comes from MCP tools and dataset prompts.
    Supports both live mode (using Fireworks LLM) and playback mode (replaying recorded trajectories).
    """

    def __init__(
        self,
        model_id: str,
        temperature: float = 0.2,
        deployment_type: str = "serverless",
        max_tokens: int = 4096,
        **kwargs,
    ):
        """
        Initialize Fireworks policy.

        Args:
            model_id: Fireworks model identifier (e.g., "accounts/fireworks/models/qwen3-235b-a22b")
            temperature: Sampling temperature (0.0 to 2.0)
            deployment_type: "serverless", "on-demand", or "auto"
            max_tokens: Maximum tokens to generate per request
        """
        super().__init__(model_id, temperature, max_tokens, **kwargs)

        self.deployment_type = deployment_type

        # Only initialize Fireworks LLM in live mode (not in playback mode)
        if not self._is_playback:
            # Import Fireworks Build SDK - optional at module level
            try:
                from fireworks import LLM

                FIREWORKS_AVAILABLE = True
            except ImportError:
                raise ImportError(
                    "The 'fireworks-ai' package is required for FireworksPolicy. "
                    "Please install it with 'pip install fireworks-ai'"
                )

            # Verify authentication
            from ...auth import get_fireworks_api_key

            api_key = get_fireworks_api_key()
            if not api_key:
                raise ValueError(
                    "FIREWORKS_API_KEY environment variable or ~/.fireworks/auth.ini file is required "
                    "to use FireworksPolicy. See the reward-kit documentation for setup instructions."
                )

            # Set the API key for the Fireworks SDK
            os.environ["FIREWORKS_API_KEY"] = api_key

            # Initialize the LLM instance using Build SDK
            try:
                self.llm = LLM(
                    model=self.model_id,
                    deployment_type=self.deployment_type,
                    temperature=self.temperature,
                )
                logger.info(
                    f"✅ Initialized Fireworks LLM: {self.model_id} ({self.deployment_type})"
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to initialize Fireworks LLM '{self.model_id}': {e}"
                )
        else:
            # In playback mode, skip expensive LLM initialization
            self.llm = None
            logger.info(
                f"🎬 Playback mode: Skipping Fireworks LLM initialization for performance"
            )

    def _clean_messages_for_api(self, messages: List[Dict]) -> List[Dict]:
        """
        Clean messages by removing metadata fields that Fireworks API doesn't accept.

        Args:
            messages: Conversation messages with potential metadata

        Returns:
            Clean messages without metadata fields
        """
        clean_messages = []
        for msg in messages:
            clean_msg = msg.copy()
            # Remove metadata field if present
            if "metadata" in clean_msg:
                del clean_msg["metadata"]
            clean_messages.append(clean_msg)
        return clean_messages

    async def _make_llm_call(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """
        Make a Fireworks API call.

        Args:
            messages: Conversation messages (may contain metadata)
            tools: Available tools in OpenAI format

        Returns:
            API response in OpenAI format
        """
        # Clean messages by removing metadata before sending to API
        clean_messages = self._clean_messages_for_api(messages)

        current_request = {
            "messages": clean_messages,
            "tools": tools,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self.llm.chat.completions.create(**current_request)
        )

        # Convert Fireworks response to standard format
        return {
            "choices": [
                {
                    "message": {
                        "content": response.choices[0].message.content,
                        "tool_calls": (
                            [
                                {
                                    "id": tc.id,
                                    "type": tc.type,
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments,
                                    },
                                }
                                for tc in (response.choices[0].message.tool_calls or [])
                            ]
                            if response.choices[0].message.tool_calls
                            else []
                        ),
                    }
                }
            ]
        }

    def _convert_mcp_tools_to_llm_format(self, mcp_tools: List[Dict]) -> List[Dict]:
        """
        Convert MCP tool schemas to OpenAI function calling format for Fireworks.

        Args:
            mcp_tools: List of MCP tool definitions

        Returns:
            List of OpenAI-compatible tool definitions
        """
        openai_tools = []

        for mcp_tool in mcp_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": mcp_tool["name"],
                    "description": mcp_tool.get(
                        "description", f"Execute {mcp_tool['name']} action"
                    ),
                    "parameters": mcp_tool.get(
                        "input_schema",
                        {"type": "object", "properties": {}, "required": []},
                    ),
                },
            }
            openai_tools.append(openai_tool)

        return openai_tools
