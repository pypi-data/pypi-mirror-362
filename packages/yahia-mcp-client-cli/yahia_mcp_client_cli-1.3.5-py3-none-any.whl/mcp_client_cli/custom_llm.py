"""Custom LLM provider for company-specific endpoints."""

import json
import logging
import requests
import traceback
import os
from typing import Any, Dict, Iterator, List, Optional, Union, AsyncIterator
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult, LLMResult
from pydantic import Field

# Set up logging
logger = logging.getLogger(__name__)

# Enable debug mode via environment variable
DEBUG_MODE = os.getenv("LLM_DEBUG", "false").lower() == "true"


class CustomLLM(BaseChatModel):
    """Custom LLM implementation for company-specific endpoints."""
    
    endpoint_url: str = Field(description="The full endpoint URL")
    api_key: str = Field(description="API key for authentication")
    auth_type: str = Field(default="Bearer", description="Authentication type")
    headers: Dict[str, str] = Field(default_factory=dict, description="Additional headers")
    temperature: float = Field(default=0.0, description="Temperature for response generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens in response")
    model_name: str = Field(default="custom-model", description="Model name for identification")
    verify_ssl: bool = Field(default=True, description="Whether to verify SSL certificates")
    ssl_cert_path: Optional[str] = Field(default=None, description="Path to SSL certificate file")
    
    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        """Return identifier of llm."""
        return "custom"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {
            "endpoint_url": self.endpoint_url,
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

    def _debug_print(self, message: str):
        """Print debug message if debug mode is enabled."""
        if DEBUG_MODE:
            print(f"DEBUG: {message}")

    def _format_message_to_dict(self, message: BaseMessage) -> Dict[str, Any]:
        """Convert a LangChain message to the format expected by your API."""
        try:
            self._debug_print(f"Formatting message: {type(message)} - {message}")
            
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            elif isinstance(message, SystemMessage):
                role = "system"
            else:
                role = "user"  # fallback
            
            # Handle different content types (text vs multimodal)
            if isinstance(message.content, str):
                content = message.content
            elif isinstance(message.content, list):
                # Handle multimodal content (text + images)
                content = message.content
            else:
                content = str(message.content)
            
            result = {
                "role": role,
                "content": content
            }
            
            self._debug_print(f"Formatted message result: {result}")
            return result
            
        except Exception as e:
            print(f"ERROR in _format_message_to_dict: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _prepare_request_body(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """Prepare the request body for your company's API."""
        try:
            self._debug_print(f"Preparing request body for {len(messages)} messages")
            
            formatted_messages = [self._format_message_to_dict(msg) for msg in messages]
            
            body = {
                "messages": formatted_messages,
                "temperature": self.temperature,
            }
            
            if self.max_tokens:
                body["max_tokens"] = self.max_tokens
                
            self._debug_print(f"Request body prepared: {json.dumps(body, indent=2)}")
            return body
            
        except Exception as e:
            print(f"ERROR in _prepare_request_body: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare headers for the API request."""
        try:
            self._debug_print(f"Preparing headers with auth_type={self.auth_type}")
            if DEBUG_MODE:
                masked_key = ('*' * (len(self.api_key) - 4) + self.api_key[-4:]) if len(self.api_key) > 4 else '***'
                self._debug_print(f"API key (masked): {masked_key}")
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"{self.auth_type} {self.api_key}",
            }
            
            # Add custom headers if they exist and are not None
            if self.headers and isinstance(self.headers, dict):
                self._debug_print(f"Adding custom headers: {list(self.headers.keys())}")
                headers.update(self.headers)
            else:
                self._debug_print("No custom headers to add")
                
            if DEBUG_MODE:
                masked_headers = dict((k, '***MASKED***' if k.lower() == 'authorization' else v) for k, v in headers.items())
                self._debug_print(f"Final headers (auth masked): {masked_headers}")
            
            return headers
            
        except Exception as e:
            print(f"ERROR in _prepare_headers: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _make_request(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Make the actual HTTP request to your company's API."""
        try:
            headers = self._prepare_headers()
            
            self._debug_print(f"Making request to {self.endpoint_url}")
            if DEBUG_MODE:
                self._debug_print(f"Request body: {json.dumps(body, indent=2)}")
                self._debug_print(f"SSL verification: {self.verify_ssl}")
                if self.ssl_cert_path:
                    self._debug_print(f"SSL cert path: {self.ssl_cert_path}")
            
            # Configure SSL verification
            verify_param = self.verify_ssl
            if self.ssl_cert_path and self.verify_ssl:
                verify_param = self.ssl_cert_path
            
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=body,
                timeout=60,
                verify=verify_param
            )
            
            self._debug_print(f"Response status: {response.status_code}")
            if DEBUG_MODE:
                self._debug_print(f"Response headers: {dict(response.headers)}")
                self._debug_print(f"Raw response: {response.text}")
            
            # Check if response is successful
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                if DEBUG_MODE:
                    self._debug_print(f"Parsed response data: {json.dumps(response_data, indent=2)}")
                return response_data
            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to parse JSON response: {e}")
                print(f"Raw response: {response.text}")
                raise Exception(f"Invalid JSON response from custom LLM: {e}")
                
        except requests.exceptions.SSLError as e:
            print(f"ERROR: SSL Certificate verification failed: {e}")
            print("SOLUTION: Add 'verify_ssl: false' to your config.json under the llm section")
            print("WARNING: This will disable SSL certificate verification (not recommended for production)")
            raise Exception(f"SSL verification failed. Consider adding 'verify_ssl: false' to config: {e}")
        except requests.exceptions.Timeout:
            print("ERROR: Request timed out")
            raise Exception("Request to custom LLM timed out")
        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: Connection error: {e}")
            raise Exception(f"Failed to connect to custom LLM endpoint: {e}")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_msg = f"HTTP {status_code} error from custom LLM"
            print(f"ERROR: {error_msg}")
            print(f"Response text: {e.response.text}")
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg += f": {error_data['error']}"
                elif "message" in error_data:
                    error_msg += f": {error_data['message']}"
            except:
                error_msg += f": {e.response.text}"
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request exception: {e}")
            raise Exception(f"Request to custom LLM failed: {e}")
        except Exception as e:
            print(f"ERROR in _make_request: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _extract_response_content(self, response: Dict[str, Any]) -> str:
        """Extract the response content from your API's response format."""
        try:
            self._debug_print(f"Extracting content from response with keys: {list(response.keys())}")
            
            # OpenAI-style format:
            if "choices" in response:
                if response["choices"] and len(response["choices"]) > 0:
                    choice = response["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        content = choice["message"]["content"]
                        self._debug_print(f"Extracted content (OpenAI style): {content}")
                        return content
                    elif "text" in choice:
                        content = choice["text"]
                        self._debug_print(f"Extracted content (text field): {content}")
                        return content
            
            # Alternative formats - adjust based on your API:
            for key in ["response", "content", "text", "completion", "output", "result", "answer", "reply", "generated_text"]:
                if key in response:
                    content = str(response[key])
                    self._debug_print(f"Extracted content ({key} field): {content}")
                    return content
            
            # Generic message format:
            if "message" in response:
                if isinstance(response["message"], dict) and "content" in response["message"]:
                    content = response["message"]["content"]
                    self._debug_print(f"Extracted content (message.content): {content}")
                    return content
                elif isinstance(response["message"], str):
                    content = response["message"]
                    self._debug_print(f"Extracted content (message string): {content}")
                    return content
            
            # If none of the above worked
            print(f"ERROR: Could not extract content from response")
            print(f"Available keys: {list(response.keys())}")
            if DEBUG_MODE:
                print(f"Full response: {response}")
            raise ValueError(f"Could not extract content from response. Available keys: {list(response.keys())}")
            
        except Exception as e:
            print(f"ERROR in _extract_response_content: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response from the custom LLM."""
        try:
            self._debug_print(f"Starting _generate with {len(messages)} messages")
            
            # Prepare the request
            body = self._prepare_request_body(messages)
            
            # Add any additional parameters from kwargs
            if stop:
                body["stop"] = stop
                self._debug_print(f"Added stop sequences: {stop}")
            
            # Make the request
            response = self._make_request(body)
            
            # Extract the content
            content = self._extract_response_content(response)
            
            # Create the response message
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            
            self._debug_print(f"Successfully generated response")
            return ChatResult(generations=[generation])
            
        except Exception as e:
            print(f"ERROR in _generate: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGeneration]:
        """Stream responses from the custom LLM."""
        try:
            self._debug_print("Starting _stream (non-streaming implementation)")
            result = self._generate(messages, stop, run_manager, **kwargs)
            yield result.generations[0]
        except Exception as e:
            print(f"ERROR in _stream: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async version of generate."""
        try:
            self._debug_print("Starting _agenerate (sync implementation)")
            return self._generate(messages, stop, run_manager, **kwargs)
        except Exception as e:
            print(f"ERROR in _agenerate: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGeneration]:
        """Async stream responses from the custom LLM."""
        try:
            self._debug_print("Starting _astream (sync implementation)")
            result = await self._agenerate(messages, stop, run_manager, **kwargs)
            yield result.generations[0]
        except Exception as e:
            print(f"ERROR in _astream: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def invoke(
        self,
        input: Union[str, List[BaseMessage], Dict],
        config: Optional[Dict] = None,
        **kwargs: Any,
    ) -> AIMessage:
        """Invoke the LLM with input."""
        try:
            self._debug_print(f"Starting invoke with input type: {type(input)}")
            
            # Convert input to messages if needed
            if isinstance(input, str):
                messages = [HumanMessage(content=input)]
            elif isinstance(input, list):
                messages = input
            elif isinstance(input, dict) and "messages" in input:
                messages = input["messages"]
            else:
                messages = [HumanMessage(content=str(input))]
            
            result = self._generate(messages, **kwargs)
            return result.generations[0].message
            
        except Exception as e:
            print(f"ERROR in invoke: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    async def ainvoke(
        self,
        input: Union[str, List[BaseMessage], Dict],
        config: Optional[Dict] = None,
        **kwargs: Any,
    ) -> AIMessage:
        """Async invoke the LLM with input."""
        try:
            self._debug_print(f"Starting ainvoke with input type: {type(input)}")
            
            # Convert input to messages if needed
            if isinstance(input, str):
                messages = [HumanMessage(content=input)]
            elif isinstance(input, list):
                messages = input
            elif isinstance(input, dict) and "messages" in input:
                messages = input["messages"]
            else:
                messages = [HumanMessage(content=str(input))]
            
            result = await self._agenerate(messages, **kwargs)
            return result.generations[0].message
            
        except Exception as e:
            print(f"ERROR in ainvoke: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def bind_tools(self, tools: List[Any], **kwargs: Any) -> "CustomLLM":
        """Bind tools to the LLM. For now, we'll return a copy of ourselves."""
        try:
            self._debug_print(f"bind_tools called with {len(tools)} tools")
            # Create a copy of the current instance with the same parameters
            # Tools will be handled by the LangGraph agent, not directly by our LLM
            return CustomLLM(
                endpoint_url=self.endpoint_url,
                api_key=self.api_key,
                auth_type=self.auth_type,
                headers=self.headers,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model_name=self.model_name,
            )
        except Exception as e:
            print(f"ERROR in bind_tools: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise

    def with_structured_output(self, schema: Any, **kwargs: Any) -> "CustomLLM":
        """Return a copy of the model configured for structured output."""
        try:
            self._debug_print("with_structured_output called")
            # For basic compatibility, return a copy of ourselves
            return CustomLLM(
                endpoint_url=self.endpoint_url,
                api_key=self.api_key,
                auth_type=self.auth_type,
                headers=self.headers,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model_name=self.model_name,
            )
        except Exception as e:
            print(f"ERROR in with_structured_output: {e}")
            if DEBUG_MODE:
                print(f"Traceback: {traceback.format_exc()}")
            raise


def create_custom_llm(
    endpoint_url: str,
    api_key: str,
    auth_type: str = "Bearer",
    headers: Optional[Dict[str, str]] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    model_name: str = "custom-model",
    verify_ssl: bool = True,
    ssl_cert_path: Optional[str] = None
) -> CustomLLM:
    """Factory function to create a custom LLM instance."""
    try:
        if DEBUG_MODE:
            print(f"DEBUG: Creating custom LLM with:")
            print(f"  endpoint_url: {endpoint_url}")
            print(f"  api_key: {'*' * len(api_key) if api_key else 'None'}")
            print(f"  auth_type: {auth_type}")
            print(f"  headers: {headers}")
            print(f"  temperature: {temperature}")
            print(f"  max_tokens: {max_tokens}")
            print(f"  model_name: {model_name}")
            print(f"  verify_ssl: {verify_ssl}")
            print(f"  ssl_cert_path: {ssl_cert_path}")
        
        return CustomLLM(
            endpoint_url=endpoint_url,
            api_key=api_key,
            auth_type=auth_type,
            headers=headers or {},
            temperature=temperature,
            max_tokens=max_tokens,
            model_name=model_name,
            verify_ssl=verify_ssl,
            ssl_cert_path=ssl_cert_path
        )
    except Exception as e:
        print(f"ERROR in create_custom_llm: {e}")
        if DEBUG_MODE:
            print(f"Traceback: {traceback.format_exc()}")
        raise