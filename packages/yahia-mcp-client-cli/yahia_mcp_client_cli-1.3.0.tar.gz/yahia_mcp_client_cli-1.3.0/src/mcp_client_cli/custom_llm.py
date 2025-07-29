"""Custom LLM provider for company-specific endpoints."""

import json
import logging
import requests
from typing import Any, Dict, Iterator, List, Optional, Union
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

# Set up logging
logger = logging.getLogger(__name__)


class CustomLLM(BaseChatModel):
    """Custom LLM implementation for company-specific endpoints."""
    
    endpoint_url: str = Field(description="The full endpoint URL including model and version")
    api_key: str = Field(description="API key for authentication")
    auth_type: str = Field(default="Bearer", description="Authentication type")
    headers: Dict[str, str] = Field(default_factory=dict, description="Additional headers")
    temperature: float = Field(default=0.0, description="Temperature for response generation")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens in response")
    model_name: str = Field(default="custom-model", description="Model name for identification")
    
    class Config:
        """Configuration for this pydantic object."""
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        """Return identifier of llm."""
        return "custom"

    def _format_message_to_dict(self, message: BaseMessage) -> Dict[str, Any]:
        """Convert a LangChain message to the format expected by your API."""
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
        
        return {
            "role": role,
            "content": content
        }

    def _prepare_request_body(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        """Prepare the request body for your company's API."""
        formatted_messages = [self._format_message_to_dict(msg) for msg in messages]
        
        body = {
            "messages": formatted_messages,
            "temperature": self.temperature,
        }
        
        if self.max_tokens:
            body["max_tokens"] = self.max_tokens
            
        return body

    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare headers for the API request."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.auth_type} {self.api_key}",
            **self.headers
        }
        return headers

    def _make_request(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """Make the actual HTTP request to your company's API."""
        headers = self._prepare_headers()
        
        logger.debug(f"Making request to {self.endpoint_url}")
        logger.debug(f"Request headers: {headers}")
        logger.debug(f"Request body: {json.dumps(body, indent=2)}")
        
        try:
            response = requests.post(
                self.endpoint_url,
                headers=headers,
                json=body,
                timeout=60
            )
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Check if response is successful
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                logger.debug(f"Response data: {json.dumps(response_data, indent=2)}")
                return response_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {response.text}")
                raise Exception(f"Invalid JSON response from custom LLM: {e}")
                
        except requests.exceptions.Timeout:
            raise Exception("Request to custom LLM timed out")
        except requests.exceptions.ConnectionError:
            raise Exception("Failed to connect to custom LLM endpoint")
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_msg = f"HTTP {status_code} error from custom LLM"
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
            raise Exception(f"Request to custom LLM failed: {e}")

    def _extract_response_content(self, response: Dict[str, Any]) -> str:
        """Extract the response content from your API's response format."""
        # Adjust this based on your API's response format
        # Common formats:
        
        # OpenAI-style format:
        if "choices" in response:
            if response["choices"] and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
                elif "text" in choice:
                    return choice["text"]
        
        # Azure OpenAI format:
        if "choices" in response and response["choices"]:
            choice = response["choices"][0]
            if "delta" in choice and "content" in choice["delta"]:
                return choice["delta"]["content"]
        
        # Alternative formats - adjust based on your API:
        if "response" in response:
            return str(response["response"])
        
        if "content" in response:
            return str(response["content"])
        
        if "text" in response:
            return str(response["text"])
        
        # Claude-style format:
        if "completion" in response:
            return response["completion"]
        
        # Generic message format:
        if "message" in response:
            if isinstance(response["message"], dict) and "content" in response["message"]:
                return response["message"]["content"]
            elif isinstance(response["message"], str):
                return response["message"]
        
        # Try to find any string value that might be the content
        for key in ["output", "result", "answer", "reply", "generated_text"]:
            if key in response:
                return str(response[key])
        
        # If none of the above, try to find the content in the response
        # You may need to adjust this based on your specific API response format
        raise ValueError(f"Could not extract content from response. Available keys: {list(response.keys())}. Response: {response}")

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate a response from the custom LLM."""
        # Prepare the request
        body = self._prepare_request_body(messages)
        
        # Add any additional parameters from kwargs
        if stop:
            body["stop"] = stop
        
        # Make the request
        response = self._make_request(body)
        
        # Extract the content
        content = self._extract_response_content(response)
        
        # Create the response message
        message = AIMessage(content=content)
        generation = ChatGeneration(message=message)
        
        return ChatResult(generations=[generation])

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGeneration]:
        """Stream responses from the custom LLM."""
        # For now, we'll implement a simple non-streaming version
        # You can extend this to support streaming if your API supports it
        result = self._generate(messages, stop, run_manager, **kwargs)
        yield result.generations[0]

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Async version of generate."""
        # For now, we'll use the sync version
        # You can implement proper async support using aiohttp if needed
        return self._generate(messages, stop, run_manager, **kwargs)


def create_custom_llm(
    endpoint_url: str,
    api_key: str,
    auth_type: str = "Bearer",
    headers: Optional[Dict[str, str]] = None,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    model_name: str = "custom-model"
) -> CustomLLM:
    """Factory function to create a custom LLM instance."""
    return CustomLLM(
        endpoint_url=endpoint_url,
        api_key=api_key,
        auth_type=auth_type,
        headers=headers or {},
        temperature=temperature,
        max_tokens=max_tokens,
        model_name=model_name
    )