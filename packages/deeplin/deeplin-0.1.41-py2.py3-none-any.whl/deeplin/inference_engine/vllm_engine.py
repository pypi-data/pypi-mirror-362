from loguru import logger

from deeplin.inference_engine.base import InferenceEngine

try:
    from vllm import LLM, SamplingParams
except ImportError:
    logger.warning("VLLM not installed. Please install vllm with 'pip install vllm'.")



class vllmInferenceEngine(InferenceEngine):
    def __init__(self,
                 model: str,
                 max_tokens: int,
                 temperature: float,
                 top_p: float,
                 tensor_parallel_size: int,
                 max_model_len: int,
                 gpu_memory_utilization: float = 0.95,
                 **kwargs):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.llm = LLM(
            model=model,
            tensor_parallel_size=tensor_parallel_size,
            max_model_len=max_model_len,
            gpu_memory_utilization=gpu_memory_utilization,
            enforce_eager=False,
            **kwargs,
        )

    def inference(self, prompts: list[str] | list[list[dict]], n=1, **kwargs) -> list[list[str]]:
        not_none_index = [i for i, prompt in enumerate(prompts) if prompt is not None]
        # If all prompts are None, return a list of None
        if len(not_none_index) == 0:
            return [[None] * n for _ in range(len(prompts))]
        sampling_params = SamplingParams(
            temperature=kwargs.get("temperature", self.temperature),
            top_p=kwargs.get("top_p", self.top_p),
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            n=n,
        )
        outputs = self.llm.generate(prompts, sampling_params)
        responses = []
        for output in outputs:
            n_responses = []
            for i in range(n):
                n_responses.append(output.outputs[i].text)
            responses.append(n_responses)
        # If all prompts are not None, return the responses
        if len(not_none_index) == len(prompts):
            return responses
        # If some prompts are None, return the responses for the non-None prompts and None for the None prompts
        # and keep the order of the original prompts
        final_responses = []
        for i in range(len(prompts)):
            if i in not_none_index:
                final_responses.append(responses[not_none_index.index(i)])
            else:
                final_responses.append([None] * n)
        return final_responses
