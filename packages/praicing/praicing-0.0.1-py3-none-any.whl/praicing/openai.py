import math
from collections.abc import Iterable
from typing import Literal, TypedDict
from urllib.request import urlopen

import tiktoken
from openai.types.chat import ChatCompletionMessageParam
from PIL import Image


class Tokens(TypedDict):
    base: int
    tile: int


COSTS_MTOK = {
    "gpt-4o-2024-08-06": {
        "base": {
            "input": 2.5,
            "output": 10,
        },
        "batch": {
            "input": 1.25,
            "output": 5,
        },
    },
    "gpt-4.1-mini-2025-04-14": {
        "base": {
            "input": 0.4,
            "output": 1.6,
        },
        "batch": {
            "input": 0.2,
            "output": 0.8,
        },
    },
    "gpt-4.1-nano-2025-04-14": {
        "base": {
            "input": 0.1,
            "output": 0.4,
        },
        "batch": {
            "input": 0.05,
            "output": 0.2,
        },
    },
}

TOKENS: dict[str, Tokens] = {"gpt-4o-2024-08-06": {"base": 85, "tile": 170}}

PATCH_SIZE = 32
MAX_PATCHES = 1536

MULTIPLIERS = {"gpt-4.1-mini-2025-04-14": 1.62, "gpt-4.1-nano-2025-04-14": 2.46}

MODELS_WITH_DETAIL = [*TOKENS]
MODELS_WITH_PATCHES = [*MULTIPLIERS]


def count_tokens_for_image_with_detail(
    image_url: str, model: str, detail: Literal["low", "high"]
) -> int:
    # Source: https://platform.openai.com/docs/guides/images-vision?api-mode=chat#gpt-4o-gpt-4-1-gpt-4o-mini-cua-and-o-series-except-o4-mini

    if detail == "low":
        # "Regardless of input size, low detail images are a fixed cost."
        return TOKENS[model]["base"]

    with Image.open(urlopen(image_url)) as img:
        width, height = img.size

    # "1. Scale to fit in a 2048px x 2048px square, maintaining original aspect ratio"
    max_dim = max(width, height)
    if max_dim > 2048:
        scale_factor = 2048 / max_dim
        width = int(width * scale_factor)
        height = int(height * scale_factor)

    # "2. Scale so that the image's shortest side is 768px long"
    min_dim = min(width, height)
    if min_dim > 768:
        scale_factor = 768 / min_dim
        width = int(width * scale_factor)
        height = int(height * scale_factor)

    # "3. Count the number of 512px squares in the image"
    tiles_wide = math.ceil(width / 512)
    tiles_high = math.ceil(height / 512)
    total_tiles = tiles_wide * tiles_high

    # "4. Add the base tokens to the total"
    total_tokens = TOKENS[model]["base"] + total_tiles * TOKENS[model]["tile"]

    return total_tokens


def count_tokens_for_image_with_patches(image_url: str, model: str) -> int:
    # Source: https://platform.openai.com/docs/guides/images-vision?api-mode=chat#gpt-4-1-mini-gpt-4-1-nano-o4-mini

    with Image.open(urlopen(image_url)) as img:
        width, height = img.size

    # "A. Calculate the number of 32px x 32px patches that are needed to fully cover the image"
    raw_patches_width = math.ceil(width / PATCH_SIZE)
    raw_patches_height = math.ceil(height / PATCH_SIZE)
    raw_patches = raw_patches_width * raw_patches_height

    # "B. If the number of patches exceeds 1536, we scale down the image so that it can be covered by no more than 1536 patches"
    if raw_patches > MAX_PATCHES:
        r = math.sqrt((PATCH_SIZE**2) * MAX_PATCHES / (width * height))

        r = r * min(
            math.floor(width * r / PATCH_SIZE) / (width * r / PATCH_SIZE),
            math.floor(height * r / PATCH_SIZE) / (height * r / PATCH_SIZE),
        )

        width = width * r
        height = height * r

    # "C. The token cost is the number of patches, capped at a maximum of 1536 tokens"
    patches_width = math.ceil(width / PATCH_SIZE)
    patches_height = math.ceil(height / PATCH_SIZE)
    patches = patches_width * patches_height
    patches = min(patches, MAX_PATCHES)

    total_tokens = math.ceil(patches * MULTIPLIERS[model])

    return total_tokens


def count_tokens_for_text(text: str, model: str) -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")

    return len(encoding.encode(text))


def count_tokens_for_messages(
    messages: Iterable[ChatCompletionMessageParam], model: str
) -> int:
    total_tokens = 0

    for message in messages:
        if message["role"] == "user":
            if isinstance(message["content"], str):
                total_tokens += count_tokens_for_text(message["content"], model)
            else:
                for part in message["content"]:
                    if part["type"] == "text":
                        total_tokens += count_tokens_for_text(part["text"], model)
                    elif part["type"] == "image_url":
                        if model in MODELS_WITH_DETAIL:
                            total_tokens += count_tokens_for_image_with_detail(
                                part["image_url"]["url"],
                                model,
                                part["image_url"]["detail"],
                            )
                        elif model in MODELS_WITH_PATCHES:
                            total_tokens += count_tokens_for_image_with_patches(
                                part["image_url"]["url"], model
                            )

    return total_tokens


def estimate_costs_for_messages(
    messages: Iterable[ChatCompletionMessageParam],
    model: str,
    pricing: Literal["base", "batch"] = "base",
) -> float:
    total_tokens = count_tokens_for_messages(messages, model)

    input_cost = COSTS_MTOK[model][pricing]["input"]
    total_cost = (input_cost * total_tokens) / 1_000_000

    return total_cost
