"""
converse_api.py
---------------
Demonstrates the Bedrock **Converse API** — the recommended way to interact
with foundation models because it is model-agnostic and supports multi-turn
conversations out of the box.

The same code works with Claude, Amazon Titan, Mistral, Meta Llama, etc.
without changing the request structure.

Usage:
    python converse_api.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    BEDROCK_MODEL_ID     – Model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)
"""

import os

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
)


def converse(messages: list[dict], system_prompt: str | None = None) -> str:
    """
    Send a list of *messages* to the model and return the assistant reply.

    Args:
        messages: List of ``{"role": "user"|"assistant", "content": [{"text": "..."}]}``
                  dicts that represent the conversation history.
        system_prompt: Optional system-level instruction.

    Returns:
        The assistant's response as a plain string.
    """
    client = boto3.client("bedrock-runtime", region_name=REGION)

    kwargs: dict = {
        "modelId": MODEL_ID,
        "inferenceConfig": {"maxTokens": 512, "temperature": 0.7},
        "messages": messages,
    }

    if system_prompt:
        kwargs["system"] = [{"text": system_prompt}]

    response = client.converse(**kwargs)
    return response["output"]["message"]["content"][0]["text"]


def _user_msg(text: str) -> dict:
    return {"role": "user", "content": [{"text": text}]}


def _assistant_msg(text: str) -> dict:
    return {"role": "assistant", "content": [{"text": text}]}


if __name__ == "__main__":
    system = (
        "You are a helpful cloud architecture assistant. "
        "Keep answers concise and accurate."
    )

    print(f"Model : {MODEL_ID}\n")

    # --- Turn 1 ---
    turn1 = "What is AWS Bedrock and what problem does it solve?"
    messages: list[dict] = [_user_msg(turn1)]
    print(f"User  : {turn1}")

    reply1 = converse(messages, system_prompt=system)
    print(f"Model : {reply1}\n")

    # --- Turn 2 (multi-turn: keep history) ---
    messages.append(_assistant_msg(reply1))
    turn2 = "Which foundation models does it support?"
    messages.append(_user_msg(turn2))
    print(f"User  : {turn2}")

    reply2 = converse(messages, system_prompt=system)
    print(f"Model : {reply2}\n")
