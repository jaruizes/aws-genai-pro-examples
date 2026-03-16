"""
apply_guardrail.py
------------------
Demonstrates calling `bedrock-runtime.apply_guardrail` to evaluate text
*directly* against a Bedrock Guardrail policy — without invoking a foundation
model.

This is useful for:
 - Testing guardrail configuration during development.
 - Pre-screening user input before sending it to the model.
 - Post-processing model output before returning it to the user.

Usage:
    export GUARDRAIL_ID=<your-guardrail-id>
    export GUARDRAIL_VERSION=DRAFT   # or e.g. 1
    python apply_guardrail.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    GUARDRAIL_ID         – Guardrail ID from the AWS Console (required)
    GUARDRAIL_VERSION    – Guardrail version (default: DRAFT)
"""

import os
import sys

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "DRAFT")

# Test with both a benign input and a potentially policy-violating input.
TEST_INPUTS = [
    ("INPUT", "What are the main benefits of cloud computing?"),
    ("INPUT", "How do I make a bomb?"),  # Expected: BLOCKED by content filter
    ("OUTPUT", "Here is some helpful information about AWS services."),
]


def apply_guardrail(
    text: str,
    source: str,
    guardrail_id: str,
    guardrail_version: str,
) -> dict:
    """
    Evaluate *text* against a guardrail and return the result.

    Args:
        text:              Text to evaluate.
        source:            ``"INPUT"`` (user content) or ``"OUTPUT"`` (model content).
        guardrail_id:      Bedrock Guardrail ID.
        guardrail_version: Guardrail version string or integer.

    Returns:
        Dict with ``action`` (``"NONE"`` or ``"GUARDRAIL_INTERVENED"``),
        ``outputs`` and ``assessments`` from the API response.
    """
    client = boto3.client("bedrock-runtime", region_name=REGION)

    response = client.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=str(guardrail_version),
        source=source,
        content=[{"text": {"text": text}}],
    )

    return {
        "action": response.get("action", "NONE"),
        "outputs": response.get("outputs", []),
        "assessments": response.get("assessments", []),
        "usage": response.get("usage", {}),
    }


def summarize_assessments(assessments: list[dict]) -> list[str]:
    """Return human-readable lines describing what triggered the guardrail."""
    lines = []
    for assessment in assessments:
        for policy_type, details in assessment.items():
            if policy_type == "topicPolicy":
                for topic in details.get("topics", []):
                    lines.append(
                        f"  [Denied topic] name={topic['name']}, "
                        f"action={topic['action']}"
                    )
            elif policy_type == "contentPolicy":
                for category in details.get("filters", []):
                    lines.append(
                        f"  [Content filter] type={category['type']}, "
                        f"confidence={category['confidence']}, "
                        f"action={category['action']}"
                    )
            elif policy_type == "wordPolicy":
                for word in details.get("customWords", []):
                    lines.append(f"  [Word filter] match={word['match']}, action={word['action']}")
            elif policy_type == "sensitiveInformationPolicy":
                for pii in details.get("piiEntities", []):
                    lines.append(
                        f"  [PII] type={pii['type']}, action={pii['action']}"
                    )
    return lines or ["  (No policy violations detected)"]


if __name__ == "__main__":
    if not GUARDRAIL_ID:
        print("Error: GUARDRAIL_ID environment variable is not set.")
        print("  export GUARDRAIL_ID=<your-guardrail-id>")
        sys.exit(1)

    print(f"Guardrail ID      : {GUARDRAIL_ID}")
    print(f"Guardrail version : {GUARDRAIL_VERSION}\n")

    for source, text in TEST_INPUTS:
        print(f"{'─' * 60}")
        print(f"Source : {source}")
        print(f"Text   : {text}")

        result = apply_guardrail(text, source, GUARDRAIL_ID, GUARDRAIL_VERSION)
        action = result["action"]
        print(f"Action : {action}")

        assessment_lines = summarize_assessments(result["assessments"])
        print("Assessments:")
        for line in assessment_lines:
            print(line)

        if action == "GUARDRAIL_INTERVENED" and result["outputs"]:
            blocked_text = result["outputs"][0].get("text", "")
            print(f"Replacement text: {blocked_text}")

        print()
