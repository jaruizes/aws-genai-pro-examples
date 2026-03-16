"""
knowledge_base_query.py
-----------------------
Demonstrates a **pure Retrieve** call against a Bedrock Knowledge Base.

The Knowledge Base performs a semantic (vector) search over your ingested
documents and returns the most relevant text chunks along with their source
metadata — *without* calling a foundation model to generate an answer.

This is useful when you want to:
 - Inspect retrieval quality independently of generation quality.
 - Use the retrieved chunks in your own generation pipeline.

Usage:
    export KNOWLEDGE_BASE_ID=<your-kb-id>
    python knowledge_base_query.py

Environment variables:
    AWS_DEFAULT_REGION   – AWS region (default: us-east-1)
    KNOWLEDGE_BASE_ID    – ID of the Bedrock Knowledge Base (required)
"""

import os
import sys

import boto3

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
KNOWLEDGE_BASE_ID = os.environ.get("KNOWLEDGE_BASE_ID", "")
QUERY = "What are the main features of AWS Bedrock?"
MAX_RESULTS = 5


def retrieve(query: str, knowledge_base_id: str, max_results: int = 5) -> list[dict]:
    """
    Query the Knowledge Base and return relevant text chunks.

    Args:
        query:              Natural-language question or search string.
        knowledge_base_id:  The Bedrock Knowledge Base ID.
        max_results:        Maximum number of chunks to return.

    Returns:
        List of result dicts, each containing ``text``, ``score``, and
        ``location`` (source document metadata).
    """
    client = boto3.client("bedrock-agent-runtime", region_name=REGION)

    response = client.retrieve(
        knowledgeBaseId=knowledge_base_id,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": max_results}
        },
    )

    results = []
    for item in response.get("retrievalResults", []):
        results.append(
            {
                "text": item["content"]["text"],
                "score": item.get("score", 0.0),
                "location": item.get("location", {}),
            }
        )
    return results


if __name__ == "__main__":
    if not KNOWLEDGE_BASE_ID:
        print("Error: KNOWLEDGE_BASE_ID environment variable is not set.")
        print("  export KNOWLEDGE_BASE_ID=<your-kb-id>")
        sys.exit(1)

    print(f"Knowledge Base ID : {KNOWLEDGE_BASE_ID}")
    print(f"Query             : {QUERY}\n")

    chunks = retrieve(QUERY, KNOWLEDGE_BASE_ID, max_results=MAX_RESULTS)

    if not chunks:
        print("No results returned. Check that your Knowledge Base has ingested documents.")
        sys.exit(0)

    print(f"Retrieved {len(chunks)} chunk(s):\n")
    for i, chunk in enumerate(chunks, start=1):
        source = chunk["location"].get("s3Location", {}).get("uri", "unknown")
        print(f"--- Chunk {i} (score: {chunk['score']:.4f}, source: {source}) ---")
        print(chunk["text"])
        print()
