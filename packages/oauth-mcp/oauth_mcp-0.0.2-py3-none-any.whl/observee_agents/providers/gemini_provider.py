"""
Google Gemini LLM provider for MCP Agent System
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, AsyncIterator
from .base import LLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini provider implementation with FastMCP support"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-pro"):
        """
        Initialize Gemini provider
        
        Args:
            api_key: Optional API key (defaults to GOOGLE_API_KEY env var)
            model: Model name (defaults to gemini-2.0-flash-exp)
        """
        from google import genai
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Configure API key
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.model_name = model
        self.client = genai.Client(api_key=self.api_key)
    
    async def generate(
        self, 
        messages: List[Dict[str, str]], 
        tools: List[Dict[str, Any]] = None,
        mcp_config: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using Gemini API
        
        Args:
            messages: Conversation history
            tools: Optional tool definitions
            mcp_config: Optional MCP configuration (for FastMCP session)
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Returns:
            Dictionary with content, tool_calls, and raw_response
        """
        from google import genai
        
        # Handle MCP session passed as tools
        if mcp_config and "session" in mcp_config:
            # FastMCP session is passed directly as a tool
            tools_to_use = [mcp_config["session"]]
        elif tools:
            # Convert standard tool definitions to Gemini format
            tools_to_use = self._convert_tools_to_gemini_format(tools)
        else:
            tools_to_use = None
        
        # Convert messages to Gemini format
        contents = self._convert_messages_to_gemini_format(messages)
        
        # Extract generation parameters
        config_params = {
            "temperature": kwargs.get("temperature", 0.7),
            "candidate_count": 1,
        }
        
        if "max_tokens" in kwargs:
            config_params["max_output_tokens"] = kwargs["max_tokens"]
        
        if tools_to_use:
            config_params["tools"] = tools_to_use
        
        # Generate response
        logger.debug(f"Generating content with model {self.model_name}")
        logger.debug(f"Tools provided: {len(tools_to_use) if tools_to_use else 0}")
        
        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=genai.types.GenerateContentConfig(**config_params)
        )
        
        logger.debug(f"Response received: {type(response)}")
        
        # Parse response
        result = {
            "content": response.text if hasattr(response, 'text') else "",
            "tool_calls": [],
            "raw_response": response
        }
        
        # Extract tool calls if present
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                for part in candidate.content.parts:
                    # Check if part has function_call attribute and it's not None
                    if hasattr(part, 'function_call') and part.function_call is not None:
                        try:
                            # Safely access function call properties
                            fc = part.function_call
                            
                            # Get function name - handle different possible attribute names
                            func_name = None
                            if hasattr(fc, 'name'):
                                func_name = fc.name
                            elif hasattr(fc, 'function_name'):
                                func_name = fc.function_name
                            
                            # Get function arguments
                            func_args = {}
                            if hasattr(fc, 'args'):
                                # Convert args to dict if it's not already
                                if isinstance(fc.args, dict):
                                    func_args = fc.args
                                else:
                                    # Try to convert to dict
                                    func_args = dict(fc.args) if fc.args else {}
                            elif hasattr(fc, 'arguments'):
                                func_args = fc.arguments
                            
                            # Only append if we have a valid function name
                            if func_name:
                                result["tool_calls"].append({
                                    "id": f"call_{len(result['tool_calls'])}",
                                    "type": "function",
                                    "function": {
                                        "name": func_name,
                                        "arguments": json.dumps(func_args)
                                    }
                                })
                            else:
                                # Log warning if function call has no name
                                logger.warning(f"Function call part found but no name attribute: {fc}")
                        except Exception as e:
                            # Log error but don't fail the entire response
                            logger.error(f"Error parsing function call: {e}")
                            logger.debug(f"Function call object: {part.function_call}")
        
        return result
    
    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        mcp_config: Dict[str, Any] = None,
        **kwargs
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Generate streaming response using Gemini API
        """
        from google import genai
        
        # Handle MCP session passed as tools
        if mcp_config and "session" in mcp_config:
            # FastMCP session is passed directly as a tool
            tools_to_use = [mcp_config["session"]]
        elif tools:
            # Convert standard tool definitions to Gemini format
            tools_to_use = self._convert_tools_to_gemini_format(tools)
        else:
            tools_to_use = None
        
        # Convert messages to Gemini format
        contents = self._convert_messages_to_gemini_format(messages)
        
        # Extract generation parameters
        config_params = {
            "temperature": kwargs.get("temperature", 0.7),
            "candidate_count": 1,
        }
        
        if "max_tokens" in kwargs:
            config_params["max_output_tokens"] = kwargs["max_tokens"]
        
        if tools_to_use:
            config_params["tools"] = tools_to_use
        
        logger.debug(f"Generating streaming content with model {self.model_name}")
        logger.debug(f"Tools provided: {len(tools_to_use) if tools_to_use else 0}")
        
        try:
            # Generate streaming response
            response_stream = await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=genai.types.GenerateContentConfig(**config_params)
            )
            
            # Track accumulated data
            accumulated_content = ""
            tool_calls = []
            
            # Process streaming chunks
            async for chunk in response_stream:
                if hasattr(chunk, 'text') and chunk.text:
                    text_chunk = chunk.text
                    accumulated_content += text_chunk
                    yield {
                        "type": "content",
                        "content": text_chunk
                    }
                
                # Handle tool calls in streaming chunks
                if hasattr(chunk, 'candidates') and chunk.candidates:
                    candidate = chunk.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                        for part in candidate.content.parts:
                            # Check if part has function_call attribute and it's not None
                            if hasattr(part, 'function_call') and part.function_call is not None:
                                try:
                                    # Safely access function call properties
                                    fc = part.function_call
                                    
                                    # Get function name - handle different possible attribute names
                                    func_name = None
                                    if hasattr(fc, 'name'):
                                        func_name = fc.name
                                    elif hasattr(fc, 'function_name'):
                                        func_name = fc.function_name
                                    
                                    # Get function arguments
                                    func_args = {}
                                    if hasattr(fc, 'args'):
                                        # Convert args to dict if it's not already
                                        if isinstance(fc.args, dict):
                                            func_args = fc.args
                                        else:
                                            # Try to convert to dict
                                            func_args = dict(fc.args) if fc.args else {}
                                    elif hasattr(fc, 'arguments'):
                                        func_args = fc.arguments
                                    
                                    # Only append if we have a valid function name
                                    if func_name:
                                        tool_call = {
                                            "id": f"call_{len(tool_calls)}",
                                            "type": "function",
                                            "function": {
                                                "name": func_name,
                                                "arguments": json.dumps(func_args)
                                            }
                                        }
                                        tool_calls.append(tool_call)
                                        
                                        yield {
                                            "type": "tool_call",
                                            "tool_call": tool_call
                                        }
                                    else:
                                        # Log warning if function call has no name
                                        logger.warning(f"Function call part found but no name attribute: {fc}")
                                except Exception as e:
                                    # Log error but don't fail the entire response
                                    logger.error(f"Error parsing function call in stream: {e}")
                                    logger.debug(f"Function call object: {part.function_call}")
            
            # Yield completion
            yield {
                "type": "done",
                "final_response": {
                    "content": accumulated_content,
                    "tool_calls": tool_calls,
                    "raw_response": chunk  # Last chunk
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Gemini streaming API: {e}")
            # Fallback to non-streaming implementation
            logger.info("Falling back to non-streaming implementation")
            result = await self.generate(messages, tools, mcp_config, **kwargs)
            
            # Yield the complete response as a single chunk
            yield {
                "type": "content",
                "content": result["content"]
            }
            
            # Yield tool calls if any
            for tool_call in result.get("tool_calls", []):
                yield {
                    "type": "tool_call",
                    "tool_call": tool_call
                }
            
            # Yield completion
            yield {
                "type": "done",
                "final_response": result
            }
    
    def _convert_messages_to_gemini_format(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Convert standard message format to Gemini format"""
        # For Gemini, we need to build a proper conversation history
        if not messages:
            return []
        
        # If there's only one message, return it as a string
        if len(messages) == 1:
            return messages[0]["content"]
        
        # For multiple messages, build a conversation with proper role mapping
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Gemini uses "user" and "model" as roles
            if role == "assistant":
                role = "model"
            elif role == "system":
                # Prepend system messages to the first user message
                if contents and contents[-1]["role"] == "user":
                    contents[-1]["parts"][0]["text"] = f"{content}\n\n{contents[-1]['parts'][0]['text']}"
                    continue
                else:
                    # Convert system to user if no user message to prepend to
                    role = "user"
            
            contents.append({
                "role": role,
                "parts": [{"text": content}]
            })
        
        return contents
    
    def _convert_tools_to_gemini_format(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert standard tool definitions to Gemini function declarations"""
        # Gemini expects tools in a specific format with function_declarations
        function_declarations = []
        
        for tool in tools:
            gemini_function = None
            
            # Handle OpenAI-style format with "type": "function"
            if tool.get("type") == "function":
                function = tool.get("function", {})
                
                # Convert to Gemini function declaration format
                gemini_function = {
                    "name": function.get("name"),
                    "description": function.get("description", ""),
                }
                
                # Convert parameters if present
                if "parameters" in function:
                    params = function["parameters"]
                    # Gemini expects specific parameter format
                    gemini_function["parameters"] = params
            
            # Handle direct MCP tool format (when filtering is enabled)
            elif "name" in tool and "input_schema" in tool:
                gemini_function = {
                    "name": tool.get("name"),
                    "description": tool.get("description", ""),
                }
                
                # Convert input_schema to parameters
                input_schema = tool.get("input_schema", {})
                if input_schema and isinstance(input_schema, dict):
                    gemini_function["parameters"] = input_schema
            
            # Add to function declarations if we successfully parsed the tool
            if gemini_function and gemini_function.get("name"):
                function_declarations.append(gemini_function)
        
        # Return a single tool object with all function declarations
        if function_declarations:
            return [{
                "function_declarations": function_declarations
            }]
        
        return []