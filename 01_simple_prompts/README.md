# 01 – Simple Prompts

This section shows three progressively more capable ways to call an AWS Bedrock foundation model.

## Scripts

### `simple_invoke.py`

The lowest-level approach: uses `bedrock-runtime` `invoke_model` with a raw JSON payload formatted for the Claude Messages API.  
Best for understanding exactly what goes over the wire.

```bash
python simple_invoke.py
```

### `converse_api.py`

Uses the higher-level [Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html) which is model-agnostic — the same code works for Claude, Titan, Mistral, etc.  
Also demonstrates a simple multi-turn conversation.

```bash
python converse_api.py
```

### `streaming_response.py`

Same as the Converse API but with `converse_stream`, which yields tokens as they are generated so long answers appear progressively in the terminal.

```bash
python streaming_response.py
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AWS_DEFAULT_REGION` | `us-east-1` | AWS region |
| `BEDROCK_MODEL_ID` | `anthropic.claude-3-sonnet-20240229-v1:0` | Foundation model to use |
