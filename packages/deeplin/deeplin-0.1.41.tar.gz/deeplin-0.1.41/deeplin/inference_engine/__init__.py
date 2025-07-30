from deeplin.inference_engine.base import InferenceEngine


def build_inference_engine(
    engine: str,
    model: str,
    max_tokens: int = 512,
    temperature: float = 0.6,
    top_p: float = 1.0,
    tensor_parallel_size: int = 1,
    max_model_len: int = 8192,
    gpu_memory_utilization: float = 0.95,
    **kwargs,
) -> InferenceEngine:
    """Build inference engine based on the provided arguments."""
    if engine == "openai":
        from .openai_engine import OpenAIApiInferenceEngine

        return OpenAIApiInferenceEngine(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
    elif engine == "vllm":
        from .vllm_engine import vllmInferenceEngine

        return vllmInferenceEngine(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            tensor_parallel_size=tensor_parallel_size,
            max_model_len=max_model_len,
            gpu_memory_utilization=gpu_memory_utilization,
            **kwargs,
        )
    elif engine == "api":
        from .hexin_engine import ApiInferenceEngine

        return ApiInferenceEngine(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
    else:
        raise ValueError(f"Unknown engine: {engine}")


def batch_inference(
    inference_engine: InferenceEngine,
    rows: list[dict],
    prompt_key: str="prompt",
    n: int = 1,
    **kwargs,
):
    """Perform batch inference using the provided inference engine."""
    prompts = [row[prompt_key] for row in rows]
    responses = inference_engine.inference(prompts, n=n, **kwargs)
    for row, n_responses in zip(rows, responses):
        choices: list[dict] = row.get("choices", [])
        start_idx = len(choices)
        for i, response in enumerate(n_responses):
            response_message = {
                "index": start_idx + i,
                "message": {
                    "role": "assistant",
                    "content": [{"type": "text", "text": response}],
                },
            }
            choices.append(response_message)
        row["choices"] = choices
    return rows
