from functools import partial
import json
from typing import Any, Dict, List, Optional, Union
import requests
import os

from loguru import logger
from requests import Response
from xlin import element_mapping

from deeplin.inference_engine.base import InferenceEngine


def get_userid_and_token(
    app_url,
    app_id,
    app_secret,
):
    d = {"app_id": app_id, "app_secret": app_secret}
    h = {"Content-Type": "application/json"}
    r = requests.post(app_url, json=d, headers=h)
    data = r.json()["data"]
    return data["user_id"], data["token"]


def retry_request(func):
    def wrapper(*args, **kwargs):
        max_retry = kwargs.get("max_retry", 3)
        debug = kwargs.get("debug", False)
        for i in range(max_retry):
            try:
                result = func(*args, **kwargs)
                if not result:
                    if debug:
                        logger.error(f"Function {func.__name__} returned None, retrying {i + 1}/{max_retry}...")
                    continue
                # logger.debug(f"Function {func.__name__} succeeded on attempt {i + 1}.")
                return result
            except Exception as e:
                if debug:
                    logger.error(f"Request failed: {e}, retrying {i + 1}/{max_retry}...")
        if debug:
            logger.error("Max retries reached, returning None.")
        return None

    return wrapper


def api_request(
    url: str,
    params: dict,
    headers: dict,
    timeout: int = 100,
):
    res = requests.post(
        url,
        json=params,
        headers=headers,
        timeout=timeout,
    )
    return res


def prepare_api_request_params(
    user_id: str,
    token: str,
    messages: List[Dict[str, Any]],
    model: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    n: int,
    stream: bool = False,
    multi_modal: bool = False,
    tools: Optional[List[Dict[str, Any]]] = None,
    functions: Optional[List[Dict[str, Any]]] = None,
    function_call: Optional[Union[str, Dict[str, Any]]] = None,
) -> tuple[str, dict, dict, int]:
    """Prepare parameters for api_request based on model type"""

    # Base parameters
    params = {
        "messages": messages,
        "temperature": temperature,
        "model": model,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "n": n,
        "stream": stream,
    }

    if tools:
        params["tools"] = tools
    if functions:
        params["functions"] = functions
    if function_call:
        params["function_call"] = function_call

    rollout_n = None
    version = "v3"

    # Model-specific handling (copied from hexin_engine.py)
    if model == "claude":
        symbol = "claude"
        params["model"] = "claude-3-7-sonnet@20250219"
        params["anthropic_version"] = "vertex-2023-10-16"
        version = "v3"
        rollout_n = params.pop("n", None)
    elif "doubao" in model or model in [
        "ep-20250204210426-gclbn",
        "ep-20250410151344-fzm9z",
        "ep-20250410145517-rpbrz",
        "deepseek-reasoner",
        "deepseek-chat",
    ]:
        symbol = "doubao"
        version = "v3"
        if "r1" in model or "reasoner" in model:
            params["model"] = "ep-20250410145517-rpbrz"
            rollout_n = params.pop("n", None)
        elif "v3" in model or "chat" in model:
            params["model"] = "ep-20250410151344-fzm9z"
    elif model == "r1-qianfan":
        symbol = "qianfan"
        params["model"] = "deepseek-r1"
        rollout_n = params.pop("n", None)
    elif model == "gemini":
        symbol = "gemini"
        params["model"] = "gemini-2.5-pro-preview-03-25"
    elif model in ["gpt-4o-mini", "o3", "o4-mini"]:
        del params["max_tokens"]
        params["max_completion_tokens"] = max_tokens
        symbol = "chatgpt"
        if model in ["o3", "o4-mini"]:
            del params["temperature"]
    else:
        symbol = "chatgpt"

    # Build URL

    if multi_modal:
        chat_url = "https://arsenal-openai.10jqka.com.cn:8443/vtuber/ai_access/chatgpt/v1/picture/chat/completions"
    else:
        chat_url = f"https://arsenal-openai.10jqka.com.cn:8443/vtuber/ai_access/{symbol}/{version}/chat/completions"

    # Build headers
    headers = {"Content-Type": "application/json", "userId": user_id, "token": token}

    return chat_url, params, headers, rollout_n


def process_api_response_to_choices(res: Response, url: str, model: str, debug: bool, rollout_n: Optional[int] = None):
    resp = res.json()
    if "data" in resp:
        resp = resp["data"]
    if debug or "choices" not in resp:
        logger.debug(f"API request to {repr(url)} returned: {json.dumps(resp, ensure_ascii=False, indent=2)}")
    if rollout_n is not None:
        if model == "claude" and "content" in resp:
            if isinstance(resp["content"], list) and len(resp["content"]) == 1 and resp["content"][0].get("type") == "text":
                resp["content"] = resp["content"][0]["text"]
            resp["choices"] = [{"message": resp}]
    choices: list = resp.get("choices", [])
    if debug:
        logger.debug(f"API request to {repr(url)} returned choices: {json.dumps(choices, ensure_ascii=False, indent=2)}")
    if len(choices) == 0:
        return None
    return choices


