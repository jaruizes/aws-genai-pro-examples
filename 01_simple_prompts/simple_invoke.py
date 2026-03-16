"""
simple_invoke.py
----------------
Demonstrates the lowest-level way to call an AWS Bedrock model:
`bedrock-runtime.invoke_model` with a raw JSON body.

The request/response format is model-specific.  This example targets the
Anthropic Claude Messages API, which is supported by all Claude 3+ models.

Usage:
    python simple_invoke.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    BEDROCK_MODEL_ID     – Model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)
"""

import json
import os

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
)
PROMPT = "Explain what AWS Bedrock is in three sentences."


def invoke_model(prompt: str) -> str:
    """Send *prompt* to the model and return the response text."""
    client = boto3.client("bedrock-runtime", region_name=REGION)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = client.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]


if __name__ == "__main__":
    print(f"Model : {MODEL_ID}")
    print(f"Prompt: {PROMPT}\n")

    answer = invoke_model(PROMPT)
    print("Response:")
    print(answer)
