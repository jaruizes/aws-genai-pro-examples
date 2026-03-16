# 03 – Guardrails

This section shows how to use **Amazon Bedrock Guardrails** to add safety and compliance controls to your AI applications.

## What are Guardrails?

Bedrock Guardrails let you define policies that are automatically applied to every model request and/or response.  You can configure:

- **Content filters** – Block harmful content (hate speech, violence, profanity, etc.) at configurable sensitivity levels.
- **Denied topics** – Prevent the model from discussing specific subjects (e.g., competitor products, legal advice).
- **Word filters** – Block or mask specific words or phrases.
- **Sensitive information redaction** – Automatically detect and redact PII (names, emails, phone numbers, etc.).
- **Grounding** – Flag responses that are not grounded in the provided context.

## Prerequisites

1. Create a [Bedrock Guardrail](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-create.html) in the AWS Console.
2. Note the **Guardrail ID** (e.g., `abc123def456`) and **version** (`DRAFT` or a published integer version).

## Scripts

### `apply_guardrail.py`

Calls `apply_guardrail` directly to evaluate a piece of text *without* invoking a foundation model.  This is the fastest way to test whether your guardrail policies are working as expected.

```bash
export GUARDRAIL_ID=<your-guardrail-id>
export GUARDRAIL_VERSION=DRAFT   # or e.g. 1
python apply_guardrail.py
```

### `converse_with_guardrail.py`

Attaches a guardrail to a full Converse API call so that both the user input **and** the model output are evaluated against the guardrail policy.

```bash
export GUARDRAIL_ID=<your-guardrail-id>
export GUARDRAIL_VERSION=DRAFT
python converse_with_guardrail.py
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS region |
| `BEDROCK_MODEL_ID` | `anthropic.claude-3-sonnet-20240229-v1:0` | Foundation model (used in `converse_with_guardrail.py`) |
| `GUARDRAIL_ID` | *(required)* | Guardrail ID from the AWS Console |
| `GUARDRAIL_VERSION` | `DRAFT` | Guardrail version |