def process_api_choices(choices: List[Dict], model: str, n: int, rollout_n: Optional[int] = None) -> List[str]:
    """Process choices from api_request into standardized format"""
    if not choices:
        return [None] * n

    # Handle special case for models that need rollout_n processing
    if rollout_n is not None:
        if model == "claude" and len(choices) > 0 and "content" in choices[0]:
            content = choices[0]["content"]
            if isinstance(content, list) and len(content) == 1 and content[0].get("type") == "text":
                content = content[0]["text"]
            choices = [{"message": {"content": content, "role": "assistant"}}]

    responses = []
    for i in range(min(n, len(choices))):
        item = choices[i]
        if "message" in item:
            message = item["message"]
            content = message.get("content", "")
            reasoning_content = message.get("reasoning_content", "")

            # Handle reasoning content
            if reasoning_content:
                content = f"<think>\n{reasoning_content}\n</think>\n{content}"

            # Handle function calls and tool calls
            if "function_call" in message:
                content = message["function_call"]
            elif "tool_calls" in message:
                content = message["tool_calls"]
        elif "text" in item:
            content = item["text"]
        else:
            content = item

        responses.append(content)

    # Fill remaining slots with None if needed
    if len(responses) < n:
        responses += [None] * (n - len(responses))

    return responses


def support_n_sampling(model: str):
    models = [
        "doubao-deepseek-r1",
        "ep-20250410145517-rpbrz",
        "deepseek-reasoner",
        "doubao-deepseek-v3",
        "ep-20250410151344-fzm9z",
        "deepseek-chat",
        "r1-qianfan",
        "claude",
    ]
    return model in models


@retry_request
def api_inference(
    user_id: str,
    token: str,
    input_message: list[dict],
    model: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
    n: int,
    multi_modal: bool = False,
    tools: list[dict] | None = None,
    functions: list[dict] | None = None,
    function_call: str | None = None,
    timeout: int = 60,
    debug: bool = False,
    max_retry: int = 3,
):
    chat_url, params, headers, rollout_n = prepare_api_request_params(
        user_id=user_id,
        token=token,
        messages=input_message,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        n=n,
        multi_modal=multi_modal,
        tools=tools,
        functions=functions,
        function_call=function_call,
    )
    res = api_request(
        url=chat_url,
        params=params,
        headers=headers,
        timeout=timeout,
    )
    choices = process_api_response_to_choices(
        res,
        url=chat_url,
        model=model,
        debug=debug,
        rollout_n=rollout_n,
    )
    responses = process_api_response_to_choices(
        choices,
        chat_url,
        model,
        debug,
        rollout_n,
    )
    return responses


class ApiInferenceEngine(InferenceEngine):
    def __init__(self, model: str, max_tokens: int, temperature: float = 0.6, top_p: float = 1.0):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        app_url = os.getenv("HITHINK_APP_URL")
        app_id = os.getenv("HITHINK_APP_ID")
        app_secret = os.getenv("HITHINK_APP_SECRET")
        if app_id is None or app_secret is None:
            raise ValueError("HITHINK_APP_ID and HITHINK_APP_SECRET must be set in environment variables.")
        self.user_id, self.token = get_userid_and_token(app_url=app_url, app_id=app_id, app_secret=app_secret)
        logger.debug(f"User ID: {self.user_id}, Token: {self.token}")
        available_models = [
            "gpt-3.5-turbo",
            "gpt4o",
            "o3",
            "o4-mini",
            "gpt4",
            "claude",
            "gemini",
            "doubao-deepseek-r1",
            "ep-20250204210426-gclbn",
            "deepseek-reasoner",  # deepseek-reasoner
            "doubao-deepseek-v3",
            "ep-20250410145517-rpbrz",
            "deepseek-chat",  # deepseek-chat
            "r1-qianfan",
        ]
        if model not in available_models:
            logger.warning(f"Model {model} is not available. Please choose from {available_models}.")

    def inference(self, prompts: list[str] | list[list[dict]], n=1, **kwargs) -> list[list[str]]:
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        temperature = kwargs.get("temperature", self.temperature)
        top_p = kwargs.get("top_p", self.top_p)
        timeout = kwargs.get("timeout", 100)
        max_retry = kwargs.get("max_retry", 3)
        debug = kwargs.get("debug", False)
        multi_modal = kwargs.get("multi_modal", False)
        tools = kwargs.get("tools", None)
        functions = kwargs.get("functions", None)
        function_call = kwargs.get("function_call", None)
        if debug:
            logger.warning(f"supports n sampling: {support_n_sampling(model)}")
        messages_list = []
        for prompt in prompts:
            if isinstance(prompt, dict):
                messages_list.append([prompt])
            elif isinstance(prompt, str):
                messages_list.append([{"role": "user", "content": prompt}])
            elif isinstance(prompt, list):
                messages_list.append(prompt)
            else:
                messages_list.append(prompt)

        def f(messages: list[dict]):
            if not messages:
                return True, [None] * n
            return True, api_inference(
                user_id=self.user_id,
                token=self.token,
                input_message=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                timeout=timeout,
                multi_modal=multi_modal,
                debug=debug,
                max_retry=max_retry,
                tools=tools,
                functions=functions,
                function_call=function_call,
            )

        def g(messages: list[dict]):
            if not messages:
                return True, None
            results = api_inference(
                user_id=self.user_id,
                token=self.token,
                input_message=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=1,
                timeout=timeout,
                multi_modal=multi_modal,
                debug=debug,
                max_retry=max_retry,
                tools=tools,
                functions=functions,
                function_call=function_call,
            )
            return True, results[0] if len(results) > 0 else None

        if support_n_sampling(model):
            n_messages_list = sum([messages_list for _ in range(n)], [])
            n_responses = element_mapping(n_messages_list, g)
            num = len(messages_list)
            responses = []
            for i in range(num):
                responses_i = []
                for j in range(n):
                    responses_i.append(n_responses[i + j * num])
                responses.append(responses_i)
            return responses
        responses = element_mapping(messages_list, f)
        return responses


