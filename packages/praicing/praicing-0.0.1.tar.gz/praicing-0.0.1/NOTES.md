# Notes

- https://github.com/joaopalmeiro/template-python-uv-package
- https://openai.com/api/pricing/
  - https://platform.openai.com/docs/guides/images-vision?api-mode=chat#calculating-costs
- https://github.com/nerveband/token-vision
- https://docs.together.ai/docs/vision-overview#pricing
- https://github.com/AgentOps-AI/tokencost
- https://github.com/pydantic/genai-prices
  - https://github.com/pydantic/genai-prices/blob/main/prices/providers/openai.yml
  - https://github.com/Helicone/helicone/tree/main/packages/cost
  - https://github.com/pydantic/genai-prices/blob/75fe8876b535c11534ecbc2310cdaa80ceabeaa9/packages/python/genai_prices/types.py#L256
  - https://docs.python.org/3/library/decimal.html: "The decimal module provides support for fast correctly rounded decimal floating-point arithmetic. It offers several advantages over the float datatype:"
- https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
- https://github.com/huggingface/tokenizers
- https://docs.anthropic.com/en/docs/build-with-claude/token-counting
- https://docs.anthropic.com/en/docs/build-with-claude/vision
  - "Very small images under 200 pixels on any given edge may degrade performance."
- https://www.stainless.com/
- https://platform.openai.com/docs/advanced-usage/managing-tokens#managing-tokens
  - https://platform.openai.com/tokenizer
- https://platform.openai.com/docs/pricing
- https://github.com/openai/openai-python?tab=readme-ov-file#using-types
  - https://pypi.org/project/openai/
  - https://github.com/openai/openai-python/blob/v1.97.0/src/openai/types/chat/chat_completion_message_param.py
  - https://github.com/openai/openai-python/blob/v1.97.0/src/openai/types/chat/chat_completion_user_message_param.py
  - https://github.com/openai/openai-python/blob/v1.97.0/src/openai/types/chat/chat_completion_content_part_image_param.py
  - [Add GPT-4.1 support](https://github.com/openai/tiktoken/issues/395) issue
  - https://huggingface.co/datasets/openai/mrcr#how-to-run: `MODEL= "gpt-4.1"` + `enc = tiktoken.get_encoding("o200k_base")`
  - https://community.openai.com/t/whats-the-tokenization-algorithm-gpt-4-1-uses/1245758: "GPT-4.1 uses the same tokenizer as 4o; same encoding."
  - https://github.com/openai/openai-python/blob/v1.97.0/src/openai/types/chat/completion_create_params.py#L37: `messages: Required[Iterable[ChatCompletionMessageParam]]`
  - https://github.com/openai/openai-python/blob/v1.97.0/api.md?plain=1#L42
- https://mypy.readthedocs.io/en/stable/typed_dict.html:
  - "Since TypedDicts are really just regular dicts at runtime, it is not possible to use `isinstance` checks to distinguish between different variants of a Union of TypedDict in the same way you can with regular objects."
  - https://mypy.readthedocs.io/en/stable/literal_types.html#tagged-unions

## Commands

```bash
python scripts/generate_images.py
```

### Clean slate

```bash
rm -rf .mypy_cache/ .ruff_cache/ .venv/ dist/ src/praicing/__pycache__/
```

## Snippets

- https://huggingface.co/datasets/openai/mrcr

```python
def n_tokens(messages : list[dict]) -> int:
    """
    Count tokens in messages.
    """
    return sum([len(enc.encode(m["content"])) for m in messages])
```

```python
from decimal import Decimal


def estimate_costs_for_messages(
    messages: Iterable[ChatCompletionMessageParam],
    model: str,
    pricing: Literal["base", "batch"] = "base",
) -> Decimal:
    total_tokens = count_tokens_for_messages(messages, model)

    # Source: https://github.com/pydantic/genai-prices/blob/v0.0.3/packages/python/genai_prices/types.py#L256-L271
    input_cost = COSTS_MTOK[model][pricing]["input"]
    total_cost = (Decimal(input_cost) * total_tokens) / 1_000_000

    print((input_cost * total_tokens) / 1_000_000)

    return total_cost
```
