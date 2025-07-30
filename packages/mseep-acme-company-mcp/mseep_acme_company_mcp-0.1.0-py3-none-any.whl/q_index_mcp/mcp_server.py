import json
from pathlib import Path

from fastmcp import FastMCP
from utils.constants import (
    BASE_MODEL_ARN,
    DEFAULT_EMAIL,
    INFERENCE_PROFILE_NAME,
    INFERENCE_PROFILE_TAGS,
    MAX_SEARCH_RESULTS,
    REGION,
    INDEX_SYSTEM_PROMPT,
    TVM_VALUES_FILE,
)
from utils.tvm_client import TVMClient

# Create FastMCP server
server = FastMCP(name="AcmeCompanyMCP")


# Helper functions from main.py
def get_credentials(email, region=REGION):
    """Get SigV4 credentials using TVM client"""
    tvm_file = Path(__file__).parent / TVM_VALUES_FILE
    try:
        creds = json.loads(Path(tvm_file).read_text()).get("TVMOidcIssuerStack", {})
    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
        raise ValueError(f"Failed to load TVM credentials from {tvm_file}: {e}")

    return TVMClient(
        issuer=creds["IssuerUrlOutput"].rstrip("/"),
        client_id=creds["QbizTVMClientID"],
        client_secret=creds["QbizTVMClientSecret"],
        role_arn=creds["QBizAssumeRoleARN"],
        region=region,
    ).get_sigv4_credentials(email=email)


def extract_context_from_search_results(search_results):
    """Extract and combine content from search results"""
    if not search_results:
        return ""

    full_context = ""
    for chunk in search_results:
        full_context += chunk["content"] + "\n"

    return full_context


# MCP Tools


@server.tool(
    description="Get answer to a question using RAG with Q Business and Bedrock"
)
async def answer_question(question: str) -> str:
    """
    Answer a question using RAG with Q Business and Bedrock.

    Args:
        question: The question to answer

    Returns:
        str: The answer from Bedrock
    """
    from utils.async_utils import AsyncBedrockClient, AsyncQBusinessClient

    # Initialize async clients
    async_bedrock = AsyncBedrockClient(region=REGION)
    async_qbiz = AsyncQBusinessClient(region=REGION)
    async_qbiz_app = AsyncQBusinessClient(
        region=REGION, credentials=get_credentials(DEFAULT_EMAIL)
    )

    # Get app and retriever IDs asynchronously
    app_id, retriever_id = await async_qbiz.get_app_and_retriever_ids()

    # Search for relevant content asynchronously
    search_results = await async_qbiz_app.call_search_relevant_content(
        app_id, retriever_id, question, MAX_SEARCH_RESULTS
    )

    # Extract context
    context = extract_context_from_search_results(search_results)

    # Setup inference profile asynchronously
    profile_arn = await async_bedrock.setup_inference_profile(
        INFERENCE_PROFILE_NAME, BASE_MODEL_ARN, INFERENCE_PROFILE_TAGS
    )

    # Query model asynchronously
    response = await async_bedrock.query_model(
        profile_arn, question, INDEX_SYSTEM_PROMPT, context
    )

    return response


# Run the server
if __name__ == "__main__":
    # Run the server
    server.run(transport="stdio")
