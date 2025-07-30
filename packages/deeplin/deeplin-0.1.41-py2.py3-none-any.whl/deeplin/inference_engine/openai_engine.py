import os
import openai


from deeplin.inference_engine.base import InferenceEngine


class OpenAIApiInferenceEngine(InferenceEngine):
    def __init__(self, model: str, max_tokens: int, temperature: float, top_p: float = 1.0):
        self.model = model
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    def inference(self, prompts: list[str] | list[list[dict]], n=1, **kwargs) -> list[list[str]]:
        responses = []
        for prompt in prompts:
            if not prompt:
                responses.append([None] * n)
                continue
            if isinstance(prompt, dict):
                messages = [prompt]
            elif isinstance(prompt, str):
                messages = [{"role": "user", "content": prompt}]
            elif isinstance(prompt, list):
                messages = prompt
            else:
                raise ValueError(f"Invalid prompt format: {prompt}")
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", self.temperature),
                top_p=kwargs.get("top_p", self.top_p),
                stop=kwargs.get("stop", None),
                n=n,
                stream=False,
            )
            n_responds = []
            for i in range(n):
                msg = response.choices[i].message
                content = msg["content"] if "content" in msg else ""
                if "reasoning_content" in msg:
                    reasoning_content = msg["reasoning_content"]
                    content = f"<think>\n{reasoning_content}\n</think>\n{content}"
                n_responds.append(content)
            responses.append(n_responds)
        return responses