from PIL import Image
from io import BytesIO
import base64


def image2base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


if __name__ == "__main__":
    # engine = ApiInferenceEngine(model="o3", max_tokens=1000)
    # path = "/Users/lxy/Documents/GitHub/LinXueyuanStdio/deeplin/assets/kline.png"
    # image = Image.open(path)
    # base64image = image2base64(image)
    # prompt = "What is in the image?"
    # messages = [
    #     {
    #         "role": "user",
    #         "content": [
    #             {"type": "image_url", "image_url": base64image},
    #             {"type": "text", "text": prompt},
    #         ]
    #      },
    # ]
    # response = engine.inference([messages], n=1, multi_modal=True, debug=True)[0][0]
    # print(response)
    from dotenv import load_dotenv

    load_dotenv("../../.env")
    load_dotenv(".env")

    tools = [
        {
            "type": "function",
            "function": {
                "name": "Search",
                "description": "通过搜索引擎搜索互联网上的内容。当知识无法回答用户提出的问题，或用户请求联网搜索时调用此工具。",
                "parameters": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "要搜索的文本内容。",
                        }
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "CodeInterpreter",
                "description": "在受限、安全的沙盒环境中执行 Python 3 代码的解释器，可用于数据处理、科学计算、自动化脚本、可视化等任务，支持大多数标准库及常见第三方科学计算库。你能看见之前已经执行的代码和执行结果，在生成新的代码时，请直接使用之前的变量名，而不是重新定义变量。",
                "parameters": {
                    "type": "object",
                    "required": ["code"],
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "要执行的 Python 代码。",
                        }
                    },
                },
            },
        },
    ]
    functions = [tool["function"] for tool in tools]

    # engine = ApiInferenceEngine(model="deepseek-chat", max_tokens=1000)
    engine = ApiInferenceEngine(model="gemini", max_tokens=1000)
    prompts = [
        # "我正在调试 function call api 功能。你的命名空间有哪些？你能用的工具有哪些？列出你的所有命名空间和每个命名空间下的内容，最后请写出用户定义的function call工具的名称和描述。除了用户的工具，你还能用哪些工具？给出每个工具的名称和描述。",
        # "使用搜索工具 *并行同时分别* 查比特币的新闻和以太币的新闻",
        # "发起多个 function calls, 并行搜索比特币最新新闻和以太币最新新闻",
        # "我正在调试 function call api 功能。please list The content of the namespaces you have, and the tools you can use. List all your namespaces and the content under each namespace, and finally write the name and description of the user-defined function call tool. Besides the user's tools, what other tools can you use? Give the name and description of each tool.",
        # "你好",
        # "你能用代码解释器（python tool）吗",
        # "你能看见的工具有哪些。除了 functions 命名空间外，你还有哪些命名空间？"
    ] + [
        # f"你能使用的工具有哪些？请写出第{i + 1}个工具的名称和描述" for i in range(10)
    ]
    # response = engine.inference(prompts, n=1, model="gpt-4o-mini", debug=True,  tools=tools)
    response = engine.inference(prompts, n=1, model="o3", debug=True, tools=tools)
    # [
    #   {
    #     "function": {
    #       "arguments": "{\"query\":\"比特币 最新 新闻\"}",
    #       "name": "Search"
    #     },
    #     "id": "call_489gSUJExpN0XE9PbZCnWtNd",
    #     "type": "function"
    #   }
    # ]
    print(json.dumps(response, ensure_ascii=False, indent=2))
    # response = engine.inference([messages], n=1, model="gemini", debug=True)[0][0]
    # print(response)