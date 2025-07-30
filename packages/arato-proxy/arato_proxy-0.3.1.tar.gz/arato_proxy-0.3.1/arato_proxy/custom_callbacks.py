from litellm.integrations.custom_logger import CustomLogger
from typing import Any, Dict, List, Mapping, Optional, Union, Literal
import requests
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check for required environment variables
required_env_vars = ["ARATO_API_URL", "ARATO_API_KEY"]
missing_vars = []

for var in required_env_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please set these variables in your .env file or environment.")
    sys.exit(1)

url = os.getenv("ARATO_API_URL")
token = os.getenv("ARATO_API_KEY")


class AratoLogHandler(CustomLogger): # https://docs.litellm.ai/docs/observability/custom_callback#callback-class
    """
    This file includes the custom callbacks for LiteLLM Proxy
    It send logs over to Arato Observability
    """
    
    async def async_log_pre_api_call(self, model, messages, kwargs):
        pass

    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        # Extract messages from kwargs
        messages = kwargs.get("messages", kwargs.get("input", []))
        
        # Extract response content safely
        response_content = None
        if hasattr(response_obj, 'choices') and response_obj.choices:
            response_content = response_obj.choices[0].message.content
        elif isinstance(response_obj, dict) and response_obj.get("choices"):
            response_content = response_obj["choices"][0].get("message", {}).get("content")
        
        # Extract usage information
        usage = None
        if hasattr(response_obj, 'usage') and response_obj.usage:
            usage = {
                "completion_tokens": response_obj.usage.completion_tokens,
                "prompt_tokens": response_obj.usage.prompt_tokens,
                "total_tokens": response_obj.usage.total_tokens
            }
            
            # Add detailed token information if available
            if hasattr(response_obj.usage, 'completion_tokens_details') and response_obj.usage.completion_tokens_details:
                details = response_obj.usage.completion_tokens_details
                if hasattr(details, 'accepted_prediction_tokens') and details.accepted_prediction_tokens is not None:
                    usage["accepted_prediction_tokens"] = details.accepted_prediction_tokens
                if hasattr(details, 'audio_tokens') and details.audio_tokens is not None:
                    usage["audio_tokens"] = details.audio_tokens
                if hasattr(details, 'reasoning_tokens') and details.reasoning_tokens is not None:
                    usage["reasoning_tokens"] = details.reasoning_tokens
                if hasattr(details, 'rejected_prediction_tokens') and details.rejected_prediction_tokens is not None:
                    usage["rejected_prediction_tokens"] = details.rejected_prediction_tokens
                if hasattr(details, 'text_tokens') and details.text_tokens is not None:
                    usage["text_tokens"] = details.text_tokens
                    
            if hasattr(response_obj.usage, 'prompt_tokens_details') and response_obj.usage.prompt_tokens_details:
                details = response_obj.usage.prompt_tokens_details
                if hasattr(details, 'audio_tokens') and details.audio_tokens is not None:
                    usage["prompt_audio_tokens"] = details.audio_tokens
                if hasattr(details, 'cached_tokens') and details.cached_tokens is not None:
                    usage["cached_tokens"] = details.cached_tokens
                if hasattr(details, 'text_tokens') and details.text_tokens is not None:
                    usage["prompt_text_tokens"] = details.text_tokens
                if hasattr(details, 'image_tokens') and details.image_tokens is not None:
                    usage["image_tokens"] = details.image_tokens
                    
        elif isinstance(response_obj, dict) and response_obj.get("usage"):
            usage_data = response_obj["usage"]
            usage = {
                "completion_tokens": usage_data.get("completion_tokens"),
                "prompt_tokens": usage_data.get("prompt_tokens"),
                "total_tokens": usage_data.get("total_tokens")
            }
            
            # Add detailed token information if available
            completion_details = usage_data.get("completion_tokens_details", {})
            if completion_details:
                if completion_details.get("accepted_prediction_tokens") is not None:
                    usage["accepted_prediction_tokens"] = completion_details["accepted_prediction_tokens"]
                if completion_details.get("audio_tokens") is not None:
                    usage["audio_tokens"] = completion_details["audio_tokens"]
                if completion_details.get("reasoning_tokens") is not None:
                    usage["reasoning_tokens"] = completion_details["reasoning_tokens"]
                if completion_details.get("rejected_prediction_tokens") is not None:
                    usage["rejected_prediction_tokens"] = completion_details["rejected_prediction_tokens"]
                if completion_details.get("text_tokens") is not None:
                    usage["text_tokens"] = completion_details["text_tokens"]
                    
            prompt_details = usage_data.get("prompt_tokens_details", {})
            if prompt_details:
                if prompt_details.get("audio_tokens") is not None:
                    usage["prompt_audio_tokens"] = prompt_details["audio_tokens"]
                if prompt_details.get("cached_tokens") is not None:
                    usage["cached_tokens"] = prompt_details["cached_tokens"]
                if prompt_details.get("text_tokens") is not None:
                    usage["prompt_text_tokens"] = prompt_details["text_tokens"]
                if prompt_details.get("image_tokens") is not None:
                    usage["image_tokens"] = prompt_details["image_tokens"]
        
        # Also try to get usage from standard_logging_object metadata if available
        if not usage:
            metadata = kwargs.get("litellm_params", {}).get("metadata", {})
            if metadata.get("usage_object"):
                usage_obj = metadata["usage_object"]
                usage = {
                    "completion_tokens": usage_obj.get("completion_tokens"),
                    "prompt_tokens": usage_obj.get("prompt_tokens"),
                    "total_tokens": usage_obj.get("total_tokens")
                }
                
                # Add detailed token information
                completion_details = usage_obj.get("completion_tokens_details", {})
                if completion_details:
                    if completion_details.get("accepted_prediction_tokens") is not None:
                        usage["accepted_prediction_tokens"] = completion_details["accepted_prediction_tokens"]
                    if completion_details.get("audio_tokens") is not None:
                        usage["audio_tokens"] = completion_details["audio_tokens"]
                    if completion_details.get("reasoning_tokens") is not None:
                        usage["reasoning_tokens"] = completion_details["reasoning_tokens"]
                    if completion_details.get("rejected_prediction_tokens") is not None:
                        usage["rejected_prediction_tokens"] = completion_details["rejected_prediction_tokens"]
                        
                prompt_details = usage_obj.get("prompt_tokens_details", {})
                if prompt_details:
                    if prompt_details.get("audio_tokens") is not None:
                        usage["prompt_audio_tokens"] = prompt_details["audio_tokens"]
                    if prompt_details.get("cached_tokens") is not None:
                        usage["cached_tokens"] = prompt_details["cached_tokens"]
                    if prompt_details.get("text_tokens") is not None:
                        usage["prompt_text_tokens"] = prompt_details["text_tokens"]
                    if prompt_details.get("image_tokens") is not None:
                        usage["image_tokens"] = prompt_details["image_tokens"]
        
        # Add response_cost to usage if available
        if usage and kwargs.get("response_cost") is not None:
            usage["response_cost"] = kwargs["response_cost"]
        
        # Extract tool calls
        tool_calls = []
        if hasattr(response_obj, 'choices') and response_obj.choices:
            if response_obj.choices[0].message.tool_calls:
                tool_calls = [
                    {
                        "type": "tool-call",
                        "toolCallId": tool_call.id,
                        "toolName": tool_call.function.name,
                        "args": tool_call.function.arguments
                    }
                    for tool_call in response_obj.choices[0].message.tool_calls
                ]
        elif isinstance(response_obj, dict) and response_obj.get("choices"):
            message_tool_calls = response_obj["choices"][0].get("message", {}).get("tool_calls", [])
            if message_tool_calls:
                tool_calls = [
                    {
                        "type": "tool-call",
                        "toolCallId": tool_call.get("id"),
                        "toolName": tool_call.get("function", {}).get("name"),
                        "args": tool_call.get("function", {}).get("arguments")
                    }
                    for tool_call in message_tool_calls
                ]
        
        # Calculate performance metrics
        total_time_ms = int((end_time - start_time).total_seconds() * 1000)
        completion_start_time = kwargs.get("completion_start_time", start_time)
        ttft_ms = int((completion_start_time - start_time).total_seconds() * 1000) if completion_start_time != start_time else 0
        
        performance = {
            "ttft": ttft_ms,  # Time to first token in milliseconds
            "ttlt": total_time_ms,  # Time to last token in milliseconds
        }
        
        # Add additional performance metrics if available
        if kwargs.get("llm_api_duration_ms"):
            performance["llm_api_duration_ms"] = kwargs["llm_api_duration_ms"]
        if kwargs.get("litellm_params", {}).get("_response_ms"):
            performance["response_ms"] = kwargs["litellm_params"]["_response_ms"]
        
        # Extract variables from kwargs or metadata
        variables = kwargs.get("variables") or kwargs.get("prompt_variables")
        
        # Extract tags from metadata or kwargs
        tags = kwargs.get("tags", {})
        metadata = kwargs.get("litellm_params", {}).get("metadata", {})
        if metadata:
            # Add useful metadata as tags
            if metadata.get("user_api_key_alias"):
                tags["user_api_key_alias"] = metadata["user_api_key_alias"]
            if metadata.get("user_api_key_team_id"):
                tags["user_api_key_team_id"] = metadata["user_api_key_team_id"]
            if metadata.get("user_api_key_user_id"):
                tags["user_api_key_user_id"] = metadata["user_api_key_user_id"]
            if metadata.get("model_group"):
                tags["model_group"] = metadata["model_group"]
            if metadata.get("deployment"):
                tags["deployment"] = metadata["deployment"]
            
            # Add openai-organization from headers if available
            headers = metadata.get("headers", {})
            if headers.get("openai-organization"):
                tags["openai_organization"] = headers["openai-organization"]
        
        # Extract trace and session IDs
        arato_thread_id = kwargs.get("litellm_session_id")
        prompt_id = kwargs.get("prompt_id")
        prompt_version = kwargs.get("prompt_version")
        
        # Use litellm_trace_id as fallback for arato_thread_id
        if not arato_thread_id:
            arato_thread_id = kwargs.get("litellm_trace_id")

        self.postLog(
            url,
            token,
            messages,
            response_content,
            kwargs.get("litellm_call_id"),
            kwargs.get("model"),
            variables,
            usage,
            performance,
            tool_calls,
            arato_thread_id,
            prompt_id,
            prompt_version,
            tags
        )

        print("Arato Log Handler: Log sent successfully")


    async def async_log_failure_event(self, kwargs, response_obj, start_time, end_time):
        pass


    async def async_pre_call_hook(self, user_api_key_dict, cache, data: dict, call_type: Literal["completion", "embeddings"]):
        pass
    
    def postLog(self, 
                api_url: str, 
                api_token: str, 
                messages: List[Dict[str, str]], 
                response: Optional[str], 
                event_id: Optional[str], 
                model: Optional[str],                                     
                variables: Optional[Dict[str, Union[str, Dict[str, str]]]], 
                usage: Optional[Mapping[str, Union[str, int]]],
                performance: Optional[Mapping[str, Union[str, int]]],
                tool_calls: Optional[List[Dict[str, Union[str, Dict[str, Any]]]]],
                arato_thread_id: Optional[str],
                prompt_id: Optional[str],
                prompt_version: Optional[str], 
                tags: Optional[Dict[str, str]]) -> requests.Response:
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_token,
        }

        # Define the JSON payload. 
        # It's recommended to send the prompt and variables. These can be used later to construct a dataset
        # It's also highly recommended to send the response. Arato can later compare the responses in your experiment to the loged responses.
        data: Dict[str, Any] = {
            "model": model, # Optional[str] model identifier (e.g. gpt-4o-mini)
            "messages": messages, # List[Dict[str, str]] list of messages to send to the model
            "response": response, # Optional[str] Example: [{"role": "model", "content": "Hello Arato!"}]
            "id": event_id, # Optional[str] event identifier. This can be later used to send additional information about this event.
            "variables": variables, # Optional[Dict[str, str]] If your template contains variables, you should pass their concrete values here.
            "usage": usage, # Optional[Dict[str, Union[str, int]]] Additional information about the usage of the model as returned by the model API
            "performance": performance, # Optional[Dict[str, Union[str, int]]] Additional information about the performance of the model as returned by the model API
            "tool_calls": tool_calls, # Optional[List[Dict[str, Union[str, Dict[str, Any]]]]] Additional information about the tool calls made by the model
            "arato_thread_id": arato_thread_id, # Optional[str] Thread identifier. This can be used to group multiple events together.
            "prompt_id": prompt_id, # Optional[str] Prompt identifier. 
            "prompt_version": prompt_version, # Optional[str] Prompt version. 
            "tags": tags # Optional[Dict[str, str]] Tags to be added to the log message
        }
        return requests.post(api_url, headers=headers, json=data)

proxy_handler_instance = AratoLogHandler()

