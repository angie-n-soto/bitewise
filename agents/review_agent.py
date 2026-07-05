from agents.sdk_loader import LocalAgentConfig, McpStdioServer, policy
from tools.web_scout_tools import fetch_reddit_rss_feed

def get_review_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Review Agent to gather brand reviews and sentiment analysis
    from online platforms using the Firecrawl MCP server and Reddit RSS feeds.
    """
    system_instructions = (
        "You are the Review Agent. Your primary purpose is to research online reviews, sentiment, "
        "and discussions on forums and platforms regarding pet food brands and products.\n\n"
        "You have access to the following tools:\n"
        "1. fetch_reddit_rss_feed: Fetches recent posts from subreddits (e.g., DogFood, CatFood) via RSS.\n"
        "2. Firecrawl MCP: Allows scraping and extracting clean markdown content from review sites, forums, and articles.\n\n"
        "Utilize these tools to answer queries about pet food quality, customer satisfaction, and real-world pet owner experiences. "
        "Summarize findings with pros, cons, and common complaints.\n\n"
        "For every brand you are asked to review, you MUST call fetch_reddit_rss_feed at least once, using the most relevant subreddit for the pet type (e.g. 'catfood' for cat products, 'dogfood' for dog products), before writing your summary.\n"
        "If fetch_reddit_rss_feed returns an error or no posts, or if you cannot find genuinely relevant real content, you must state plainly that no Reddit data could be retrieved for this brand. "
        "Do not generate plausible-sounding sentiment, reviews, or opinions that are not directly grounded in real tool output."
    )
    
    # Configure the MCP Stdio Server.
    firecrawl_server = McpStdioServer(
        name="firecrawl-mcp",
        command="npx",
        args=["-y", "firecrawl-mcp-server"]
    )
    
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        tools=[fetch_reddit_rss_feed],
        mcp_servers=[firecrawl_server],
        policies=[policy.allow_all()]
    )
