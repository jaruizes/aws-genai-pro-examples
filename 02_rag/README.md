# 02 – RAG (Retrieval-Augmented Generation)

This section shows how to use **Amazon Bedrock Knowledge Bases** to ground model responses in your own documents, reducing hallucinations and keeping answers up-to-date.

## How it works

```
User Question
     │
     ▼
Bedrock Knowledge Base (Retrieve)
     │  returns relevant chunks from your documents
     ▼
Foundation Model (Generate)
     │  produces a grounded answer with citations
     ▼
Response to User
```

## Prerequisites

1. Create a [Bedrock Knowledge Base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html) in the AWS Console (or via CloudFormation / CDK).
2. Ingest documents (PDF, TXT, HTML, etc.) stored in S3 into the Knowledge Base.
3. Note the **Knowledge Base ID** — it looks like `XXXXXXXXXX`.

## Scripts

### `knowledge_base_query.py`

Calls the **Retrieve** API to search the Knowledge Base and return the most relevant document chunks, *without* generating an answer.  Useful for inspecting retrieval quality before adding a model on top.

```bash
export KNOWLEDGE_BASE_ID=<your-kb-id>
python knowledge_base_query.py
```

### `retrieve_and_generate.py`

Calls the **RetrieveAndGenerate** API to perform the full RAG pipeline in a single call: the service retrieves relevant chunks and feeds them as context to the model, which then generates a cited answer.

```bash
export KNOWLEDGE_BASE_ID=<your-kb-id>
python retrieve_and_generate.py
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS region |
| `BEDROCK_MODEL_ID` | `anthropic.claude-3-sonnet-20240229-v1:0` | Foundation model used for generation |
| `KNOWLEDGE_BASE_ID` | *(required)* | ID of the Bedrock Knowledge Base |
