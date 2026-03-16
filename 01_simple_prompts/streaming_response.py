"""
streaming_response.py
---------------------
Demonstrates **streaming** responses from AWS Bedrock using
`bedrock-runtime.converse_stream`.

Tokens are printed to the terminal as they arrive, which gives a better user
experience for long-form answers.

Usage:
    python streaming_response.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    BEDROCK_MODEL_ID     – Model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)
"""

import os
import sys

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
)
PROMPT = (
    "Write a short poem (4–6 lines) about cloud computing and the future of AI."
)


def stream_response(prompt: str) -> str:
    """
    Stream the model's response token-by-token, printing each chunk as it
    arrives.  Returns the complete response text when done.
    """
    client = boto3.client("bedrock-runtime", region_name=REGION)

    messages = [{"role": "user", "content": [{"text": prompt}]}]

    response = client.converse_stream(
        modelId=MODEL_ID,
        inferenceConfig={"maxTokens": 512, "temperature": 0.9},
        messages=messages,
    )

    full_text = []

    print("Response (streaming):\n")
    for event in response["stream"]:
        if "contentBlockDelta" in event:
            delta = event["contentBlockDelta"].get("delta", {})
            token = delta.get("text", "")
            print(token, end="", flush=True)
            full_text.append(token)
        elif "messageStop" in event:
            stop_reason = event["messageStop"].get("stopReason", "")
            print(f"\n\n[Stop reason: {stop_reason}]")

    return "".join(full_text)


if __name__ == "__main__":
    print(f"Model : {MODEL_ID}")
    print(f"Prompt: {PROMPT}\n")

    try:
        stream_response(PROMPT)
    except KeyboardInterrupt:
        print("\n[Interrupted]")
        sys.exit(0)
