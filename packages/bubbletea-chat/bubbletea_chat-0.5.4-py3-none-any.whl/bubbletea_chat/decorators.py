"""
Decorators for creating BubbleTea chatbots
"""

import asyncio
import inspect
from typing import Any, Callable, Dict, List, AsyncGenerator, Generator, Union, Tuple, Optional
from functools import wraps

from .components import Component, Done
from .schemas import ComponentChatRequest, ComponentChatResponse, ImageInput, BotConfig

# Module-level registry for config function
_config_function: Optional[Tuple[Callable, str]] = None


class ChatbotFunction:
    """Wrapper for chatbot functions"""
    
    def __init__(self, func: Callable, name: str = None, stream: bool = None):
        self.func = func
        self.name = name or func.__name__
        self.is_async = inspect.iscoroutinefunction(func)
        self.is_generator = inspect.isgeneratorfunction(func) or inspect.isasyncgenfunction(func)
        self.stream = stream if stream is not None else self.is_generator
        
    async def __call__(self, message: str, images: List[ImageInput] = None, user_email: str = None, user_uuid: str = None, conversation_uuid: str = None, chat_history: Union[List[Dict[str, Any]], str] = None) -> Union[List[Component], AsyncGenerator[Component, None]]:
        """Execute the chatbot function"""
        # Check function signature to determine what parameters it accepts
        sig = inspect.signature(self.func)
        params = list(sig.parameters.keys())
        
        # Build kwargs based on what the function accepts
        kwargs = {}
        if 'images' in params:
            kwargs['images'] = images
        if 'user_email' in params:
            kwargs['user_email'] = user_email
        if 'user_uuid' in params:
            kwargs['user_uuid'] = user_uuid
        if 'conversation_uuid' in params:
            kwargs['conversation_uuid'] = conversation_uuid
            
        # Handle chat_history parameter compatibility
        if 'chat_history' in params:
            # Check if the function signature expects a specific type
            param_annotation = sig.parameters['chat_history'].annotation
            if param_annotation == str or param_annotation == Optional[str]:
                # Function expects string, convert list to string if needed
                if isinstance(chat_history, list):
                    kwargs['chat_history'] = str(chat_history)
                else:
                    kwargs['chat_history'] = chat_history
            else:
                # Function expects list or is untyped, keep as is
                kwargs['chat_history'] = chat_history
            
        # Call function with appropriate parameters
        if self.is_async:
            result = await self.func(message, **kwargs)
        else:
            result = self.func(message, **kwargs)
            
        # Handle different return types
        if self.is_generator:
            # Generator functions yield components
            if inspect.isasyncgen(result):
                return result
            else:
                # Convert sync generator to async
                async def async_wrapper():
                    for item in result:
                        yield item
                return async_wrapper()
        else:
            # Non-generator functions return list of components
            if not isinstance(result, list):
                result = [result]
            return result
    
    async def handle_request(self, request: ComponentChatRequest):
        """Handle incoming chat request and return appropriate response"""
        components = await self(
            request.message, 
            images=request.images,
            user_email=request.user_email,
            user_uuid=request.user_uuid,
            conversation_uuid=request.conversation_uuid,
            chat_history=request.chat_history
        )
        
        if self.stream:
            # Return async generator for streaming
            return components
        else:
            # Return list for non-streaming
            if inspect.isasyncgen(components):
                # Collect all components from generator
                collected = []
                async for component in components:
                    if not isinstance(component, Done):
                        collected.append(component)
                return ComponentChatResponse(responses=collected)
            else:
                return ComponentChatResponse(responses=components)


def chatbot(name: str = None, stream: bool = None):
    """
    Decorator to create a BubbleTea chatbot from a function
    
    Args:
        name: Optional name for the chatbot (defaults to function name)
        stream: Whether to stream responses (auto-detected from generator functions)
    
    Example:
        @chatbot()
        def my_bot(message: str):
            yield Text("Hello!")
            yield Image("https://example.com/image.jpg")
    """
    def decorator(func: Callable) -> ChatbotFunction:
        return ChatbotFunction(func, name=name, stream=stream)
    
    # Allow using @chatbot without parentheses
    if callable(name):
        func = name
        return ChatbotFunction(func)
    
    return decorator


def config(path: str = "/config"):
    """
    Decorator to define bot configuration endpoint
    
    Args:
        path: Optional path for the config endpoint (defaults to "/config")
    
    Example:
        @config()
        def get_config():
            return BotConfig(
                name="My Bot",
                url="https://mybot.example.com",
                is_streaming=True,
                emoji="🤖",
                initial_text="Hello! How can I help?"
                authorization="private",
                authorized_emails=["test@example.com"]
            )
    """
    def decorator(func: Callable) -> Callable:
        global _config_function
        _config_function = (func, path)
        return func
    
    # Allow using @config without parentheses
    if callable(path):
        func = path
        _config_function = (func, "/config")
        return func
    
    return decorator