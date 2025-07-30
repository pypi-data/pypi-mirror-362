from pathlib import Path
from typing import Callable
from functools import partial

from transformers import AutoTokenizer

from xlin import xmap, draw_histogram


def token_counts(texts: list[str], tokenizer, **kwargs) -> list[int]:
    # 批量分词
    encoded_inputs = tokenizer(texts, **kwargs)

    # 统计每个文本的 token 数
    token_counts = [len(input_ids) for input_ids in encoded_inputs["input_ids"]]

    return token_counts


def assign_token_count(
    rows: list[dict],
    text_fn: Callable[[dict[str, str]], str],
    tokenizer,
) -> list[dict]:
    texts = [text_fn(row) for row in rows]
    inputs = tokenizer(texts, add_special_tokens=False)
    filtered_rows = []
    for row, input_ids in zip(rows, inputs["input_ids"]):
        row["token_count"] = len(input_ids)
        filtered_rows.append(row)
    return filtered_rows


def response_text_fn(row: dict[str, str]) -> str:
    return row["messages"][-1]["content"]


def draw_token_count_histogram(
    tokenizer_path: str,
    jsonlist: list[dict[str, str]],
    text_fn: Callable[[dict[str, str]], str],
    output_path: str,
):
    """
    统计文本长度分布并绘制直方图
    :param jsonlist: jsonlist
    :param text_fn: 文本函数
    :param output_dir: 输出目录
    """
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    assign_token_count_fn = partial(
        assign_token_count, text_fn=text_fn, tokenizer=tokenizer
    )
    rows = xmap(
        jsonlist,
        assign_token_count_fn,
        max_workers=16,
        is_batch_work_func=True,
    )
    lengths = [row["token_count"] for row in rows]
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    draw_histogram(
        lengths,
        bins=100,
        title="Token Count Distribution",
        fig_save_path=output_path,
    )


if __name__ == "__main__":
    from xlin import load_json_or_jsonl
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Token count statistics")
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the input JSONL file",
    )
    parser.add_argument(
        "--tokenizer_path",
        type=str,
        required=True,
        help="Path to the tokenizer model",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="token_count_histogram.png",
        help="Path to the output histogram file",
    )
    args = parser.parse_args()
    data_path = Path(args.data_path)
    jsonlist = load_json_or_jsonl(data_path)
    draw_token_count_histogram(
        args.tokenizer_path,
        jsonlist,
        response_text_fn,
        args.output_path,
    )

    print(f"Token count histogram saved to: {args.output_path}")
