"""
FastAPI server that proxies OpenAI API endpoints using the hexin_engine backend.
"""
import os
import time
import uuid
from typing import List, Optional, Dict, Any, Union, AsyncGenerator, Literal
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import StreamingResponse
from loguru import logger
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_chunk import Choice as ChunkChoice, ChoiceDelta
from openai.types.completion_usage import CompletionUsage
from openai.types.model import Model
from pydantic import BaseModel

from deeplin.inference_engine.hexin_engine import (
  get_userid_and_token,
  api_request,
  prepare_api_request_params,
  process_api_choices,
  process_api_response_to_choices,
)


# Global variables for authentication
USER_ID: Optional[str] = None
TOKEN: Optional[str] = None

# Fixed API key for client authentication
FIXED_API_KEY = "sk-deeplin-fastapi-proxy-key-12345"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize authentication on startup"""
    global USER_ID, TOKEN

    app_url = os.getenv("HITHINK_APP_URL")
    app_id = os.getenv("HITHINK_APP_ID")
    app_secret = os.getenv("HITHINK_APP_SECRET")

    if not app_id or not app_secret:
        raise ValueError("HITHINK_APP_ID and HITHINK_APP_SECRET must be set in environment variables.")

    try:
        USER_ID, TOKEN = get_userid_and_token(app_url=app_url, app_id=app_id, app_secret=app_secret)
        logger.info(f"Authentication successful. User ID: {USER_ID}")
    except Exception as e:
        logger.error(f"Failed to authenticate: {e}")
        raise

    yield

    # Cleanup (if needed)
    logger.info("Shutting down FastAPI server")


app = FastAPI(
    title="OpenAI API Proxy",
    description="A FastAPI server that proxies OpenAI API endpoints using hexin_engine backend",
    version="1.0.0",
    lifespan=lifespan
)


def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format. Use 'Bearer <api_key>'")

    api_key = authorization[7:]  # Remove "Bearer " prefix
    if api_key != FIXED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key


# Pydantic models for request/response
class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.6
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[str, Dict[str, Any]]] = None
    debug: Optional[bool] = True


class ListModelsResponse(BaseModel):
    object: Literal["list"] = "list"
    data: List[Model]


# Available models mapping
AVAILABLE_MODELS = [
    {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "gpt-4o",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "gpt-4o-mini",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "o3",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "o4-mini",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "gpt4",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
    },
    {
        "id": "claude",
        "object": "model",
        "created": 1677610602,
        "owned_by": "anthropic",
    },
    {
        "id": "gemini",
        "object": "model",
        "created": 1677610602,
        "owned_by": "google",
    },
    {
        "id": "doubao-deepseek-r1",
        "object": "model",
        "created": 1677610602,
        "owned_by": "bytedance",
    },
    {
        "id": "ep-20250204210426-gclbn",
        "object": "model",
        "created": 1677610602,
        "owned_by": "bytedance",
    },
    {
        "id": "deepseek-reasoner",
        "object": "model",
        "created": 1677610602,
        "owned_by": "deepseek",
    },
    {
        "id": "doubao-deepseek-v3",
        "object": "model",
        "created": 1677610602,
        "owned_by": "bytedance",
    },
    {
        "id": "ep-20250410145517-rpbrz",
        "object": "model",
        "created": 1677610602,
        "owned_by": "bytedance",
    },
    {
        "id": "deepseek-chat",
        "object": "model",
        "created": 1677610602,
        "owned_by": "deepseek",
    },
    {
        "id": "r1-qianfan",
        "object": "model",
        "created": 1677610602,
        "owned_by": "baidu",
    },
]




def create_chat_completion_response(
    choices_data: List[str],
    model: str,
    request_id: str,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
) -> ChatCompletion:
    """Create a ChatCompletion response from API response"""
    choices = []

    for i, content in enumerate(choices_data):
        if content is None:
            continue

        # Handle function calls or tool calls
        if isinstance(content, dict):
            # Check if it's a function call
            if "name" in content and "arguments" in content:
                message = ChatCompletionMessage(
                    role="assistant",
                    content=None,
                    function_call=content
                )
            else:
                # Generic dict content
                message = ChatCompletionMessage(
                    role="assistant",
                    content=None,
                    function_call=content.get("function_call"),
                    tool_calls=content.get("tool_calls")
                )
        elif isinstance(content, list):
            # Handle tool calls list
            message = ChatCompletionMessage(
                role="assistant",
                content=None,
                tool_calls=content
            )
        else:
            # Regular text content
            message = ChatCompletionMessage(
                role="assistant",
                content=str(content)
            )

        choice = Choice(
            index=i,
            message=message,
            finish_reason="stop"
        )
        choices.append(choice)

    usage = CompletionUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens
    )

    return ChatCompletion(
        id=request_id,
        choices=choices,
        created=int(time.time()),
        model=model,
        object="chat.completion",
        usage=usage
    )


async def create_chat_completion_stream(
    choices_data: List[str],
    model: str,
    request_id: str,
) -> AsyncGenerator[str, None]:
    """Create streaming response for chat completion"""

    for i, content in enumerate(choices_data):
        if content is None:
            continue

        # Handle different content types
        if isinstance(content, dict):
            # Function call or tool call
            if "name" in content and "arguments" in content:
                # Function call format
                delta = ChoiceDelta(function_call=content)
            else:
                # Generic dict format
                delta = ChoiceDelta(
                    function_call=content.get("function_call"),
                    tool_calls=content.get("tool_calls")
                )
        elif isinstance(content, list):
            # Tool calls list
            delta = ChoiceDelta(tool_calls=content)
        else:
            # Regular text content - split into chunks
            text_content = str(content)

            # Send content in chunks
            chunk_size = 20  # Smaller chunks for better streaming experience
            for j in range(0, len(text_content), chunk_size):
                chunk_text = text_content[j:j + chunk_size]
                delta = ChoiceDelta(content=chunk_text)

                chunk_choice = ChunkChoice(
                    index=i,
                    delta=delta,
                    finish_reason=None
                )

                chunk = ChatCompletionChunk(
                    id=request_id,
                    choices=[chunk_choice],
                    created=int(time.time()),
                    model=model,
                    object="chat.completion.chunk"
                )

                yield f"data: {chunk.model_dump_json()}\n\n"

            # Send final chunk for this choice
            delta = ChoiceDelta()
            chunk_choice = ChunkChoice(
                index=i,
                delta=delta,
                finish_reason="stop"
            )

            chunk = ChatCompletionChunk(
                id=request_id,
                choices=[chunk_choice],
                created=int(time.time()),
                model=model,
                object="chat.completion.chunk"
            )

            yield f"data: {chunk.model_dump_json()}\n\n"
            continue

        # For function/tool calls, send as single chunk
        chunk_choice = ChunkChoice(
            index=i,
            delta=delta,
            finish_reason="stop"
        )

        chunk = ChatCompletionChunk(
            id=request_id,
            choices=[chunk_choice],
            created=int(time.time()),
            model=model,
            object="chat.completion.chunk"
        )

        yield f"data: {chunk.model_dump_json()}\n\n"

    # Send final [DONE] marker
    yield "data: [DONE]\n\n"


@app.get("/v1/models", response_model=ListModelsResponse)
async def list_models(api_key: str = Header(None, alias="authorization")):
    """List available models"""
    verify_api_key(api_key)
    models = [Model(**model_data) for model_data in AVAILABLE_MODELS]
    return ListModelsResponse(data=models)


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest, authorization: Optional[str] = Header(None)):
    """Create a chat completion"""
    # Verify API key
    verify_api_key(authorization)

    global USER_ID, TOKEN

    if not USER_ID or not TOKEN:
        raise HTTPException(status_code=500, detail="Server authentication not initialized")

    # Extract parameters
    model = request.model
    messages = request.messages
    max_tokens = request.max_tokens or 1000
    temperature = request.temperature or 0.6
    top_p = request.top_p or 1.0
    n = request.n or 1
    stream = request.stream or False
    tools = request.tools
    functions = request.functions
    function_call = request.function_call
    debug = request.debug or False

    # Validate model
    available_model_ids = [m["id"] for m in AVAILABLE_MODELS]
    if model not in available_model_ids:
        raise HTTPException(status_code=400, detail=f"Model {model} not available")

    request_id = f"chatcmpl-{uuid.uuid4().hex}"

    try:
        # Prepare API request parameters
        chat_url, params, headers, rollout_n = prepare_api_request_params(
            user_id=USER_ID,
            token=TOKEN,
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            tools=tools,
            functions=functions,
            function_call=function_call,
        )

        # Call the backend API directly
        res = api_request(
            url=chat_url,
            params=params,
            headers=headers,
            timeout=100,
        )
        res.raise_for_status()

        choices = process_api_response_to_choices(
            res,
            url=chat_url,
            model=model,
            debug=debug,
            rollout_n=rollout_n,
        )
        responses = process_api_choices(choices, model, n, rollout_n)

        if stream:
            return StreamingResponse(
                create_chat_completion_stream(
                    responses, model, request_id,
                ),
                media_type="text/plain",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:

            if all(r is None for r in responses):
                raise HTTPException(status_code=500, detail="Failed to get valid response from backend")
            # Non-streaming response
            completion = create_chat_completion_response(
                responses, model, request_id,
                prompt_tokens=len(str(messages)),  # Rough estimation
                completion_tokens=sum(len(str(r)) for r in responses if r)  # Rough estimation
            )
            return completion

    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "authenticated": USER_ID is not None and TOKEN is not None}


if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv

    load_dotenv()
    parser = argparse.ArgumentParser(description="Run the FastAPI server for OpenAI API proxy")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8777)
    args = parser.parse_args()

    uvicorn.run(
        "deeplin.inference_engine.hexin_server:app",
        host=args.host,
        port=args.port,
        reload=True,
        log_level="info",
    )
