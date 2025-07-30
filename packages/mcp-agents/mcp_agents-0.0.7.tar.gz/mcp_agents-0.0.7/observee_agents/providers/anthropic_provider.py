"""
Anthropic Claude LLM provider
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, AsyncIterator
from .base import LLMProvider

logger = logging.getLogger(__name__)


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        import anthropic
        from dotenv import load_dotenv
        
        load_dotenv()
        self.client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = model
    
    async def generate(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None, mcp_config: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Generate response using Anthropic API with native MCP support"""
        # Extract parameters
        max_tokens = kwargs.get("max_tokens", 1000)
        temperature = kwargs.get("temperature", 0.7)
        
        # Convert to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Use native MCP if config provided
        if mcp_config:
            response = self.client.beta.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=anthropic_messages,
                mcp_servers=[mcp_config],
                extra_headers={
                    "anthropic-beta": "mcp-client-2025-04-04"
                }
            )
        # Fallback to standard tool calling
        elif tools:
            # Convert tools to Anthropic format
            anthropic_tools = []
            for tool in tools:
                anthropic_tools.append({
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "input_schema": tool.get("inputSchema", {"type": "object", "properties": {}})
                })
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=anthropic_messages,
                tools=anthropic_tools,
                temperature=temperature
            )
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=anthropic_messages,
                temperature=temperature
            )
        
        # Extract content and tool calls
        content = ""
        if hasattr(response, 'content') and response.content:
            if isinstance(response.content, list):
                for item in response.content:
                    if hasattr(item, 'text'):
                        content += item.text
            else:
                content = str(response.content)
        
        return {
            "content": content,
            "raw_response": response
        }
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        mcp_config: Dict[str, Any] = None,
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Generate streaming response using Anthropic API with native MCP support
        """
        # Extract parameters
        max_tokens = kwargs.get("max_tokens", 1000)
        temperature = kwargs.get("temperature", 0.7)
        
        # Convert to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        logger.debug(f"Calling Anthropic streaming with model {self.model}")
        logger.debug(f"MCP config provided: {mcp_config is not None}")
        logger.debug(f"Tools provided: {len(tools) if tools else 0}")
        
        try:
            # Use native MCP if config provided
            if mcp_config:
                stream = self.client.beta.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=anthropic_messages,
                    mcp_servers=[mcp_config],
                    extra_headers={
                        "anthropic-beta": "mcp-client-2025-04-04"
                    },
                    stream=True
                )
            # Fallback to standard tool calling
            elif tools:
                # Convert tools to Anthropic format
                anthropic_tools = []
                for tool in tools:
                    anthropic_tools.append({
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "input_schema": tool.get("inputSchema", {"type": "object", "properties": {}})
                    })
                
                stream = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=anthropic_messages,
                    tools=anthropic_tools,
                    temperature=temperature,
                    stream=True
                )
            else:
                stream = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=anthropic_messages,
                    temperature=temperature,
                    stream=True
                )
            
            # Track accumulated data
            accumulated_content = ""
            tool_calls = []
            
            # Process the streaming response
            for chunk in stream:
                if chunk.type == "content_block_delta":
                    if chunk.delta.type == "text_delta":
                        text_chunk = chunk.delta.text
                        accumulated_content += text_chunk
                        yield {
                            "type": "content",
                            "content": text_chunk
                        }
                elif chunk.type == "content_block_start":
                    # Handle tool use blocks
                    if hasattr(chunk.content_block, 'type') and chunk.content_block.type == "tool_use":
                        tool_call = {
                            "id": chunk.content_block.id,
                            "type": "function",
                            "function": {
                                "name": chunk.content_block.name,
                                "arguments": ""
                            }
                        }
                        tool_calls.append(tool_call)
                elif chunk.type == "content_block_delta":
                    # Handle tool use input delta
                    if chunk.delta.type == "input_json_delta":
                        # Find the current tool call and accumulate arguments
                        if tool_calls:
                            tool_calls[-1]["function"]["arguments"] += chunk.delta.partial_json
                elif chunk.type == "message_stop":
                    # Yield any completed tool calls
                    for tool_call in tool_calls:
                        yield {
                            "type": "tool_call",
                            "tool_call": tool_call
                        }
                    
                    # Yield completion
                    yield {
                        "type": "done",
                        "final_response": {
                            "content": accumulated_content,
                            "tool_calls": tool_calls,
                            "raw_response": chunk
                        }
                    }
                    break
                    
        except Exception as e:
            logger.error(f"Error calling Anthropic streaming API: {e}")
            raise