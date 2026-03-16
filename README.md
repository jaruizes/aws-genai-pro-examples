# AWS Bedrock Playground

A hands-on repository to learn and experiment with [AWS Bedrock](https://aws.amazon.com/bedrock/) — from simple model prompts to Retrieval-Augmented Generation (RAG), guardrails, and more.

## Overview

AWS Bedrock is a fully managed service that provides access to foundation models (FMs) from leading AI companies through a unified API. This playground walks through progressively more advanced use cases:

| Section | Description |
|---------|-------------|
| [01 – Simple Prompts](./01_simple_prompts/) | Direct model invocation, the Converse API, and streaming responses |
| [02 – RAG](./02_rag/) | Retrieval-Augmented Generation using Bedrock Knowledge Bases |
| [03 – Guardrails](./03_guardrails/) | Content filtering and policy enforcement with Bedrock Guardrails |

## Prerequisites

- Python 3.10+
- An AWS account with Amazon Bedrock access enabled
- IAM permissions for `bedrock`, `bedrock-runtime`, and `bedrock-agent-runtime`
- (Optional) An S3 bucket and a Bedrock Knowledge Base for the RAG examples
- (Optional) A Bedrock Guardrail for the guardrails examples

## Setup

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
# or set environment variables:
# export AWS_ACCESS_KEY_ID=...
# export AWS_SECRET_ACCESS_KEY=...
# export AWS_DEFAULT_REGION=us-east-1
```

## Sections

### 01 – Simple Prompts

Three self-contained scripts that show the fundamentals of calling a Bedrock model:

- **`simple_invoke.py`** – lowest-level call via `invoke_model` using the raw JSON payload for Claude 3.
- **`converse_api.py`** – the recommended multi-turn [Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) that works with any supported model.
- **`streaming_response.py`** – real-time token streaming with `converse_stream` so long responses display progressively.

```bash
cd 01_simple_prompts
python simple_invoke.py
python converse_api.py
python streaming_response.py
```

### 02 – RAG

Examples that combine a Bedrock Knowledge Base with a foundation model to answer questions grounded in your own documents:

- **`knowledge_base_query.py`** – pure *Retrieve* call; returns relevant document chunks without generating an answer.
- **`retrieve_and_generate.py`** – full RAG pipeline: retrieves context **and** generates a grounded answer in one call.

```bash
cd 02_rag
# Set the Knowledge Base ID (created in the AWS Console or via IaC)
export KNOWLEDGE_BASE_ID=<your-kb-id>
python knowledge_base_query.py
python retrieve_and_generate.py
```

### 03 – Guardrails

Examples that show how to add safety layers on top of model responses:

- **`apply_guardrail.py`** – calls `apply_guardrail` directly to test whether text passes a guardrail policy.
- **`converse_with_guardrail.py`** – wraps the Converse API with a guardrail so every request/response pair is screened automatically.

```bash
cd 03_guardrails
# Set the Guardrail ID and version
export GUARDRAIL_ID=<your-guardrail-id>
export GUARDRAIL_VERSION=DRAFT   # or a published version number
python apply_guardrail.py
python converse_with_guardrail.py
```

## Environment Variables Reference

| Variable | Required by | Description |
|---|---|---|
| `AWS_DEFAULT_REGION` | all | AWS region (default `us-east-1`) |
| `BEDROCK_MODEL_ID` | all | Foundation model ID (default `anthropic.claude-3-sonnet-20240229-v1:0`) |
| `KNOWLEDGE_BASE_ID` | 02_rag | ID of the Bedrock Knowledge Base |
| `GUARDRAIL_ID` | 03_guardrails | ID of the Bedrock Guardrail |
| `GUARDRAIL_VERSION` | 03_guardrails | Version of the guardrail (default `DRAFT`) |

## Useful Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)
- [Boto3 Bedrock Runtime Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Supported Foundation Models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)

## License

This project is open-source and available under the [MIT License](LICENSE).
