import argparse

from dotenv import load_dotenv
from loguru import logger

from deeplin.inference_engine import build_inference_engine


load_dotenv()


def main(args):
    """
    1. read data: [{"prompt": "<|im_start|>user\n\nprompt", "messages": [{"role": "user", "content": "prompt"}]}]
    2. build inference engine
    3. run inference
    4. save results at key 'choices': [{"index": 0, "message": {"role": "assistant", "content": "<think> reasoning process here </think><answer> answer here </answer>"}}]
    """
    batch_size = args.batch_size
    inference_engine = build_inference_engine(
        engine=args.engine,
        model=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        tensor_parallel_size=args.tensor_parallel_size,
    )
    results = inference_engine.inference(
        [args.prompt],
        n=args.n,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        timeout=args.timeout,
        debug=args.debug,
    )
    logger.info(f"Results: {results}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inference script")
    parser.add_argument(
        "--engine",
        type=str,
        choices=["vllm", "api", "openai"],
        default="vllm",
        help="Inference engine to use",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name or path. r1 is ep-20250204210426-gclbn",
    )
    parser.add_argument(
        "--max_tokens", type=int, default=8192, help="Maximum number of tokens"
    )
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for VLLM")
    parser.add_argument(
        "--temperature", type=float, default=0.6, help="Temperature for sampling"
    )
    parser.add_argument(
        "--top_p", type=float, default=1.0, help="Top-p (nucleus) sampling"
    )
    parser.add_argument(
        "--tensor_parallel_size",
        type=int,
        default=1,
        help="Tensor parallel size for VLLM",
    )
    parser.add_argument(
        "--n", type=int, default=1, help="Number of responses to generate"
    )
    parser.add_argument(
        "--timeout", type=int, default=100, help="Timeout for API requests"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--prompt",
        type=str,
        default="introduce yourself",
        help="Key for the prompt in the input data",
    )

    args = parser.parse_args()

    main(args)
