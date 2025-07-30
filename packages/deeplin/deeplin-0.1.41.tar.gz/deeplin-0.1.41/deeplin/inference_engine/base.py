class InferenceEngine:
    def inference(self, prompts: list[str | list[dict]], n=1, **kwargs) -> list[list[str] | str]:
        raise NotImplementedError("For each prompt, return n responses. If n=1, the return is a list of one element list of strings.")

    def inference_one(self, prompt: str | list[dict] | list[str | list[dict]], **kwargs) -> list[str] | str:
        # This function is used to get one response for each prompt.
        if isinstance(prompt, str):
            prompts = [{"role": "user", "content": prompt}]
        elif isinstance(prompt, list):
            if isinstance(prompt[0], dict):
                prompts = [prompt]
            else:
                prompts = prompt
        response = self.inference(prompts, n=1, **kwargs)
        if isinstance(response, list) and len(response) == 1:
            return response[0]
        return response

    def __call__(self, prompts: list[str | list[dict]], n=1, **kwargs) -> list[list[str] | str]:
        response = self.inference(prompts, n=n, **kwargs)
        return response if isinstance(response, list) else [response]
