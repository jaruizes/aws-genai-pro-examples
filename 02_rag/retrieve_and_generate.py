"""
retrieve_and_generate.py
------------------------
Demonstrates the full **Retrieve and Generate** pipeline using a Bedrock
Knowledge Base.

In a single API call the service:
 1. Converts the question into an embedding.
 2. Retrieves the most relevant document chunks from the Knowledge Base.
 3. Passes those chunks as context to the foundation model.
 4. Returns a grounded answer together with citations.

Usage:
    export KNOWLEDGE_BASE_ID=<your-kb-id>
    python retrieve_and_generate.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    BEDROCK_MODEL_ID     – Foundation model ARN or ID used for generation
                           (default: anthropic.claude-3-sonnet-20240229-v1:0)
    KNOWLEDGE_BASE_ID    – ID of the Bedrock Knowledge Base (required)
"""

import os
import sys

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"
)
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")
QUERY = "What are the main features of AWS Bedrock and how does it help developers?"


def build_model_arn(model_id: str, region: str) -> str:
    """
    Convert a model ID into the ARN format required by RetrieveAndGenerate.
    If the value already looks like an ARN it is returned unchanged.
    """
    if model_id.startswith("arn:"):
        return model_id
    return f"arn:aws:bedrock:{region}::foundation-model/{model_id}"


def retrieve_and_generate(
    query: str,
    knowledge_base_id: str,
    model_arn: str,
    max_results: int = 5,
) -> dict:
    """
    Run a full RAG query against the Knowledge Base and return the result.

    Args:
        query:              Natural-language question.
        knowledge_base_id:  The Bedrock Knowledge Base ID.
        model_arn:          ARN of the foundation model used for generation.
        max_results:        Number of chunks to retrieve for context.

    Returns:
        Dict with keys ``answer`` (str) and ``citations`` (list).
    """
    client = boto3.client("bedrock-agent-runtime", region_name=REGION)

    response = client.retrieve_and_generate(
        input={"text": query},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": knowledge_base_id,
                "modelArn": model_arn,
                "retrievalConfiguration": {
                    "vectorSearchConfiguration": {"numberOfResults": max_results}
                },
            },
        },
    )

    answer = response["output"]["text"]
    citations = []
    for citation in response.get("citations", []):
        for ref in citation.get("retrievedReferences", []):
            citations.append(
                {
                    "text": ref["content"]["text"],
                    "source": ref.get("location", {})
                    .get("s3Location", {})
                    .get("uri", "unknown"),
                }
            )

    return {"answer": answer, "citations": citations}


if __name__ == "__main__":
    if not KNOWLEDGE_BASE_ID:
        print("Error: KNOWLEDGE_BASE_ID environment variable is not set.")
        print("  export KNOWLEDGE_BASE_ID=<your-kb-id>")
        sys.exit(1)

    model_arn = build_model_arn(MODEL_ID, REGION)

    print(f"Knowledge Base ID : {KNOWLEDGE_BASE_ID}")
    print(f"Model             : {model_arn}")
    print(f"Query             : {QUERY}\n")

    result = retrieve_and_generate(QUERY, KNOWLEDGE_BASE_ID, model_arn)

    print("=== Answer ===")
    print(result["answer"])

    if result["citations"]:
        print(f"\n=== Citations ({len(result['citations'])}) ===")
        for i, citation in enumerate(result["citations"], start=1):
            print(f"\n[{i}] Source: {citation['source']}")
            print(f"    {citation['text'][:200]}{'...' if len(citation['text']) > 200 else ''}")
