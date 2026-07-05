---
name: review_agent_skill
description: Guidelines for gathering and analyzing social reviews and public sentiment about pet food brands.
---
# Review Agent Skill

Use this skill when processing social sentiment, forums, reviews, or platform-specific comments about pet food.

## Sentiment Aggregation Guidelines
- Connect to online platforms using the web-scrape/Firecrawl MCP tool and the Reddit RSS fetch tool.
- For Reddit data, RSS-feed-sourced posts (e.g. subreddit .rss endpoints) are the primary and only approved data source for sentiment gathering since formal MCP approval is pending.
- If a data source returns no results or fails, state that plainly (e.g., "No Reddit data could be retrieved for this brand") rather than generating plausible-sounding sentiment from general knowledge.
- Filter out spam, generic reviews, and biased marketing posts.
- Focus on extracting real-world outcomes: palatability ("picky eater approved"), digestive responses, and skin/coat improvements.
- Summarize findings into clear sections: Common Praise, Common Criticisms, and Overall Public Sentiment.
