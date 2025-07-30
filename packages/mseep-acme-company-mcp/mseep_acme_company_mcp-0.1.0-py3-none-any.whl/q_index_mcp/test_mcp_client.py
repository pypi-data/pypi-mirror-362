import asyncio
import json
from pathlib import Path
from fastmcp import Client

async def main():
    # Connect to the MCP server
    client = Client("mcp_server.py")
    
    async with client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")
        
        # # Test search_q_business tool
        # print("\nTesting search_q_business...")
        # result = await client.call_tool("search_q_business", {"query": "keyboard issues"})
        # print(f"Search results: {result[:100]}...")  # Show first 100 chars
        
        # Test answer_question tool
        print("\nTesting answer_question...")
        answer = await client.call_tool("answer_question", {"question": "What do I do if I am unable to access my backup files?"})

        # Extract just the text from TextContent
        if hasattr(answer[0], 'text'):
            print(f"Answer: {answer[0].text}")
        else:
            print(f"Answer: {answer}")

if __name__ == "__main__":
    asyncio.run(main())