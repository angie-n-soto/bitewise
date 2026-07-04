from agents.sdk_loader import LocalAgentConfig, McpStdioServer, policy

def get_review_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Review Agent to gather brand reviews and sentiment analysis
    from online platforms using Reddit MCP and Firecrawl MCP servers.
    """
    system_instructions = (
        "You are the Review Agent. Your primary purpose is to research online reviews, sentiment, "
        "and discussions on forums and platforms regarding pet food brands and products.\n\n"
        "You have access to tools via the following MCP servers:\n"
        "1. Reddit MCP: Allows querying discussions, threads, and comments on subreddits like r/pets, r/dogfood, etc.\n"
        "2. Firecrawl MCP: Allows scraping and extracting clean markdown content from review sites, forums, and articles.\n\n"
        "Utilize these tools to answer queries about pet food quality, customer satisfaction, and real-world pet owner experiences. "
        "Summarize findings with pros, cons, and common complaints."
    )
    
    # Configure the MCP Stdio Servers.
    # When executed, the agent process will spawn these MCP servers in the background.
    # Note: These require 'node' and 'npx' to be available on the user's PATH.
    reddit_server = McpStdioServer(
        name="reddit-mcp",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-reddit"]
    )
    
    firecrawl_server = McpStdioServer(
        name="firecrawl-mcp",
        command="npx",
        args=["-y", "firecrawl-mcp-server"]
    )
    
    # Using policy.allow_all() because running MCP servers is a sensitive operation
    # that requires explicit permission gates.
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        mcp_servers=[reddit_server, firecrawl_server],
        policies=[policy.allow_all()]
    )
