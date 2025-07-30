# Agentic RAG for JIRA Case Management using Strands Agents with MCPs Clients for Amazon Q Index & Perplexity
 

This solution uses Strands Agents with MCP Tools powered by Amazon Q Business Cross App index and Perplexity Ask

![image](https://github.com/user-attachments/assets/3e9d9ec5-178d-4778-80be-0e9699e726ca)

## Set up

Perform the steps for setting up MCP powered using Q Index based RAG by visiting the [q_index_mcp/README.md](q_index_mcp/README.md)



### Configuration

Create .env file in the root of this module.

```shell
touch .env
```

The application uses environment variables for configuration. You can modify these in the `.env` file:

```
REGION=us-east-1
Q_BUSINESS_APP_NAME=REPLACE_WITH_YOUR_Q_BUSINESS_APP_NAME
PERPLEXITY_API_KEY=PERPLEXITY_API_KEY
```

For PERPLEXITY_API_KEY, visit [Generating an API Key](https://docs.perplexity.ai/guides/getting-started#generating-an-api-key)

### Setup and Running with UV

This project uses `uv` for dependency management instead of traditional Python venv.

For Mac, you **MUST** run `brew install uv` for smooth MCP experience. Otherwise you may run into [ENOENT challenges](https://github.com/orgs/modelcontextprotocol/discussions/20)

```shell
brew install uv
```

## Running the Server

You can run the server using the provided script:

```bash
./run_with_uv.sh
```

This script will:
1. Create a uv environment if it doesn't exist
2. Install the required dependencies
3. Spins up the bot that runs strands agent powered up by MCP servers.

### Manual Setup

If you prefer to set up manually:

```bash
# Create and activate uv environment
uv venv .uv
source .uv/bin/activate

# Install dependencies
uv pip install boto3 "mcp[cli]" requests fastmcp httpx python-dotenv strands-agents strands-agents-tools

# Run strands agent
uv run main.py
```

## Required Packages

- boto3
- mcp[cli]
- requests
- fastmcp
- httpx
- python-dotenv
- strands-agents
- strands-agents-tools

## Test Q Index MCP Server

```shell
cd q_index_mcp/ && uv run test_mcp_client.py && cd ..
```

## Questions to Ask based on tickets in `synthetic_data` and `ticket_pdfs` directory

Refer [q_index_mcp/rag_sample_queries.md](q_index_mcp/rag_sample_queries.md) that has sample questions along with expected info and context associated with query.

```text
What are some of the reasons of keyboard failure?
What are software installation issues caused by?
What is the remediation of password not working?
What do I do if I am unable to access my backup files?

What immediate action did AnyCompany take to improve the Voice receptionist service while discussing the upgrade?
During which hours did Michael Chen notice the most significant delays?
```

## Using just MCP Host instead of strands agents

### Set up Perplexity ASK MCP Server

Refer [Integrating MCP with Perplexity's Sonar API](https://docs.perplexity.ai/guides/mcp-server) and [Perplexity Ask MCP Server](https://github.com/ppl-ai/modelcontextprotocol/tree/main)

### Sample prompt for MCP Hosts (Claude Desktop, Amazon Q CLI etc.,)

Sample prompt. Feel free to tweak according to your needs.

```text
You are a helpful AI assistant who answers question correctly and accurately about a AcmeCompany's IT tickets and also rely on Perplexity MCP Server for general knowledge.
You answer in the format as follows:
<response>
    <datasource> 
    </datasource>
    <perplexityknowledge> 
    </perplexityknowledge>
</response>

** For datasource section: **
    Use tool answer_question from AnyCompany MCP Server.
    Do not makeup answers and only answer from the provided knowledge. 
    If the query doesn't has any Info about IT Tickets, you must acknowledge that. 
** For  perplexityknowledge section: **
    Provide info by obtaining the results from perplexity-ask MCP using it's preplexity_ask tool for addressing the query.

Here is the query:
During which hours did Michael Chen notice the most significant delays?
```

### Using Claude Desktop

![image](https://github.com/user-attachments/assets/a4899220-a7f1-4fcc-b47a-29b8eaf34ea9)

### Using Q Dev CLI

![image](https://github.com/user-attachments/assets/b8a147a3-8052-4b64-b8f8-064bf91c8601)

![image](https://github.com/user-attachments/assets/4df4189c-c3ee-4b45-adb8-5437ec219151)


